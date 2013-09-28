from time import time as now

from scal2 import core
from scal2.locale_man import tr as _
from scal2 import ui

from gi.repository.GObject import timeout_add

from gi.repository import Gtk
from gi.repository import Gdk

from scal2.ui_gtk.decorators import *
from scal2.ui_gtk import gtk_ud as ud
from scal2.ui_gtk.utils import set_tooltip, myRaise
from scal2.ui_gtk.mywidgets.multi_spin_button import IntSpinButton
from scal2.ui_gtk import gtk_ud as ud
from scal2.ui_gtk.customize import CustomizableCalObj

iconSizeList = [
    ('Menu', Gtk.IconSize.MENU),
    ('Small Toolbar', Gtk.IconSize.SMALL_TOOLBAR),
    ('Button', Gtk.IconSize.BUTTON),
    ('Large Toolbar', Gtk.IconSize.LARGE_TOOLBAR),
    ('DND', Gtk.IconSize.DND),
    ('Dialog', Gtk.IconSize.DIALOG),
] ## in size order
iconSizeDict = dict(iconSizeList)


@registerSignals
class ToolbarItem(Gtk.ToolButton, CustomizableCalObj):
    def __init__(self, name, stockName, method, tooltip='', text='', desc=''):
        #print 'ToolbarItem', name, stockName, method, tooltip, text
        self.method = method
        ######
        if not desc and tooltip:
            desc = tooltip
        ###
        if tooltip is '':
            tooltip = name.capitalize()
        ###
        if not text:
            text = name.capitalize()
        text = _(text)
        ######
        Gtk.ToolButton.__init__(self)
        self.set_icon_widget(
            Gtk.Image.new_from_stock(
                getattr(Gtk, 'STOCK_%s'%(stockName.upper())),
                Gtk.IconSize.DIALOG,
            ) if stockName else None,
        )
        self.set_label(text)
        self._name = name
        self.desc = desc
        self.initVars()
        if tooltip is not None:
            set_tooltip(self, _(tooltip))
        self.set_is_important(True)## FIXME
    show = lambda self: self.show_all()


