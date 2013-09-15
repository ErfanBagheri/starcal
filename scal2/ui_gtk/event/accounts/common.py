# -*- coding: utf-8 -*-

from scal2.locale_man import tr as _

from gi.repository import Gtk
from gi.repository import Gdk


class AccountWidget(Gtk.VBox):
    def __init__(self, account):
        Gtk.VBox.__init__(self)
        self.account = account
        ########
        self.sizeGroup = Gtk.SizeGroup(Gtk.SizeGroupMode.HORIZONTAL)
        #####
        hbox = Gtk.HBox()
        label = Gtk.Label(label=_('Title'))
        label.set_alignment(0, 0.5)
        hbox.pack_start(label, 0, 0, 0)
        self.sizeGroup.add_widget(label)
        self.titleEntry = Gtk.Entry()
        hbox.pack_start(self.titleEntry, 1, 1, 0)
        self.pack_start(hbox, 0, 0, 0)
    def updateWidget(self):
        self.titleEntry.set_text(self.account.title)
    def updateVars(self):
        self.account.title = self.titleEntry.get_text()







