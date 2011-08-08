# -*- coding: utf-8 -*-
#
# amsn - a python client for the WLM Network
#
# Copyright (C) 2008 Dario Freddi <drf54321@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import time, sys, os
reload(sys)

import papyon
from amsn2.ui import base
from amsn2.views import ContactView, StringView, ImageView

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import Qt
from PyQt4 import uic

ufp = os.path.join(os.path.split(__file__)[0], 'chatWindow.ui')

class aMSNChatWindow(QtGui.QTabWidget, base.aMSNChatWindow):
    def __init__(self, amsn_core, parent=None):
        QtGui.QTabWidget.__init__(self, parent)
        self.setDocumentMode(True)
        self.setTabsClosable(True)
        self.setMovable(True)
        self.resize(500, 400)
        self._core = amsn_core

    def add_chat_widget(self, chat_widget):
        self.addTab(chat_widget, "test")
        
    def set_title(self, text):
        self.setWindowTitle(text)


class aMSNChatWidget(QtGui.QWidget, base.aMSNChatWidget):
    def __init__(self, amsn_conversation, parent, contacts_uid):
        QtGui.QWidget.__init__(self, parent)
        self._amsn_conversation = amsn_conversation
        self.ui = uic.loadUi(ufp, self)
        self._statusBar = QtGui.QStatusBar(self)
        self._statusBar.setFixedHeight(14)
        self._statusBar.setSizeGripEnabled(False)
        self.layout().addWidget(self._statusBar)
        self.ui.inputWidget.installEventFilter(self)
        self.cursor = QtGui.QTextCursor(self.ui.inputWidget.document())
        self.ui.splitter.setStretchFactor(0, 95)
        self.ui.splitter_2.setStretchFactor(0, 95)
        self.ui.splitter_3.setStretchFactor(0, 95)
        self.ui.splitter_3.setStretchFactor(1, 1)
        self.last_sender = ''
        self.nickstyle = "color:#555555; margin-left:2px"
        self.msgstyle = "margin-left:15px"
        self.infostyle = "margin-left:2px; font-style:italic; color:#6d6d6d"
        self.loadEmoticonList()
        self.font = QtGui.QFont() #TODO : load the default font
        self.ui.inputWidget.setCurrentFont(self.font)
        self.color = QtGui.QColor(QtCore.Qt.black) #TODO : load the default color
        self.ui.inputWidget.setTextColor(self.color)

        remoteContact = self._amsn_conversation._core._contactlist_manager.get_contact(contacts_uid[0])
        remoteDPImgs = remoteContact.dp.imgs
        foundDP = False
        for (type, data) in remoteDPImgs:
            if type == ImageView.FILENAME:
                self.ui.remoteDP.setPixmap(QtGui.QPixmap(data))
                foundDP = True
                break
            
        if not foundDP:
            remoteDP = QtGui.QPixmap.fromImage(QtGui.QImage("amsn2/themes/displaypic/default/nopic.png"))
            self.ui.remoteDP.setPixmap(remoteDP.scaled(96, 96, 0, 1))
            
        localDPImgs = self._amsn_conversation._core._personalinfo_manager._personalinfoview.dp.imgs
        foundDP = False
        for (type, data) in localDPImgs:
            if type == ImageView.FILENAME:
                localDP = QtGui.QPixmap(data)
                self.ui.localDP.setPixmap(localDP.scaled(96, 96, 0, 1))
                foundDP = True
                break

        if not foundDP:
            localDP = QtGui.QPixmap.fromImage(QtGui.QImage("amsn2/themes/displaypic/default/nopic.png"))
            self.ui.localDP.setPixmap(localDP.scaled(96, 96, 0, 1))
            
        remoteContactNick = remoteContact.nickname.parse_default_smileys().to_HTML_string()
        remoteContactStatus = remoteContact.status.to_HTML_string()
        if len(str(remoteContact.current_media.to_HTML_string())) == 0:
            remoteContactMessage = remoteContact.personal_message.parse_default_smileys().to_HTML_string()
        else:
            remoteContactMessage = remoteContact.current_media.to_HTML_string()

        
        self.ui.userinfo.setTextFormat(1) #rich text
        self.ui.userinfo.setText("To: {0} &lt;{1}&gt; {2} ({3})".format(
            remoteContactNick, remoteContact.account, remoteContactMessage, remoteContactStatus)
        )

        QtCore.QObject.connect(self.ui.actionInsert_Emoticon, QtCore.SIGNAL("triggered()"), self.showEmoticonList)
        QtCore.QObject.connect(self.ui.actionFont, QtCore.SIGNAL("triggered()"), self.chooseFont)
        QtCore.QObject.connect(self.ui.actionColor, QtCore.SIGNAL("triggered()"), self.chooseColor)
        QtCore.QObject.connect(self.ui.actionNudge, QtCore.SIGNAL("triggered()"), self.__sendNudge)


        #TODO: remove this when papyon is "fixed"...
        sys.setdefaultencoding("utf8")

    def eventFilter(self, obj, ev):
        #We can filter event msgs by obj/type
        if obj.objectName() == "inputWidget":
            if ev.type() == QtCore.QEvent.KeyPress:
                if ev.key() == QtCore.Qt.Key_Return or ev.key() == QtCore.Qt.Key_Enter:
                    self.__sendMessage()
                    return True
                else:
                    self.processInput()
                    return False
            else:
                return False
    
        return False


    def chooseFont(self):
        txt = self.ui.inputWidget.toPlainText()
        position = self.ui.inputWidget.textCursor().position()
        ok = False
        (font, ok) = QtGui.QFontDialog.getFont(self.font, self)
        if ok:
            self.font = font
            self.ui.inputWidget.clear()
            self.ui.inputWidget.setCurrentFont(self.font)
            self.ui.inputWidget.setPlainText(txt)
            cursor = self.ui.inputWidget.textCursor()
            cursor.setPosition(position)
            self.ui.inputWidget.setTextCursor(cursor)


    def chooseColor(self):
        txt = self.ui.inputWidget.toPlainText()
        position = self.ui.inputWidget.textCursor().position()
        color = QtGui.QColorDialog.getColor(self.color, self)
        if color.isValid():
            self.color = color
            self.ui.inputWidget.clear()
            self.ui.inputWidget.setTextColor(self.color)
            self.ui.inputWidget.setPlainText(txt)
            cursor = self.ui.inputWidget.textCursor()
            cursor.setPosition(position)
            self.ui.inputWidget.setTextCursor(cursor)


    def processInput(self):
        """ Here we process what is inside the widget... so showing emoticon
        and similar stuff"""
        position = self.cursor.position()
        #We don't want the entire text but only current word
        self.cursor.select(QtGui.QTextCursor.WordUnderCursor)
        text = self.cursor.selectedText()
        self.cursor.clearSelection()
        for emoticon in self.emoticonList:
            if text.contains(emoticon) == True:
                text.replace(emoticon, "<img src=\"throbber.gif\" />")
        self.cursor.setPosition(position)
        self.__typingNotification()

    def loadEmoticonList(self):
        self.emoticonList = QtCore.QStringList()

        """ TODO: Request emoticon list from amsn core, maybe use a QMap to get the image URL? """

        """ TODO: Discuss how to handle custom emoticons. We have to provide an option
        to change the default icon theme, this includes standard emoticons too.
        Maybe qrc? """

        #self.emoticonList << ";)" << ":)" << "EmOtIcOn"
        #We want :) and ;) to work for now :p
        self.emoticonList << "EmOtIcOn"

    def showEmoticonList(self):
        """ Let's popup emoticon selection here """
        print "Guess what? No emoticons. But I'll put in a random one for you"
        self.appendImageAtCursor("throbber.gif")

    def __sendMessage(self):
        # TODO: Switch to this when implemented
        """ msg = self.ui.inputWidget.toHtml()
        self.ui.inputWidget.clear()
        strv = StringView()
        strv.appendElementsFromHtml(msg) """

        msg = QtCore.QString.fromUtf8(self.ui.inputWidget.toPlainText())
        self.ui.inputWidget.clear()
        color = self.color
        hex8 = "%.2x%.2x%.2x" % ((color.red()), (color.green()), (color.blue()))
        style = papyon.TextFormat.NO_EFFECT
        info = QtGui.QFontInfo(self.font)
        if info.bold(): style |= papyon.TextFormat.BOLD
        if info.italic():  style |= papyon.TextFormat.ITALIC
        if self.font.underline(): style |= papyon.TextFormat.UNDERLINE
        if self.font.strikeOut(): style |= papyon.TextFormat.STRIKETHROUGH
        font_family = str(info.family())
        format = papyon.TextFormat(font=font_family, color=hex8, style=style)
        strv = StringView()
        strv.append_text(str(msg))
        ## as we send our msg to the conversation:
        self._amsn_conversation.send_message(strv, format)
        # this one will also notify us of our msg.
        # so no need to do:
        #self.ui.textEdit.append("<b>/me says:</b><br>"+unicode(msg)+"")

    def __sendNudge(self):
        self._amsn_conversation.send_nudge()
        
    def on_nudge_sent(self):
        self.ui.textEdit.append("<b>/me sent a nudge</b>")

    def __typingNotification(self):
        self._amsn_conversation.send_typing_notification()

    def appendTextAtCursor(self, text):
        self.ui.inputWidget.textCursor().insertHtml(unicode(text))

    def appendImageAtCursor(self, image):
        self.ui.inputWidget.textCursor().insertHtml(QtCore.QString("<img src=\"" + str(image) + "\" />"))

    def on_user_joined(self, contact):
        self.ui.textEdit.append(unicode("<b>"+QtCore.QString.fromUtf8(contact.to_HTML_string())+" "+self.tr("has joined the conversation")+("</b>")))
        pass

    def on_user_left(self, contact):
        self.ui.textEdit.append(unicode("<b>"+QtCore.QString.fromUtf8(contact.to_HTML_string())+" "+self.tr("has left the conversation")+("</b>")))
        pass

    def on_user_typing(self, contact):
        self._statusBar.showMessage(unicode(QtCore.QString.fromUtf8(contact.to_HTML_string()) + " is typing"), 7000)

    def on_message_received(self, messageview, formatting=None):
        print "Ding!"

        text = messageview.to_stringview().parse_default_smileys().to_HTML_string()
        nick, msg = text.split('\n', 1)
        nick = nick.replace('\n', '<br/>')
        msg = msg.replace('\n', '<br/>')
        sender = messageview.sender.to_HTML_string()

        # peacey: Check formatting of styles and perform the required changes
        if formatting:
            fmsg = '''<span style="'''
            if formatting.font:
                fmsg += "font-family: %s;" % formatting.font
            if formatting.color:
                fmsg += "color: %s;" % ("#"+formatting.color)
            if formatting.style & papyon.TextFormat.BOLD == papyon.TextFormat.BOLD:
                fmsg += "font-weight: bold;"
            if formatting.style & papyon.TextFormat.ITALIC == papyon.TextFormat.ITALIC:
                fmsg += "font-style: italic;"
            if formatting.style & papyon.TextFormat.UNDERLINE == papyon.TextFormat.UNDERLINE:
                fmsg += "text-decoration: underline;"
            if formatting.style & papyon.TextFormat.STRIKETHROUGH == papyon.TextFormat.STRIKETHROUGH:
                fmsg += "text-decoration: line-through;"
            if formatting.right_alignment:
                fmsg += "text-align: right;"
            fmsg = fmsg.rstrip(";")
            fmsg += '''">'''
            fmsg += msg
            fmsg += "</span>"
        else:
            fmsg = msg

        html = '<div>'
        if (self.last_sender != sender):
            html += '<span style="%s">%s</span><br/>' % (self.nickstyle, nick)
        html += '<span style="%s">[%s] %s</span></div>' % (self.msgstyle, time.strftime('%X'), fmsg)

        self.ui.textEdit.append(QtCore.QString.fromUtf8(html))
        self.last_sender = sender
        
        self._statusBar.clearMessage()

    def on_nudge_received(self, sender):
        self.ui.textEdit.append(unicode("<b>"+QtCore.QString.fromUtf8(sender.nickname.to_HTML_string())+" "+self.tr("sent you a nudge!")+("</b>")))
        pass
