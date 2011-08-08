from amsn2.views import PersonalInfoView

class aMSNPersonalInfoManager:
    def __init__(self, core):
        """
        @type core: L{amsn2.core.amsn.aMSNCore}
        """

        self._core = core
        self._backend_manager = core._backend_manager
        self._em = core._event_manager
        self._personalinfoview = PersonalInfoView(self)
        self._papyon_profile = None

    def set_account(self, amsn_account):
        """
        @type amsn_account: L{amsn2.core.account_manager.aMSNAccount}
        """
        self._papyon_profile = amsn_account.client.profile

        # set nickname at login
        # could be overriden by the one set in the saved account
        # TODO: add setting display picture
        nick = unicode(amsn_account.view.nick)
        if not nick or nick == amsn_account.view.email:
            nick = self._papyon_profile.display_name
        self._personalinfoview.nick = nick

        # TODO: The psm doesn't seem to get fetched from server. Papyon issue?
        psm = unicode(amsn_account.view.psm)
        self._personalinfoview.psm = psm

        # set login presence, from this moment the client appears to the others
        self._personalinfoview.presence = self._core.p2s[amsn_account.view.presence]

    """ Actions from ourselves """
    def _on_nick_changed(self, new_nick):
        """
        @type new_nick: str
        """
        # TODO: parsing
        self._papyon_profile.display_name = new_nick.encode("utf-8")

    def _on_PSM_changed(self, new_psm):
        """
        @type new_psm: str
        """
        # TODO: parsing
        self._papyon_profile.personal_message = new_psm.encode("utf-8")

    def _on_presence_changed(self, new_presence):
        """
        @type new_presence: string defined in L{papyon.papyon.profile.Presence}
        """
        # TODO: manage custom presence
        for key in self._core.p2s:
            if self._core.p2s[key] == new_presence:
                self._papyon_profile.presence = key
                return

    def _on_DP_change_request(self):
        self._core._ui_manager.load_DP_chooser_window()

    def _on_DP_changed(self, dp_msnobj):
        """
        @type dp_msnobj: L{papyon.papyon.p2p.MSNObject}
        """
        self._papyon_profile.msn_object = dp_msnobj

    """ Actions from the core """
    def _on_CM_changed(self, new_media):
        """
        @type new_media: Tuple
        @param new_media: (artist, song)
        """
        self._papyon_profile.current_media = new_media

    """ Notifications from the server """
    def on_nick_updated(self, nick):
        """
        @type nick: str
        """
        # TODO: parse fields for smileys, format, etc
        self._personalinfoview._nickname.reset()
        self._personalinfoview._nickname.append_text(nick.decode('utf-8'))
        self._em.emit(self._em.events.PERSONALINFO_UPDATED, self._personalinfoview)

    def on_PSM_updated(self, psm):
        """
        @type psm: str
        """
        # TODO: parse fields for smileys, format, etc
        self._personalinfoview._psm.reset()
        self._personalinfoview._psm.append_text(psm.decode('utf-8'))
        self._em.emit(self._em.events.PERSONALINFO_UPDATED, self._personalinfoview)

    def on_DP_updated(self, dp_msnobj):
        """
        @type dp_msnobj: L{papyon.papyon.p2p.MSNObject}
        """        
        self._personalinfoview._image.reset()
        path = self._backend_manager.get_file_location_DP(self._papyon_profile.account,
                                                       self._papyon_profile.id,
                                                       dp_msnobj._data_sha)
        self._personalinfoview._image.load('Filename', path)
        self._em.emit(self._em.events.PERSONALINFO_UPDATED, self._personalinfoview)

    def on_presence_updated(self, presence):
        """
        @type presence: string defined in L{papyon.papyon.profile.Presence}
        """
        self._personalinfoview._presence = self._core.p2s[presence]
        self._em.emit(self._em.events.PERSONALINFO_UPDATED, self._personalinfoview)

    def on_CM_updated(self, cm):
        """
        @type cm: Tuple
        @param cm: (artist, song)
        """
        self._personalinfoview._current_media.reset()
        #TODO: insert separators
        self._personalinfoview._current_media.append_text(cm[0])
        self._personalinfoview._current_media.append_text(cm[1])
        self._em.emit(self._em.events.PERSONALINFO_UPDATED, self._personalinfoview)

    # TODO: connect to papyon event, maybe build a mailbox_manager
    """ Actions from outside """
    def _on_new_mail(self, info):
        """
        @type info: object
        @param info: currently unused
        """
        self._em.emit(self._em.events.PERSONALINFO_UPDATED, self._personalinfoview)


