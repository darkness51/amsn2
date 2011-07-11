
import papyon
import papyon.event

class MailboxEvents(papyon.event.MailboxEventInterface):
    def __init__(self, client, amsn_core):
        """
        @type client: L{amsn2.protocol.client.Client}
        @type amsn_core: L{amsn2.core.amsn.aMSNCore}
        """
        self._amsn_core = amsn_core
        papyon.event.MailboxEventInterface.__init__(self, client)

    def on_mailbox_unread_mail_count_changed(self, unread_mail_count,
                                                   initial=False):
        """The number of unread mail messages
        @type unread_mail_count: int
        @type initial: bool
        """
        pass

    def on_mailbox_new_mail_received(self, mail_message):
        """New mail message notification
        @type mail_message: object
        """
        pass
