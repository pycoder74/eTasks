from PyQt6.QtCore import QTimer, Qt, QRectF, QPropertyAnimation, QEasingCurve
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
        pen.setWidth(10)
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
        # If full circle reached
        if self.span_ang >= 360:
            self.span_ang = 360  # Set the angle explicitly to 360
            self.timer.stop()  # Stop the timer
            self.onFadeOutFinished()  # Fade out the splash screen
        self.repaint()  # Force a repaint to see the updated arc

    def fadeInMainWindow(self):
        # Create an animation for the main window's opacity
        self.win_animation = QPropertyAnimation(self.win, b'windowOpacity')
        self.win_animation.setDuration(1000)  # Duration in milliseconds
        self.win_animation.setStartValue(0.0)
        self.win_animation.setEndValue(1.0)
        self.win_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.win_animation.start()

    def onFadeOutFinished(self):
        self.close()


    
if __name__ == "__main__":
    app = QApplication([])

    win = QMainWindow()
    splash = SplashScreen(win, span_ang=0)
    splash.resize(400, 400)
    splash.show()

    sys.exit(app.exec())
