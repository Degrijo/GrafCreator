# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import qdarkgraystyle
from logic import Graf
from items import *
from pickle import dump, load


class Tab(QtWidgets.QWidget):
    def __init__(self, parent):
        super(Tab, self).__init__()
        self.parent = parent
        self.edge = []
        self.graf = Graf()
        self.scene = QtWidgets.QGraphicsScene(self.rect().x(), self.rect().y(), self.rect().width(),
                                              self.rect().height())
        self.view = QtWidgets.QGraphicsView()
        self.layout = QtWidgets.QVBoxLayout()
        self.view.setRenderHints(QtGui.QPainter.Antialiasing |
                                 QtGui.QPainter.HighQualityAntialiasing)
        self.view.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)
        self.view.setScene(self.scene)
        self.layout.addWidget(self.view)
        self.setLayout(self.layout)

    def resizeEvent(self, QResizeEvent):
        self.scene.setSceneRect(self.rect().x(), self.rect().y(), self.rect().width(), self.rect().height())

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == QtCore.Qt.Key_Delete:
            self.edge.clear()
            for item in self.scene.selectedItems():
                if type(item) is VertexItem:
                    for edge in self.graf.get_vertex_item(item).edges:
                        self.scene.removeItem(edge.item)
                    self.scene.removeItem(item)
                    self.graf.del_vertex(self.graf.get_vertex_item(item))
                elif type(item) is EdgeItem:
                    edge = self.graf.get_edge_item(item)
                    if edge is not None:
                        self.scene.removeItem(item)
                        self.graf.del_edge(edge.vertex1, edge.vertex2)
        if QKeyEvent.key() == QtCore.Qt.Key_W:
            print('1')
            print(self.scene.selectedItems())
            if len(self.scene.selectedItems()) is 1 and type(self.scene.selectedItems()[0]) is EdgeItem:
                print('2')
                msg = QtWidgets.QInputDialog
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setWindowTitle("Weight of selected edge")
                msg.exec()

    def mousePressEvent(self, event):
        self.edge.clear()
        if event.button() == QtCore.Qt.RightButton:
            if self.parent.vertex:
                self.parent.change_edge()
            else:
                self.parent.change_vertex()

    def mouseDoubleClickEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            if self.parent.vertex:
                vert_item = self.addVertexItem((event.pos().x() - 25, event.pos().y() - 25, 50, 50),
                                               str(len(self.graf.vertexes)), 10)
                self.graf.add_vertex(vert_item)

    def addEdgeItem(self):
        if not self.parent.vertex:
            if len(self.scene.selectedItems()) is not 1:
                return
            item = self.scene.selectedItems()[0]
            self.edge.append(item)
            if len(self.edge) is 2:
                vert1 = self.graf.get_vertex_item(self.edge[0])
                vert2 = self.graf.get_vertex_item(self.edge[1])
                if vert1 is not None and vert2 is not None:
                    if self.graf.get_edge(vert1, vert2) is None:
                        if vert1 == vert2:
                            item = EdgeItem(self.edge[0], self.edge[1], QtGui.QPen(self.parent.color, 10.0),
                                            QtGui.QPen(self.getLightColor(), 10), self, True)
                        elif self.graf.get_edge(vert2, vert1) is not None:
                            self.graf.get_edge(vert2, vert1).item.makeNotOriented()
                        else:
                            item = EdgeItem(self.edge[0], self.edge[1], QtGui.QPen(self.parent.color, 10.0),
                                            QtGui.QPen(self.getLightColor(), 10.0), self)
                        self.scene.addItem(item)
                        self.graf.add_edge(vert1, vert2, item)
                        self.edge.clear()

    def getLightColor(self):
        col = self.parent.color
        if col == QtGui.QColor(205, 0, 0):
            return QtGui.QColor(255, 0, 0)
        elif col == QtGui.QColor(0, 205, 0):
            return QtGui.QColor(0, 255, 0)
        elif col == QtGui.QColor(0, 0, 205):
            return QtGui.QColor(0, 0, 255)
        else:
            return QtGui.QColor(255, 255, 255)

    def addVertexItem(self, rect, name, font_size):
        item = VertexItem(rect, QtGui.QBrush(self.parent.color), QtGui.QBrush(self.getLightColor()), name, font_size,
                          self)
        self.scene.addItem(item)
        return item

    def delVertexItem(self, item):
        vert = self.graf.get_vertex_item(item)
        for edge in vert.edges:
            self.scene.removeItem(edge.item)
        self.graf.del_vertex(vert)
        self.scene.removeItem(item)

    def delEdgeItem(self, item):
        edge = self.graf.get_edge_item(item)
        self.graf.del_edge(edge.vertex1, edge.vertex2)
        self.scene.removeItem(item)

    def clear(self):
        self.scene.clear()

    def radius(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setWindowTitle("Radius of current Graph")
        rez = self.graf.radius_diameter()
        if rez is not None:
            msg.setText(str(rez[0]))
        else:
            msg.setText("Empty graph")
        msg.exec()

    def diameter(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setWindowTitle("Diameter of current Graph")
        rez = self.graf.radius_diameter()
        if rez is not None:
            msg.setText(str(rez[1]))
        else:
            msg.setText("Empty graph")
        msg.exec()


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
        self.actionVertex = QtWidgets.QAction(QtGui.QIcon("icons/vertex.png"), "Vertex", GrafCreator)
        self.actionVertex.setDisabled(True)
        self.actionVertex.triggered.connect(self.change_vertex)
        self.actionEdge = QtWidgets.QAction(QtGui.QIcon("icons/edge.png"), "Edge", GrafCreator)
        self.actionEdge.triggered.connect(self.change_edge)
        self.actionEdge.setDisabled(True)
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
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.actionVertex)
        self.actionVertex.setCheckable(True)
        self.actionVertex.setChecked(True)
        self.toolbar.addAction(self.actionEdge)
        self.actionEdge.setCheckable(True)
        self.actionWhite.setCheckable(True)
        self.actionWhite.setChecked(True)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.actionWhite)
        self.actionRed.setCheckable(True)
        self.toolbar.addAction(self.actionRed)
        self.actionGreen.setCheckable(True)
        self.toolbar.addAction(self.actionGreen)
        self.actionBlue.setCheckable(True)
        self.toolbar.addAction(self.actionBlue)
        self.toolbar.addSeparator()
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
        self.actionVertex.setText(_translate("GrafCreator", "Vertex"))
        self.actionEdge.setText(_translate("GrafCreator", "Edge"))
        self.actionWhite.setText(_translate("GrafCreator", "White"))
        self.actionRed.setText(_translate("GrafCreator", "Red"))
        self.actionGreen.setText(_translate("GrafCreator", "Green"))
        self.actionBlue.setText(_translate("GrafCreator", "Blue"))
        self.actionRadius.setText(_translate("GrafCreator", "Radius"))
        self.actionDiameter.setText(_translate("GrafCreator", "Diameter"))

    def __init__(self):
        self.color = QtGui.QColor(205, 205, 205)
        self.vertex = True

    def change_vertex(self):
        self.vertex = True
        self.actionVertex.setChecked(True)
        self.actionEdge.setChecked(False)

    def change_edge(self):
        self.vertex = False
        self.actionVertex.setChecked(False)
        self.actionEdge.setChecked(True)

    def new_tab(self):
        tab = Tab(self)
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
        for action in [self.actionClear, self.actionSave, self.actionVertex, self.actionEdge, self.actionWhite,
                       self.actionRed, self.actionGreen, self.actionBlue, self.actionRadius, self.actionDiameter,
                       self.actionCloseTab]:
            action.setDisabled(True)

    def save(self):
        filename = self.tabWidget.currentWidget().objectName() + '.pickle'
        print(filename)
        with open('loads/' + filename, 'wb') as file:
            print('ok')
            dump(self.tabWidget.currentWidget().graf, file)
            print('finish')

    def open(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self.tabWidget.currentWidget(), 'Open file',
                                                      '')  # БГУиР/4 Сем/ОТС/Editor/loads
        if fname[0] != '':
            if fname[0][-7:] == '.pickle':
                with open(fname[0], 'rb') as file:
                    tab = Tab(self)
                    tab.graf = load(file)
                    tab.setObjectName(fname[0][fname[0].index('/') + 1:-7])
                    self.tabWidget.addTab(tab, fname[0][fname[0].rindex('/') + 1:-7])
                    self.tabWidget.setCurrentWidget(tab)
                    for action in self.toolbar.actions():
                        action.setDisabled(False)

    def clear(self):
        self.tabWidget.currentWidget().clear()

    def white(self):
        for action in [self.actionRed, self.actionGreen, self.actionBlue]:
            action.setChecked(False)
        self.actionWhite.setChecked(True)
        self.color = QtGui.QColor(205, 205, 205)

    def red(self):
        for action in [self.actionWhite, self.actionGreen, self.actionBlue]:
            action.setChecked(False)
        self.actionRed.setChecked(True)
        self.color = QtGui.QColor(205, 0, 0)

    def green(self):
        for action in [self.actionRed, self.actionWhite, self.actionBlue]:
            action.setChecked(False)
        self.actionGreen.setChecked(True)
        self.color = QtGui.QColor(0, 205, 0)

    def blue(self):
        for action in [self.actionRed, self.actionGreen, self.actionWhite]:
            action.setChecked(False)
        self.actionBlue.setChecked(True)
        self.color = QtGui.QColor(0, 0, 205)

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
