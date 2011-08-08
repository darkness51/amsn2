
class basebackend():
    """
    Base backend, used as a model to implement others backends.
    It contains the functions that should be available for every backend.
    """

    def save_config(self, amsn_account, config):
        """
        @type amsn_account: L{amsn2.core.account_manager.aMSNAccount}
        @type config: L{amsn2.core.config.aMSNConfig}
        """
        raise NotImplementedError

    def load_config(self, amsn_account):
        """
        @type amsn_account: L{amsn2.core.account_manager.aMSNAccount}
        """
        raise NotImplementedError

    def load_account(self, email):
        """
        @type email: str
        """
        raise NotImplementedError

    def load_accounts(self):
        raise NotImplementedError

    def save_account(self, amsn_account):
        """
        @type amsn_account: L{amsn2.core.account_manager.aMSNAccount}
        """
        raise NotImplementedError

    def set_account(self, email):
        """
        @type email: str
        """
        raise NotImplementedError

    def clean(self):
        """
        Delete temporary things and prepare the backend to be detached
        or to begin another session with the same backend (e.g. with nullbackend)
        """
        raise NotImplementedError


    """ DPs """
    def get_file_location_DP(self, email, uid, shaci):
        """
        @type email: str
        @type uid: str
        @type shaci: str
        """
        raise NotImplementedError

    def get_DPs(self, email):
        """
        @type email: str
        """
        raise NotImplementedError
