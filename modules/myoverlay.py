# -*- coding: utf-8 -*-

import urwid
import common.modulehelper as modulehelper
from common.urwidwidgetwrapper import Button as MyButton
import logging
import common.dialog as dialog

log = logging.getLogger('overlay')
blank = urwid.Divider('*')

class MyOverlay(urwid.WidgetWrap):
    def __init__(self, parent, language = modulehelper.LanguageType.CHINESE):
        self.parent = parent
        self.screen = None
        self.name = 'Overlay'
        self.visible = True
        self.language = language

    def refresh(self):
        pass

    def apply(self, args=None):
        pass


    def callback(self, button):
        msg = 'this is a button %s'
        self.show_submenu(urwid.Text(msg), u"submenu")

    def callback_item1(self, button):
        pass

    def callback_item2(self, button):
        self.parent.mainloop.widget = self.overlay_widget.bottom_w

    def show_submenu(self, body, title):
        self.linebox = urwid.LineBox(
            urwid.ListBox(urwid.SimpleListWalker(
                [
                    MyButton(u'menu item 1', self.callback_item1),
                    MyButton(u'menu item 2', self.callback_item2)
                ]
            )), title
        )
        self.linebox = urwid.AttrWrap(self.linebox, 'body')

        self.linebox = urwid.LineBox(
            urwid.ListBox(urwid.SimpleListWalker(
                [
                    MyButton(u'menu item 3', self.callback_item1),
                    MyButton(u'menu item 4', self.callback_item2)
                ]
            )), title
        )
        self.linebox = urwid.AttrWrap(self.linebox, 'body')

        self.overlay_widget = urwid.Overlay(self.linebox, self.parent.mainloop.widget,
                                       'center', ('relative', 60), 'middle',
                                       ('relative', 40))

        self.parent.mainloop.widget = self.overlay_widget




    def screenUI(self):
        self.text0 = urwid.Text(u'Overlay包含了两个组件，一个组件在另外一个组件的上方')
        self.text1 = urwid.Text(u'点击下列按钮展开子菜单')
        self.button_top = MyButton(u'展开', self.callback)


        listbox_content = [self.text0, self.text1, blank, self.button_top]

        return urwid.ListBox(urwid.SimpleListWalker(listbox_content))


