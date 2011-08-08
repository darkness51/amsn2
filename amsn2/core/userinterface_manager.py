# -*- coding: utf-8 -*-

from amsn2.views import ImageView, AccountView

import logging
logger = logging.getLogger('amsn2.ui_manager')

class aMSNUserInterfaceManager(object):
    front_ends = {}
    def __init__(self, core):
        """
        @type core: L{amsn2.core.amsn.aMSNCore}
        """
        self._core = core
        self._ui = None
        self._splash = None
        self._login = None
        self._contactlist = None

    @staticmethod
    def register_frontend(name, module):
        """
        @type name: str
        @type module: module
        """
        aMSNUserInterfaceManager.front_ends[name] = module

    @staticmethod
    def list_frontends():
        return aMSNUserInterfaceManager.front_ends.keys()

    @staticmethod
    def frontend_exists(front_end):
        """
        @type front_end: str
        """
        return front_end in aMSNUserInterfaceManager.list_frontends()

    def load_UI(self, ui_name):
        """
        @type ui_name: str
        """
        if self.frontend_exists(ui_name):
            self._ui = self.front_ends[ui_name].load()

            self._core._loop = self._ui.aMSNMainLoop(self._core)
            self._main = self._ui.aMSNMainWindow(self._core)
            self._core._main = self._main
            self._skin_manager = self._ui.SkinManager(self._core)
            self._core._skin_manager = self._skin_manager

        else:
            logger.error('Unable to load UI %s. Available front ends are: %s.'
                         % (ui_name, ", ".join(self.list_frontends())))
            self._core.quit()

    def load_splash(self):
        self._splash = self._ui.aMSNSplashScreen(self._core, self._main)
        image = ImageView()
        image.load("Filename","/path/to/image/here")

        self._splash.image = image
        self._splash.text = "Loading..."
        self._splash.show()
        self._main.set_title("aMSN 2 - Loading")
        return self._splash

    def load_login(self, accounts):
        """
        @type accounts: list
        """
        if self._splash:
            self._splash.hide()
            self._splash = None

        if self._contactlist:
            self.unload_contactlist()

        if not self._login:
            self._login = self._ui.aMSNLoginWindow(self._core, self._main)
            self._login.set_accounts(accounts)
            self._login.set_p2s(self._core.p2s)
            if accounts and accounts[0].autologin:
                self._core.signin_to_account(self._login, accounts[0])
        else:
            self._login.signout()
            self._login.set_accounts(accounts)
            self._login.set_p2s(self._core.p2s)

        self._main.set_title("aMSN 2 - Login")

        self._login.show()

    def unload_login(self):
        self._login.hide()
        self._login = None

    def load_contactlist(self):
        self._contactlist = self._ui.aMSNContactListWindow(self._core, self._main)

        em = self._core._event_manager
        em.register(em.events.PERSONALINFO_UPDATED, self._contactlist.my_info_updated)

        clwidget = self._contactlist.get_contactlist_widget()
        em.register(em.events.CLVIEW_UPDATED, clwidget.contactlist_updated)
        em.register(em.events.GROUPVIEW_UPDATED, clwidget.group_updated)
        em.register(em.events.CONTACTVIEW_UPDATED, clwidget.contact_updated)

        if self._login:
            self.unload_login()

        self._main.set_title("aMSN 2")
        self._contactlist.show()

    def unload_contactlist(self):
        self._contactlist.hide()

        em = self._core._event_manager
        em.unregister(em.events.PERSONALINFO_UPDATED, self._contactlist.my_info_updated)

        clwidget = self._contactlist.get_contactlist_widget()
        em.unregister(em.events.CLVIEW_UPDATED, clwidget.contactlist_updated)
        em.unregister(em.events.GROUPVIEW_UPDATED, clwidget.group_updated)
        em.unregister(em.events.CONTACTVIEW_UPDATED, clwidget.contact_updated)

        self._contactlist = None

    def show_dialog(self, message, buttons):
        """
        @type message: str
        @type buttons: tuple
        """
        win = self._ui.aMSNDialogWindow(message, buttons)
        win.set_title("aMSN 2 - Dialog")
        win.show()

    def show_notification(self, message):
        """
        @type message: str
        """
        win = self._ui.aMSNNotificationWindow(message)
        win.set_title("aMSN 2 - Notification")
        win.show()

    def show_error(self, message):
        """
        @type message: str
        """
        win = self._ui.aMSNErrorWindow(message)
        win.set_title("aMSN 2 - Error")
        win.show()

    def load_chat_window(self, conv_manager):
        """
        @type conv_manager: L{amsn2.core.conversation_manager.aMSNConversationManager}
        """
        return self._ui.aMSNChatWindow(conv_manager)

    def load_chat_widget(self, conversation, window, cuids):
        """
        @type conversation: L{amsn2.core.conversation.aMSNConversation}
        @type window: L{amsn2.ui.base.window.aMSNWindow}
        @type cuids: list of str
        """
        return self._ui.aMSNChatWidget(conversation, window, cuids)

    def load_contact_input_window(self, callback, groupviews):
        """
        @type callback: L{amsn2.core.event_manager.aMSNEventCallback}
        @type groupviews: list of L{amsn2.views.contactlistview.GroupView}
        """
        win = self._ui.aMSNContactInputWindow(('Contact to add: ', 'Invite message: '),
                                                 callback, groupviews, "aMSN 2 - Add a Contact")
        win.show()
        return win

    def load_contact_delete_window(self, callback, contactviews):
        """
        @type callback: L{amsn2.core.event_manager.aMSNEventCallback}
        @type contactviews: list of L{amsn2.views.contactlistview.ContactView}
        """
        win = self._ui.aMSNContactDeleteWindow(('Contact to remove: ',), callback, contactviews, "aMSN 2 - Delete a Contact")
        win.show()
        return win

    def load_group_input_window(self, callback, contactviews):
        """
        @type callback: L{amsn2.core.event_manager.aMSNEventCallback}
        @type contactviews: list of L{amsn2.views.contactlistview.ContactView}
        """
        win = self._ui.aMSNGroupInputWindow(('Group to add: ',), callback, contactviews, "aMSN 2 - Add a Group")
        win.show()
        return win

    def load_group_delete_window(self, callback, groupviews):
        """
        @type callback: L{amsn2.core.event_manager.aMSNEventCallback}
        @type groupviews: list of L{amsn2.views.contactlistview.GroupView}
        """
        win = self._ui.aMSNGroupDeleteWindow(('Group to remove: ',), callback, groupviews, "aMSN 2 - Delete a Group")
        win.show()
        return win

    def load_DP_chooser_window(self):
        win = self._ui.aMSNDPChooserWindow(self._core._account.set_dp ,self._core._backend_manager, "aMSN 2 - Choose a Display Picture")
        win.show()

    # Common methods for all UI

    def get_accountview_from_email(self, email):
        """
        Search in the list of accounts and return the view of the given email

        @type email: str
        @param email: email to find
        @rtype: AccountView
        @return: Returns AccountView if it was found, otherwise return None
        """

        accv = [accv for accv in self._login._account_views if accv.email == email]

        if len(accv) == 0:
            return AccountView(self._core, email)
        else:
            return accv[0]



