#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scal2 import core
from scal2.locale_man import tr as _

from scal2 import event_lib
from gi.repository import Gtk
from gi.repository import Gdk

'''
class MultiValueRule(Gtk.HBox):
    def __init__(self, rule, ValueWidgetClass):
        self.rule = rule
        self.ValueWidgetClass = ValueWidgetClass
        ##
        Gtk.HBox.__init__(self)
        self._widgetsBox = Gtk.HBox()
        self.pack_start(self._widgetsBox, 0, 0, 0)
        ##
        self.removeButton = Gtk.Button()
        self.removeButton.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_REMOVE, Gtk.IconSize.MENU))
        self.removeButton.connect('clicked', self.removeLastWidget)
        ##


        ##
        self.removeButton.hide()## FIXME

    def removeLastWidget(self, obj=None):

    def addWidget(self, obj=None):
        widget = self.ValueWidgetClass()
'''


