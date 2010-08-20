
from amsn2.ui import base
from amsn2.core import views
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class aMSNErrorWindow(base.aMSNErrorWindow, QMessageBox):
    def __init__(self, error_text, title = "aMSN Error", parent = None):
        QMessageBox.__init__(self, QMessageBox.Critical, "aMSN Error", error_text, QMessageBox.Ok, parent)
        self.setModal(False)
        self.adress = self # Workaround to make the window not disapear as it is poped
        QObject.connect(self, SIGNAL("finished(int)"), self.finish)
        self.show()

    def set_title(self, title):
        self.setWindowTitle(title)

    def show(self):
        QDialog.show(self)

    def closeEvent(self, e):
        self.finish()
        e.accept()

    def finish(self, i = 0):
        self.close()
        self.deleteLater()


class aMSNNotificationWindow(base.aMSNNotificationWindow, QMessageBox):
    def __init__(self, notification_text, title = "aMSN Notification", parent = None):
        QMessageBox.__init__(self, QMessageBox.Information, "aMSN Notification", notification_text, QMessageBox.Ok, parent)
        self.setModal(False)
        self.adress = self # Workaround to make the window not disapear as it is poped
        QObject.connect(self, SIGNAL("finished(int)"), self.finish)
        self.show()

    def set_title(self, title):
        self.setWindowTitle(title)

    def show(self):
        QDialog.show(self)

    def closeEvent(self, e):
        self.finish()
        e.accept()

    def finish(self, i = 0):
        self.close()
        self.deleteLater()


class aMSNDialogWindow(base.aMSNDialogWindow, QMessageBox):
    def __init__(self, message, actions, title = "aMSN Dialog", parent = None):
        QMessageBox.__init__(self, QMessageBox.Information, "aMSN Dialog", message, QMessageBox.NoButton, parent)

        for action in actions:
            name, callback = action
            button = QPushButton(name)
            QObject.connect(button, SIGNAL("clicked()"), callback)
            self.addButton(button, QMessageBox.AcceptRole)

        self.setModal(False)
        self.adress = self # Workaround to make the window not disapear as it is poped
        QObject.connect(self, SIGNAL("finished(int)"), self.finish)
        self.show()

    def set_title(self, title):
        self.setWindowTitle(title)

    def show(self):
        QDialog.show(self)

    def closeEvent(self, e):
        self.finish()
        e.accept()

    def finish(self, i = 0):
        self.close()
        self.deleteLater()


class aMSNContactInputWindowSingleton(base.aMSNContactInputWindow, QDialog):
    def __init__(self):
        self.firstTime = True

    def __call__(self, message, callback, groups, title = "aMSN Contact Input", parent = None):
        if self.firstTime :
            QDialog.__init__(self, parent)

            self.vboxlayout = QVBoxLayout()
            self.hboxlayout1 = QHBoxLayout()
            self.label = QLabel()
            self.hboxlayout1.addWidget(self.label)
            self._name = QLineEdit()
            self.hboxlayout1.addWidget(self._name)
            self.vboxlayout.addLayout(self.hboxlayout1)

            self.hboxlayout2 = QHBoxLayout()
            self.label2 = QLabel()
            self.hboxlayout2.addWidget(self.label2)
            self._message = QLineEdit()
            self.hboxlayout2.addWidget(self._message)
            self.vboxlayout.addLayout(self.hboxlayout2)

            self.scrollarea = QScrollArea()
            self.scrollvbox = QVBoxLayout()
            self.scrollarea.setLayout(self.scrollvbox)
            self.vboxlayout.addWidget(self.scrollarea)

            self.buttonbox = QDialogButtonBox()

            self.buttonOk = QPushButton("Ok", self)
            QObject.connect(self.buttonOk, SIGNAL("clicked()"), self.accept)
            QObject.connect(self, SIGNAL("accepted()"), self.onOk)
            self.buttonbox.addButton(self.buttonOk,QDialogButtonBox.ActionRole)

            self.buttonCancel = QPushButton("Cancel", self)
            QObject.connect(self.buttonCancel, SIGNAL("clicked()"), self.reject)
            QObject.connect(self, SIGNAL("rejected()"), self.onCancel)
            self.buttonbox.addButton(self.buttonCancel,QDialogButtonBox.ActionRole)

            self.vboxlayout.addWidget(self.buttonbox)

            self.setLayout(self.vboxlayout)

        self.dicgroups = {}
        for group in groups:
            checkbox = QCheckBox(group.name.to_HTML_string())
            self.scrollvbox.addWidget(checkbox)
            self.dicgroups[checkbox] = group
        self.spacer = QWidget()
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
        QDialog.show(self)

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
                selectedgroups.append(self.dicgroups[checkbox])
        print self.scrollarea.children()
        self._callback(name, msg, selectedgroups)
        self.empty()
        self.done(-1)

    def onCancel(self):
        self.empty()
        self.done(-1)

