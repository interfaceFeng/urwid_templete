# -*- coding: utf-8 -*-

import urwid
import common.modulehelper as modulehelper
import logging
import common.dialog as dialog

log = logging.getLogger('lineboxanddivider')
blank = urwid.Divider(' ')

class MyLineBoxAndDivider(urwid.WidgetWrap):
    def __init__(self, parent, language = modulehelper.LanguageType.CHINESE):
        self.parent = parent
        self.screen = None
        self.name = 'LineBox And Divider'
        self.visible = True
        self.language = language

    def refresh(self):
        pass

    def apply(self, args=None):
        pass



    def screenUI(self):
        self.text0 = urwid.Text(u'LineBox是一个在包装组件外围画一圈的组件')
        self.text1 = urwid.Text([u'Divider是指定',('red', u'一个'), u'字符作为填充符，大小为的一行的组件'])
        self.divider1 = urwid.Divider('*')
        self.divider2 = urwid.Divider('-', 5, 3)
        self.text2 = urwid.Text(u'')
        self.text2 = urwid.AttrWrap(self.text2, 'header')
        self.text3 = urwid.Text(u'')
        self.text3 = urwid.AttrWrap(self.text3, 'header')
        self.list_inner = [self.text2, self.text3, self.divider1, self.divider2]
        self.inner_list_box = urwid.ListBox(urwid.SimpleListWalker(self.list_inner))
        # self.inner_list_box = urwid.BoxAdapter(self.inner_list_box, 3)
        self.inner_box = urwid.BoxAdapter(self.inner_list_box, 20)




        self.text2.set_text(u"divider1 的内容为 %s" % ",".join(self.divider1.render((10, )).text))
        self.text3.set_text(u"divider2 的内容为 %s" % ",".join(self.divider2.render((10, )).text))

        self.list_content = [self.text0, self.text1, urwid.Divider(' '), self.inner_box]

        listbox = urwid.ListBox(urwid.SimpleListWalker(self.list_content))
        listbox = urwid.AttrWrap(listbox, 'padding')

        linebox_listbox = urwid.LineBox(listbox, title=u'My LineBox', tline='#', lline='$', trcorner='%', blcorner='^',
                                        rline='&', bline='*', brcorner='!')
        return linebox_listbox

