
class aMSNLoginWindow(object):
    """ This interface will represent the login window of the UI"""
    def __init__(self, amsn_core, parent):
        """Initialize the interface. You should store the reference to the core in here 
        @type amsn_core: L{amsn2.core.amsn.aMSNCore}
        @type parent: L{amsn2.ui.base.main.aMSNMainWindow}
        """
        raise NotImplementedError

    def show(self):
        """ Draw the login window """
        raise NotImplementedError

    def hide(self):
        """ Hide the login window """
        raise NotImplementedError

    def set_accounts(self, accountviews):
        """ This method will be called when the core needs the login window to
        let the user select among some accounts.
        
        @type accountviews: list
        @param accountviews: list of accountviews describing accounts
        The first one in the list
        should be considered as default. """
        raise NotImplementedError

    def signing_in(self):
        """ This method will be called when the core needs the login window to start the signin process.
        This is intended only to change the look of the login window. """
        raise NotImplementedError

    def signout(self):
        """ This method will be called when the core needs the login window to stop the signin process.
        This is intended only to change the look of the login window. """
        raise NotImplementedError

    def on_connecting(self, progress, message):
        """ This method will be called to notify the UI that we are connecting.

        @type progress: float
        @param progress: the current progress of the connexion (to be
        exploited as a progress bar, for example)
        @type message: str
        @param message: the message to show while loging in """
        raise NotImplementedError