#@registerSignals
class CustomizableToolbar(Gtk.Toolbar, CustomizableCalObj):
    _name = 'toolbar'
    desc = _('Toolbar')
    styleList = ('Icon', 'Text', 'Text below Icon', 'Text beside Icon')
    defaultItems = []
    defaultItemsDict = {}
    def __init__(self, funcOwner, vertical=False, onPressContinue=False):
        Gtk.Toolbar.__init__(self)
        self.funcOwner = funcOwner
        self.set_orientation(Gtk.Orientation.VERTICAL if vertical else Gtk.Orientation.HORIZONTAL)
        self.add_events(Gdk.EventMask.POINTER_MOTION_MASK)
        self.onPressContinue = onPressContinue
        ###
        optionsWidget = Gtk.VBox()
        ##
        hbox = Gtk.HBox()
        hbox.pack_start(Gtk.Label(_('Style')), 0, 0, 0)
        self.styleCombo = Gtk.ComboBoxText()
        for item in self.styleList:
            self.styleCombo.append_text(_(item))
        hbox.pack_start(self.styleCombo, 0, 0, 0)
        optionsWidget.pack_start(hbox, 0, 0, 0)
        ##
        hbox = Gtk.HBox()
        hbox.pack_start(Gtk.Label(_('Icon Size')), 0, 0, 0)
        self.iconSizeCombo = Gtk.ComboBoxText()
        for (i, item) in enumerate(iconSizeList):
            self.iconSizeCombo.append_text(_(item[0]))
        hbox.pack_start(self.iconSizeCombo, 0, 0, 0)
        optionsWidget.pack_start(hbox, 0, 0, 0)
        self.iconSizeHbox = hbox
        ##
        hbox = Gtk.HBox()
        hbox.pack_start(Gtk.Label(_('Buttons Border')), 0, 0, 0)
        self.buttonsBorderSpin = IntSpinButton(0, 99)
        hbox.pack_start(self.buttonsBorderSpin, 0, 0, 0)
        optionsWidget.pack_start(hbox, 0, 0, 0)
        ##
        self.initVars(optionsWidget=optionsWidget)
        self.iconSizeCombo.connect('changed', self.iconSizeComboChanged)
        self.styleCombo.connect('changed', self.styleComboChanged)
        self.buttonsBorderSpin.connect('changed', self.buttonsBorderSpinChanged)
        #self.styleComboChanged()
        ##
        #print 'toolbar state', self.get_state()## STATE_NORMAL
        #self.set_state(Gtk.StateType.ACTIVE)## FIXME
        #self.set_property('border-width', 0)
        #style = self.get_style()
        #style.border_width = 10
        #self.set_style(style)
    getIconSizeName = lambda self: iconSizeList[self.iconSizeCombo.get_active()][0]
    setIconSizeName = lambda self, size_name: self.set_icon_size(iconSizeDict[size_name])
    ## Gtk.Toolbar.set_icon_size was previously Deprecated, but it's not Deprecated now!!
    def setButtonsBorder(self, bb):
        for item in self.items:
            item.set_border_width(bb)
    def iconSizeComboChanged(self, combo=None):
        self.setIconSizeName(self.getIconSizeName())
    def styleComboChanged(self, combo=None):
        style = self.styleCombo.get_active()
        self.set_style(style)
        #self.showHideWidgets()## FIXME
        self.iconSizeHbox.set_sensitive(style!=1)
    def buttonsBorderSpinChanged(self, spin=None):
        self.setButtonsBorder(self.buttonsBorderSpin.get_value())
    def moveItemUp(self, i):
        button = self.items[i]
        self.remove(button)
        self.insert(button, i-1)
        self.items.insert(i-1, self.items.pop(i))
    #def insertItem(self, item, pos):
    #    CustomizableCalObj.insertItem(self, pos, item)
    #    Gtk.Toolbar.insert(self, item, pos)
    #    item.show()
    def appendItem(self, item):
        CustomizableCalObj.appendItem(self, item)
        Gtk.Toolbar.insert(self, item, -1)
        if item.enable:
            item.show()
    def getData(self):
        return {
            'items': self.getItemsData(),
            'iconSize': self.getIconSizeName(),
            'style': self.styleList[self.styleCombo.get_active()],
            'buttonsBorder': self.buttonsBorderSpin.get_value(),
        }
    def setupItemSignals(self, item):
        if item.method:
            if isinstance(item.method, str):
                func = getattr(self.funcOwner, item.method)
            else:
                func = item.method
            if self.onPressContinue:
                item.get_child().connect('button-press-event', lambda obj, ev: self.itemPress(func))
                item.get_child().connect('button-release-event', self.itemRelease)
            else:
                item.connect('clicked', func)
    def setData(self, data):
        for (name, enable) in data['items']:
            try:
                item = self.defaultItemsDict[name]
            except KeyError:
                myRaise()
            else:
                item.enable = enable
                self.setupItemSignals(item)
                self.appendItem(item)
        ###
        iconSize = data['iconSize']
        for (i, item) in enumerate(iconSizeList):
            if item[0]==iconSize:
                self.iconSizeCombo.set_active(i)
        self.setIconSizeName(iconSize)
        ###
        styleNum = self.styleList.index(data['style'])
        self.styleCombo.set_active(styleNum)
        self.set_style(styleNum)
        ###
        bb = data.get('buttonsBorder', 0)
        self.buttonsBorderSpin.set_value(bb)
        self.setButtonsBorder(bb)
        ###
    def itemPress(self, func):
        self.lastPressTime = now()
        self.remain = True
        func()
        timeout_add(ui.timeout_initial, self.itemPressRemain, func)
    def itemPressRemain(self, func):
        if self.remain and now()-self.lastPressTime>=ui.timeout_repeat/1000.0:
            func()
            timeout_add(ui.timeout_repeat, self.itemPressRemain, func)
    def itemRelease(self, widget, event=None):
        self.remain = False


