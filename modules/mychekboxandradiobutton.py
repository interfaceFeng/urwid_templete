# -*- coding: utf-8 -*-

import urwid
import common.modulehelper as modulehelper
import logging
import common.dialog as dialog

log = logging.getLogger('checkandradio')
blank = urwid.Divider(' ')

class MyCheckBoxAndRadioButton(urwid.WidgetWrap):
    def __init__(self, parent, language = modulehelper.LanguageType.CHINESE):
        self.parent = parent
        self.screen = None
        self.name = 'CheckBox And RadioButton'
        self.visible = True
        self.language = language

    def refresh(self):
        pass

    def change_checkbox(self, checkbox, args1, args2):
        if args2 == 1:
            self.text1.set_text('checkbox1 状态变化为 %s'%args1)
        elif args2 == 2:
            self.text2.set_text('checkbox2 状态变化为 %s'%args1)

    def change_radiobutton(self, radiobutton, args1, args2):
        if args2 == 1:
            self.text3.set_text('radiobutton1 状态变化为 %s'%args1)
        elif args2 == 2:
            self.text4.set_text('radiobutton2 状态变化为 %s'%args1)

    def apply(self, args):
        pass

    def screenUI(self):
        self.checkbox = urwid.CheckBox(u'有混合模式的checkbox', 'mixed', True)
        self.text1 = urwid.Text('status checkbox1')
        self.checkbox2 = urwid.CheckBox(u'没有混合模式的checkbox', False, False)
        self.text2 = urwid.Text('status checkbox2')
        self.content_list = [self.checkbox, self.checkbox2, self.text1, self.text2]

        urwid.connect_signal(self.checkbox, 'change', self.change_checkbox, 1)
        urwid.connect_signal(self.checkbox2, 'change', self.change_checkbox, 2)

        blank_list = [blank, blank, blank]
        self.content_list.extend(blank_list)
        self.rgroup = []
        self.radiobutton1 = urwid.RadioButton(self.rgroup, u"radiobutton1", False, )
        self.text3 = urwid.Text('status radiobutton1')
        self.radiobutton2 = urwid.RadioButton(self.rgroup, u"rasiobutton2", True)
        self.text4 = urwid.Text('status radiobutton2')
        urwid.connect_signal(self.radiobutton1, 'change', self.change_radiobutton, 1)
        urwid.connect_signal(self.radiobutton2, 'change', self.change_radiobutton, 2)

        self.content_list.extend([self.radiobutton1, self.radiobutton2, self.text3, self.text4])

        return urwid.ListBox(urwid.SimpleListWalker(self.content_list))

