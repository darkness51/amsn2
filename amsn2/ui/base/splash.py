
class aMSNSplashScreen(object):
    """ This interface will represent the splashscreen of the UI"""
    def __init__(self, amsn_core, parent):
        """Initialize the interface. You should store the reference to the core in here
        as well as a reference to the window where you will show the splash screen
        @type amsn_core: L{amsn2.core.amsn.aMSNCore}
        @type parent: L{amsn2.ui.base.main.aMSNMainWindow}
        """
        raise NotImplementedError

    def show(self):
        """ Draw the splashscreen """
        raise NotImplementedError

    def hide(self):
        """ Hide the splashscreen """
        raise NotImplementedError

    def set_text(self, text):
        """ Shows a different text inside the splashscreen 
        @type text: str
        """
        raise NotImplementedError

    def set_image(self, image):
        """ Set the image to show in the splashscreen. This is an ImageView object 
        @type image: L{amsn2.views.imageview.ImageView}
        """

        raise NotImplementedError

