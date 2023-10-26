from PyQt6.QtCore import QTimer, Qt, QRectF
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QSplashScreen, QApplication, QMainWindow
import sys

class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__()
        self.message = "Loading..."
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowOpacity(0.5)
    def closeSplash(self):
        self.message = 'App ready'
        self.repaint()  # Trigger a repaint so the new message is shown
        self.close()
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QColor(0, 0, 0))
        rect = QRectF(0, 0, self.width(), self.height())
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.message)

if __name__ == "__main__":
    app = QApplication([])

    splash = SplashScreen()
    splash.resize(400, 400)
    splash.show()

    win = QMainWindow()

    def close_splash_screen():
        splash.closeSplash()
        win.show()

    # Use QTimer to call the function after 5 seconds
    QTimer.singleShot(5000, close_splash_screen)

    sys.exit(app.exec())
