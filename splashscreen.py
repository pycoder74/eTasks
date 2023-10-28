from PyQt6.QtCore import QTimer, Qt, QRectF
from PyQt6.QtGui import QPainter, QColor, QPen, QFont
from PyQt6.QtWidgets import QSplashScreen, QApplication, QMainWindow
import sys

class SplashScreen(QSplashScreen):
    def __init__(self, win : QMainWindow, span_ang : int):
        super().__init__()
        self.span_ang = span_ang
        self.start_ang = 0
        self.max_span_ang = 360
        self.win = win
        self.setWindowOpacity(0.5)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        # Timer to update arc span
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateArc)
        self.timer.start(100)  # Adjust interval for faster/slower animation

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(QColor(0, 0, 255))
        pen.setWidth(15)
        painter.setPen(pen)

        circle_size = self.width() * 0.5
        x = (self.width() - circle_size) / 2
        y = (self.height() - circle_size) / 2
        rect = QRectF(x, y, circle_size, circle_size)

        painter.drawArc(rect, int(self.start_ang * 16), int(self.span_ang * 16))

        # Drawing percentage text
        percentage_text = f"{int((self.span_ang / 360) * 100)}%"
        painter.setPen(QColor(255, 0, 0))  # Set color for text
        painter.setFont(QFont("Arial", 20))  # Setting font for text
        print(percentage_text)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, percentage_text)

    def updateLoadingProgress(self, percentage):
        self.span_ang = (percentage / 100) * self.max_span_ang
        self.repaint()

    def updateArc(self):
        self.span_ang += 10  # Increment by 10 degrees each time
        if self.span_ang >= 360:  # Full circle reached
            self.span_ang = 0  # Reset the span angle
        self.repaint()  # Force a repaint to see the updated arc

    def close_splash(self):
        self.close()
        self.win.show()

if __name__ == "__main__":
    app = QApplication([])

    win = QMainWindow()

    splash = SplashScreen(win, span_ang=10)
    splash.resize(400, 400)
    splash.show()

    # Use QTimer to call the function after 5 seconds
    QTimer.singleShot(9000, splash.close_splash)

    sys.exit(app.exec())
