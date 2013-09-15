from scal2.locale_man import tr as _
from scal2 import event_lib
from scal2 import ui

from gi.repository import Gtk

from scal2.ui_gtk.utils import dialog_add_button

class AccountEditorDialog(Gtk.Dialog):
    def __init__(self, account=None):
        Gtk.Dialog.__init__(self)
        self.set_title(_('Edit Account') if account else _('Add New Account'))
        ###
        dialog_add_button(self, Gtk.STOCK_CANCEL, _('_Cancel'), Gtk.ResponseType.CANCEL)
        dialog_add_button(self, Gtk.STOCK_OK, _('_OK'), Gtk.ResponseType.OK)
        ##
        self.connect('response', lambda w, e: self.hide())
        #######
        self.account = account
        self.activeWidget = None
        #######
        hbox = Gtk.HBox()
        combo = Gtk.ComboBoxText()
        for cls in event_lib.classes.account:
            combo.append_text(cls.desc)
        hbox.pack_start(Gtk.Label(_('Account Type')), 0, 0, 0)
        hbox.pack_start(combo, 0, 0, 0)
        hbox.pack_start(Gtk.Label(''), 1, 1, 0)
        self.vbox.pack_start(hbox, 0, 0, 0)
        ####
        if self.account:
            self.isNew = False
            combo.set_active(event_lib.classes.account.names.index(self.account.name))
        else:
            self.isNew = True
            defaultAccountTypeIndex = 0
            combo.set_active(defaultAccountTypeIndex)
            self.account = event_lib.classes.account[defaultAccountTypeIndex]()
        self.activeWidget = None
        combo.connect('changed', self.typeChanged)
        self.comboType = combo
        self.vbox.show_all()
        self.typeChanged()
    def dateModeChanged(self, combo):
        pass
    def typeChanged(self, combo=None):
        if self.activeWidget:
            self.activeWidget.updateVars()
            self.activeWidget.destroy()
        cls = event_lib.classes.account[self.comboType.get_active()]
        account = cls()
        if self.account:
            account.copyFrom(self.account)
            account.setId(self.account.id)
            del self.account
        if self.isNew:
            account.title = cls.desc ## FIXME
        self.account = account
        self.activeWidget = account.makeWidget()
        self.vbox.pack_start(self.activeWidget, 0, 0, 0)
    def run(self):
        if self.activeWidget is None or self.account is None:
            return None
        if Gtk.Dialog.run(self) != Gtk.ResponseType.OK:
            return None
        self.activeWidget.updateVars()
        self.account.save()
        if self.isNew:
            event_lib.lastIds.save()
        else:
            ui.eventAccounts[self.account.id] = self.account
        self.destroy()
        return self.account


class FetchRemoteGroupsDialog(Gtk.Dialog):
    def __init__(self, account):
        Gtk.Dialog.__init__(self)
        self.account = account


