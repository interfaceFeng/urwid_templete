# -*- coding: utf-8 -*-
import logging
log = logging.getLogger('dasoneuser')

import urwid
import common.modulehelper as modulehelper
from settings import Settings
import time
from collections import OrderedDict


class DASONEUser(urwid.WidgetWrap):
    def __init__(self, parent, language=modulehelper.LanguageType.CHINESE):
        self.parent = parent
        self.screen = None
        self.name = None
        self.visible = True
        self.language = language

        # list the fields need to choose language
        self.language_field = {
            'header_content': None,
            'button_label': None,
            'name': None,
            'defaults': None
        }

        # choose language default choice is chinese
        self.language_field = modulehelper.LanguageType.choose_language("DASONEUSER",
                                                  language, language_field=self.language_field)

        # save strings as class member
        self.defaults = self.language_field['defaults']
        self.name = self.language_field['name']
        self.button_label = self.language_field['button_label']
        self.header_content = self.language_field['header_content']
        self.fields = ["DASONE_ACCESS/password", "CONFIRM_PASSWORD"]

        self.oldsettings = self.load()

    def load(self):
        # read yaml file
        defaultsettings = Settings().read(self.parent.defaultsettingsfile)
        oldsettings = defaultsettings
        oldsettings.update(Settings().read(self.parent.settingsfile))
        log.debug(oldsettings)

        # oldsettings = Settings().read(self.parent.settingsfile)
        for setting in self.defaults.keys():
            try:
                if "/" in setting:
                    part1, part2 = setting.split("/")
                    self.defaults[setting]["value"] = oldsettings[part1][part2]
                else:
                    self.defaults[setting]["value"] = oldsettings[setting]
            except Exception:
                log.warning("No setting named %s found." % setting)
                continue
        return oldsettings



    def save(self, responses):
        # generic settings start
        newsettings = OrderedDict()
        for setting in responses.keys():
            if "/" in setting:
                part1, part2 = setting.split("/")
                if part1 not in newsettings:
                    #We may not touch all settings, so copy oldsettings first
                    try:
                        newsettings[part1] = self.oldsettings[part1]
                    except Exception:
                        if part1 not in newsettings.keys():
                            newsettings[part1] = OrderedDict()
                        log.warning("issues setting newsettings %s " % setting)
                        log.warning("current newsettings: %s" % newsettings)
                newsettings[part1][part2] = responses[setting]
            else:
                newsettings[setting] = responses[setting]
        Settings().write(newsettings,
                         defaultsfile=self.parent.defaultsettingsfile,
                         outfn=self.parent.settingsfile)

        self.parent.footer.original_widget.set_text("Changes applied successfully.")
        # Reset fields
        self.cancel(None)





    def check(self, args):
        """Validate that all fields have valid values and sanity checks."""
        self.parent.footer.original_widget.set_text("Checking data...")
        self.parent.refresh_screen()
        #time.sleep(2)


        # get all textfield information
        responses = dict()

        for index, filename in enumerate(self.fields):
            responses[filename] = self.edits[index].original_widget.get_edit_text()

        # validate each field
        errors = []

        # passwords must match
        if responses["DASONE_ACCESS/password"] != responses["CONFIRM_PASSWORD"]:
            if responses["DASONE_ACCESS/password"] != self.defaults[
                        "DASONE_ACCESS/password"]["value"]:
                errors.append("Passwords do not match.")
            else:
                errors.append("Passwords do not be changed")

        # password needs to be in ASCII character set
        try:
            if responses["DASONE_ACCESS/password"].decode('ascii'):
                pass
        except UnicodeDecodeError:
            errors.append("Password contains non-ASCII characters.")

        if len(errors) > 0:
            self.parent.footer.original_widget.set_text("Error: %s"
                                                        % (errors[0]))
            log.error("Error: %s %s" % (len(errors), errors))
            return False
        else:
            self.parent.footer.original_widget.set_text("No error found.")
            # Remove confirm from responses so it isn't saved
            del responses["CONFIRM_PASSWORD"]
            return responses

    def cancel(self, args=None):
        if modulehelper.ModuleHelper.cancel(self):
            self.parent.footer.original_widget.set_text('you have'
                                                        ' cancel your edits')

    def apply(self, args=None):
        responses = self.check(args)
        if responses is False:
            log.error("Check failed, can not apply")
            log.error("%s" % (responses))
            for index, fieldname in enumerate(self.fields):
                if fieldname == "DASONE_ACCESS/password":
                    return (self.edits[index].original_widget.get_edit_text() == "")
            return False
        self.save(responses)
        return True

    def refresh(self):
        pass


    def screenUI(self):
        return modulehelper.ModuleHelper.screenUI(self, self.header_content,
                                                  self.fields, self.defaults,
                                                  show_all_button=True,
                                                  button_label=self.button_label)


