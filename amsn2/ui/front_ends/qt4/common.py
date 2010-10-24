from amsn2.views import StringView, MenuItemView
from PyQt4 import Qt
from PyQt4 import QtCore
from PyQt4 import QtGui


def create_menu_items_from_view(menu, items):
    # TODO: images & radio groups, for now only basic representation
    for item in items:
        if item.type is MenuItemView.COMMAND:
            it = QtGui.QAction(item.label, menu)
            QtCore.QObject.connect(it, QtCore.SIGNAL("triggered()"), item.command)
            menu.addAction(it)
        elif item.type is MenuItemView.CASCADE_MENU:
            men = QtGui.QMenu(item.label, menu)
            create_menu_items_from_view(men, item.items)
            menu.addMenu(men)
        elif item.type is MenuItemView.SEPARATOR:
            menu.addSeparator()
        elif item.type is MenuItemView.CHECKBUTTON:
            it = QtGui.QAction(item.label, menu)
            it.setCheckable(True)
            if item.checkbox: #TODO : isn't it checkbox_value instead of checkbox ? By the way the MenuItemView constructor doesn't store the checkbox_value passed to it
                it.setChecked(True)
            QtCore.QObject.connect(it, QtCore.SIGNAL("triggered()"), item.command)
            menu.addAction(it)
        elif item.type is MenuItemView.RADIOBUTTON:
            it = QtGui.QAction(item.label, menu)
            it.setCheckable(True)
            if item.checkbox:
                it.setChecked(True)
            QtCore.QObject.connect(it, QtCore.SIGNAL("triggered()"), item.command)
        elif item.type is MenuItemView.RADIOBUTTONGROUP:
            group = QtGui.QActionGroup(menu)
            create_menu_items_from_view(group, item.items)
            menu.addActions(group)
