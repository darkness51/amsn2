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

from amsn2.ui import base

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui_contactlist import Ui_ContactList
from styledwidget import StyledWidget

from image import *
from amsn2.views import StringView, ContactView, GroupView, ImageView, PersonalInfoView
import common

class aMSNContactListWindow(base.aMSNContactListWindow):
    def __init__(self, amsn_core, parent):
        self._amsn_core = amsn_core
        self._parent = parent
        self._skin = amsn_core._skin_manager.skin
        self._theme_manager = self._amsn_core._theme_manager
        self._myview = amsn_core._personalinfo_manager._personalinfoview
        self._clwidget = aMSNContactListWidget(amsn_core, self)
        self._clwidget.show()
        self.__create_controls()
        self._clwidget.ui.pixUser.setIconSize(QSize(96,96))
        self._clwidget.ui.pixUser.setIcon(QIcon("amsn2/ui/front_ends/qt4/msn-userimage2.png"))
        QObject.connect(self._clwidget.ui.pixUser, SIGNAL("clicked()"),self._myview.changeDP)

    def __create_controls(self):
        #status list
        for key in self._amsn_core.p2s:
            name = self._amsn_core.p2s[key]
            _, path = self._theme_manager.get_statusicon("buddy_%s" % name)
            if (name == self._amsn_core.p2s['FLN']): continue
            self._clwidget.ui.status.addItem(QIcon(path), str.capitalize(name), key)

    def show(self):
        self._clwidget.show()

    def hide(self):
        self._clwidget.hide()

    def set_title(self, text):
        self._parent.setTitle(text)

    def set_menu(self, menu):
        self._parent.setMenu(menu)

    def my_info_updated(self, view):
        # TODO image, ...
        imview = view.dp
        if len(imview.imgs) > 0:
            pixbuf = QPixmap(imview.imgs[0][1])
            pixbuf = pixbuf.scaled(96,96,0,1)
            self._clwidget.ui.pixUser.setIcon(QIcon(pixbuf))
        nk = view.nick
        self._clwidget.ui.nickName.setHtml(nk.to_HTML_string())
        message = view.psm.to_HTML_string()
        if len(view.current_media.to_HTML_string()) > 0:
            message += ' ' + view.current_media.to_HTML_string()
        self._clwidget.ui.statusMessage.setHtml('<i>'+message+'</i>')
        for key in self._amsn_core.p2s:
            if self._amsn_core.p2s[key] == view.presence:
                self._clwidget.ui.status.setCurrentIndex(self._clwidget.ui.status.findData(key))

    def get_contactlist_widget(self):
        return self._clwidget

class itemDelegate(QStyledItemDelegate):
    #Dooooon't touch anything here!!! Or it will break into a million pieces and you'll be really sorry!!!
    def paint(self, painter, option, index):
        if not index.isValid():
            return
        painter.translate(0, 0)
        options = QStyleOptionViewItemV4(option)
        self.initStyleOption(options, index)
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, True)
        doc = QTextDocument()
        doc.setHtml(options.text)
        options.text = ""
        QApplication.style().drawControl(QStyle.CE_ItemViewItem, options, painter, options.widget)
        painter.translate(options.rect.left() + self.sizeDp(index) + 3, options.rect.top()) #paint text right after the dp + 3pixels
        rect = QRectF(0, 0, options.rect.width(), options.rect.height())
        doc.drawContents(painter, rect)
        painter.restore()

    def sizeHint(self, option, index):
        options = QStyleOptionViewItemV4(option)
        self.initStyleOption(options, index)
        doc = QTextDocument()
        doc.setHtml(options.text)
        doc.setTextWidth(options.rect.width())

        #if group, leave as it, if contactitem, use dp height for calculating sizeHint.
        model = index.model()
        qv = QPixmap(model.data(model.index(index.row(), 0, index.parent()), Qt.DecorationRole))
        if qv.isNull():
            size = QSize(doc.idealWidth(), doc.size().height())
        else:
            size = QSize(doc.idealWidth(), qv.height() + 6)
            
        return size

    def sizeDp(self, index):
        model = index.model()
        qv = QPixmap(model.data(model.index(index.row(), 0, index.parent()), Qt.DecorationRole))
        return qv.width()

