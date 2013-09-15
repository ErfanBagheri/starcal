from scal2.ui_gtk.event.groups.group import GroupWidget as NormalGroupWidget

from scal2.locale_man import tr as _
from gi.repository import Gtk

class GroupWidget(NormalGroupWidget):
    def __init__(self, group):
        NormalGroupWidget.__init__(self, group)
        ####
        hbox = Gtk.HBox()
        self.showSeperatedYmdInputsCheck = Gtk.CheckButton(_('Show Seperated Inputs for Year, Month and Day'))
        hbox.pack_start(self.showSeperatedYmdInputsCheck, 0, 0, 0)
        hbox.pack_start(Gtk.Label(''), 1, 1, 0)
        self.pack_start(hbox, 0, 0, 0)
    def updateWidget(self):
        NormalGroupWidget.updateWidget(self)
        self.showSeperatedYmdInputsCheck.set_active(self.group.showSeperatedYmdInputs)
    def updateVars(self):
        NormalGroupWidget.updateVars(self)
        self.group.showSeperatedYmdInputs = self.showSeperatedYmdInputsCheck.get_active()



