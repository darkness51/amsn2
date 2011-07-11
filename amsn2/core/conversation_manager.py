from contactlist_manager import *
from conversation import aMSNConversation

class aMSNConversationManager:
    def __init__(self, core):
        """
        @type core: L{amsn2.core.amsn.aMSNCore}
        """

        self._core = core
        self._convs = []
        self._wins = []

    def on_invite_conversation(self, conversation):
        """
        @type conversation: L{amsn2.core.conversation.aMSNConversation}
        """
        print "new conv"
        contacts_uid = [c.id for c in conversation.participants]
        #TODO: What if the contact_manager has not build a view for that contact?
        c = aMSNConversation(self._core, self, conversation, contacts_uid)
        self._convs.append(c)

    def new_conversation(self, contacts_uid):
        """
        @type contacts_uid: list
        """
        #TODO: check if no conversation like this one already exists
        c = aMSNConversation(self._core, self, None, contacts_uid)
        self._convs.append(c)



    def get_conversation_window(self, amsn_conversation):
        """
        @type amsn_conversation: L{amsn2.core.conversation.aMSNConversation}
        """
        #TODO:
        #contacts should be a list of contact view
        # for the moment, always create a new win
        win = self._core._ui_manager.load_chat_window(self)
        self._wins.append(win)
        return win


