from scal2.locale_man import tr as _
from scal2 import ui

from gi.repository import Gtk

from scal2.ui_gtk.utils import dialog_add_button
from scal2.ui_gtk.mywidgets.icon import IconSelectButton


class TrashEditorDialog(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_title(_('Edit Trash'))
        #self.connect('delete-event', lambda obj, e: self.destroy())
        #self.resize(800, 600)
        ###
        dialog_add_button(self, Gtk.STOCK_CANCEL, _('_Cancel'), Gtk.ResponseType.CANCEL)
        dialog_add_button(self, Gtk.STOCK_OK, _('_OK'), Gtk.ResponseType.OK)
        ##
        self.connect('response', lambda w, e: self.hide())
        #######
        self.trash = ui.eventTrash
        ##
        sizeGroup = Gtk.SizeGroup(Gtk.SizeGroupMode.HORIZONTAL)
        #######
        hbox = Gtk.HBox()
        label = Gtk.Label(label=_('Title'))
        label.set_alignment(0, 0.5)
        hbox.pack_start(label, 0, 0, 0)
        sizeGroup.add_widget(label)
        self.titleEntry = Gtk.Entry()
        hbox.pack_start(self.titleEntry, 1, 1, 0)
        self.vbox.pack_start(hbox, 0, 0, 0)
        ####
        hbox = Gtk.HBox()
        label = Gtk.Label(label=_('Icon'))
        label.set_alignment(0, 0.5)
        hbox.pack_start(label, 0, 0, 0)
        sizeGroup.add_widget(label)
        self.iconSelect = IconSelectButton()
        hbox.pack_start(self.iconSelect, 0, 0, 0)
        hbox.pack_start(Gtk.Label(''), 1, 1, 0)
        self.vbox.pack_start(hbox, 0, 0, 0)
        ####
        self.vbox.show_all()
        self.updateWidget()
    def run(self):
        if Gtk.Dialog.run(self)==Gtk.ResponseType.OK:
            self.updateVars()
        self.destroy()
    def updateWidget(self):
        self.titleEntry.set_text(self.trash.title)
        self.iconSelect.set_filename(self.trash.icon)
    def updateVars(self):
        self.trash.title = self.titleEntry.get_text()
        self.trash.icon = self.iconSelect.filename
        self.trash.save()

