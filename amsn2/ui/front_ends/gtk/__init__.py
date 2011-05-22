from amsn2.core import aMSNUserInterfaceManager
import sys
import traceback

# Here we load the actual front end.
# We need to import the front end module and return it
# so the guimanager can access its classes
def load():
    try:
        import gtk_
    except ImportError, e:
        etype, value, tb = sys.exc_info()
        traceback.print_exception(etype, value, tb.tb_next)
        return None
    return gtk_

# Initialize the front end by checking for any
# dependency then register it to the guimanager
try:
    #import imp                  #Don't do that. imp.find_module() can't work with any packager (py2exe and family)
    #imp.find_module("gtk")      #so it will fail. Instead just try to import directy.
    import gtk
    aMSNUserInterfaceManager.register_frontend("gtk", sys.modules[__name__])

except ImportError:
    pass

