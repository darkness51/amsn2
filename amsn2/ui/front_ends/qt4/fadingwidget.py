
from PyQt4 import Qt
from PyQt4 import QtCore
from PyQt4 import QtGui

class FadingWidget(QtGui.QWidget):
    def __init__(self, bgColor, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self._timeLine = QtCore.QTimeLine(640) # Not too fast, not too slow...
        self._opacity = 0.0
        self._bgColor = bgColor
        QtCore.QObject.connect(self._timeLine, QtCore.SIGNAL("valueChanged(qreal)"), self.__setOpacity)
        QtCore.QObject.connect(self._timeLine, QtCore.SIGNAL("finished()"), self.__animCompleted)

    def __animCompleted(self):
        if self._opacity == 0.0:
            self.emit(QtCore.SIGNAL("fadeInCompleted()"))
        elif self._opacity == 1.0:
            self.emit(QtCore.SIGNAL("fadeOutCompleted()"))

    def fadeIn(self):
        self._timeLine.setDirection(QtCore.QTimeLine.Backward)
        if self._timeLine.state() == QtCore.QTimeLine.NotRunning:
            self._timeLine.start()

    def fadeOut(self):
        self._timeLine.setDirection(QtCore.QTimeLine.Forward)
        if self._timeLine.state() == QtCore.QTimeLine.NotRunning:
            self._timeLine.start()

    def __setOpacity(self, newOpacity):
        self._opacity = newOpacity
        self.update()

    def paintEvent(self, event):
        if self._opacity > 0.0:
            p = QtGui.QPainter()
            p.begin(self)
            p.setBrush(self._bgColor)
            p.setOpacity(self._opacity)
            p.drawRect(self.rect())
            p.end()
