
import papyon
import papyon.event

class ContactEvents(papyon.event.ContactEventInterface):

    def __init__(self, client, contact_manager):
        """
        @type client: L{amsn2.protocol.client.Client}
        @type contact_manager: L{amsn2.core.contact_manager.aMSNContactManager}
        """
        self._contact_manager = contact_manager
        papyon.event.ContactEventInterface.__init__(self, client)

    def on_contact_presence_changed(self, contact):
        """
        @type contact: L{papyon.papyon.profile.Contact}
        """
        self._contact_manager.on_contact_changed(contact)

    def on_contact_display_name_changed(self, contact):
        """
        @type contact: L{papyon.papyon.profile.Contact}
        """
        self._contact_manager.on_contact_changed(contact)

    def on_contact_personal_message_changed(self, contact):
        """
        @type contact: L{papyon.papyon.profile.Contact}
        """
        self._contact_manager.on_contact_changed(contact)

    def on_contact_current_media_changed(self, contact):
        """
        @type contact: L{papyon.papyon.profile.Contact}
        """
        self._contact_manager.on_contact_changed(contact)

    def on_contact_msn_object_changed(self, contact):
        """
        @type contact: L{papyon.papyon.profile.Contact}
        """
        # if the msnobject has been removed, just remove the buddy's DP
        if contact.msn_object is None:
            self._contact_manager.on_contact_DP_changed(contact)
            return

        # TODO: filter objects
        if contact.msn_object._type is papyon.p2p.MSNObjectType.DISPLAY_PICTURE:
            self._contact_manager.on_contact_DP_changed(contact)

    def on_contact_memberships_changed(self, contact):
        """
        @type contact: L{papyon.papyon.profile.Contact}
        """
        pass

    def on_contact_infos_changed(self, contact, infos):
        """
        @type contact: L{papyon.papyon.profile.Contact}
        @type infos: object
        """
        pass

    def on_contact_client_capabilities_changed(self, contact):
        """
        @type contact: L{papyon.papyon.profile.Contact}
        """
        pass

