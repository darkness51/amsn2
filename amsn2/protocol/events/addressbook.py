# -*- coding: utf-8 -*-
#
# amsn - a python client for the WLM Network
#
# Copyright (C) 2008 Dario Freddi <drf54321@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import papyon
import papyon.event

class AddressBookEvents(papyon.event.AddressBookEventInterface):
    def __init__(self, client, amsn_core):
        """
        @type client: L{amsn2.protocol.client.Client}
        @type amsn_core: L{amsn2.core.amsn.aMSNCore}
        """
        self._amsn_core = amsn_core
        self._contactlist_manager = amsn_core._contactlist_manager
        papyon.event.AddressBookEventInterface.__init__(self, client)

    def on_addressbook_messenger_contact_added(self, contact):
        """
        @type contact: L{papyon.papyon.profile.Contact}
        """
        self._contactlist_manager.on_contact_added(contact)

    def on_addressbook_contact_deleted(self, contact):
        """
        @type contact: L{papyon.papyon.profile.Contact}
        """
        self._contactlist_manager.on_contact_removed(contact)

    def on_addressbook_contact_blocked(self, contact):
        """
        @type contact: L{papyon.papyon.profile.Contact}
        """
        self._contactlist_manager.on_contact_blocked(contact)

    def on_addressbook_contact_unblocked(self, contact):
        """
        @type contact: L{papyon.papyon.profile.Contact}
        """
        self._contactlist_manager.on_contact_unblocked(contact)

    def on_addressbook_group_added(self, group):
        """
        @type group: L{papyon.papyon.profile.Group}
        """
        self._contactlist_manager.on_group_added(group)

    def on_addressbook_group_deleted(self, group):
        """
        @type group: L{papyon.papyon.profile.Group}
        """
        self._contactlist_manager.on_group_deleted(group)

    def on_addressbook_group_renamed(self, group):
        """
        @type group: L{papyon.papyon.profile.Group}
        """
        self._contactlist_manager.on_group_renamed(group)

    def on_addressbook_group_contact_added(self, group, contact):
        """
        @type group: L{papyon.papyon.profile.Group}
        @type contact: L{papyon.papyon.profile.Contact}
        """
        self._contactlist_manager.on_group_contact_added(group, contact)

    def on_addressbook_group_contact_deleted(self, group, contact):
        """
        @type group: L{papyon.papyon.profile.Group}
        @type contact: L{papyon.papyon.profile.Contact}
        """
        self._contactlist_manager.on_group_contact_deleted(group, contact)

