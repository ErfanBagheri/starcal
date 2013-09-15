#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scal2 import core
from scal2.locale_man import tr as _

from scal2 import event_lib
from gi.repository import Gtk
from gi.repository import Gdk

class RuleWidget(Gtk.ComboBox):
    def __init__(self, rule):
        self.rule = rule
        ###
        ls = Gtk.ListStore(str)
        Gtk.ComboBox.__init__(self)
        self.set_model(ls)
        ###
        cell = Gtk.CellRendererText()
        self.pack_start(cell, True)
        self.add_attribute(cell, 'text', 0)
        ###
        self.append_text(_('Every Week'))
        self.append_text(_('Odd Weeks'))
        self.append_text(_('Even Weeks'))
        self.set_active(0)
    def updateWidget(self):
        self.set_active(self.rule.weekNumMode)
    def updateVars(self):
        self.rule.weekNumMode = self.get_active()


