from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenuBar, QMenu, QFileDialog, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QIcon, QPainter, QPen, QBrush
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
        self.node_rad = 20
        self.selected = None
        self.graf = Graf()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        colorMenu = mainMenu.addMenu("Color")
        vertexMenu = mainMenu.addMenu("Vertex")
        edgeMenu = mainMenu.addMenu("Edge")

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

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.vertex:
                self.graf.add_vertex(event.pos().x(), event.pos().y())
                self.selected = self.graf.vertexes[-1]
                self.scene.addEllipse(event.pos().x(), event.pos().y()-self.node_rad//2, self.node_rad, self.node_rad)
                print(event.pos().x(), event.pos().y())
                print(self.scene.sceneRect())

    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);; ALL Files(*.*)")
        if filePath == "":
            return
        self.image.save(filePath)

    def clear(self):
        self.image.fill(Qt.White)
        self.update()

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
