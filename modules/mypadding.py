# -*- coding: utf-8 -*-

import urwid
import common.modulehelper as modulehelper
import logging
import common.dialog as dialog

log = logging.getLogger('padding')
blank = urwid.Divider(' ')

class MyPadding(urwid.WidgetWrap):
    def __init__(self, parent, language = modulehelper.LanguageType.CHINESE):
        self.parent = parent
        self.screen = None
        self.name = 'Padding'
        self.visible = True
        self.language = language

    def refresh(self):
        pass

    def apply(self, args=None):
        pass



    def screenUI(self):
        self.text0 = urwid.Text(u'padding是一个在包装的组件两边留空隙的组件')
        self.text1 = urwid.Text(u"下面两个text空间包裹在在同一个padding组件内")
        self.text2 = urwid.Text(u'')
        self.text2 = urwid.AttrWrap(self.text2, 'header')
        self.text3 = urwid.Text(u'')
        self.text3 = urwid.AttrWrap(self.text3, 'header')
        self.list_inner = [self.text2, urwid.Divider(' '), self.text3]
        self.inner_list_box = urwid.ListBox(urwid.SimpleListWalker(self.list_inner))
        self.padding = urwid.Padding(self.inner_list_box, align='center', width=30)
        self.padding = urwid.AttrWrap(self.padding, 'padding')
        self.inner_box = urwid.BoxAdapter(self.padding, 10)




        self.text2.set_text(u"该padding的边距模式为%s" % self.padding.original_widget.align)
        self.text3.set_text(u"该padding包装的组件宽度为%s" % self.padding.original_widget.width)

        self.list_content = [self.text0, self.text1, urwid.Divider(' '), self.inner_box]

        listbox = urwid.ListBox(urwid.SimpleListWalker(self.list_content))
        return listbox

