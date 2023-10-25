from PyQt6.QtCore import QTimer, Qt, QPoint, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QConicalGradient
from PyQt6.QtWidgets import QSplashScreen, QApplication, QMainWindow
import time
import math
import sys
class AnimatedSplashScreen(QSplashScreen):
    finished = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.angle = 0  # This will track the current rotation angle of the circle

        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        self.timer = QTimer(self)  # Initialize the QTimer
        self.timer.timeout.connect(self.rotate)  # Connect the timer's timeout signal to rotate method
        self.timer.start(100)
    def rotate(self):
        self.angle += 10  # Increase the angle by 2 degrees
        self.angle %= 360  # Keep the angle value between 0 and 360
        print(f"Angle: {self.angle}")
        self.update()  # Trigger paintEvent
    def paintEvent(self, event):
        print("paintEvent called")
        painter = QPainter(self)
        painter.setBrush(QColor(0, 0, 0))  # Black color for the dots
        painter.setPen(Qt.PenStyle.NoPen)  # No outline

        # Radius of the circle path along which the dots rotate
        radius = min(self.width(), self.height()) / 3

        # Draw 6 dots around a circle
        for i in range(6):
            # Calculate the position for each dot WITHOUT adding self.angle
            theta = i * 60  # 60 degrees separation between dots
            x = self.width() / 2 + radius * math.cos(math.radians(theta + self.angle))
            y = self.height() / 2 - radius * math.sin(math.radians(theta + self.angle))

            # Draw the dot
            painter.drawEllipse(QPoint(int(x), int(y)), 8, 8)
    def closeSplash(self):
        self.timer.stop()
        self.finished.emit()  # Emit the finished signal instead of closing directly
        self.close()
    
if __name__ == "__main__":

    app = QApplication([])

    splash = AnimatedSplashScreen()
    splash.resize(400, 400)
    splash.show()
    app.processEvents()

    window = QMainWindow()
    window.show()

    sys.exit(app.exec())




