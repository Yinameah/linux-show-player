# -*- coding: utf-8 -*-
#
# This file is part of Linux Show Player
#
# Copyright 2012-2016 Francesco Ceruti <ceppofrancy@gmail.com>
# Copyright 2016-1017 Aurélien Cibrario <aurelien.cibrario@gmail.com>
#
# Linux Show Player is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Linux Show Player is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Linux Show Player.  If not, see <http://www.gnu.org/licenses/>.

"""
Custom QTabWidget and QTabBar. Has ability to "fold" when double click on tab is detected
It has been designed for only one tabbar, as used in cue_setting_panel.py
"""

from PyQt5.QtWidgets import QTabWidget, QTabBar, QSizePolicy
from PyQt5.QtCore import QSize


class QFoldableTab(QTabWidget):

    def __init__(self):
        super().__init__()

        self.setTabBar(QFoldableTabBar())

        self.is_fold = False

        # Just for initialization. These values should overridden when a tab is added
        self.min_folded_width = 100
        self.min_widget_width = 100
        self.min_widget_height = 100

        sizepol = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.setSizePolicy(sizepol)

        self.tabBarDoubleClicked.connect(self.toggle_fold)

    def toggle_fold(self):
        if self.is_fold:
            self.unfold()
            self.is_fold = False
        else:
            self.fold()
            self.is_fold = True

    def fold(self):
        self.is_fold = True
        self.hide()
        self.show()
        self.settings_page.hide()

    def unfold(self):
        self.is_fold = False
        self.hide()
        self.show()
        self.settings_page.show()

    def mouseDoubleClickEvent(self, event):
        self.toggle_fold()

    def addTab(self, widget, *__args):
        super().addTab(widget, *__args)
        # Can't be done before a widget as been added
        self.min_folded_width = self.tabBar().tabSizeHint(0).width()
        self.min_widget_height = widget.MinHeight
        self.min_widget_width = widget.MinWidth

        self.settings_page = widget

    def sizeHint(self):
        if self.is_fold:
            size = QSize(self.min_folded_width, self.min_widget_height)
        else:
            size = QSize(self.min_widget_width, self.min_widget_height)
        return size

    def minimumSizeHint(self):
        return self.sizeHint()


class QFoldableTabBar(QTabBar):

    def __init__(self):
        super().__init__()

    def tabSizeHint(self, index):
        """ Seem to be needed to access the sizeHint from QFoldableTab """
        return super().tabSizeHint(index)