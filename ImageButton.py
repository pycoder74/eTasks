from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QSize

class ImageButton(QPushButton):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)

        print(f"Loading image from: {image_path}")  # Debugging line
        pixmap = QPixmap(image_path)
        pixmap_resized = pixmap.scaled(50, 50, Qt.AspectRatioMode.IgnoreAspectRatio)

        self.setIcon(QIcon(pixmap_resized))
        self.setStyleSheet("background-color: transparent")
        self.setIconSize(QSize(50, 50))  # Set the button icon size to a fixed size
        self.setFixedSize(QSize(50, 50))  # Set the button size to a fixed size

        print(f"Button size: {self.size()}")  # Debugging line

