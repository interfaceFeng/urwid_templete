# -*- coding: utf-8 -*-

import urwid
import common.modulehelper as modulehelper
import common.dialog as dialog

class MyEditAndButton(urwid.WidgetWrap):
    def __init__(self, parent, language = modulehelper.LanguageType.CHINESE):
        self.parent = parent
        self.screen = None
        self.name = 'Edit And Button'
        self.visible = True
        self.language = language

    def refresh(self):
        pass

    def check(self, button):
        str = self.edit1.edit_text
        if not str[0].isdigit():
            msg = u'请在第一个框内输入数字'
            dialog.display_dialog(self, urwid.Text(msg),
                                  u"输入错误")
            return False
        str = self.edit2.edit_text
        if not str[0].isalpha():
            msg = u'请在第二个框内输入字母'
            dialog.display_dialog(self, urwid.Text(msg),
                                  u"输入错误")
            return False
        msg = u'姜毅是真的帅'
        dialog.display_dialog(self, urwid.Text(msg),
                              u"告诉你个秘密")
        self.cool_num += 1
        self.text.set_text(self.text.text.replace('%d'%(self.cool_num - 1), '%d'%self.cool_num))
        self.edit1.original_widget.set_mask('*')
        return True

    def apply(self, args=None):
        pass


    def screenUI(self):
        self.text = urwid.Text(u'请在第一个编辑框输入数字，第二个编辑框输入字母，点击确认，有惊喜! 确认0次')
        list_content = [self.text]
        self.cool_num = 0;
        self.edit1 = urwid.Edit(('important', u'数字'.ljust(10)), '123')
        self.edit1 = urwid.AttrWrap(self.edit1, 'editbx')
        self.edit2 = urwid.Edit(('important', u'字母'.ljust(10)), 'abc', edit_pos=2)
        self.edit2 = urwid.AttrWrap(self.edit2, 'editbx')
        self.button = urwid.Button('OK', self.check)
        self.button = urwid.AttrWrap(self.button, None, 'reversed')
        list_content.append(self.edit1)
        list_content.append(self.edit2)

        self.text2 = urwid.Text('')
        self.text3 = urwid.Text('')
        size = (10, )
        pref_col1 = self.edit1.get_pref_col(size)
        pref_col2 = self.edit2.get_pref_col(size)
        self.text2.set_text("第一个编辑框的默认光标位置在%s" % pref_col1)
        self.text3.set_text("第二个编辑框的默认光标位置在%s" % pref_col2)

        list_content.extend([self.text2, self.text3])


        list_content.append(self.button)
        list_box = urwid.ListBox(urwid.SimpleListWalker(list_content))

        return list_box


