# -*- coding: utf-8 -*-
from scal2 import core
from scal2.locale_man import tr as _

from scal2 import event_lib
from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk

from scal2.ui_gtk.mywidgets.multi_spin_button import IntSpinButton

class RuleWidget(IntSpinButton):
    def __init__(self, rule):
        self.rule = rule
        IntSpinButton.__init__(self, 0, 999999)
    def updateWidget(self):
        self.set_value(self.rule.getData())
    def updateVars(self):
        self.rule.setData(self.get_value())

