# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import qdarkgraystyle
from logic import Graf
from items import VertexItem
from pickle import dump, load


# запрещать нажатие алгоритма, если у графа ни одной вершины
class Tab(QtWidgets.QMainWindow):
    def __init__(self):
        super(Tab, self).__init__()
        self.vertex = True
        self.color = QtGui.QColor(205, 205, 205)
        # self.selected = None
        self.graf = Graf()
        self.scene = QtWidgets.QGraphicsScene(self.rect().x(), self.rect().y(), self.rect().width(), self.rect().height())
        self.view = QtWidgets.QGraphicsView()
        self.view.setRenderHints(QtGui.QPainter.Antialiasing |
                                 QtGui.QPainter.HighQualityAntialiasing)
        self.view.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)
        self.view.setScene(self.scene)
        self.setCentralWidget(self.view)

    def white(self):
        self.color = QtGui.QColor(205, 205, 205)

    def red(self):
        self.color = QtGui.QColor(205, 0, 0)

    def green(self):
        self.color = QtGui.QColor(0, 205, 0)

    def blue(self):
        self.color = QtGui.QColor(0, 0, 205)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            self.vertex = not self.vertex
            print('changing')

    def mouseDoubleClickEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            print('click-click')
            if self.vertex:
                vert_item = self.addGraphicsItem((event.pos().x()-25, event.pos().y()-25, 50, 50), str(len(self.graf.vertexes)), 10)
                self.graf.add_vertex(vert_item)
                # self.selected = self.graf.vertexes[-1]
                print('vertex added')

    def addGraphicsItem(self, rect, name, font_size):
        brush1 = QtGui.QBrush(self.color)
        if self.color is QtGui.QColor(205, 0, 0):
            brush2 = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        elif self.color is QtGui.QColor(0, 205, 0):
            brush2 = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        elif self.color is QtGui.QColor(0, 0, 205):
            brush2 = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        else:
            brush2 = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        item = VertexItem(rect, brush1, brush2, name, font_size, self)
        self.scene.addItem(item)
        return item

    def clear(self):
        self.clear()

    def radius(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Accepted)
        msg.setText("Radius of current Graph")
        # msg.setWindowTitle("")
        msg.setDetailedText(str(self.graf.radius_diameter()[0]))
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)

    def diameter(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Accepted)
        msg.setText("Diameter of current Graph")
        # msg.setWindowTitle("")
        msg.setDetailedText(str(self.graf.radius_diameter()[1]))
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)


