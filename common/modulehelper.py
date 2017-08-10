import logging
import urwid
import common.urwidwidgetwrapper as urwidwrapper
import six
import os
try:
    from collections import OrderedDict
except Exception:
    # python 2.6 or earlier use backport
    from ordereddict import OrderedDict
import yaml

log = logging.getLogger('common.modulehelper')

blank = urwid.Divider()

class LanguageType(object):
    CHINESE = 1 # default value
    ENGLISH = 2
    tail ={
        CHINESE: "_ch",
        ENGLISH: "_en"
    }
    @classmethod
    def choose_language(cls, part, language=CHINESE,
                        language_field=None):
        stringdir = "%s/strings" % \
                     os.getcwd()
        language_tail = cls.tail.get(language, "_ch")
        stringsfile = stringdir + '/' + 'strings' + language_tail + '.yaml'
        strings = cls._read_string_by_language(stringsfile,
                                              part, language_tail)

        for key in language_field:
            language_field[key] = strings[key]

        return language_field

    @classmethod
    def _read_string_by_language(cls, yamlfile, partname,
                                tail):
        try:
            infile = file(yamlfile, 'r')
            strings = yaml.load(infile)
            if strings is not None:
                strings = strings[partname]
                # if strings is not None:
                #     strings = strings[tail]
                #     return strings
                # else:
                #     log.warning("there is no strings in language %s"
                #             % tail)
                #     return OrderedDict()
                return strings
            else:
                log.warning("there is no part %s in strings file"
                    % partname)
                return OrderedDict()
        except Exception:
            if yamlfile is not None:
                import logging
                log.error("Unable to read YAML: %s" % yamlfile)
            log.debug("return empty orderedDict")
            return OrderedDict()


class WidgetType(object):
    TEXT_FIELD = 1  # default value. may be skipped
    LABEL = 2
    RADIO = 3
    CHECKBOX = 4
    LIST = 5
    BUTTON = 6



class ModuleHelper(object):
    @classmethod
    def _get_header_content(cls, header_text):
        # this method can extend its function
        # when header_text is not only text-type
        # by add a filter
        def _convert(text):
            if isinstance(text, six.string_types):
                return urwid.Text(text)
            return text

        return [_convert(text) for text in header_text]

    @classmethod
    def _create_button_widget(cls, default_data):
        label = default_data.get('label')
        callback = default_data.get('callback')
        button = urwidwrapper.Button(label, callback)
        return button

    @classmethod
    def _create_widget(cls, key, default_data, toolbar):
        field_type = default_data.get('type', WidgetType.TEXT_FIELD)

        # you can expend widget's type here
        if field_type == WidgetType.TEXT_FIELD:
            ispassword = "PASSWORD" in key.upper()
            label = default_data.get('label', '')
            default = default_data.get('value', '')
            tooltip = default_data.get('tooltip', '')
            return urwidwrapper.TextField(key, label, left_width=20,
                                          default_value=default,
                                          tooltip=tooltip, tool_bar=toolbar,
                                          ispassword=ispassword)
        elif field_type == WidgetType.BUTTON:
            return cls._create_button_widget(default_data)

    @classmethod
    def _setup_widgets(cls, toolbar, fields, defaults):
        return [cls._create_widget(key, defaults.get(key, {}), toolbar)
                for key in fields]

    @classmethod
    def _get_check_column(cls, modobj, show_all_button, button_label):
        # check button
        button_check = urwidwrapper.Button(button_label[0], modobj.check)

        # Button to revert to previously saved settings
        button_cancel = urwidwrapper.Button(button_label[1], modobj.cancel)

        # Button to apply (and check again)
        button_apply = urwidwrapper.Button(button_label[2], modobj.apply)

        if modobj.parent.globalsave and show_all_button is False:
            return urwidwrapper.Columns([button_check])
        return urwidwrapper.Columns([
            button_check, button_cancel,
            button_apply, ('weight', 2, blank)])

    @classmethod
    def cancel(cls, modobj, button=None):
        for index, fieldname in enumerate(modobj.fields):
            if fieldname != "blank" and "label" not in fieldname:
                try:
                    modobj.edits[index].set_edit_text(modobj.defaults[fieldname][
                                                       'value'])
                    return True
                except AttributeError:
                    log.warning("Field %s unable to reset text" % fieldname)
                    return False

    @classmethod
    def screenUI(cls, modobj, header_text=None, fields=None,
                 defaults=None, show_all_button=False, button_visible=True,
                 button_label=None):
        log.debug("Preparing screen UI for %s", modobj.name)
        # preparing header_content
        log.debug("Preparing header_context for %s", modobj.name)
        listbox_content = cls._get_header_content(header_text)

        # preparing editable fields with widgets
        log.debug("Preparing setup widgets for %s", modobj.name)
        edits = cls._setup_widgets(modobj.parent.footer, fields, defaults)
        # use listbox_content to store header_text and edits fields
        listbox_content.append(blank)
        listbox_content.extend(edits)
        listbox_content.append(blank)

        # Wrap buttons into Columns so it doesn't expand and look ugly
        log.debug("Preparing button for %s", modobj.name)
        if button_visible:
            check_column = cls._get_check_column(modobj, show_all_button,
                                                button_label)
            listbox_content.append(check_column)

        # add everything into a listbox and return it
        listwalker = urwidwrapper.TabbedListWalker(listbox_content)
        screen = urwid.ListBox(listwalker)

        # save information which may used in future

        modobj.edits = edits
        modobj.walker = listwalker
        modobj.listbox_content = listbox_content

        return screen



