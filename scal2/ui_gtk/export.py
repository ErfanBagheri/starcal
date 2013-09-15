# -*- coding: utf-8 -*-
#
# Copyright (C) 2009-2011 Saeed Rasooli <saeed.gnu@gmail.com>
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

import os, sys

from scal2.locale_man import tr as _

from scal2.cal_types import calTypes
from scal2 import core

from scal2 import ui
from scal2.monthcal import getMonthStatus, getCurrentMonthStatus
from scal2.export import exportToHtml

from scal2.ui_gtk.mywidgets.multi_spin_button import DateButton, TimeButton, YearMonthButton
from scal2.ui_gtk.utils import openWindow, dialog_add_button

from gi.repository import Gtk
from gi.repository import Gdk

#gdkColorToHtml = lambda color: '#%.2x%.2x%.2x'%(color.red/256, color.green/256, color.blue/256)



class ExportDialog(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_title(_('Export to %s')%'HTML')
        ## parent=None FIXME
        #self.set_has_separator(False)
        ########
        hbox = Gtk.HBox(spacing=2)
        hbox.pack_start(Gtk.Label(_('Month Range')), 0, 0, 0)
        combo = Gtk.ComboBoxText()
        for t in ('Current Month', 'Whole Current Year', 'Custom'):
            combo.append_text(_(t))
        hbox.pack_start(combo, 0, 0, 0)
        hbox.pack_start(Gtk.Label(''), 1, 1, 0)
        self.combo = combo
        ###
        hbox2 = Gtk.HBox(spacing=2)
        hbox2.pack_start(Gtk.Label(_('from month')), 0, 0, 0)
        self.ymBox0 = YearMonthButton()
        hbox2.pack_start(self.ymBox0, 0, 0, 0)
        hbox2.pack_start(Gtk.Label(''), 1, 1, 0)
        hbox2.pack_start(Gtk.Label(_('to month')), 0, 0, 0)
        self.ymBox1 = YearMonthButton()
        hbox2.pack_start(self.ymBox1, 0, 0, 0)
        hbox.pack_start(hbox2, 1, 1, 0)
        self.hbox2 = hbox2
        combo.set_active(0)
        self.vbox.pack_start(hbox, 0, 0, 0)
        ########
        self.fcw = Gtk.FileChooserWidget(action=Gtk.FileChooserAction.SAVE)
        self.vbox.pack_start(self.fcw, 1, 1, 0)
        self.vbox.set_focus_child(self.fcw)## FIXME
        self.vbox.show_all()
        combo.connect('changed', self.comboChanged)
        ##
        dialog_add_button(self, Gtk.STOCK_CANCEL, _('_Cancel'), 1, self.onDelete)
        dialog_add_button(self, Gtk.STOCK_SAVE, _('_Save'), 2, self.save)
        ##
        self.connect('delete-event', self.onDelete)
        try:
            self.fcw.set_current_folder(core.deskDir)
        except AttributeError:## PyGTK < 2.4
            pass
    def comboChanged(self, widget=None, ym=None):
        i = self.combo.get_active()
        if ym==None:
            ym = (ui.cell.year, ui.cell.month)
        if i==0:
            self.fcw.set_current_name('calendar-%.4d-%.2d.html'%ym)
            self.hbox2.hide()
        elif i==1:
            self.fcw.set_current_name('calendar-%.4d.html'%ym[0])
            self.hbox2.hide()
        else:#elif i==2
            self.fcw.set_current_name('calendar.html')
            self.hbox2.show()
        ## select_region(0, -4) ## FIXME
    def onDelete(self, widget=None, event=None):## hide(close) File Chooser Dialog
        self.hide()
        return True
    def save(self, widget=None):
        self.get_window().set_cursor(Gdk.Cursor.new(Gdk.CursorType.WATCH))
        while Gtk.events_pending():
            Gtk.main_iteration_do(False)
        path = self.fcw.get_filename()
        if path in (None, ''):
            return
        print 'Exporting to html file "%s"'%path
        i = self.combo.get_active()
        months = []
        module = calTypes[core.primaryMode]
        if i==0:
            s = getCurrentMonthStatus()
            months = [s]
            title = '%s %s'%(core.getMonthName(core.primaryMode, s.month, s.year), _(s.year))
        elif i==1:
            for i in xrange(1, 13):
                months.append(getMonthStatus(ui.cell.year, i))
            title = '%s %s'%(_('Calendar'), _(ui.cell.year))
        elif i==2:
            y0, m0 = self.ymBox0.get_value()
            y1, m1 = self.ymBox1.get_value()
            for ym in xrange(y0*12+m0-1, y1*12+m1):
                y, m = divmod(ym, 12)
                m += 1
                months.append(getMonthStatus(y, m))
            title = _('Calendar')
        exportToHtml(path, months, title)
        self.get_window().set_cursor(Gdk.Cursor.new(Gdk.CursorType.LEFT_PTR))
        self.hide()
    def showDialog(self, year, month):
        self.comboChanged(ym=(year, month))
        self.ymBox0.set_value((year, month))
        self.ymBox1.set_value((year, month))
        self.resize(1, 1)
        openWindow(self)
    '''
    def exportSvg(self, path, monthList):## FIXME
        ## monthList is a list of tuples (year, month)
        #import cairo
        hspace = 20
        mcal = ui.mainWin.mcal
        w = mcal.get_allocation().width
        h0 = mcal.get_allocation().height
        n = len(monthList)
        h = n*h0 + (n-1)*hspace
        fo = open(path+'.svg', 'w')
        surface = cairo.SVGSurface(fo, w, h)
        cr0 = cairo.Context(surface)
        cr = Gdk.CairoContext(cr0)
        year = ui.cell.year
        month = ui.cell.month
        day = self.mcal.day
        ui.mainWin.show() ## ??????????????
        for i in range(n):
            surface.set_device_offset(0, i*(h0+hspace))
            mcal.dateChange((monthList[i][0], monthList[i][1], 1))
            mcal.drawAll(cr=cr, cursor=False)
            mcal.queue_draw()
        ui.mainWin.dateChange((year, month, day))
        surface.finish()
    '''



class ExportToIcsDialog(Gtk.Dialog):
    def __init__(self, saveIcsFunc, defaultFileName):
        self.saveIcsFunc = saveIcsFunc
        Gtk.Dialog.__init__(self)
        self.set_title(_('Export to %s')%'iCalendar')
        ## parent=None FIXME
        #self.set_has_separator(False)
        ########
        hbox = Gtk.HBox(spacing=2)
        hbox.pack_start(Gtk.Label(_('From')+' '), 0, 0, 0)
        self.startDateInput = DateButton()
        hbox.pack_start(self.startDateInput, 0, 0, 0)
        hbox.pack_start(Gtk.Label(' '+_('To')+' '), 0, 0, 0)
        self.endDateInput = DateButton()
        hbox.pack_start(self.endDateInput, 0, 0, 0)
        self.vbox.pack_start(hbox, 0, 0, 0)
        ####
        year, month, day = ui.todayCell.dates[core.primaryMode]
        self.startDateInput.set_value((year, 1, 1, 0))
        self.endDateInput.set_value((year+1, 1, 1, 0))
        ########
        self.fcw = Gtk.FileChooserWidget(action=Gtk.FileChooserAction.SAVE)
        self.vbox.pack_start(self.fcw, 1, 1, 0)
        self.vbox.set_focus_child(self.fcw)## FIXME
        self.vbox.show_all()
        ##
        dialog_add_button(self, Gtk.STOCK_CANCEL, _('_Cancel'), 1, self.onDelete)
        dialog_add_button(self, Gtk.STOCK_SAVE, _('_Save'), 2, self.save)
        ##
        self.connect('delete-event', self.onDelete)
        self.fcw.connect('file-activated', self.save)## not working FIXME
        ##
        try:
            self.fcw.set_current_folder(core.deskDir)
        except AttributeError:## PyGTK < 2.4
            pass
        if not defaultFileName.endswith('.ics'):
            defaultFileName += '.ics'
        self.fcw.set_current_name(defaultFileName)
    def onDelete(self, widget=None, event=None):## hide(close) File Chooser Dialog
        self.destroy()
        return True
    def save(self, widget=None):
        self.get_window().set_cursor(Gdk.Cursor.new(Gdk.CursorType.WATCH))
        while Gtk.events_pending():
            Gtk.main_iteration_do(False)
        path = self.fcw.get_filename()
        if path in (None, ''):
            return
        print 'Exporting to ics file "%s"'%path
        self.saveIcsFunc(
            path,
            core.primary_to_jd(*self.startDateInput.get_value()),
            core.primary_to_jd(*self.endDateInput.get_value()),
        )
        self.get_window().set_cursor(Gdk.Cursor.new(Gdk.CursorType.LEFT_PTR))
        self.destroy()