aMSNContactInputWindow = aMSNContactInputWindowSingleton()

class aMSNGroupInputWindowSingleton(base.aMSNGroupInputWindow, QDialog):
    def __init__(self):
        self.firstTime = True
 
    def __call__(self, message, callback, contacts, title = "aMSN Group Input", parent = None):
        if self.firstTime :
            QDialog.__init__(self, parent)

            self.vboxlayout = QVBoxLayout()
            self.label = QLabel()
            self.vboxlayout.addWidget(self.label)
            self._name = QLineEdit()
            self.vboxlayout.addWidget(self._name)

            self.scrollarea = QScrollArea()
            self.scrollvbox = QVBoxLayout()
            self.scrollarea.setLayout(self.scrollvbox)
            self.vboxlayout.addWidget(self.scrollarea)

            self.buttonbox = QDialogButtonBox()

            self.buttonOk = QPushButton("Ok", self)
            QObject.connect(self.buttonOk, SIGNAL("clicked()"), self.accept)
            QObject.connect(self, SIGNAL("accepted()"), self.onOk)
            self.buttonbox.addButton(self.buttonOk,QDialogButtonBox.ActionRole)

            self.buttonCancel = QPushButton("Cancel", self)
            QObject.connect(self.buttonCancel, SIGNAL("clicked()"), self.reject)
            QObject.connect(self, SIGNAL("rejected()"), self.onCancel)
            self.buttonbox.addButton(self.buttonCancel,QDialogButtonBox.ActionRole)

            self.vboxlayout.addWidget(self.buttonbox)

            self.setLayout(self.vboxlayout)

        self.diccontacts = {}
        for contact in contacts:
            checkbox = QCheckBox(str(contact.name))
            self.scrollvbox.addWidget(checkbox)
            self.diccontacts[checkbox] = contact
        self.spacer = QWidget()
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
        QDialog.show(self)

    def empty(self):
        self._name.clear()
        for checkbox in self.diccontacts:
            checkbox.setParent = None
            checkbox.deleteLater()
        self.spacer.setParent = None
        self.spacer.deleteLater()

    def onOk(self):
        name = str(self._name.text())
        self._callback(name)
        self.empty()
        self.done(-1)
        self.deleteLater()

    def onCancel(self):
        self.empty()
        self.done(-1)

aMSNGroupInputWindow = aMSNGroupInputWindowSingleton()


class aMSNContactDeleteWindowSingleton(base.aMSNContactDeleteWindow, QInputDialog): 
    def __init__(self):
        self.firstTime = True
 
    def __call__(self, message, callback, contacts, title = "aMSN Delete Contact", parent = None):
        if self.firstTime :
            QInputDialog.__init__(self, parent)
            self.setInputMode(QInputDialog.TextInput)
            QObject.connect(self, SIGNAL("accepted()"), self.onOk)
            QObject.connect(self, SIGNAL("rejected()"), self.onCancel)

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
        QDialog.show(self)

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


class aMSNGroupDeleteWindowSingleton(base.aMSNGroupDeleteWindow, QInputDialog): 
    def __init__(self):
        self.firstTime = True
 
    def __call__(self, message, callback, contacts, title = "aMSN Delete Group", parent = None):
        if self.firstTime :
            QInputDialog.__init__(self, parent)
            self.setInputMode(QInputDialog.TextInput)
            QObject.connect(self, SIGNAL("accepted()"), self.onOk)
            QObject.connect(self, SIGNAL("rejected()"), self.onCancel)

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
        QDialog.show(self)

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