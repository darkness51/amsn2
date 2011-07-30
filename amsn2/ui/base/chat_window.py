from window import aMSNWindow

class aMSNChatWindow(aMSNWindow):
    """ This interface will represent a chat window of the UI
        It can have many aMSNChatWidgets"""
    def __init__(self, amsn_core):
        """
        @type amsn_core: L{amsn2.core.amsn.aMSNCore}
        """
        raise NotImplementedError

    def add_chat_widget(self, chat_widget):
        """ add an aMSNChatWidget to the window 
        @type chat_widget: L{amsn2.ui.base.chat_window.aMSNChatWidget}
        """
        raise NotImplementedError

    """TODO: move, remove, detach, attach (shouldn't we use add ?), close,
        flash..."""


class aMSNChatWidget(object):
    """ This interface will present a chat widget of the UI """
    def __init__(self, amsn_conversation, parent, contacts_uid):
        """ create the chat widget for the 'parent' window, but don't attach to
        it.
        @type amsn_conversation: L{amsn2.core.conversation.aMSNConversation}
        @type parent: L{amsn2.ui.base.chat_window.aMSNChatWindow}
        @type contacts_uid: str
        """
        raise NotImplementedError

    def on_message_received(self, messageview):
        """ Called for incoming and outgoing messages
        message: a MessageView of the message
        @type messageview: L{amsn2.views.messageview.MessageView}
        """
        raise NotImplementedError

    def on_nudge_received(self, contact):
        """
        @type contact: L{amsn2.core.contactlist_manager.aMSNContact}
        """
        raise NotImplementedError

    def on_user_typing(self, contact):
        """
        @type contact: L{amsn2.core.contactlist_manager.aMSNContact}
        """
        raise NotImplementedError

    def on_nudge_sent(self):
        raise NotImplementedError