# -*- coding: utf-8 -*-

import urwid
import common.modulehelper as modulehelper
import logging
import common.dialog as dialog
from common.urwidwidgetwrapper import Button as MyButton, BoxText
import copy

log = logging.getLogger('gridflow')
blank = urwid.Divider(' ')

class MyGridFlow(urwid.WidgetWrap):
    def __init__(self, parent, language = modulehelper.LanguageType.CHINESE):
        self.parent = parent
        self.screen = None
        self.name = 'GridFlow'
        self.visible = True
        self.language = language

    def refresh(self):
        pass

    def apply(self, args=None):
        pass


    def callback_button(self, button):
        msg = 'this is a menu item, %s is called' % button.get_label()
        dialog.display_dialog(self, urwid.Text(msg), "Hello")

    def callback_edit(self, edit, newtext, args1):
        self.text3.set_text(u"你选择了edit %s, edit中编辑的内容为%s, 你的光标所在的位置为%s"
                            %(args1, newtext, str(self.gridflow.get_cursor_coords(((100, ))))))

    def callback_radiobutton(self, radiobutton, args1, args2):
        self.text3.set_text(u"你选择了radiobutton %s, 该radiobutton"
                            u"在gridflow的第%s个元素中, "
                            u"该元素为%s"%(args2, self.gridflow.focus_position,
                                       str(self.gridflow.focus)))

    def callback_movebutton(self, button):
        self.gridflow.set_focus(0)
        self.text3.set_text(u"")
        self.gridflow.keypress((100, ), 'enter')




    def screenUI(self):
        self.text0 = urwid.Text(u'GridFlow 是一个由多个cell组成的流组件，其中每个组件都是流组件，宽度相同')
        self.text1 = urwid.Text(u"对于该组件的cell序列，grid会先横向排列，当一行占满时才会使用第二行")
        self.text2 = urwid.Text(u'你可以拖动鼠标变化控制台大小查看显示效果')
        self.text3 = urwid.Text(u'状态信息看这里')
        button_list = []
        for i in range(0, 10):
            button = MyButton(u"button %s"%i, self.callback_button)
            button_list.append(button)
        self.button_listbox = urwid.ListBox(urwid.SimpleListWalker(button_list))
        self.button_listbox = urwid.AttrWrap(self.button_listbox, 'header')
        self.button_listbox_flo = urwid.BoxAdapter(self.button_listbox, 10)

        edit_list = []
        for i in range(0, 10):
            edit = urwid.Edit((u'edit%s'%i).ljust(12))
            urwid.connect_signal(edit, 'change', self.callback_edit, i)
            edit_list.append(edit)
        self.edit_listbox = urwid.ListBox(urwid.SimpleListWalker(edit_list))
        self.edit_listbox = urwid.AttrWrap(self.edit_listbox, 'editbx', 'editfc')
        self.edit_listbox_flo = urwid.BoxAdapter(self.edit_listbox, 10)

        text_list = []
        for i in range(0, 10):
            text = urwid.Text(u'text %s'%i)
            text_list.append(text)
        text_listbox = urwid.ListBox(urwid.SimpleListWalker(text_list))
        text_listbox = urwid.AttrWrap(text_listbox, 'padding')
        text_listbox_flo = urwid.BoxAdapter(text_listbox, 10)

        radiobutton_list = []
        self.rgroup = []
        for i in range(0, 10):
            radiobutton = urwid.RadioButton(self.rgroup, u'radiobutton %s'%i, False,
                                     self.callback_radiobutton, i)
            radiobutton_list.append(radiobutton)
        self.radiobutton_listbox = urwid.ListBox(urwid.SimpleListWalker(radiobutton_list))
        self.radiobutton_listbox_flo = urwid.BoxAdapter(self.radiobutton_listbox, 10)

        self.move_button = MyButton(u"点击将焦点设置到第一个组件的起始位置", self.callback_movebutton)

        grid_list = [self.button_listbox_flo, text_listbox_flo, self.edit_listbox_flo,
                     self.radiobutton_listbox_flo]

        self.gridflow = urwid.GridFlow(grid_list, 50, 2, 3, 'center')
        listbox_content = [self.text0, self.text1, self.text2, blank, self.gridflow,
                           self.text3, self.move_button]

        return urwid.ListBox(urwid.SimpleListWalker(listbox_content))


