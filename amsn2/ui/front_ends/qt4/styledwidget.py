
from PyQt4 import Qt
from PyQt4 import QtCore
from PyQt4 import QtGui

from fadingwidget import FadingWidget

# Styled Widget: QWidget subclass that directly supports Qt StyleSheets
class StyledWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

    # Needed to support StyleSheets on pure subclassed QWidgets
    # See: http://doc.trolltech.com/4.4/stylesheet-reference.html
    def paintEvent(self, event):
        opt = QtGui.QStyleOption()
        opt.init(self)
        p = QtGui.QPainter(self)
        self.style().drawPrimitive(QtGui.QStyle.PE_Widget, opt, p, self)
