#!/usr/bin/python
# -*- coding: utf-8 -*-

# program entry
# 2017.3.29 create

import logging

import consts
import common.utils as utils
import string
import settings
import modules as modules
from common.modulehelper import LanguageType

logging.basicConfig(filename = consts.LOGFILE,
                    format = "%(name)s %(asctime)s %(levelname)s %(message)s",
                    level = logging.DEBUG)

import os
import sys
import signal
import urwid
import time
import optparse

import urwid.raw_display
import urwid.web_display

log = logging.getLogger('dsMenu.loader')
blank = urwid.Divider(" ")

class DASONESetUp(object):
    def __init__(self):
        self.footer = None
        self.header = None
        self.screen = None
        self.globalsave = True
        self.version = utils.get_dsMenu_version()
        self.defaultsettingsfile = "%s/settings.yaml" \
                                  % (os.path.dirname(__file__))
        self.settingsfile = "/etc/dsMenu/astute.yaml"
        self.begintime = time.asctime(time.localtime(time.time()))
        self.children = []
        self.child = None
        self.choices = []
        self.menubox = None
        self.childpage = None
        self.childfill = None
        self.childbox = None
        self.cols = None
        self.listwalker = None
        self.listbox = None
        self.frame = None
        self.mainloop = None
        self.langtype = None

        #default setting kwargs
        self.templete_kwargs = {
            'version':self.version,
            'begintime':self.begintime
        }

        setting_file = os.path.join(os.path.dirname(__file__), "settings")

        self.main()
        self.choices = []

    def exit_program(self, button):

        raise urwid.ExitMainLoop()

    def menu(self, title, choices):
        body = [urwid.Text(title), blank]
        for c in choices:
            button = urwid.Button(c)
            urwid.connect_signal(button, 'click', self.menuitem_chosen, c)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))
        return urwid.ListBox(urwid.SimpleListWalker(body))

    def menuitem_chosen(self, button, c):
        size = self.screen.get_cols_rows()
        self.screen.draw_screen(size, self.frame.render(size))
        for item in self.menuitems.body.contents:
            try:
                if isinstance(item.base_widget, urwid.Button):
                    if item.base_widget.get_label() == c:
                        item.set_attr_map({None: 'header'})

                    else:
                        item.set_attr_map({None: None})
            except AttributeError:
                log.exception("Unable to set menu item %s" % item)
        self.set_child_screen(name=c)

    def set_child_screen(self, name=None):
        if name is None:
            self.child = self.children[0]
        else:
            self.child = self.children[int(self.choices.index(name))]
        if not self.child.screen:
            self.child.screen = self.child.screenUI()
        self.draw_child_screen(self.child.screen)

    def draw_child_screen(self, child_screen, focus_on_child=False):
        self.childpage = child_screen
        self.childfill = urwid.Filler(self.childpage, 'top', 40)
        self.childbox = urwid.BoxAdapter(self.childfill, 40)
        self.cols = urwid.Columns(
            [
                ('fixed', 20, urwid.Pile([
                    urwid.AttrMap(self.menubox, 'bright'),
                    blank])),
                ('weight', 3, urwid.Pile([
                    blank,
                    self.childbox,
                    blank]))
            ], 1)
        if focus_on_child:
            self.cols.focus_position=1 # focus on childbox
        self.child.refresh()
        self.listwalker[:] = [self.cols]

    def refresh_screen(self):
        size = self.screen.get_cols_rows()
        self.screen.draw_screen(size, self.frame.render(size))


    def global_save(self):
        #Runs save function for every module
        for module, modulename in zip(self.children, self.choices):
            #Run invisible modules. They may not have screen methods
            module.apply(None)
        return True, None



    def main(self):
        # this program use frame as the topmost widget, header and footer
        # play roles of the top and bottom lines of the frame

        # field which need to choose language
        language_field = {
            'text_header' : None,
            'text_footer' : None,
            'menu_label' : None
        }

        #language choose
        language_field = LanguageType.choose_language("DASONEMENU",
                                                      LanguageType.CHINESE,
                                                      language_field=language_field)
        # replace $ with dasonemenu version
        language_field['text_header'] = language_field['text_header'].replace('$', self.version)

        self.header = urwid.AttrMap(urwid.Text(language_field['text_header']), 'header')
        self.footer = urwid.AttrMap(urwid.Text(language_field['text_footer']), 'footer')

        self.children = []

        # load the modules will be used,
        # every module is one child
        # you can extend the num of modules by modify modules.__init__.py file
        for clsobj in modules.__all__:
            modobj = clsobj(self, LanguageType.CHINESE) # default language is chinese
            self.children.append(modobj)

        if len(self.children) == 0:
            log.debug('there is no available modules, dsMenu exit')
            sys.exit(1)

        # build list of choices
        self.choices = [m.name for m in self.children]

        # build list of visible choices
        self.visiblechoices = []
        for child, choice in zip(self.children, self.choices):
            if child.visible:
                self.visiblechoices.append(choice)

        # finish menu box
        self.menuitems = self.menu(language_field['menu_label'], self.visiblechoices)
        menufill = urwid.Filler(self.menuitems, 'top', 40)
        self.menubox = urwid.BoxAdapter(menufill, 40)

        # finish child box
        self.child = self.children[0] # use DaSone user modules default
        self.childpage = self.child.screenUI()
        self.childfill = urwid.Filler(self.childpage, 'top', 22)
        self.childbox = urwid.BoxAdapter(self.childfill, 22)
        # create col widget contain menubox and child box
        self.cols = urwid.Columns(
            [
                ('fixed', 20, urwid.Pile([
                    urwid.AttrMap(self.menubox, 'body'),
                    urwid.Divider(" ")])),
                ('weight', 3, urwid.Pile([
                    blank,
                    self.childbox,
                    blank]))
            ], 1)

        # top second widget -- Listbox
        self.listwalker = urwid.SimpleListWalker([self.cols])
        self.listbox = urwid.ListBox(self.listwalker)

        #topmost widget --Frame
        self.frame = urwid.Frame(urwid.AttrMap(self.listbox, 'body'),
                                 header=self.header, footer=self.footer)

        palette = \
            [
                ('body', 'black', 'light gray', 'standout'),
                ('reverse', 'light gray', 'black'),
                ('header', 'white', 'dark red', 'bold'),
                ('important', 'dark blue', 'light gray',
                    ('standout', 'underline')),
                ('editfc', 'white', 'dark blue', 'bold'),
                ('editbx', 'light gray', 'light blue'),
                ('editcp', 'black', 'light gray', 'standout'),
                ('bright', 'dark gray', 'light gray', ('bold', 'standout')),
                ('buttn', 'black', 'dark cyan'),
                ('buttnf', 'white', 'dark blue', 'bold'),
                ('light gray', 'white', 'light gray', 'bold'),
                ('red', 'dark red', 'light gray', 'bold'),
                ('black', 'black', 'black', 'bold'),
                ('padding', 'white', 'black', 'bold'),
                ('filler', 'white', 'black', 'bold')
        ]

        # use appropriate Screen class
        if urwid.web_display.is_web_request():
            self.screen = urwid.web_display.Screen()
        else:
            self.screen = urwid.raw_display.Screen()
        # handle unexpected signal
        def handle_extra_input(key):
            if key == 'f12':
                raise urwid.ExitMainLoop()
            if key == 'shift tab':
                self.child.walker.tab_prev()
            if key == 'tab':
                self.child.walker.tab_next()

        # begin mainloop
        self.mainloop = urwid.MainLoop(self.frame, palette, self.screen,
                                       unhandled_input=handle_extra_input)

        self.mainloop.run()

def main(*args, **kwargs):
    if urwid.VERSION < (1, 1, 0):
        print ("This program requires urwid 1.1.0 or greater.")

    parser = optparse.OptionParser()
    parser.add_option("-s", "--save-only", dest="save_only",
                      action="store_true",
                      help="Save default values and exit")

    # parser.add_option("-i", "--iface", dest="iface", metavar="IFACE",
    #                   default="eth0", help="Set IFACE as primary.")
    #
    options, args = parser.parse_args()

    if options.save_only:
        pass
    else:
        setup()










def setup(**kwargs):
    urwid.web_display.set_preferences('DaSone setup')
    #处理 short web requests
    if urwid.web_display.handle_short_request():
        return
    DASONESetUp(**kwargs)

if '__main__' == __name__ or urwid.web_display.is_web_request():
    setup()



