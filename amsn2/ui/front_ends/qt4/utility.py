
from amsn2.ui import base
from amsn2 import views

from PyQt4 import Qt
from PyQt4 import QtCore
from PyQt4 import QtGui

class aMSNErrorWindow(base.aMSNErrorWindow, QtGui.QMessageBox):
    def __init__(self, error_text, title = "aMSN Error", parent = None):
        QtGui.QMessageBox.__init__(self, QtGui.QMessageBox.Critical,
                                   "aMSN Error", error_text, QtGui.QMessageBox.Ok, parent)
        self.setModal(False)
        self.adress = self # Workaround to make the window not disapear as it is poped
        QtCore.QtCore.QObject.connect(self, QtCore.SIGNAL("finished(int)"), self.finish)
        self.show()

    def set_title(self, title):
        self.setWindowTitle(title)

    def show(self):
        QtGui.QDialog.show(self)

    def closeEvent(self, e):
        self.finish()
        e.accept()

    def finish(self, i = 0):
        self.close()
        self.deleteLater()


class aMSNNotificationWindow(base.aMSNNotificationWindow, QtGui.QMessageBox):
    def __init__(self, notification_text, title = "aMSN Notification", parent = None):
        QtGui.QMessageBox.__init__(self, QtGui.QMessageBox.Information,
                                   "aMSN Notification", notification_text, QtGui.QMessageBox.Ok, parent)
        self.setModal(False)
        self.adress = self # Workaround to make the window not disapear as it is poped
        QtCore.QObject.connect(self, QtCore.SIGNAL("finished(int)"), self.finish)
        self.show()

    def set_title(self, title):
        self.setWindowTitle(title)

    def show(self):
        QtGui.QDialog.show(self)

    def closeEvent(self, e):
        self.finish()
        e.accept()

    def finish(self, i = 0):
        self.close()
        self.deleteLater()


class aMSNDialogWindow(base.aMSNDialogWindow, QtGui.QMessageBox):
    def __init__(self, message, actions, title = "aMSN Dialog", parent = None):
        QtGui.QMessageBox.__init__(self, QtGui.QMessageBox.Information,
                                   "aMSN Dialog", message, QtGui.QMessageBox.NoButton, parent)

        for action in actions:
            name, callback = action
            button = QtGui.QPushButton(name)
            QtCore.QObject.connect(button, QtCore.SIGNAL("clicked()"), callback)
            self.addButton(button, QtGui.QMessageBox.AcceptRole)

        self.setModal(False)
        self.adress = self # Workaround to make the window not disapear as it is poped
        QtCore.QObject.connect(self, QtCore.SIGNAL("finished(int)"), self.finish)
        self.show()

    def set_title(self, title):
        self.setWindowTitle(title)

    def show(self):
        QtGui.QDialog.show(self)

    def closeEvent(self, e):
        self.finish()
        e.accept()

    def finish(self, i = 0):
        self.close()
        self.deleteLater()


