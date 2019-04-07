from PyQt5 import QtCore, QtGui, QtWidgets


class VertexItem(QtWidgets.QGraphicsItem):
    def __init__(self, rect, brush1, brush2, name, font_size, parent=None):
        super(VertexItem, self).__init__()

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, True)

        self.setAcceptHoverEvents(True)
        self.brush1 = brush1
        self.brush2 = brush2
        self.parent = parent
        self.font_size = font_size

        self.rect = QtCore.QRectF(rect[0], rect[1], rect[2], rect[3])
        self.name = '\n'.join([name[i:i+(rect[0]+rect[2])//self.font_size] for i in range(0, len(name), (rect[0]+rect[2])//self.font_size)])

    def mouseMoveEvent(self, event):
        QtWidgets.QGraphicsItem.mouseMoveEvent(self, event)

    def mousePressEvent(self, event):
        self.setZValue(self.parent.scene.items()[0].zValue() + 1)
        self.setSelected(True)
        QtWidgets.QGraphicsItem.mousePressEvent(self, event)

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
