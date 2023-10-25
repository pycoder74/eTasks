import sys
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import Qt

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.label = QtWidgets.QLabel(self)
        canvas = QtGui.QPixmap(400, 300)
        canvas.fill(Qt.GlobalColor.white)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)

        # Create an inner label for text
        self.inner_label = QtWidgets.QLabel(self.label)
        self.inner_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.inner_label.setGeometry(10, 10, 100, 100)  # Same geometry as the circle
        self.inner_label.setText("EK")  # Set the text you want

        # Adjust the font size
        font = self.inner_label.font()
        font.setPointSize(50)  # Start with a large font size
        padding = 10  # adjust padding as needed
        target_height = 100 - 2 * padding  # circle height minus top and bottom padding
        
        while True:
            # Get the height of the text with current font size
            metrics = QtGui.QFontMetrics(font)
            text_height = metrics.boundingRect(self.inner_label.text()).height()
            if text_height > target_height:
                font.setPointSize(font.pointSize() - 1)
            else:
                break

        self.inner_label.setFont(font)

        self.draw_something()

    def draw_something(self):
        canvas = self.label.pixmap()
        painter = QtGui.QPainter(canvas)
        pen = QtGui.QPen()
        pen.setWidth(3)
        pen.setColor(QtGui.QColor(0, 0, 0))  # r, g, b for the border
        painter.setPen(pen)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        # Fill the circle with blue
        painter.setBrush(QtGui.QColor(0, 0, 255))
        painter.drawEllipse(10, 10, 100, 100)

        painter.end()
        self.label.setPixmap(canvas)

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
