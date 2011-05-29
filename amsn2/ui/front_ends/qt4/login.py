# -*- coding: utf-8 -*-
import os
from amsn2.ui import base
from amsn2.views import AccountView, ImageView

from PyQt4 import Qt
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import uic
from styledwidget import StyledWidget

ufp = os.path.join(os.path.split(__file__)[0], 'login.ui')

class LoginThrobber(StyledWidget):
    def __init__(self, parent):
        StyledWidget.__init__(self, parent)
        # Throbber
        self.plsWait = QtGui.QLabel(self)
        self.plsWait.setText("<strong>Please wait...</strong>")
        self.plsWait.setAlignment(QtCore.Qt.AlignCenter)
        self.status = QtGui.QLabel(self)
        self.status.setText("")
        self.status.setAlignment(QtCore.Qt.AlignCenter)
        self.throbber = QtGui.QLabel(self)
        self.movie = QtGui.QMovie(self)
        self.movie.setFileName("amsn2/gui/front_ends/qt4/throbber.gif")
        self.movie.start()
        self.throbber.setMovie(self.movie)
        # Layout, for horizontal centering
        self.hLayout = QtGui.QHBoxLayout()
        self.hLayout.addStretch()
        self.hLayout.addWidget(self.throbber)
        self.hLayout.addStretch()
        # Layout, for vertical centering
        self.vLayout = QtGui.QVBoxLayout()
        self.vLayout.addStretch()
        self.vLayout.addLayout(self.hLayout)
        self.vLayout.addWidget(self.plsWait)
        self.vLayout.addWidget(self.status)
        self.vLayout.addStretch()
        # Top level layout
        self.setLayout(self.vLayout)
        # Apply StyleSheet
        self.setStyleSheet("background: white;")

class aMSNLoginWindow(StyledWidget, base.aMSNLoginWindow):
    def __init__(self, amsn_core, parent):
        StyledWidget.__init__(self, parent)
        self._amsn_core = amsn_core
        self._parent = parent
        self._skin = amsn_core._skin_manager.skin
        self._theme_manager = self._amsn_core._theme_manager
        self._ui_manager = self._amsn_core._ui_manager
        self.ui = uic.loadUi(ufp, self)
        self._parent = parent
        self.loginThrobber = None
        QtCore.QObject.connect(self.ui.pushSignIn, QtCore.SIGNAL("clicked()"), self.__login_clicked)
        QtCore.QObject.connect(self.ui.linePassword, QtCore.SIGNAL("returnPressed()"), self.__login_clicked)
        QtCore.QObject.connect(self.ui.checkRememberMe, QtCore.SIGNAL("toggled(bool)"), self.__on_toggled_cb)
        QtCore.QObject.connect(self.ui.checkRememberPass, QtCore.SIGNAL("toggled(bool)"), self.__on_toggled_cb)
        QtCore.QObject.connect(self.ui.checkSignInAuto, QtCore.SIGNAL("toggled(bool)"), self.__on_toggled_cb)
        QtCore.QObject.connect(self.ui.comboAccount, QtCore.SIGNAL("currentIndexChanged(QString)"), self.__on_user_comboxEntry_changed)
        styleData = QtCore.QFile()
        styleData.setFileName("amsn2/ui/front_ends/qt4/style1.qss")
        if styleData.open(QtCore.QIODevice.ReadOnly|QtCore.QIODevice.Text):
            styleReader = QtCore.QTextStream(styleData)
            self.setStyleSheet(styleReader.readAll())
            
    def __on_user_comboxEntry_changed(self, text):
        self.__switch_to_account(text)

    def show(self):
        if not self.loginThrobber:
            self._parent.fadeIn(self)

    def hide(self):
        pass

    def set_accounts(self, accountviews):
        self._account_views = accountviews

        for accv in self._account_views:
            self.ui.comboAccount.addItem(accv.email)

        if len(accountviews)>0 :
            # first in the list, default
            self.__switch_to_account(self._account_views[0].email)

            if self._account_views[0].autologin:
                self.signing_in()

    def set_p2s(self, p2s):
        # status list
        for key in p2s:
            name = p2s[key]
            _, path = self._theme_manager.get_statusicon("buddy_%s" % name)
            if (name == p2s['FLN']): continue
            self.ui.comboStatus.addItem(QtGui.QIcon(path), str.capitalize(name), key)

    def __switch_to_account(self, email):

        accv = self._ui_manager.get_accountview_from_email(email)

        if accv is None:
            accv = AccountView(self._amsn_core, email)

        self.ui.comboAccount.setEditText(accv.email)

        if accv.password:
            self.ui.linePassword.clear()
            self.ui.linePassword.insert(accv.password)

        self.ui.checkRememberMe.setChecked(accv.save)
        self.ui.checkRememberPass.setChecked(accv.save_password)
        self.ui.checkSignInAuto.setChecked(accv.autologin)

    def __login_clicked(self):
        email = str(self.ui.comboAccount.currentText())
        accv = self._ui_manager.get_accountview_from_email(email)

        if accv is None:
            accv = AccountView(self._amsn_core, str(email))

        accv.password = self.ui.linePassword.text().toLatin1().data()
        accv.presence = str(self.ui.comboStatus.itemData(self.ui.comboStatus.currentIndex()).toString())

        accv.save = self.ui.checkRememberMe.isChecked()
        accv.save_password = self.ui.checkRememberPass.isChecked()
        accv.autologin = self.ui.checkSignInAuto.isChecked()
        print accv
        self._amsn_core.signin_to_account(self, accv)

    def signout(self):
        pass

    def signing_in(self):
        self.loginThrobber = LoginThrobber(self)
        self._parent.fadeIn(self.loginThrobber)

    def on_connecting(self, progress, message):
        self.loginThrobber.status.setText(str(message))

    def __on_toggled_cb(self, bool):
        email = str(self.ui.comboAccount.currentText())
        accv = self._ui_manager.get_accountview_from_email(email)

        if accv is None:
            accv = AccountView(self._amsn_core, email)

        sender = self.sender()
        #just like wlm :)
        if sender == self.ui.checkRememberMe:
            accv.save = bool
            if not bool:
                self.ui.checkRememberPass.setChecked(False)
                self.ui.checkSignInAuto.setChecked(False)
        elif sender == self.ui.checkRememberPass:
            accv.save_password = bool
            if bool:
                self.ui.checkRememberMe.setChecked(True)
            else:
                self.ui.checkSignInAuto.setChecked(False)
        elif sender == self.ui.checkSignInAuto:
            accv.autologin = bool
            if bool:
                self.ui.checkRememberMe.setChecked(True)
                self.ui.checkRememberPass.setChecked(True)

