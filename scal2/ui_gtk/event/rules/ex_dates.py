# -*- coding: utf-8 -*-
#
# Copyright (C) 2011-2012 Saeed Rasooli <saeed.gnu@gmail.com>
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

from scal2 import core
from scal2.locale_man import tr as _
from scal2.locale_man import textNumEncode, textNumDecode
from scal2.date_utils import dateEncode, dateDecode

from scal2 import event_lib
from scal2 import ui

from gi.repository import Gtk
from gi.repository import Gdk

from scal2.ui_gtk.utils import toolButtonFromStock, set_tooltip

## FIXME
encode = lambda d: textNumEncode(dateEncode(d))
decode = lambda s: dateDecode(textNumDecode(s))
validate = lambda s: encode(decode(s))

class RuleWidget(Gtk.HBox):
    def __init__(self, rule):
        self.rule = rule
        Gtk.HBox.__init__(self)
        ###
        self.countLabel = Gtk.Label(label='')
        self.pack_start(self.countLabel, 0, 0, 0)
        ###
        self.editButton = Gtk.Button(_('Edit'))
        self.editButton.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_EDIT, Gtk.IconSize.BUTTON))
        self.editButton.connect('clicked', self.showDialog)
        self.pack_start(self.editButton, 0, 0, 0)
        ###
        self.dialog = Gtk.Dialog(title=rule.desc)
        ##
        self.treev = Gtk.TreeView()
        self.treev.set_headers_visible(True)
        self.trees = Gtk.ListStore(str)
        self.treev.set_model(self.trees)
        ##
        cell = Gtk.CellRendererText()
        cell.set_property('editable', True)
        cell.connect('edited', self.dateCellEdited)
        col = Gtk.TreeViewColumn(_('Date'), cell, text=0)
        self.treev.append_column(col)
        ##
        toolbar = Gtk.Toolbar()
        toolbar.set_orientation(Gtk.Orientation.VERTICAL)
        size = Gtk.IconSize.SMALL_TOOLBAR
        ##
        tb = toolButtonFromStock(Gtk.STOCK_ADD, size)
        set_tooltip(tb, _('Add'))
        tb.connect('clicked', self.addClicked)
        toolbar.insert(tb, -1)
        #self.buttonAdd = tb
        ##
        tb = toolButtonFromStock(Gtk.STOCK_DELETE, size)
        set_tooltip(tb, _('Delete'))
        tb.connect('clicked', self.deleteClicked)
        toolbar.insert(tb, -1)
        #self.buttonDel = tb
        ##
        tb = toolButtonFromStock(Gtk.STOCK_GO_UP, size)
        set_tooltip(tb, _('Move up'))
        tb.connect('clicked', self.moveUpClicked)
        toolbar.insert(tb, -1)
        ##
        tb = toolButtonFromStock(Gtk.STOCK_GO_DOWN, size)
        set_tooltip(tb, _('Move down'))
        tb.connect('clicked', self.moveDownClicked)
        toolbar.insert(tb, -1)
        ##
        dialogHbox = Gtk.HBox()
        dialogHbox.pack_start(self.treev, 1, 1, 0)
        dialogHbox.pack_start(toolbar, 0, 0, 0)
        self.dialog.vbox.pack_start(dialogHbox, 1, 1, 0)
        self.dialog.vbox.show_all()
        self.dialog.resize(200, 300)
        self.dialog.connect('response', lambda w, e: self.dialog.hide())
        ##
        okButton = self.dialog.add_button(Gtk.STOCK_OK, Gtk.ResponseType.CANCEL)
        if ui.autoLocale:
            okButton.set_label(_('_OK'))
            okButton.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_OK, Gtk.IconSize.BUTTON))
    def updateCountLabel(self):
        self.countLabel.set_label(' '*2 + _('%s items')%_(len(self.trees)) + ' '*2)
    def showDialog(self, w=None):
        self.dialog.run()
        self.updateCountLabel()
    def dateCellEdited(self, cell, path, newText):
        index = int(path)
        self.trees[index][0] = validate(newText)
    def getSelectedIndex(self):
        cur = self.treev.get_cursor()
        try:
            path, col = cur
            index = path[0]
            return index
        except:
            return None
    def addClicked(self, button):
        index = self.getSelectedIndex()
        mode = self.rule.getMode()## FIXME
        row = [encode(core.getSysDate(mode))]
        if index is None:
            newIter = self.trees.append(row)
        else:
            newIter = self.trees.insert(index+1, row)
        self.treev.set_cursor(self.trees.get_path(newIter))
        #col = self.treev.get_column(0)
        #cell = col.get_cell_renderers()[0]
        #cell.start_editing(...) ## FIXME
    def deleteClicked(self, button):
        index = self.getSelectedIndex()
        if index is None:
            return
        del self.trees[index]
    def moveUpClicked(self, button):
        index = self.getSelectedIndex()
        if index is None:
            return
        t = self.trees
        if index<=0 or index>=len(t):
            Gdk.beep()
            return
        t.swap(t.get_iter(index-1), t.get_iter(index))
        self.treev.set_cursor(index-1)
    def moveDownClicked(self, button):
        index = self.getSelectedIndex()
        if index is None:
            return
        t = self.trees
        if index<0 or index>=len(t)-1:
            Gdk.beep()
            return
        t.swap(t.get_iter(index), t.get_iter(index+1))
        self.treev.set_cursor(index+1)
    def updateWidget(self):
        for date in self.rule.dates:
            self.trees.append([encode(date)])
        self.updateCountLabel()
    def updateVars(self):
        dates = []
        for row in self.trees:
            dates.append(decode(row[0]))
        self.rule.setDates(dates)


