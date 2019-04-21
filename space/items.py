from PyQt5 import QtCore, QtGui, QtWidgets
from math import sin, cos


class VertexItem(QtWidgets.QGraphicsItem):
    def __init__(self, rect, brush1, brush2, name, font_size, parent=None):
        super(VertexItem, self).__init__()
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.setAcceptHoverEvents(True)
        self.brush1 = brush1
        self.brush2 = brush2
        self.parent = parent
        self.font_size = font_size
        self.rect = QtCore.QRectF(rect[0], rect[1], rect[2], rect[3])
        self.name = '\n'.join([name[i:i + (rect[0] + rect[2]) // self.font_size] for i in
                               range(0, len(name), (rect[0] + rect[2]) // self.font_size)])

    def mouseMoveEvent(self, event):
        QtWidgets.QGraphicsItem.mouseMoveEvent(self, event)

    def mousePressEvent(self, event):
        QtWidgets.QGraphicsItem.mousePressEvent(self, event)
        self.setZValue(self.parent.scene.items()[0].zValue() + 1)
        self.parent.scene.clearSelection()
        self.setSelected(True)
        self.parent.addEdgeItem()

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget=None):
        if self.isSelected():
            painter.setBrush(self.brush2)
        else:
            painter.setBrush(self.brush1)
        painter.drawEllipse(self.rect)
        painter.setPen(QtGui.QColor(0, 0, 0))
        painter.setFont(QtGui.QFont('Decorative', self.font_size))
        painter.drawText(self.rect, QtCore.Qt.AlignCenter, self.name)


class EdgeItem(QtWidgets.QGraphicsLineItem):
    def __init__(self, vert1, vert2, pen1, pen2, parent=None, loop=False):
        super(EdgeItem, self).__init__()
        self.vert1 = vert1
        self.vert2 = vert2
        self.loop = loop
        self.pen1 = pen1
        self.pen2 = pen2
        self.weight = False
        self.oriented = True
        self.setAcceptHoverEvents(True)
        self.setFlag(QtWidgets.QGraphicsLineItem.ItemIsSelectable, True)
        self.parent = parent

    def mousePressEvent(self, event):
        QtWidgets.QGraphicsLineItem.mousePressEvent(self, event)
        self.setZValue(self.parent.scene.items()[0].zValue() + 1)
        self.parent.scene.clearSelection()
        self.setSelected(True)

    def boundingRect(self):
        rect1 = self.vert1.boundingRect()
        rect2 = self.vert2.boundingRect()
        center1 = (rect1.x() + rect1.width() // 2 + self.vert1.x(), rect1.y() + rect1.height() // 2 + self.vert1.y())
        center2 = (rect2.x() + rect2.width() // 2 + self.vert2.x(), rect2.y() + rect2.height() // 2 + self.vert2.y())
        if self.loop:
            return QtCore.QRectF(rect1.x() + self.vert1.x() - 10, rect1.y() + self.vert1.y() - 10,
                                 rect1.x() + rect1.width() // 2 + self.vert1.x(), rect1.y() + self.vert1.y() + rect1.height() + 10)
        else:
            return QtCore.QRectF(center1[0], center1[1] - self.pen1.width() // 2,  # типичная ошибка с длиной и шириной
                                 center2[0] - center1[0], self.pen1.width())

    def paint(self, painter, option, widget=None):
        if self.isSelected():
            print('selected')
            painter.setPen(self.pen2)
        else:
            painter.setPen(self.pen1)
        rect1 = self.vert1.boundingRect()
        rect2 = self.vert2.boundingRect()
        center1 = (rect1.x() + rect1.width() // 2 + self.vert1.x(), rect1.y() + rect1.height() // 2 + self.vert1.y())
        center2 = (rect2.x() + rect2.width() // 2 + self.vert2.x(), rect2.y() + rect2.height() // 2 + self.vert2.y())
        if center1 == center2:
            if self.loop:
                painter.pen().setWidth(3)
                painter.drawArc(rect1.x() + self.vert1.x() - 10, rect1.y() + self.vert1.y() - 10,
                                rect1.width() + 20, rect1.height() + 20, 90 * 16, 180 * 16)
                painter.drawLine(center1[0], center1[1], center1[0],
                                 center1[1] - rect1.height() // 2 - 10)
                painter.drawLine(center1[0], center1[1], center1[0],
                                 center1[1] + rect1.height() // 2 + 10)
            else:
                return
        else:
            if not self.oriented:
                painter.drawLine(center1[0], center1[1], center2[0], center2[1])
            else:
                line = QtCore.QLineF(center1[0], center1[1], center2[0], center2[1])
                painter.drawLine(line)
                m = (rect1.width() / 2) * (center1[0] - center2[0]) // (
                            (center1[1] - center2[1]) ** 2 + (center1[0] - center2[0]) ** 2) ** (1 / 2) + center2[0]
                n = ((rect1.width() // 2) ** 2 - (m - center2[0]) ** 2) ** (1 / 2) + center2[1]
                painter.drawLine(m - 30 * sin(line.angle() + 30), n - 30 * cos(line.angle() + 30), m, n)
                painter.drawLine(m + 30 * sin(line.angle() + 30), n + 30 * cos(line.angle() + 30), m, n)

    def makeNotOriented(self):
        self.oriented = False

    def makeWeighted(self, weight):
        self.weight = weight
