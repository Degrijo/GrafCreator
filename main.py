from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenuBar, QMenu, QFileDialog, QGraphicsScene, \
    QGraphicsView, QMessageBox
from PyQt5.QtGui import QIcon, QPainter, QPen, QBrush, QFont
from PyQt5.QtCore import Qt, QPoint, QRectF
import sys
from logic import *


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        top = 400
        left = 400
        width = 800
        height = 600

        self.setWindowIcon(QIcon("icons/icon.png"))
        self.setWindowTitle("GrafCreator")
        self.setGeometry(top, left, width, height)
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(QRectF(0, 0, width, height))
        self.graphics_view = QGraphicsView()
        self.graphics_view.setScene(self.scene)
        self.setCentralWidget(self.graphics_view)
        self.vertex = True
        self.color = Qt.black
        self.selected = None
        self.graf = Graf(20)

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        colorMenu = mainMenu.addMenu("Color")
        vertexMenu = mainMenu.addMenu("Vertex")
        edgeMenu = mainMenu.addMenu("Edge")
        algoMenu = mainMenu.addMenu("Algorithms")

        saveAction = QAction(QIcon("icons/save.png"), "Save", self)
        saveAction.setShortcut("Ctrl+S")
        saveAction.triggered.connect(self.save)
        fileMenu.addAction(saveAction)
        clearAction = QAction(QIcon("icons/clear.png"), "Clear", self)
        clearAction.setShortcut("Ctrl+O")
        fileMenu.addAction(clearAction)
        clearAction.triggered.connect(self.clear)
        blackAction = QAction(QIcon("icons/black.png"), "Black", self)
        blackAction.setShortcut("Ctrl+1")
        colorMenu.addAction(blackAction)
        blackAction.triggered.connect(self.black)
        redAction = QAction(QIcon("icons/red.png"), "Red", self)
        redAction.setShortcut("Ctrl+2")
        colorMenu.addAction(redAction)
        redAction.triggered.connect(self.red)
        greenAction = QAction(QIcon("icons/green.png"), "Green", self)
        greenAction.setShortcut("Ctrl+3")
        colorMenu.addAction(greenAction)
        greenAction.triggered.connect(self.green)
        blueAction = QAction(QIcon("icons/blue.png"), "Blue", self)
        blueAction.setShortcut("Ctrl+4")
        colorMenu.addAction(blueAction)
        blueAction.triggered.connect(self.blue)
        diamAction = QAction(QIcon("icons/diameter.png"), "Diameter", self)
        diamAction.setShortcut("Ctrl+5")
        algoMenu.addAction(diamAction)
        #diamAction.triggered.connect(self.show_diameter())
        radAction = QAction(QIcon("icons/radius.png"), "Radius", self)
        diamAction.setShortcut("Ctrl+6")
        algoMenu.addAction(radAction)
        #radAction.triggered.connect(self.show_radius())

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            print('click-click')
            if self.vertex:
                self.graf.add_vertex(event.pos().x(), event.pos().y()-self.graf.node_rad//2)
                self.selected = self.graf.vertexes[-1]
                self.scene.addEllipse(event.pos().x(), event.pos().y()-self.graf.node_rad//2, self.graf.node_rad, self.graf.node_rad, QPen(self.color, 10.0))
                print('vertex added')

    def mousePressEvent(self, event):  # найти события для кнопок
        '''if event.button() == Qt.Key_I:
            if self.selected is not None:
                if not self.graf.get_vertex(event.pos().x(), event.pos().y()):
                    # окошко с текст филдом
                    self.graf.get_vertex(event.pos().x(), event.pos().y()).set_name('123')
                    print("renaming")'''
        if event.button() == Qt.LeftButton:
            print('click')
            if self.vertex:
                if self.graf.get_vertex(event.pos().x(), event.pos().y()):
                    self.selected = self.graf.get_vertex(event.pos().x(), event.pos().y())
                    print('selections')
            else:
                if self.selected is None:
                    if self.graf.get_vertex(event.pos().x(), event.pos().y()):
                        self.selected = self.graf.get_vertex(event.pos().x(), event.pos().y())
                        print('selection')
                else:
                    sec_vert = self.graf.get_vertex(event.pos().x(), event.pos().y())
                    if sec_vert:
                        if sec_vert != self.selected:
                            if not self.graf.get_edge(self.selected, sec_vert):
                                arc_coor = [self.selected.x, self.selected.y, sec_vert.x, sec_vert.y]
                                pen = QPen(self.color, 10.0)
                                self.graf.add_edge(self.selected, sec_vert, True)
                                '''if self.selected.x - sec_vert.x > pen.width():  # pyqt добавление изменяемых объектов на сцену/qwidget
                                    arc_coor[0] -= pen.width()
                                    arc_coor[2] += pen.width()
                                else:
                                    arc_coor[0] += pen.width()
                                    arc_coor[2] -= pen.width()
                                if self.selected.y - sec_vert.y > pen.width():
                                    arc_coor[1] -= pen.width()
                                    arc_coor[3] += pen.width()
                                else:
                                    arc_coor[1] += pen.width()
                                    arc_coor[3] -= pen.width()'''
                                self.scene.addLine(arc_coor[0], arc_coor[1], arc_coor[2], arc_coor[3], pen)
                                print('edge ' + self.selected.name + ' - ' + sec_vert.name + ' added')
                                self.selected = None
        elif event.button() == Qt.RightButton:
            self.vertex = not self.vertex
            self.selected = None
            print('changing')

    def show_diameter(self):
        font = QFont()
        font.setPointSize(12)
        self.scene.addText(str(self.graf.radius_diameter()[0]), font, QRectF(0, 0, 100, 25))

    def show_radius(self):
        font = QFont()
        font.setPointSize(12)
        self.scene.addText(str(self.graf.radius_diameter()[1]), font, QRectF(0, 25, 100, 50))

    def save(self):
        pass

    def clear(self):
        self.scene.clear()

    def black(self):
        self.color = Qt.black

    def red(self):
        self.color = Qt.red

    def green(self):
        self.color = Qt.green

    def blue(self):
        self.color = Qt.blue


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = Window()
    myapp.show()
    sys.exit(app.exec_())
