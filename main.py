from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenuBar, QMenu, QFileDialog
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, QPoint
import sys
from random import choice


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
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.vertex = True
        self.point = QPoint
        self.color = Qt.black
        self.selected = None

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
                #self.vertexes.append(Vertex(event.pos()[0], event.pos()[1], self.color))
                #self.selected = self.vertexes[-1]
                print(event.pos())
                # нарисовать вершину
                '''painter = QPainter(self.image)
                painter.setPen(QPen(self.color, self.vertrad, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                painter.drawLine(self.point, event.pos())
                self.point = event.pos()
                self.update()

    def clickOnVertex(self, event):
        if self.vertex:
            for vert in self.vertexes:
                if self.x <= event.pos()[0] <= vert.x + self.vertrad and self.y <= event.pos()[1] <= vert.y + self.vertrad:
                    self.selected = vert'''

    def buttonPushEvent(self, event):
        if self.selected is not None:
            if event.key() == Qt.Key_I:
                if type(self.selected) is Vertex:
                    #выводить окошко
                    pass
            elif event.button() == Qt.Key_Delete:
                if type(self.selected) is Vertex:
                    # удалять абсолютно все упоминания объекта
                    self.vertexes.remove(self.selected)
                    self.selected = None

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


class Graf:
    def __init__(self):
        self.vertexes = []
        self.vertexRad = 5

    def diameter(self):
        borderVert = []
        for vert in self.vertexes:
            if len(vert.edges):
                borderVert.append(vert)
        for vert in borderVert:
            states = self.vertexes.copy()
            while vert not in borderVert:




class Vertex:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.name = ""
        self.color = color
        self.edges = []


class Edge:
    def __init__(self, color, vertex1, vertex2):
        self.color = color
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.weight = int()
        self.side = bool()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = Window()
    myapp.show()
    sys.exit(app.exec_())
