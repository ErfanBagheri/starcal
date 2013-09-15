#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scal2 import core
from scal2.locale_man import tr as _

from scal2 import event_lib
from gi.repository import Gtk
from gi.repository import Gdk

from scal2.ui_gtk.mywidgets.num_ranges_entry import NumRangesEntry

class RuleWidget(NumRangesEntry):
    def __init__(self, rule):
        self.rule = rule
        NumRangesEntry.__init__(self, 1, 31, 10)
    def updateWidget(self):
        self.setValues(self.rule.values)
    def updateVars(self):
        self.rule.values = self.getValues()


