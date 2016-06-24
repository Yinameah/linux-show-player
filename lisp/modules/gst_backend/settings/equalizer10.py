# -*- coding: utf-8 -*-
#
# This file is part of Linux Show Player
#
# Copyright 2012-2016 Francesco Ceruti <ceppofrancy@gmail.com>
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

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QGroupBox, QGridLayout, QLabel, QSlider, QVBoxLayout

from lisp.modules.gst_backend.elements.equalizer10 import Equalizer10
from lisp.ui.settings.settings_page import SettingsPage


class Equalizer10Settings(SettingsPage):

    Name = "Equalizer"
    ELEMENT = Equalizer10

    FREQ = ["30Hz", "60Hz", "120Hz", "240Hz", "475Hz", "950Hz", "1900Hz",
            "3800Hz", "7525Hz", "15KHz"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignTop)

        self.groupBox = QGroupBox(self)
        self.groupBox.resize(self.size())
        self.groupBox.setTitle("10 Bands Equalizer (IIR)")
        self.groupBox.setLayout(QGridLayout())
        self.groupBox.layout().setVerticalSpacing(0)
        self.layout().addWidget(self.groupBox)

        self.sliders = {}

        for n in range(10):
            label = QLabel(self.groupBox)
            label.setMinimumWidth(QFontMetrics(label.font()).width('000'))
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setNum(0)
            self.groupBox.layout().addWidget(label, 0, n)

            slider = QSlider(self.groupBox)
            slider.setRange(-24, 12)
            slider.setPageStep(1)
            slider.setValue(0)
            slider.setOrientation(QtCore.Qt.Vertical)
            slider.valueChanged.connect(label.setNum)
            self.groupBox.layout().addWidget(slider, 1, n)
            self.groupBox.layout().setAlignment(slider, QtCore.Qt.AlignHCenter)
            self.sliders["band" + str(n)] = slider

            fLabel = QLabel(self.groupBox)
            fLabel.setStyleSheet('font-size: 8pt;')
            fLabel.setAlignment(QtCore.Qt.AlignCenter)
            fLabel.setText(self.FREQ[n])
            self.groupBox.layout().addWidget(fLabel, 2, n)

    def enable_check(self, enable):
        self.groupBox.setCheckable(enable)
        self.groupBox.setChecked(False)

    def get_settings(self):
        settings = {}

        if not (self.groupBox.isCheckable() and not self.groupBox.isChecked()):
            for band in self.sliders:
                settings[band] = self.sliders[band].value()

        return settings

    def load_settings(self, settings):
        for band in self.sliders:
            self.sliders[band].setValue(settings.get(band, 0))