# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Saeed Rasooli <saeed.gnu@gmail.com>
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

import pytz

from scal2.locale_man import tr as _

from scal2 import ui

import gtk
from gtk import gdk

from scal2.ui_gtk.utils import dialog_add_button, TimeZoneComboBoxEntry

class BulkSaveTimeZoneDialog(gtk.Dialog):
    def __init__(self):
        gtk.Dialog.__init__(self)
        self.set_title(_('Time Zone'))
        ####
        dialog_add_button(self, gtk.STOCK_CANCEL, _('_Cancel'), gtk.RESPONSE_CANCEL)
        dialog_add_button(self, gtk.STOCK_OK, _('_OK'), gtk.RESPONSE_OK)
        ###
        self.connect('response', self.onResponse)
        ####
        label = gtk.Label()
        label.set_markup(''.join([
            _('"Time Zone" property is newly added to events')+'\n',
            _('But this property needs to be saved for current events')+'\n',
            _('Select the time zone for your current location')+'\n\n',
            '<small>',
            _('If you have been in a different time zone while adding some of your event, you need to edit those events manually and change the time zone')+'\n',
            _('Time zone for All-Day events will be disabled by default'),
            '</small>',
        ]))
        label.set_line_wrap(True)
        self.vbox.pack_start(label, 1, 1)
        ####
        hbox = gtk.HBox()
        self.timeZoneInput = TimeZoneComboBoxEntry()
        hbox.pack_start(gtk.Label(''), 1, 1)
        hbox.pack_start(self.timeZoneInput, 0, 0)
        hbox.pack_start(gtk.Label(''), 1, 1)
        hbox.set_border_width(20)
        self.vbox.pack_start(hbox, 1, 1)
        ####
        self.errorLabel = gtk.Label()
        self.vbox.pack_start(self.errorLabel, 1, 1)
        ####
        self.vbox.pack_start(gtk.Label(''), 1, 1)
        ####
        self.vbox.show_all()
    def onResponse(self, dialog, responseId):
        if responseId == gtk.RESPONSE_OK:
            timeZone = self.timeZoneInput.get_text()
            try:
                pytz.timezone(timeZone)
            except Exception, e:
                self.errorLabel.set_text(
                    _('Time zone is invalid') + '\n' + str(e)
                )
            else:
                try:
                    for event in ui.iterAllEvents():
                        event.timeZone = timeZone
                        event.afterModify()
                        event.save()
                except Exception, e:
                    self.errorLabel.set_text(
                        str(e)
                    )
                else:
                    self.hide()
        else:
            self.hide()
        while gtk.events_pending():
            gtk.main_iteration_do(False)
            

if __name__=='__main__':
    BulkSaveTimeZoneDialog().run()

