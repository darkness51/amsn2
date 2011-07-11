

import papyon
import papyon.event

class InviteEvents(papyon.event.InviteEventInterface):

    def __init__(self, client, amsn_core):
        """
        @type client: L{amsn2.protocol.client.Client}
        @type amsn_core: L{amsn2.core.amsn.aMSNCore}
        """
        self._amsn_core = amsn_core
        papyon.event.InviteEventInterface.__init__(self, client)

    def on_invite_conversation(self, conversation):
        """
        @type conversation: L{amsn2.core.conversation.aMSNConversation}
        """
        self._amsn_core._conversation_manager.on_invite_conversation(conversation)
