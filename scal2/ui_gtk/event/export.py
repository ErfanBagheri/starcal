from os.path import join, split, splitext

from scal2.path import deskDir
from scal2.json_utils import *
from scal2.locale_man import tr as _
from scal2 import core
from scal2.core import DATE_GREG
from scal2 import ui

from gi.repository import Gtk

from scal2.ui_gtk.utils import dialog_add_button
from scal2.ui_gtk.event.common import GroupsTreeCheckList


class SingleGroupExportDialog(Gtk.Dialog):
    def __init__(self, group):
        self._group = group
        Gtk.Dialog.__init__(self)
        self.set_title(_('Export Group'))
        ####
        dialog_add_button(self, Gtk.STOCK_CANCEL, _('_Cancel'), Gtk.ResponseType.CANCEL)
        dialog_add_button(self, Gtk.STOCK_OK, _('_OK'), Gtk.ResponseType.OK)
        self.connect('response', lambda w, e: self.hide())
        ####
        hbox = Gtk.HBox()
        frame = Gtk.Frame()
        frame.set_label(_('Format'))
        radioBox = Gtk.VBox()
        ##
        self.radioIcs = Gtk.RadioButton(label='iCalendar')
        self.radioJsonCompact = Gtk.RadioButton(label=_('Compact JSON (StarCalendar)'), group=self.radioIcs)
        self.radioJsonPretty = Gtk.RadioButton(label=_('Pretty JSON (StarCalendar)'), group=self.radioIcs)
        ##
        radioBox.pack_start(self.radioJsonCompact, 0, 0, 0)
        radioBox.pack_start(self.radioJsonPretty, 0, 0, 0)
        radioBox.pack_start(self.radioIcs, 0, 0, 0)
        ##
        self.radioJsonCompact.set_active(True)
        self.radioIcs.connect('clicked', self.formatRadioChanged)
        self.radioJsonCompact.connect('clicked', self.formatRadioChanged)
        self.radioJsonPretty.connect('clicked', self.formatRadioChanged)
        ##
        frame.add(radioBox)
        hbox.pack_start(frame, 0, 0, 0)
        hbox.pack_start(Gtk.Label(''), 1, 1, 0)
        self.vbox.pack_start(hbox, 0, 0, 0)
        ########
        self.fcw = Gtk.FileChooserWidget(action=Gtk.FileChooserAction.SAVE)
        try:
            self.fcw.set_current_folder(deskDir)
        except AttributeError:## PyGTK < 2.4
            pass
        self.vbox.pack_start(self.fcw, 1, 1, 0)
        ####
        self.vbox.show_all()
        self.formatRadioChanged()
    def formatRadioChanged(self, widget=None):
        fpath = self.fcw.get_filename()
        if fpath:
            fname_nox, ext = splitext(split(fpath)[1])
        else:
            fname_nox, ext = '', ''
        if not fname_nox:
            fname_nox = core.fixStrForFileName(self._group.title)
        if self.radioIcs.get_active():
            if ext != '.ics':
                ext = '.ics'
        else:
            if ext != '.json':
                ext = '.json'
        self.fcw.set_current_name(fname_nox + ext)
    def save(self):
        fpath = self.fcw.get_filename()
        if self.radioJsonCompact.get_active():
            text = dataToCompactJson(ui.eventGroups.exportData([self._group.id]))
            open(fpath, 'wb').write(text)
        elif self.radioJsonPretty.get_active():
            text =  dataToPrettyJson(ui.eventGroups.exportData([self._group.id]))
            open(fpath, 'wb').write(text)
        elif self.radioIcs.get_active():
            ui.eventGroups.exportToIcs(fpath, [self._group.id])
    def run(self):
        if Gtk.Dialog.run(self)==Gtk.ResponseType.OK:
            self.save()
        self.destroy()


class MultiGroupExportDialog(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_title(_('Export'))
        self.vbox.set_spacing(10)
        ####
        dialog_add_button(self, Gtk.STOCK_CANCEL, _('_Cancel'), Gtk.ResponseType.CANCEL)
        dialog_add_button(self, Gtk.STOCK_OK, _('_OK'), Gtk.ResponseType.OK)
        self.connect('response', lambda w, e: self.hide())
        ####
        hbox = Gtk.HBox()
        frame = Gtk.Frame()
        frame.set_label(_('Format'))
        radioBox = Gtk.VBox()
        ##
        self.radioIcs = Gtk.RadioButton(label='iCalendar')
        self.radioJsonCompact = Gtk.RadioButton(label=_('Compact JSON (StarCalendar)'), group=self.radioIcs)
        self.radioJsonPretty = Gtk.RadioButton(label=_('Pretty JSON (StarCalendar)'), group=self.radioIcs)
        ##
        radioBox.pack_start(self.radioJsonCompact, 0, 0, 0)
        radioBox.pack_start(self.radioJsonPretty, 0, 0, 0)
        radioBox.pack_start(self.radioIcs, 0, 0, 0)
        ##
        self.radioJsonCompact.set_active(True)
        self.radioIcs.connect('clicked', self.formatRadioChanged)
        self.radioJsonCompact.connect('clicked', self.formatRadioChanged)
        self.radioJsonPretty.connect('clicked', self.formatRadioChanged)
        ##
        frame.add(radioBox)
        hbox.pack_start(frame, 0, 0, 0)
        hbox.pack_start(Gtk.Label(''), 1, 1, 0)
        self.vbox.pack_start(hbox, 0, 0, 0)
        ########
        hbox = Gtk.HBox(spacing=2)
        hbox.pack_start(Gtk.Label(_('File')+':'), 0, 0, 0)
        self.fpathEntry = Gtk.Entry()
        self.fpathEntry.set_text(join(deskDir, 'events-%.4d-%.2d-%.2d'%core.getSysDate(DATE_GREG)))
        hbox.pack_start(self.fpathEntry, 1, 1, 0)
        self.vbox.pack_start(hbox, 0, 0, 0)
        ####
        self.groupSelect = GroupsTreeCheckList()
        swin = Gtk.ScrolledWindow()
        swin.add(self.groupSelect)
        swin.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.vbox.pack_start(swin, 1, 1, 0)
        ####
        self.vbox.show_all()
        self.formatRadioChanged()
        self.resize(600, 600)
    def formatRadioChanged(self, widget=None):
        #self.dateRangeBox.set_visible(self.radioIcs.get_active())
        ###
        fpath = self.fpathEntry.get_text()
        if fpath:
            fpath_nox, ext = splitext(fpath)
            if fpath_nox:
                if self.radioIcs.get_active():
                    if ext != '.ics':
                        ext = '.ics'
                else:
                    if ext != '.json':
                        ext = '.json'
                self.fpathEntry.set_text(fpath_nox + ext)
    def save(self):
        fpath = self.fpathEntry.get_text()
        activeGroupIds = self.groupSelect.getValue()
        if self.radioIcs.get_active():
            ui.eventGroups.exportToIcs(fpath, activeGroupIds)
        else:
            data = ui.eventGroups.exportData(activeGroupIds)
            ## what to do with all groupData['info'] s? FIXME
            if self.radioJsonCompact.get_active():
                text = dataToCompactJson(data)
            elif self.radioJsonPretty.get_active():
                text = dataToPrettyJson(data)
            else:
                raise RuntimeError
            open(fpath, 'w').write(text)
    def run(self):
        if Gtk.Dialog.run(self)==Gtk.ResponseType.OK:
            self.save()
        self.destroy()

