
class aMSNMainWindow(object):
    """ This Interface represents the main window of the application. Everything will be done from here
    When the window is shown, it should call: amsn_core.mainWindowShown()
    When the user wants to close that window, amsn_core.quit() should be called.
    """

    def __init__(self, amsn_core):
        """
        @type amsn_core: L{amsn2.core.amsn.aMSNCore}
        """

        pass

    def show(self):
        raise NotImplementedError

    def hide(self):
        raise NotImplementedError

    def set_title(self,title):
        """
        @type title: str
        """
        raise NotImplementedError

    def set_menu(self,menu):
        """
        @type menu: L{amsn2.views.menuview.MenuView}
        """
        raise NotImplementedError

