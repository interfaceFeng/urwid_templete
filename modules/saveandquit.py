# -*- coding: utf-8 -*-
import urwid
import logging
from common.modulehelper import LanguageType
from common.urwidwidgetwrapper import Button as WrapButton
import common.dialog as dialog
import common.modulehelper as modulehelper
import time

log = logging.getLogger('saveandquit')

class SaveAndQuit(urwid.WidgetWrap):
    def __init__(self, parent, language=LanguageType.CHINESE):
        self.parent = parent
        self.screen = None
        self.language_field = {
            'name': None,
            'header_content': None
        }
        modulehelper.LanguageType.choose_language("SAVEANDQUIT",
                                                  language,
                                                  self.language_field)
        self.name = self.language_field['name']
        self.visible = True
        self.header_content = [self.language_field['header_content']]
        self.fields = []
        self.defaults = dict()

        self.button_label = None # do not effect in this module

        # UI content 3 button
        self.saveandcontinue_button = None
        self.saveandquit_button = None
        self.quitwithoutsaving_button = None
        self.con_button_language(language)
        self.savebutton = [self.saveandcontinue_button,
                               self.saveandquit_button, self.quitwithoutsaving_button]
        self.header_content.extend(self.savebutton)

    def con_button_language(self, language):
        if language == LanguageType.ENGLISH:
            self.saveandcontinue_button = WrapButton("Save and Continue",
                                                   self.save_and_continue)
            self.saveandquit_button = WrapButton("Save and Quit", self.save_and_quit)
            self.quitwithoutsaving_button = WrapButton("Quit without saving",
                                                 self.quit_without_saving)
        elif language == LanguageType.CHINESE:
            self.saveandcontinue_button = WrapButton("保存并继续",
                                                self.save_and_continue)
            self.saveandquit_button = WrapButton("保存并退出", self.save_and_quit)
            self.quitwithoutsaving_button = WrapButton("退出不保存",
                                                  self.quit_without_saving)

    def save_and_continue(self, args):
        self.save()

    def save_and_quit(self, args):
        if self.save():
            self.parent.refresh_screen()
            time.sleep(1.5)
            self.parent.exit_program(None)


    def quit_without_saving(self, args):
        # time.sleep(1.5)
        self.parent.exit_program(None)


    def save(self):
        results, modulename = self.parent.global_save()
        if results:
            self.parent.footer.original_widget.set_text("All changes saved successfully!")
            return True
        else:
            #show pop up with more details
            msg = "ERROR: Module %s failed to save. Go back" % (modulename) \
                  + " and fix any mistakes or choose Quit without Saving."
            dialog.display_dialog(self, urwid.Text(msg),
                                  "Error saving changes!")
            return False

    def refresh(self):
        pass

    def apply(self, args=None):
        pass

    def screenUI(self):
        return modulehelper.ModuleHelper.screenUI(self, self.header_content,
                                                  self.fields, self.defaults,
                                                  button_visible=False)