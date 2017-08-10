# -*- coding: utf-8 -*-

import urwid
import common.modulehelper as modulehelper
import logging
import common.dialog as dialog

log = logging.getLogger('filler')
blank = urwid.Divider(' ')

class MyFiller(urwid.WidgetWrap):
    def __init__(self, parent, language = modulehelper.LanguageType.CHINESE):
        self.parent = parent
        self.screen = None
        self.name = 'Filler'
        self.visible = True
        self.language = language

    def refresh(self):
        pass

    def apply(self, args=None):
        pass



    def screenUI(self):
        self.text0 = urwid.Text(u'filler是一个在包装的组件上下留空隙的组件')
        self.text1 = urwid.Text(u'下面两个text包裹在同一个filler组件中')
        self.text2 = urwid.Text(u'')
        self.text2 = urwid.AttrWrap(self.text2, 'header')
        self.text3 = urwid.Text(u'')
        self.text3 = urwid.AttrWrap(self.text3, 'header')
        self.list_inner = [self.text2, urwid.Divider(' '), self.text3]
        self.inner_list_box = urwid.ListBox(urwid.SimpleListWalker(self.list_inner))
        self.inner_list_box = urwid.BoxAdapter(self.inner_list_box, 3)
        self.filler = urwid.Filler(self.inner_list_box, valign='middle', top=1, bottom=2)
        self.filler = urwid.AttrWrap(self.filler, 'padding')
        self.inner_box = urwid.BoxAdapter(self.filler, 20)




        self.text2.set_text(u"该filler的边距模式为%s" % self.filler.original_widget.valign_type)
        self.text3.set_text(u"该filler包装组件后预设的头尾的填充行为%s %s" % (self.filler.original_widget.top,
                                                                self.filler.original_widget.bottom))

        self.list_content = [self.text0, self.text1, urwid.Divider(' '), self.inner_box]

        listbox = urwid.ListBox(urwid.SimpleListWalker(self.list_content))
        return listbox

