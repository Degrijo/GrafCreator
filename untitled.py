# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_GrafCreator(object):
    def setupUi(self, GrafCreator):
        GrafCreator.setObjectName("GrafCreator")
        GrafCreator.resize(1124, 819)
        GrafCreator.setDocumentMode(True)
        self.centralwidget = QtWidgets.QWidget(GrafCreator)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setToolTipDuration(-1)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout.addWidget(self.tabWidget)
        GrafCreator.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(GrafCreator)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1124, 26))
        self.menubar.setToolTipDuration(2)
        self.menubar.setDefaultUp(True)
        self.menubar.setNativeMenuBar(True)
        self.menubar.setObjectName("menubar")
        self.menunew = QtWidgets.QMenu(self.menubar)
        self.menunew.setObjectName("menunew")
        self.menuopen = QtWidgets.QMenu(self.menubar)
        self.menuopen.setObjectName("menuopen")
        GrafCreator.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(GrafCreator)
        self.statusbar.setObjectName("statusbar")
        GrafCreator.setStatusBar(self.statusbar)
        self.actionNew = QtWidgets.QAction(GrafCreator)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtWidgets.QAction(GrafCreator)
        self.actionOpen.setObjectName("actionOpen")
        self.menunew.addAction(self.actionNew)
        self.menunew.addAction(self.actionOpen)
        self.menubar.addAction(self.menunew.menuAction())
        self.menubar.addAction(self.menuopen.menuAction())

        self.retranslateUi(GrafCreator)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(GrafCreator)

    def retranslateUi(self, GrafCreator):
        _translate = QtCore.QCoreApplication.translate
        GrafCreator.setWindowTitle(_translate("GrafCreator", "GrafCreator"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("GrafCreator", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("GrafCreator", "Tab 2"))
        self.menunew.setTitle(_translate("GrafCreator", "File"))
        self.menuopen.setTitle(_translate("GrafCreator", "Edit"))
        self.actionNew.setText(_translate("GrafCreator", "New"))
        self.actionOpen.setText(_translate("GrafCreator", "Open"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    GrafCreator = QtWidgets.QMainWindow()
    ui = Ui_GrafCreator()
    ui.setupUi(GrafCreator)
    GrafCreator.show()
    sys.exit(app.exec_())

