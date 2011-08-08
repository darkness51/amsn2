from amsn2.ui import base

class aMSNWindow(base.aMSNWindow):
    """ This Interface represents a window of the application. Everything will be done from here """
    def __init__(self, amsn_core):
        pass

    def show(self):
        """ This launches the window, creates it, etc.."""
        print "aMSNWindow.show"
        pass

    def hide(self):
        """ This should hide the window"""
        print "aMSNWindow.hide"
        pass

    def set_title(self, text):
        """ This will allow the core to change the current window's title
        @type text: string
        """
        print "aMSNWindow.setTitle"
        pass

    def set_menu(self, menu):
        """ This will allow the core to change the current window's main menu
        @type menu: L{amsn2.views.menuview.MenuView}
        """
        print "aMSNWindow.setMenu"
        pass
