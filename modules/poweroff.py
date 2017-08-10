# -*- coding: utf-8 -*-
import urwid
import logging
import common.modulehelper as modulehelper
import common.dialog as dialog
from os import system
import time
log = logging.getLogger('poweroff')

class PowerOff(urwid.WidgetWrap):
    def __init__(self, parent, language=modulehelper.LanguageType.CHINESE):
        self.parent = parent
        self.screen = None
        self.name = None
        self.visible = True
        self.language = language

        # list the fields need to choose language
        self.language_field = {
            'header_content': None,
            'name': None,
            'defaults': None
        }

        # choose language default is chinese
        self.language_field = modulehelper.LanguageType.choose_language("POWEROFF",
                                                        language, language_field=self.language_field)

        # save strings as class member
        self.header_content = self.language_field['header_content']
        self.name = self.language_field['name']
        self.fields = ['button_content']
        self.default = self.language_field['defaults']

        # add callback to button
        extra_fields = {'callback': self.power_off}
        self.default['button_content'].update(extra_fields)


    def power_off(self, args=None):
        if not self.parent.globalsave:
            if self.language == modulehelper.LanguageType.CHINESE:
                msg = u"请确认已经保存了修改"
            elif self.language == modulehelper.LanguageType.ENGLISH:
                msg = u"please check you have saved your changes"
            dialog.display_dialog(self, urwid.Text(msg),
                                  "You cannot power off immediate!")
            return False

        else:
            time.sleep(1.5)
            system('reboot')
            self.parent.exit_program(None)


    def refresh(self):
        pass

    def apply(self, args=None):
        pass

    def check(self, args=None):
        pass

    def cancel(self, args=None):
        pass


    def screenUI(self):
        return modulehelper.ModuleHelper.screenUI(self, self.header_content,
                                                  self.fields, self.default,
                                                  button_visible=False)