class aMSNContactInputWindowSingleton(base.aMSNContactInputWindow, QtGui.QDialog):
    def __init__(self):
        self.firstTime = True

    def __call__(self, message, callback, groups, title = "aMSN Contact Input", parent = None):
        if self.firstTime :
            QtGui.QDialog.__init__(self, parent)

            self.vboxlayout = QtGui.QVBoxLayout()
            self.hboxlayout1 = QtGui.QHBoxLayout()
            self.label = QtGui.QLabel()
            self.hboxlayout1.addWidget(self.label)
            self._name = QtGui.QLineEdit()
            self.hboxlayout1.addWidget(self._name)
            self.vboxlayout.addLayout(self.hboxlayout1)

            self.hboxlayout2 = QtGui.QHBoxLayout()
            self.label2 = QtGui.QLabel()
            self.hboxlayout2.addWidget(self.label2)
            self._message = QtGui.QLineEdit()
            self.hboxlayout2.addWidget(self._message)
            self.vboxlayout.addLayout(self.hboxlayout2)

            self.scrollarea = QtGui.QScrollArea()
            self.scrollvbox = QtGui.QVBoxLayout()
            self.scrollarea.setLayout(self.scrollvbox)
            self.vboxlayout.addWidget(self.scrollarea)

            self.buttonbox = QtGui.QDialogButtonBox()

            self.buttonOk = QtGui.QPushButton("Ok", self)
            QtCore.QObject.connect(self.buttonOk, QtCore.SIGNAL("clicked()"), self.accept)
            QtCore.QObject.connect(self, QtCore.SIGNAL("accepted()"), self.onOk)
            self.buttonbox.addButton(self.buttonOk, QtGui.QDialogButtonBox.ActionRole)

            self.buttonCancel = QtGui.QPushButton("Cancel", self)
            QtCore.QObject.connect(self.buttonCancel, QtCore.SIGNAL("clicked()"), self.reject)
            QtCore.QObject.connect(self, QtCore.SIGNAL("rejected()"), self.onCancel)
            self.buttonbox.addButton(self.buttonCancel, QtGui.QDialogButtonBox.ActionRole)

            self.vboxlayout.addWidget(self.buttonbox)

            self.setLayout(self.vboxlayout)

        self.dicgroups = {}
        for group in groups:
            checkbox = QtGui.QCheckBox(group.name.to_HTML_string())
            self.scrollvbox.addWidget(checkbox)
            self.dicgroups[checkbox] = group
        self.spacer = QtGui.QWidget()
        self.scrollvbox.addWidget(self.spacer, 1)

        self.setWindowTitle(title)
        self.label.setText(message[0])
        self.label2.setText(message[1])
        self.firstTime = False
        self._callback = callback
        self.show()
        self.activateWindow()
        return self

    def set_title(self, title):
        self.setWindowTitle(title)

    def show(self):
        QtGui.QDialog.show(self)

    def empty(self):
        self._name.clear()
        self._message.clear()
        for checkbox in self.dicgroups:
            checkbox.setParent = None
            checkbox.deleteLater()
        self.spacer.setParent = None
        self.spacer.deleteLater()

    def onOk(self):
        name = str(self._name.text())
        msg = str(self._message.text())
        selectedgroups = []
        for checkbox in self.dicgroups:
            if checkbox.isChecked():
                selectedgroups.append(self.dicgroups[checkbox].uid)
        self._callback(name, msg, selectedgroups)
        self.empty()
        self.done(-1)

    def onCancel(self):
        self.empty()
        self.done(-1)

aMSNContactInputWindow = aMSNContactInputWindowSingleton()

