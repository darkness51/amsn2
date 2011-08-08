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

from amsn2.protocol.events import conversation
from amsn2.core.contactlist_manager import *
from amsn2.views import *
import papyon

class aMSNConversation:
    def __init__(self, core, conv_manager, conv = None, contacts_uid = None):
        """
        @type core: L{amsn2.core.amsn.aMSNCore}
        @type conv_manager: L{amsn2.core.conversation_manager.aMSNConversationManager}
        @type conv: L{papyon.papyon.conversation.SwitchboardConversation}
        @type contacts_uid: list of str
        """

        if (contacts_uid is None):
            raise ValueError("aMSNConversation: contacts_uid is None")

        self._core = core
        self._conversation_manager = conv_manager
        self._contacts_uid = contacts_uid
        if conv is None:
            #New conversation
            papyon_contacts = [core._contactlist_manager.get_contact(uid) for uid in contacts_uid]
            papyon_contacts = [c._papyon_contact for c in papyon_contacts if c is not None]
            #if c was None.... wtf?
            self._conv = papyon.Conversation(self._core._account.client, papyon_contacts)
        else:
            #From an existing conversation
            self._conv = conv

        self._win = self._conversation_manager.get_conversation_window(self)
        self._convo_events = conversation.ConversationEvents(self)
        self._conv_widget = core._ui_manager.load_chat_widget(self, self._win, contacts_uid)
        self._win.add_chat_widget(self._conv_widget)
        self._win.show()
        if contacts_uid:
            if len(contacts_uid) > 1:
                self._win.set_title("aMSN2 - Multi Chat")
            else:
                c = self._core._contactlist_manager.get_contact(contacts_uid[0])
                self._win.set_title("Chat with " + unicode(c.nickname))
        else:
            self._win.set_title("aMSN2 - Chat")


    """ events from outside """
    def on_state_changed(self, state):
        """
        @type state: object
        """
        print "state changed"

    def on_error(self, type, error):
        """
        @type type: object
        @type error: str
        """
        print error

    def on_user_joined(self, contact_uid):
        """
        @type contact_uid: str
        """
        c = self._core._contactlist_manager.get_contact(contact_uid)
        self._conv_widget.on_user_joined(c.nickname)

    def on_user_left(self, contact_uid):
        """
        @type contact_uid: str
        """
        c = self._core._contactlist_manager.get_contact(contact_uid)
        self._conv_widget.on_user_left(c.nickname)

    def on_user_typing(self, contact_uid):
        """
        @type contact_uid: str
        """
        c = self._core._contactlist_manager.get_contact(contact_uid)
        self._conv_widget.on_user_typing(c.nickname)

    def on_message_received(self, message, sender_uid=None, formatting=None):
        """
        @type message: str
        @type sender_uid: str
        @type formatting: L{papyon.papyon.conversation.TextFormat}
        """
        #TODO: messageView
        mv = MessageView()
        if sender_uid is None:
            mv.sender.append_stringview(self._core._personalinfo_manager._personalinfoview.nick)
        else:
            c = self._core._contactlist_manager.get_contact(sender_uid)
            mv.sender_icon = c.icon
            mv.message_type = MessageView.MESSAGE_OUTGOING
            mv.sender.append_stringview(c.nickname)
        mv.msg = message
        self._conv_widget.on_message_received(mv, formatting)

    def on_nudge_received(self, sender_uid):
        """
        @type sender_uid: str
        """
        contact = self._core._contactlist_manager.get_contact(sender_uid)
        self._conv_widget.on_nudge_received(contact)

    """ Actions from ourselves """
    def send_message(self, msg, formatting=None):
        """ 
        @type msg: L{amsn2.views.stringview.StringView}
        @type formatting: L{papyon.papyon.conversation.TextFormat}
        """
        # for the moment, no smiley substitution... (TODO)
        self.on_message_received(msg, formatting=formatting)
        message = papyon.ConversationMessage(unicode(msg), formatting)
        self._conv.send_text_message(message)

    def send_nudge(self):
        self._conv.send_nudge()
        
    def on_nudge_sent(self):
        self._conv_widget.on_nudge_sent()

    def send_typing_notification(self):
        self._conv.send_typing_notification()

    def leave(self):
        self._conv.leave()

    def invite_contact(self, contact_uid):
        """
        @type contact_uid: str
        @param contact_uid: the Id of the contact to invite 
        """
        c = self._core._contactlist_manager.get_contact(contact_uid)
        self._conv.invite_user(c.papyon_contact)

    #TODO: ...
