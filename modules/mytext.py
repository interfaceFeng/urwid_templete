# -*- coding: utf-8 -*-

import urwid
import common.modulehelper as modulehelper

class MyText(urwid.WidgetWrap):
    def __init__(self, parent, language = modulehelper.LanguageType.CHINESE):
        self.parent = parent
        self.screen = None
        self.name = 'Text'
        self.visible = True
        self.language = language

    def refresh(self):
        pass

    def apply(self, args=None):
        pass

    def screenUI(self):
        text_list = []
        pos = ['left', 'center', 'right']
        for i in range(1, 4):
            text = urwid.Text('')
            text.set_align_mode(pos[i % 3])
            text.set_text('姜毅帅第%s次' % i)
            size = text.pack()
            size_col, size_row = size
            size_argus = (size_col, size_row, pos[i % 3])
            text2 = urwid.Text('上面这句话最少需要%s列%s行的空间, 文本位置在%s' % size_argus)
            text_list.append(text)
            text_list.append(text2)
        text_box = urwid.ListBox(urwid.SimpleListWalker(text_list))
        return text_box
