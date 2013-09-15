#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scal2 import core
from scal2.locale_man import getMonthName
from scal2.locale_man import tr as _


from scal2 import event_lib
from gi.repository import Gtk
from gi.repository import Gdk

from scal2.ui_gtk.utils import WeekDayComboBox, MonthComboBox

class RuleWidget(Gtk.HBox):
    def __init__(self, rule):
        self.rule = rule
        #####
        Gtk.HBox.__init__(self)
        ###
        combo = Gtk.ComboBoxText()
        for item in rule.wmIndexNames:
            combo.append_text(item)
        self.pack_start(combo, 0, 0, 0)
        self.nthCombo = combo
        ###
        combo = WeekDayComboBox()
        self.pack_start(combo, 0, 0, 0)
        self.weekDayCombo = combo
        ###
        self.pack_start(Gtk.Label(_(' of ')), 0, 0, 0)
        ###
        combo = MonthComboBox(True)
        combo.build(rule.getMode())
        self.pack_start(combo, 0, 0, 0)
        self.monthCombo = combo
    def updateVars(self):
        self.rule.wmIndex = self.nthCombo.get_active()
        self.rule.weekDay = self.weekDayCombo.getValue()
        self.rule.month = self.monthCombo.getValue()
    def updateWidget(self):
        self.nthCombo.set_active(self.rule.wmIndex)
        self.weekDayCombo.setValue(self.rule.weekDay)
        self.monthCombo.setValue(self.rule.month)
    def changeMode(self, newMode):
        self.monthCombo.build(newMode)



