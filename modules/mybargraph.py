# -*- coding: utf-8 -*-

import urwid
import common.modulehelper as modulehelper
import logging
import common.dialog as dialog
from common.urwidwidgetwrapper import Button as MyButton, BoxText

log = logging.getLogger('columnsandpile')
blank = urwid.Divider(' ')

class MyColumnsAndPile(urwid.WidgetWrap):
    def __init__(self, parent, language = modulehelper.LanguageType.CHINESE):
        self.parent = parent
        self.screen = None
        self.name = 'Columns And Pile'
        self.visible = True
        self.language = language

    def refresh(self):
        pass

    def apply(self, args=None):
        pass


    def callback(self, button):
        msg = 'this is a menu item'
        self.show_text2.set_text(u"你选择了%s, 它在第%s行"%(button.get_label(), self.cols1.get_focus_column()))
        dialog.display_dialog(self, urwid.Text(msg), "Hello")

    def _create_menu_col1(self):
        pile = urwid.Pile(
            [
                ('pack', MyButton(u'Pile1', self.callback)),
                ('pack', MyButton(u'menu item 1', self.callback)),
                ('pack', MyButton(u'menu item 2', self.callback)),
                ('pack', MyButton(u'menu item 2', self.callback)),
            ],
            #inital focus pos
            1
        )
        return pile

    def _create_text_col1(self):
        pile = urwid.Pile(
            [
                urwid.Text(u'Pile2'),
                urwid.Text(u'text item 1'),
                urwid.Text(u'text item 2'),
                urwid.Text(u'text item 3')
            ],
            #inital focus pos
            2
        )
        return pile

    def _create_menu_col2(self):
        pile = urwid.Pile(
            [
                (3, MyButton(u'Pile1', self.callback)),
                (2, MyButton(u'menu item 1', self.callback)),
                ('weight', 3, MyButton(u'menu item 2', self.callback)),
                #('weight', 1, MyButton(u'menu item 3', self.callback)),
            ],
            #inital focus pos
            1
        )
        return pile

    def _create_text_col2(self):
        pile = urwid.Pile(
            [
                (3, BoxText(u'Pile2')),
                (2, BoxText(u'text item 1')),
                ('weight', 3, BoxText(u'text item 2')),
                #('weight', 1, BoxText(u'text item3'))
            ],
            #inital focus pos
            1
        )
        return pile


    def screenUI(self):
        self.text0 = urwid.Text(u'Columns是一个将装饰的组件序列水平安置的盒组件，'
                                u'其中所有组件全部是可迭代的')
        self.text1 = urwid.Text(u'Pile是一个将装饰的组件序列垂直安置的盒组件，'
                                u'其中所有组件全部是可迭代的')
        self.text2 = urwid.Text(u'下列展示的样本中每一列都是column的一列，其中每列的每个元素都是一个pile的一个元素')

        self.text_show1 = urwid.Text(u'样本:col看做流组件，其中每一列pile看做盒组件，盒组件的每一个元素是流组件')
        # self.text_show2 = urwid.Text(u'样本2 col看做盒组件，其中每一列pile看做盒组件，盒组件的每一个元素是盒组件')

        menu_col1 = self._create_menu_col1()
        menu_col1 = urwid.AttrWrap(menu_col1, 'red')
        text_col1 = self._create_text_col1()
        text_col1 = urwid.AttrWrap(text_col1, 'padding')

        self.cols1 = urwid.Columns(
            [
                (20, menu_col1),

                ('weight', 5, text_col1)
            ],
            10
        )
        self.show_text1 = urwid.Text(u"")
        self.show_text2 = urwid.Text(u"状态信息看这里")
        self.show_text1.set_text(u"该col中各列的宽度为：%s" % (",".join(str(i) for i in self.cols1.column_widths((100, 20)))))
        #self.show_text2.set_text(u"该col的各Pile中是盒组件的有 %s" % str(self.cols1.box_columns))
        #self.list_box1 = urwid.ListBox(urwid.SimpleListWalker([self.cols1]))

        # menu_col2 = self._create_menu_col2()
        # text_col2 =self._create_text_col2()
        #
        # self.cols2 = urwid.Columns(
        #     [
        #         (20, menu_col1),
        #
        #         (50, text_col1)
        #     ],
        #     10
        # )
        #self.list_box2 = urwid.ListBox(urwid.SimpleListWalker([urwid.BoxAdapter(self.cols2)]))

        listbox_content = [self.text0, self.text1, self.text2, blank, self.text_show1, blank,
                           self.cols1, blank, self.show_text1, self.show_text2]

        return urwid.ListBox(urwid.SimpleListWalker(listbox_content))