class GlobalFilter(QObject):
    def __init__(self,parent =None):
        QObject.__init__(self,parent)

    def eventFilter(self, obj, e):
        if obj.objectName() == "nickName":
          if e.type() == QEvent.FocusOut:
            obj.emit(SIGNAL("nickChange()"))
            return False
          if e.type() == QEvent.KeyPress and (e.key() == Qt.Key_Enter or e.key() == Qt.Key_Return):
            return True

        if obj.objectName() == "statusMessage":
          if e.type() == QEvent.FocusOut:
            obj.emit(SIGNAL("psmChange()"))
            return False
          if e.type() == QEvent.KeyPress and (e.key() == Qt.Key_Enter or e.key() == Qt.Key_Return):
            return True
        return False

class aMSNContactListWidget(StyledWidget, base.aMSNContactListWidget):
    def __init__(self, amsn_core, parent):
        StyledWidget.__init__(self, parent._parent)
        self._amsn_core = amsn_core
        self._myview = parent._myview
        self.ui = Ui_ContactList()
        self.ui.setupUi(self)
        delegate = itemDelegate(self)
        self.ui.cList.setItemDelegate(delegate)
        self._parent = parent
        self._mainWindow = parent._parent
        self._model = QStandardItemModel(self)
        self._model.setColumnCount(4)
        self._proxyModel = QSortFilterProxyModel(self)
        self._proxyModel.setSourceModel(self._model)
        self.ui.cList.setModel(self._proxyModel)
        self._contactDict = dict()
        self.groups = []
        self.contacts = {}

        self._proxyModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self._proxyModel.setFilterKeyColumn(-1)

        (self.ui.cList.header()).resizeSections(1) #auto-resize column wigth
        (self.ui.cList.header()).setSectionHidden(1, True) #hide --> (group/contact ID)
        (self.ui.cList.header()).setSectionHidden(2, True) #hide --> (boolean value. Do I really need this?)
        (self.ui.cList.header()).setSectionHidden(3, True) #hide --> (contact/group view object)

        self.connect(self.ui.searchLine, SIGNAL('textChanged(QString)'), self._proxyModel, SLOT('setFilterFixedString(QString)'))
        self.connect(self.ui.nickName, SIGNAL('nickChange()'), self.__nickChange)
        self.connect(self.ui.statusMessage, SIGNAL('psmChange()'), self.__psmChange)
        self.connect(self.ui.status, SIGNAL('currentIndexChanged(int)'), self.__statusChange)
        self.connect(self.ui.cList, SIGNAL('doubleClicked(QModelIndex)'), self.__clDoubleClick)

        self.ui.nickName.installEventFilter(GlobalFilter(self.ui.nickName))
        self.ui.statusMessage.installEventFilter(GlobalFilter(self.ui.statusMessage))


    def show(self):
        self._mainWindow.fadeIn(self)

    def hide(self):
        pass

    def __nickChange(self):
        sv = StringView()
        sv.append_text(str(self.ui.nickName.toPlainText()))
        self._myview.nick = str(sv)

    def __psmChange(self):
        sv = StringView()
        sv.append_text(str(self.ui.statusMessage.toPlainText()))
        self._myview.psm = str(sv)

    def __statusChange(self, i):
        if self.ui.status.count()+1 != len(self._amsn_core.p2s): return
        for key in self._amsn_core.p2s:
            if key == str(self.ui.status.itemData(i).toString()):
                self._myview.presence = self._amsn_core.p2s[key]

    def __search_by_id(self, id):
        parent = self._model.item(0)
        children = []

        while (parent is not None):
            obj = str(self._model.item(self._model.indexFromItem(parent).row(), 1).text())

            if (obj == id): return parent
            child = parent.child(0)
            nc = 0
            while (child is not None):
                cobj = str(parent.child(nc, 1).text())
                if (cobj == id): children.append(child)
                nc = nc + 1
                child = self._model.item(self._model.indexFromItem(parent).row()).child(nc)
            parent = self._model.item(self._model.indexFromItem(parent).row() + 1)
            if parent is None: break

        if children: return children
        else:  return None

    def contactlist_updated(self, view):
        guids = self.groups
        self.groups = []

        # New groups
        for gid in view.group_ids:
            if (gid == 0): gid = '0'
            self.groups.append(gid)
            if gid not in guids:
                self._model.appendRow([QStandardItem(gid), QStandardItem(gid), QStandardItem("group"), QStandardItem()])

        # Remove unused groups
        for gid in guids:
            if gid not in self.groups:
                gitem = self.__search_by_id(gid)
                self._model.removeRow((self._model.indexFromItem(gitem)).row())
                try:
                    del self.contacts[gid]
                except KeyError:
                    pass
                #self.groups.remove(gid)

    def contact_updated(self, contact):
        
        citems = self.__search_by_id(contact.uid)
        if citems is None: return

        dp = Image(self._parent._theme_manager, contact.dp)
        dp = dp.to_size(28, 28)
        #icon = Image(self._parent._theme_manager, contact.icon)

        for citem in citems:
            gitem = citem.parent()
            if gitem is None: continue

            gitem.child(self._model.indexFromItem(citem).row(), 0).setData(QVariant(dp), Qt.DecorationRole)
            #gitem.child(self._model.indexFromItem(citem).row(), 0).setData(QVariant(icon), Qt.DecorationRole)

            gitem.child(self._model.indexFromItem(citem).row(), 3).setData(QVariant(contact), Qt.DisplayRole)
            cname = StringView()
            cname = contact.name.to_HTML_string()
            gitem.child(self._model.indexFromItem(citem).row(), 0).setText(QString.fromUtf8(cname))

    def group_updated(self, group):
        if (group.uid == 0): group.uid = '0'
        if group.uid not in self.groups: return
        
        gitem = self.__search_by_id(group.uid)
        self._model.item(self._model.indexFromItem(gitem).row(), 3).setData(QVariant(group), Qt.DisplayRole)
        gname = StringView()
        gname = group.name
        self._model.item((self._model.indexFromItem(gitem)).row(), 0).setText('<b>'+QString.fromUtf8(gname.to_HTML_string())+'</b>')

        try:
            cuids = self.contacts[group.uid]
        except:
            cuids = []
        self.contacts[group.uid] = group.contact_ids.copy()

        for cid in group.contact_ids:
            if cid not in cuids:
                gitem = self.__search_by_id(group.uid)
                gitem.appendRow([QStandardItem(cid), QStandardItem(cid), QStandardItem("contact"), QStandardItem()])

        # Remove unused contacts
        for cid in cuids:
            if cid not in self.contacts[group.uid]:
                citems = self.__search_by_id(cid)
                for citem in citems:
                    self._model.removeRow((self._model.indexFromItem(citem)).row())

    def group_removed(self, group):
        gid = self.__search_by_id(group.uid)
        self._model.takeRow(self._model.indexFromItem(gid))

    def configure(self, option, value):
        pass

    def cget(self, option, value):
        pass

    def size_request_set(self, w, h):
        pass

    def __clDoubleClick(self, index):

        model = index.model()
        qvart = model.data(model.index(index.row(), 2, index.parent()))
        qvarv = model.data(model.index(index.row(), 3, index.parent()))

        type = qvart.toString()
        view = qvarv.toPyObject()

        #is the double-clicked item a contact?
        if type == "contact":
            view.on_click(view.uid)
        else:
            print "Double click on group!"

    def contextMenuEvent(self, event):
        l = self.ui.cList.selectedIndexes()
        index = l[0]
        model = index.model()
        qvart = model.data(model.index(index.row(), 2, index.parent()))
        qvarv = model.data(model.index(index.row(), 3, index.parent()))

        type = qvart.toString()
        view = qvarv.toPyObject()

        if type == "contact":
            menuview = view.on_right_click_popup_menu
            menu = QMenu("Contact Popup", self)
            common.create_menu_items_from_view(menu, menuview.items)
            menu.popup(event.globalPos())
        if type == "group":
            menuview = view.on_right_click_popup_menu
            menu = QMenu("Group Popup", self)
            common.create_menu_items_from_view(menu, menuview.items)
            menu.popup(event.globalPos())

    def set_contact_context_menu(self, cb):
        #TODO:
        pass

    def group_added(self, group):
        pi = self._model.invisibleRootItem()

        # Adding Group Item

        groupItem = QStandardItem()
        gname = StringView()
        gname = group.name
        self._model.item(groupItem.row(), 0).setText('<b>'+QString.fromUtf8(gname.toHtmlString())+'</b>')
        self._model.item(groupItem.row(), 1).setText(QString.fromUtf8(str(group.uid)))
        pi.appendRow(groupItem)

        for contact in group.contacts:
            contactItem = QStandardItem()
            cname = StringView()
            cname = contact.name
            self._model.item(contactItem.row(), 0).setText(QString.fromUtf8(cname.toHtmlString()))
            self._model.item(contactItem.row(), 1).setText(QString.fromUtf8(str(contact.uid)))

            groupItem.appendRow(contactItem)

            self._contactDict[contact.uid] = contact
