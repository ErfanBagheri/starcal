# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Saeed Rasooli <saeed.gnu@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/gpl.txt>.
# Also avalable in /usr/share/common-licenses/GPL on Debian systems
# or /usr/share/licenses/common/GPL3/license.txt on ArchLinux
from time import localtime

import sys

from scal2.locale_man import tr as _
from scal2.locale_man import rtl, rtlSgn
from scal2.cal_types import calTypes
from scal2 import core
from scal2 import ui

from gi.repository import Gtk

from scal2.ui_gtk.decorators import *
from scal2.ui_gtk.utils import dialog_add_button
from scal2.ui_gtk import gtk_ud as ud
from scal2.ui_gtk.event.occurrence_view import DayOccurrenceView


@registerSignals
class AllDateLabelsVBox(Gtk.VBox, ud.IntegratedCalObj):
    _name = 'allDateLabels'
    desc = _('Dates')
    def __init__(self):
        Gtk.VBox.__init__(self)
        self.initVars()
        ##
        self.set_spacing(5)
    def onDateChange(self, *a, **ka):
        ud.IntegratedCalObj.onDateChange(self, *a, **ka)
        for child in self.get_children():
            child.destroy()
        sgroup = Gtk.SizeGroup(Gtk.SizeGroupMode.HORIZONTAL)
        for i, module in calTypes.iterIndexModule():
            hbox = Gtk.HBox()
            label = Gtk.Label(label=_(module.desc))
            label.set_alignment(0, 0.5)
            hbox.pack_start(label, 0, 0, 0)
            sgroup.add_widget(label)
            hbox.pack_start(Gtk.Label('  '), 0, 0, 0)
            ###
            hbox.pack_start(
                Gtk.Label(
                    ui.cell.format(ud.dateFormatBin, i)
                ),
                0,
                0,
                0,
            )
            ###
            self.pack_start(hbox, 0, 0, 0)
        self.show_all()


@registerSignals
class PluginsTextView(Gtk.TextView, ud.IntegratedCalObj):
    _name = 'pluginsText'
    desc = _('Plugins Text')
    def __init__(self):
        Gtk.TextView.__init__(self)
        self.initVars()
        ###
        self.set_wrap_mode(Gtk.WrapMode.WORD)
        self.set_editable(False)
        self.set_cursor_visible(False)
        self.set_justification(Gtk.Justification.CENTER)
    def onDateChange(self, *a, **ka):
        ud.IntegratedCalObj.onDateChange(self, *a, **ka)
        self.get_buffer().set_text(ui.cell.pluginsText)


@registerSignals
class DayInfoDialog(Gtk.Dialog, ud.IntegratedCalObj):
    _name = 'dayInfo'
    desc = _('Day Info')
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.initVars()
        ud.windowList.appendItem(self)
        ###
        self.set_title(_('Day Info'))
        self.connect('delete-event', self.onClose)
        self.vbox.set_spacing(15)
        ###
        dialog_add_button(self, Gtk.STOCK_CLOSE, _('Close'), 0, self.onClose)
        dialog_add_button(self, '', _('Previous'), 1, self.goBack)
        dialog_add_button(self, '', _('Today'), 2, self.goToday)
        dialog_add_button(self, '', _('Next'), 3, self.goNext)
        ###
        self.allDateLabels = AllDateLabelsVBox()
        self.pluginsTextView = PluginsTextView()
        self.eventsView = DayOccurrenceView()
        ###
        for item in (self.allDateLabels, self.pluginsTextView, self.eventsView):
            self.appendItem(item)
            ###
            exp = Gtk.Expander()
            exp.set_label(item.desc)
            exp.add(item)
            exp.set_expanded(True)
            self.vbox.pack_start(exp, 0, 0, 0)
        self.vbox.show_all()
        ###
    def onClose(self, obj=None, event=None):
        self.hide()
        return True
    def goBack(self, obj=None):
        ui.jdPlus(-1)
        self.onDateChange()
    def goToday(self, obj=None):
        ui.gotoJd(core.getCurrentJd())
        self.onDateChange()
    def goNext(self, obj=None):
        ui.jdPlus(1)
        self.onDateChange()