class aMSNGroupInputWindowSingleton(base.aMSNGroupInputWindow, QtGui.QDialog):
    def __init__(self):
        self.firstTime = True

    def __call__(self, message, callback, contacts, title = "aMSN Group Input", parent = None):
        if self.firstTime :
            QtGui.QDialog.__init__(self, parent)

            self.vboxlayout = QtGui.QVBoxLayout()
            self.label = QtGui.QLabel()
            self.vboxlayout.addWidget(self.label)
            self._name = QtGui.QLineEdit()
            self.vboxlayout.addWidget(self._name)

            self.scrollarea = QtGui.QScrollArea()
            self.scrollvbox = QtGui.QVBoxLayout()
            self.scrollarea.setLayout(self.scrollvbox)
            self.vboxlayout.addWidget(self.scrollarea)

            self.buttonbox = QtGui.QDialogButtonBox()

            self.buttonOk = QtGui.QPushButton("Ok", self)
            QtCore.QObject.connect(self.buttonOk, QtCore.SIGNAL("clicked()"), self.accept)
            QtCore.QObject.connect(self, QtCore.SIGNAL("accepted()"), self.onOk)
            self.buttonbox.addButton(self.buttonOk, QtGui.QDialogButtonBox.ActionRole)

            self.buttonCancel = QtGui.QPushButton("Cancel", self)
            QtCore.QObject.connect(self.buttonCancel, QtCore.SIGNAL("clicked()"), self.reject)
            QtCore.QObject.connect(self, QtCore.SIGNAL("rejected()"), self.onCancel)
            self.buttonbox.addButton(self.buttonCancel, QtGui.QDialogButtonBox.ActionRole)

            self.vboxlayout.addWidget(self.buttonbox)

            self.setLayout(self.vboxlayout)

        self.diccontacts = {}
        for contact in contacts:
            checkbox = QtGui.QCheckBox(str(contact.name))
            self.scrollvbox.addWidget(checkbox)
            self.diccontacts[checkbox] = contact
        self.spacer = QtGui.QWidget()
        self.scrollvbox.addWidget(self.spacer, 1)

        self.setWindowTitle(title)
        self.label.setText(message[0])
        self.firstTime = False
        self._callback = callback
        self.show()
        self.activateWindow()
        return self

    def set_title(self, title):
        self.setWindowTitle(title)

    def show(self):
        QtGui.QDialog.show(self)

    def empty(self):
        self._name.clear()
        for checkbox in self.diccontacts:
            checkbox.setParent = None
            checkbox.deleteLater()
        self.spacer.setParent = None
        self.spacer.deleteLater()

    def onOk(self):
        name = str(self._name.text())
        selectedcontacts = []
        for checkbox in self.diccontacts:
            if checkbox.isChecked():
                selectedcontacts.append(self.diccontacts[checkbox].account)
        self._callback(name, selectedcontacts)
        self.empty()
        self.done(-1)
        self.deleteLater()

    def onCancel(self):
        self.empty()
        self.done(-1)

aMSNGroupInputWindow = aMSNGroupInputWindowSingleton()


class aMSNContactDeleteWindowSingleton(base.aMSNContactDeleteWindow, QtGui.QInputDialog):
    def __init__(self):
        self.firstTime = True

    def __call__(self, message, callback, contacts, title = "aMSN Delete Contact", parent = None):
        if self.firstTime :
            QtGui.QInputDialog.__init__(self, parent)
            self.setInputMode(QtGui.QInputDialog.TextInput)
            QtCore.QObject.connect(self, QtCore.SIGNAL("accepted()"), self.onOk)
            QtCore.QObject.connect(self, QtCore.SIGNAL("rejected()"), self.onCancel)

        self._callback = callback
        self.setWindowTitle(title)
        self.setLabelText(message[0])
        self.firstTime = False
        self.show()
        self.activateWindow()
        return self

    def set_title(self, title):
        self.setWindowTitle(title)

    def show(self):
        QtGui.QDialog.show(self)

    def empty(self):
        self.setTextValue("")

    def onOk(self):
        self._callback(str(self.textValue()))
        self.empty()
        self.done(-1)

    def onCancel(self):
        self.empty()
        self.done(-1)

aMSNContactDeleteWindow = aMSNContactDeleteWindowSingleton()


class aMSNGroupDeleteWindowSingleton(base.aMSNGroupDeleteWindow, QtGui.QInputDialog):
    def __init__(self):
        self.firstTime = True

    def __call__(self, message, callback, contacts, title = "aMSN Delete Group", parent = None):
        if self.firstTime :
            QtGui.QInputDialog.__init__(self, parent)
            self.setInputMode(QtGui.QInputDialog.TextInput)
            QtCore.QObject.connect(self, QtCore.SIGNAL("accepted()"), self.onOk)
            QtCore.QObject.connect(self, QtCore.SIGNAL("rejected()"), self.onCancel)

        self._callback = callback
        self.setWindowTitle(title)
        self.setLabelText(message[0])
        self.firstTime = False
        self.show()
        self.activateWindow()
        return self

    def set_title(self, title):
        self.setWindowTitle(title)

    def show(self):
        QtGui.QDialog.show(self)

    def empty(self):
        self.setTextValue("")

    def onOk(self):
        self._callback(str(self.textValue()))
        self.empty()
        self.done(-1)

    def onCancel(self):
        self.empty()
        self.done(-1)

aMSNGroupDeleteWindow = aMSNGroupDeleteWindowSingleton()
