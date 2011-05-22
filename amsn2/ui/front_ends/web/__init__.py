import traceback
import sys

from amsn2.core import aMSNUserInterfaceManager

# Here we load the actual front end.
# We need to import the front end module and return it
# so the guimanager can access its classes
def load():
    try:
        import amsn2.ui.front_ends.web._web
    except ImportError:
        etype, value, trace = sys.exc_info()
        traceback.print_exception(etype, value, trace.tb_next)
        return None
    return amsn2.ui.front_ends.web._web

# Initialize the front end by checking for any
# dependency then register it to the guimanager
try:
    #import imp                  #Don't do that. imp.find_module() can't work with any packager (py2exe and family)
    #imp.find_module("gobject")     #so it will fail. Instead just try to import directy.
    import gobject
    aMSNUserInterfaceManager.register_frontend("web", sys.modules[__name__])

except ImportError:
    pass

