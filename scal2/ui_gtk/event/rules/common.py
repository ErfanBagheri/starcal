#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scal2 import core
from scal2.locale_man import tr as _

from scal2 import event_lib
from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk

'''
class MultiValueRule(gtk.HBox):
    def __init__(self, rule, ValueWidgetClass):
        self.rule = rule
        self.ValueWidgetClass = ValueWidgetClass
        ##
        gtk.HBox.__init__(self)
        self._widgetsBox = gtk.HBox()
        self.pack_start(self._widgetsBox, 0, 0, 0)
        ##
        self.removeButton = gtk.Button()
        self.removeButton.set_image(gtk.Image.new_from_stock(gtk.STOCK_REMOVE, gtk.IconSize.MENU))
        self.removeButton.connect('clicked', self.removeLastWidget)
        ##


        ##
        self.removeButton.hide()## FIXME

    def removeLastWidget(self, obj=None):

    def addWidget(self, obj=None):
        widget = self.ValueWidgetClass()
'''


