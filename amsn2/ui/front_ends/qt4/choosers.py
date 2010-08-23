# -*- coding: utf-8 -*-
from amsn2.ui import base
import image
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class aMSNFileChooserWindow(base.aMSNFileChooserWindow):
    def __init__(self, filters, directory, callback, parent = None):

        filefilter = QString()

        if filters:
            first = True
            for name in filters.keys():
                if first == False:
                    filefilter = filefilter + ";;"
                filefilter = filefilter + name + " ("
                for ext in filters[name]:
                    filefilter = filefilter + ext + " "
                filefilter = filefilter + ")"
                first = False

        filename=QFileDialog.getOpenFileName(parent, "aMSN2 - Choose a file", "", filefilter)


        self.callback = callback
        if str(filename)=="":
            pass
        else:
            self.callback(filename)





class aMSNDPChooserWindowSingleton(base.aMSNDPChooserWindow, QDialog):
    def __init__(self):
        self.firstTime = True

    def __call__(self, callback, backend_manager, title ="aMSN - Choose a Display Picture", parent = None):
        if self.firstTime:
            QDialog.__init__(self, parent)
            self.iconview = QListWidget()
            self.iconview.setViewMode(1)
            self.iconview.setResizeMode(1)
            self.iconview.setMovement(0)
            self.iconview.setIconSize(QSize(96,96))
            self.iconview.setWordWrap( True )
            self.iconview.setGridSize(QSize(106,121))
            QObject.connect(self.iconview, SIGNAL("itemDoubleClicked(QListWidgetItem)"), self._on_dp_dblclick)
            self.buttonOk= QPushButton("Ok")
            QObject.connect(self.buttonOk, SIGNAL("clicked()"), self._on_ok_clicked)
            self.buttonCancel = QPushButton("Cancel")
            QObject.connect(self.buttonCancel, SIGNAL("clicked()"), self.reject)
            QObject.connect(self, SIGNAL("rejected()"), self._on_reject)
            self.buttonOpen = QPushButton("Open File")
            QObject.connect(self.buttonOpen, SIGNAL("clicked()"), self._open_file)
            self.vboxlayout = QVBoxLayout()
            self.hboxlayout = QHBoxLayout()
            self.vboxlayout.addWidget(self.buttonOk)
            self.vboxlayout.addWidget(self.buttonCancel)
            self.vboxlayout.addWidget(self.buttonOpen)
            self.vboxlayout.addStretch(1)
            self.hboxlayout.addWidget(self.iconview)
            self.hboxlayout.addLayout(self.vboxlayout)
            self.setLayout(self.hboxlayout)

        default_dps = []
        for dp in default_dps:
            self._update_dp_list(default_dps)
        self.resize(550, 450)
        self.setWindowTitle(title)
        self.callback = callback
        self.show()
        self.activateWindow()
        self.firstTime = False
        return self


    def _open_file(self):
        filters = {'Image files':("*.png", "*.jpeg", "*.jpg", "*.gif", "*.bmp"),
                   'All files':('*.*')}
        self.filechooser = aMSNFileChooserWindow(filters, None, self._update_dp_list,self)


    def empty(self):
        #self.iconview.clear()
        pass #we should clear the view each time and re add all the images given by the core, but for now, no images are passed so i just leave the ones added and don't clear


    def _dp_chosen(self, path):
        self.callback(str(path))
        self.accept()
        self.empty()
        self.done(-1)

    def _on_reject(self):
        self.empty()
        self.done(-1)


    def _on_ok_clicked(self):
        item = self.iconview.currentItem()
        if item == None:
            return

        path = item.data(Qt.UserRole)
        path = path.toString()
        self._dp_chosen(path)


    def _on_dp_dblclick(self, item):
        path = item.data(Qt.UserRole)
        path = path.toString()
        self._dp_chosen(path)


    def set_title(self, title):
        self.setWindowTitle(title)


    def show(self):
        QDialog.show(self)


    def _update_dp_list(self, dp_path):
        im = QPixmap(dp_path) #should pass the image to the core then get the rescaled pixmap from it
        im = im.scaled(96,96,0,1) #should also check if the given path really contains an image, or the core should ?
        name = QString(dp_path)
        name.remove(0, (name.lastIndexOf("/")+1))
        item = QListWidgetItem(QIcon(im), name)
        item.setData(Qt.UserRole, dp_path)
        self.iconview.addItem(item)

aMSNDPChooserWindow = aMSNDPChooserWindowSingleton()