# -*- coding: utf-8 -*-

import urwid
import common.modulehelper as modulehelper
import logging
import common.dialog as dialog

log = logging.getLogger('listbox')
blank = urwid.Divider('*')

class MyListBox(urwid.WidgetWrap):
    def __init__(self, parent, language = modulehelper.LanguageType.CHINESE):
        self.parent = parent
        self.screen = None
        self.name = 'ListBox'
        self.visible = True
        self.language = language

    def refresh(self):
        pass

    def apply(self, args=None):
        pass


    def callback(self, button):
        msg = 'this is a button'
        dialog.display_dialog(self, urwid.Text(msg), "Hello")


    def screenUI(self):
        self.text0 = urwid.Text(u'ListBox是一个将装饰的组件序列垂直排列的盒组件，其中所有组件全部必须是流组件')

        self.text1 = urwid.Text(u'我是Text组件')
        self.text1 = urwid.AttrWrap(self.text1, 'header')

        self.button = urwid.Button(u'我是Button组件')
        urwid.connect_signal(self.button, 'click', self.callback)
        self.button = urwid.AttrWrap(self.button, 'header')

        self.filler = urwid.Filler(urwid.AttrWrap(urwid.Text(u"我是经过BoxAdapter流化后的filler组件"), 'header'), 'middle', top=3, bottom=4)
        self.filler = urwid.BoxAdapter(self.filler, 12)
        self.filler = urwid.AttrWrap(self.filler, 'padding')

        self.padding = urwid.Padding(urwid.AttrWrap(urwid.Text(u"我是经过BoxAdapter流化后的padding组件"), 'header'), 'center', left=5, right=10)
        #self.padding = urwid.BoxAdapter(self.padding, 12)
        self.padding = urwid.AttrWrap(self.padding, 'padding')


        self.list_content_inner = [self.text1, blank, self.button, blank, self.filler, blank, self.padding]

        listbox_inner = urwid.ListBox(urwid.SimpleListWalker(self.list_content_inner))
        listbox_inner = urwid.AttrWrap(listbox_inner, 'padding')

        listbox_content = [self.text0, urwid.BoxAdapter(listbox_inner, 40)]

        return urwid.ListBox(urwid.SimpleListWalker(listbox_content))


