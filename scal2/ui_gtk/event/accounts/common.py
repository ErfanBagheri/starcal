# -*- coding: utf-8 -*-

from scal2.locale_man import tr as _

from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk


class AccountWidget(gtk.VBox):
    def __init__(self, account):
        gtk.VBox.__init__(self)
        self.account = account
        ########
        self.sizeGroup = gtk.SizeGroup(gtk.SizeGroupMode.HORIZONTAL)
        #####
        hbox = gtk.HBox()
        label = gtk.Label(label=_('Title'))
        label.set_alignment(0, 0.5)
        hbox.pack_start(label, 0, 0, 0)
        self.sizeGroup.add_widget(label)
        self.titleEntry = gtk.Entry()
        hbox.pack_start(self.titleEntry, 1, 1, 0)
        self.pack_start(hbox, 0, 0, 0)
    def updateWidget(self):
        self.titleEntry.set_text(self.account.title)
    def updateVars(self):
        self.account.title = self.titleEntry.get_text()







