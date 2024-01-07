import sys
from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QStackedWidget
from PyQt6.QtCore import Qt

class WindowNavigator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Window Navigator')

        self.layout = QVBoxLayout(self)

        self.stacked_widget = QStackedWidget(self)
        self.layout.addWidget(self.stacked_widget)

        # Create a few sample windows
        for i in range(5):
            window = QWidget()
            window_layout = QVBoxLayout(window)
            window_layout.addWidget(QPushButton(f"Window {i + 1}"))
            self.stacked_widget.addWidget(window)

        # Add navigation buttons
        self.prev_button = QPushButton("Previous", self)
        self.prev_button.clicked.connect(self.show_previous_window)
        self.layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Next", self)
        self.next_button.clicked.connect(self.show_next_window)
        self.layout.addWidget(self.next_button)

    def show_previous_window(self):
        current_index = self.stacked_widget.currentIndex()
        if current_index > 0:
            self.stacked_widget.setCurrentIndex(current_index - 1)

    def show_next_window(self):
        current_index = self.stacked_widget.currentIndex()
        if current_index < self.stacked_widget.count() - 1:
            self.stacked_widget.setCurrentIndex(current_index + 1)

app = QApplication(sys.argv)
main_window = WindowNavigator()
main_window.show()
sys.exit(app.exec())
