from PyQt6.QtCore import QTimer, Qt, QRectF
from PyQt6.QtGui import QPainter, QColor, QPen
from PyQt6.QtWidgets import QSplashScreen, QApplication, QMainWindow
import sys

class SplashScreen(QSplashScreen):
    def __init__(self, win):
        super().__init__()
        self.start_ang = 0
        self.span_ang = 0
        self.win = win
        self.setWindowOpacity(0.5)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        # Timer to update arc span
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateArc)
        self.timer.start(50)  # Adjust interval for faster/slower animation

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(QColor(0, 0, 255))
        pen.setWidth(15)
        painter.setPen(pen)

        circle_size = self.width() * 0.5
        x = (self.width() - circle_size) / 2
        y = (self.height() - circle_size) / 2
        rect = QRectF(x, y, circle_size, circle_size)

        painter.drawArc(rect, self.start_ang * 16, self.span_ang * 16)

    def updateArc(self):
        self.span_ang += 8  # Increment span angle
        if self.span_ang >= 360:  # Full circle reached
            self.span_ang = 5 # Stop the timer once the arc completes the circle
        self.repaint()  # Force a repaint to see the updated arc
    def close_splash(self):
        self.close()
        self.win.show()

if __name__ == "__main__":
    app = QApplication([])

    win = QMainWindow()

    splash = SplashScreen(win)
    splash.resize(400, 400)
    splash.show()

    # Use QTimer to call the function after 5 seconds
    QTimer.singleShot(5000, splash.close_splash)

    sys.exit(app.exec())
