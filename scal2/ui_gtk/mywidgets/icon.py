from os.path import join

from scal2.path import *
from scal2.locale_man import tr as _
from scal2 import ui

from gi.repository import Gtk
from gi.repository import Gdk

from scal2.ui_gtk.decorators import *
from scal2.ui_gtk.utils import labelStockMenuItem


@registerSignals
class IconSelectButton(Gtk.Button):
    signals = [
        ('changed', [str]),
    ]
    def __init__(self, filename=''):
        Gtk.Button.__init__(self)
        self.image = Gtk.Image()
        self.add(self.image)
        self.dialog = Gtk.FileChooserDialog(
            title=_('Select Icon File'),
            action=Gtk.FileChooserAction.OPEN,
        )
        okB = self.dialog.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        cancelB = self.dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        clearB = self.dialog.add_button(Gtk.STOCK_CLEAR, Gtk.ResponseType.REJECT)
        if ui.autoLocale:
            cancelB.set_label(_('_Cancel'))
            cancelB.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_CANCEL,Gtk.IconSize.BUTTON))
            okB.set_label(_('_OK'))
            okB.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_OK,Gtk.IconSize.BUTTON))
            clearB.set_label(_('Clear'))
            clearB.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_CLEAR,Gtk.IconSize.BUTTON))
        ###
        menu = Gtk.Menu()
        self.menu = menu
        menu.add(labelStockMenuItem(_('None'), None, self.menuItemActivate, ''))
        for item in ui.eventTags:
            icon = item.icon
            if icon:
                menuItem = Gtk.ImageMenuItem(item.desc)
                menuItem.set_image(Gtk.Image.new_from_file(icon))
                menuItem.connect('activate', self.menuItemActivate, icon)
                menu.add(menuItem)
        menu.show_all()
        ###
        self.dialog.connect('file-activated', self.fileActivated)
        self.dialog.connect('response', self.dialogResponse)
        #self.connect('clicked', lambda button: button.dialog.run())
        self.connect('button-press-event', self.buttonPressEvent)
        ###
        self.set_filename(filename)
    def buttonPressEvent(self, widget, event):
        b = event.button
        if b==1:
            self.dialog.run()
        elif b==3:
            self.menu.popup(None, None, None, b, event.time)
    menuItemActivate = lambda self, widget, icon: self.set_filename(icon)
    def dialogResponse(self, dialog, response=0):
        dialog.hide()
        if response == Gtk.ResponseType.OK:
            fname = dialog.get_filename()
        elif response == Gtk.ResponseType.REJECT:
            fname = ''
        else:
            return
        self.set_filename(fname)
        self.emit('changed', fname)
    def fileActivated(self, dialog):
        fname = dialog.get_filename()
        self.filename = fname
        self.image.set_from_file(self.filename)
        self.emit('changed', fname)
        self.dialog.hide()
    get_filename = lambda self: self.filename
    def set_filename(self, filename):
        if filename is None:
            filename = ''
        self.dialog.set_filename(filename)
        self.filename = filename
        if not filename:
            self.image.set_from_file(join(pixDir, 'empty.png'))
        else:
            self.image.set_from_file(filename)

