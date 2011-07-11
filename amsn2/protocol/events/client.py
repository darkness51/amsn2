
import papyon
import papyon.event


class ClientEvents(papyon.event.ClientEventInterface):
    def __init__(self, client, amsn_core):
        """
        @type client: L{amsn2.protocol.client.Client}
        @type amsn_core: L{amsn2.core.amsn.aMSNCore}
        """
        self._amsn_core = amsn_core
        papyon.event.ClientEventInterface.__init__(self, client)

    def on_client_state_changed(self, state):
        """
        @type state: L{papyon.papyon.event.client.ClientState}
        """
        self._amsn_core.connection_state_changed(self._client._amsn_account, state)

    def on_client_error(self, error_type, error):
        """
        @type error_type: L{papyon.papyon.errors.ClientErrorType}
        @type error: str
        """
        print "ERROR :", error_type, " ->", error