# показывать текущий цвет пера и инструмент (вершина или ребро)
# спрашивало "сохранились ли вы?"
class Ui_GrafCreator(object):
    def setupUi(self, GrafCreator):
        GrafCreator.setObjectName("GrafCreator")
        GrafCreator.setWindowIcon(QtGui.QIcon("icons/icon.png"))
        GrafCreator.setEnabled(True)
        GrafCreator.resize(1112, 826)
        GrafCreator.setDocumentMode(True)
        self.tabWidget = QtWidgets.QTabWidget()
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)
        GrafCreator.setCentralWidget(self.tabWidget)
        self.menubar = QtWidgets.QMenuBar(GrafCreator)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1112, 26))
        self.menubar.setToolTipDuration(2)
        self.menubar.setNativeMenuBar(True)
        self.toolbar = QtWidgets.QToolBar(GrafCreator)
        self.menunew = QtWidgets.QMenu(self.menubar)
        self.menuColor = QtWidgets.QMenu(self.menubar)
        self.menuAlgorithms = QtWidgets.QMenu(self.menubar)
        GrafCreator.setMenuBar(self.menubar)
        GrafCreator.addToolBar(self.toolbar)
        self.actionNew = QtWidgets.QAction(QtGui.QIcon("icons/new.png"), "New", GrafCreator)
        self.actionNew.setShortcut("Ctrl+N")
        self.actionNew.triggered.connect(self.new_tab)
        self.actionOpen = QtWidgets.QAction(QtGui.QIcon("icons/open.png"), "Open", GrafCreator)
        self.actionOpen.setShortcut("Ctrl+O")
        self.actionOpen.triggered.connect(self.open)
        self.actionSave = QtWidgets.QAction(QtGui.QIcon("icons/save.png"), "Save", GrafCreator)
        self.actionSave.setShortcut("Ctrl+S")
        self.actionSave.setDisabled(True)
        self.actionSave.triggered.connect(self.save)
        self.actionClear = QtWidgets.QAction(QtGui.QIcon("icons/clear.png"), "Clear", GrafCreator)
        self.actionClear.setShortcut("Ctrl+C")
        self.actionClear.setDisabled(True)
        self.actionClear.triggered.connect(self.clear)
        self.actionWhite = QtWidgets.QAction(QtGui.QIcon("icons/white.png"), "White", GrafCreator)
        self.actionWhite.setShortcut("Ctrl+1")
        self.actionWhite.setDisabled(True)
        self.actionWhite.triggered.connect(self.white)
        self.actionRed = QtWidgets.QAction(QtGui.QIcon("icons/red.png"), "Red", GrafCreator)
        self.actionRed.setShortcut("Ctrl+2")
        self.actionRed.setDisabled(True)
        self.actionRed.triggered.connect(self.red)
        self.actionGreen = QtWidgets.QAction(QtGui.QIcon("icons/green.png"), "Green", GrafCreator)
        self.actionGreen.setShortcut("Ctrl+3")
        self.actionGreen.setDisabled(True)
        self.actionGreen.triggered.connect(self.green)
        self.actionBlue = QtWidgets.QAction(QtGui.QIcon("icons/blue.png"), "Blue", GrafCreator)
        self.actionBlue.setShortcut("Ctrl+4")
        self.actionBlue.setDisabled(True)
        self.actionBlue.triggered.connect(self.blue)
        self.actionRadius = QtWidgets.QAction(QtGui.QIcon("icons/radius.png"), "Radius", GrafCreator)
        self.actionRadius.setShortcut("Ctrl+R")
        self.actionRadius.setDisabled(True)
        self.actionRadius.triggered.connect(self.radius)
        self.actionDiameter = QtWidgets.QAction(QtGui.QIcon("icons/diameter.png"), "Diameter", GrafCreator)
        self.actionDiameter.setShortcut("Ctrl+D")
        self.actionDiameter.setDisabled(True)
        self.actionDiameter.triggered.connect(self.diameter)
        self.actionCloseTab = QtWidgets.QAction(QtGui.QIcon("icons/close.png"), "Close tab", GrafCreator)
        self.actionCloseTab.setShortcut("Ctrl+W")
        self.actionCloseTab.setDisabled(True)
        self.actionCloseTab.triggered.connect(self.closeCurrentTab)
        self.menunew.addAction(self.actionNew)
        self.menunew.addAction(self.actionOpen)
        self.menunew.addAction(self.actionCloseTab)
        self.menunew.addAction(self.actionSave)
        self.menunew.addSeparator()
        self.menunew.addAction(self.actionClear)
        self.menuColor.addAction(self.actionWhite)
        self.menuColor.addAction(self.actionRed)
        self.menuColor.addAction(self.actionGreen)
        self.menuColor.addAction(self.actionBlue)
        self.menuAlgorithms.addAction(self.actionRadius)
        self.menuAlgorithms.addAction(self.actionDiameter)
        self.menubar.addAction(self.menunew.menuAction())
        self.menubar.addAction(self.menuColor.menuAction())
        self.menubar.addAction(self.menuAlgorithms.menuAction())

        self.toolbar.addAction(self.actionNew)
        self.toolbar.addAction(self.actionOpen)
        self.toolbar.addAction(self.actionCloseTab)
        self.toolbar.addAction(self.actionSave)
        self.toolbar.addAction(self.actionClear)
        self.actionWhite.setCheckable(True)
        self.actionWhite.setChecked(True)
        self.toolbar.addAction(self.actionWhite)
        self.actionRed.setCheckable(True)
        self.toolbar.addAction(self.actionRed)
        self.actionGreen.setCheckable(True)
        self.toolbar.addAction(self.actionGreen)
        self.actionBlue.setCheckable(True)
        self.toolbar.addAction(self.actionBlue)
        self.toolbar.addAction(self.actionRadius)
        self.toolbar.addAction(self.actionDiameter)

        self.retranslateUi(GrafCreator)
        QtCore.QMetaObject.connectSlotsByName(GrafCreator)

    def retranslateUi(self, GrafCreator):
        _translate = QtCore.QCoreApplication.translate
        GrafCreator.setWindowTitle(_translate("GrafCreator", "GrafCreator"))
        self.menunew.setTitle(_translate("GrafCreator", "File"))
        self.menuColor.setTitle(_translate("GrafCreator", "Color"))
        self.menuAlgorithms.setTitle(_translate("GrafCreator", "Algorithms"))
        self.actionNew.setText(_translate("GrafCreator", "New"))
        self.actionOpen.setText(_translate("GrafCreator", "Open"))
        self.actionSave.setText(_translate("GrafCreator", "Save"))
        self.actionClear.setText(_translate("GrafCreator", "Clear"))
        self.actionWhite.setText(_translate("GrafCreator", "White"))
        self.actionRed.setText(_translate("GrafCreator", "Red"))
        self.actionGreen.setText(_translate("GrafCreator", "Green"))
        self.actionBlue.setText(_translate("GrafCreator", "Blue"))
        self.actionRadius.setText(_translate("GrafCreator", "Radius"))
        self.actionDiameter.setText(_translate("GrafCreator", "Diameter"))

    def new_tab(self):
        tab = Tab()
        self.tabWidget.addTab(tab, 'Tab {}'.format(len(self.tabWidget)))
        self.tabWidget.setCurrentWidget(tab)
        for action in self.toolbar.actions():
            action.setDisabled(False)

    def closeTab(self, currentIndex):
        self.tabWidget.widget(currentIndex).deleteLater()
        if len(self.tabWidget.tabBar()) == 1:
            self.disableActions()

    def closeCurrentTab(self):
        self.tabWidget.currentWidget().deleteLater()
        if len(self.tabWidget.tabBar()) == 1:
            self.disableActions()

    def disableActions(self):
        self.actionClear.setDisabled(True)
        self.actionSave.setDisabled(True)
        self.actionWhite.setDisabled(True)
        self.actionRed.setDisabled(True)
        self.actionGreen.setDisabled(True)
        self.actionBlue.setDisabled(True)
        self.actionRadius.setDisabled(True)
        self.actionDiameter.setDisabled(True)
        self.actionCloseTab.setDisabled(True)

    def save(self):
        filename = self.tabWidget.currentWidget().objectName()+'.pickle'
        print(filename)
        with open('loads/'+filename, 'wb') as file:
            print('ok')
            dump(self.tabWidget.currentWidget().graf, file)
            print('finish')

    def open(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self.tabWidget.currentWidget(), 'Open file', '')  # БГУиР/4 Сем/ОТС/Editor/loads
        print(fname[0][-7:])
        if fname[0] != '':
            if fname[0][-7:] == '.pickle':
                with open(fname[0], 'rb') as file:
                    tab = Tab()
                    tab.graf = load(file)
                    tab.setObjectName(fname[0][fname[0].index('/')+1:-7])
                    self.tabWidget.addTab(tab, fname[0][fname[0].rindex('/')+1:-7])
                    self.tabWidget.setCurrentWidget(tab)

    def clear(self):
        if self.tabWidget.currentWidget() is not None:
            self.tabWidget.currentWidget().clear()

    def white(self):
        for action in self.toolbar.actions():
            if action.isCheckable and action is not self.actionWhite:
                action.setChecked(False)
        self.tabWidget.currentWidget().black()

    def red(self):
        for action in self.toolbar.actions():
            if action.isCheckable and action is not self.actionRed:
                action.setChecked(False)
        self.tabWidget.currentWidget().red()

    def green(self):
        for action in self.toolbar.actions():
            if action.isCheckable and action is not self.actionGreen:
                action.setChecked(False)
        self.tabWidget.currentWidget().green()

    def blue(self):
        for action in self.toolbar.actions():
            if action.isCheckable and action is not self.actionBlue:
                action.setChecked(False)
        self.tabWidget.currentWidget().blue()

    def radius(self):
        self.tabWidget.currentWidget().radius()

    def diameter(self):
        self.tabWidget.currentWidget().diameter()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkgraystyle.load_stylesheet())
    GrafCreator = QtWidgets.QMainWindow()
    ui = Ui_GrafCreator()
    ui.setupUi(GrafCreator)
    GrafCreator.show()
    sys.exit(app.exec_())
