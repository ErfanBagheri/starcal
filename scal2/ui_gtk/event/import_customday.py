from os.path import isfile

from scal2.import_customday import customFile, importAndDeleteCustomDB
from scal2.locale_man import tr as _
from scal2 import core
from scal2 import ui

from gi.repository import Gtk
from gi.repository import Gdk

from scal2.ui_gtk.utils import dialog_add_button, DateTypeCombo

class CustomDayImporterDialog(Gtk.Dialog):
    def onResponse(self, dialog, response_id):
        if response_id==Gtk.ResponseType.OK:
            importAndDeleteCustomDB(
                self.modeCombo.get_active(),
                self.groupTitleEntry.get_text(),
            )
        self.destroy()
    def __init__(self):
        Gtk.Dialog.__init__(self)
        ####
        dialog_add_button(self, Gtk.STOCK_OK, _('_OK'), Gtk.ResponseType.OK)
        self.connect('response', self.onResponse)
        ####
        sizeGroup = Gtk.SizeGroup(Gtk.SizeGroupMode.HORIZONTAL)
        ####
        hbox = Gtk.HBox()
        label = Gtk.Label(label=_('Calendar Type'))
        label.set_alignment(0, 0.5)
        sizeGroup.add_widget(label)
        hbox.pack_start(label, 0, 0, 0)
        combo = DateTypeCombo()
        combo.set_active(core.primaryMode)
        hbox.pack_start(combo, 0, 0, 0)
        hbox.pack_start(Gtk.Label(''), 1, 1, 0)
        self.vbox.pack_start(hbox, 0, 0, 0)
        self.modeCombo = combo
        ####
        hbox = Gtk.HBox()
        hbox = Gtk.HBox()
        label = Gtk.Label(label=_('Group Title'))
        label.set_alignment(0, 0.5)
        sizeGroup.add_widget(label)
        hbox.pack_start(label, 0, 0, 0)
        self.groupTitleEntry = Gtk.Entry()
        self.groupTitleEntry.set_text(_('Imported Events'))
        hbox.pack_start(self.groupTitleEntry, 0, 0, 0)
        self.vbox.pack_start(hbox, 0, 0, 0)
        ####
        self.vbox.show_all()

if isfile(customFile):
    CustomDayImporterDialog().run()

