# -*- coding: utf-8 -*-

import urwid
import common.modulehelper as modulehelper
import logging
import common.dialog as dialog

log = logging.getLogger('frame')
blank = urwid.Divider(' ')

class MyFrame(urwid.WidgetWrap):
    def __init__(self, parent, language = modulehelper.LanguageType.CHINESE):
        self.parent = parent
        self.screen = None
        self.name = 'Frame'
        self.visible = True
        self.language = language

    def refresh(self):
        pass

    def apply(self, args=None):
        pass


    def callback(self, button):
        pass


    def screenUI(self):
        self.text0 = urwid.Text(u'Frame是一个在顶部和底部分别有组件的容器组件')
        self.header = urwid.Text(u'头部在这里')
        self.footer = urwid.Text(u'底部在这里')
        self.footer = urwid.AttrWrap(self.footer, None, 'standout')


        self.text1 = urwid.Text(u'整个配置界面的顶层容器就是一个frame，frame原生不能用键盘移动焦点位置')
        self.text1 = urwid.AttrWrap(self.text1, 'header')


        self.list_content_inner = [self.text1]

        listbox_inner = urwid.ListBox(urwid.SimpleListWalker(self.list_content_inner))
        listbox_inner = urwid.AttrWrap(listbox_inner, 'padding')

        self.frame = urwid.Frame(listbox_inner, self.header, self.footer)
        self.frame.set_focus('footer')

        self.list_content = [self.text0, urwid.BoxAdapter(self.frame, 20)]
        return urwid.ListBox(urwid.SimpleListWalker(self.list_content))


