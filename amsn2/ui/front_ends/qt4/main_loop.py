# -*- coding: utf-8 -*-
from amsn2.ui import base
import sys, os

from PyQt4 import QtCore
from PyQt4 import QtGui
import gobject
import signal
from amsn2.core import aMSNCore

class aMSNMainLoop(base.aMSNMainLoop):
    def __init__(self, amsn_core):
        self._amsn_core = amsn_core
        os.putenv("QT_NO_GLIB", "1") # FIXME: Temporary workaround for segfault
                                     #        caused by GLib Event Loop integration
        self.app = QtGui.QApplication(sys.argv)
        self.gmainloop = gobject.MainLoop()
        self.gcontext = self.gmainloop.get_context()

    def __del__(self):
        self.gmainloop.quit()

    def on_keyboard_interrupt(self, signal, stack):
        self._amsn_core.quit()

    def run(self):
        self.idletimer = QtCore.QTimer(QtGui.QApplication.instance())
        QtCore.QObject.connect(self.idletimer, QtCore.SIGNAL('timeout()'), self.on_timeout)
        self.idletimer.start(100)
        signal.signal(signal.SIGINT, self.on_keyboard_interrupt)
        self.app.exec_()

    def on_timeout(self):
        iter = 0
        while iter < 10 and self.gcontext.pending():
            self.gcontext.iteration()
            iter += 1

    def idler_add(self, func):
        gobject.idle_add(func)

    def timer_add(self, delay, func):
        gobject.timeout_add(delay, func)

    def quit(self):
        self.gmainloop.quit()
