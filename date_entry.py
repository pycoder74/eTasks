from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QFormLayout, QToolButton, QCalendarWidget, QDialog, QVBoxLayout
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QPixmap, QIcon

class DateEntry(QWidget):
    def __init__(self, image_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QFormLayout()

        self.image_button = QToolButton()
        self.set_image(image_path)

        self.image_button.clicked.connect(self.open_calendar_dialog)

        layout.addRow(self.image_button)
        self.setLayout(layout)

    def set_image(self, image_path):
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)

        icon = QIcon(scaled_pixmap)  # Create QIcon from QPixmap
        self.image_button.setIcon(icon)
        self.image_button.setIconSize(scaled_pixmap.size())
        self.image_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)

    def open_calendar_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Date")
        dialog.setModal(True)

        calendar = QCalendarWidget()
        calendar.setGridVisible(True)
        calendar.clicked.connect(self.on_date_selected)

        layout = QVBoxLayout()
        layout.addWidget(calendar)
        dialog.setLayout(layout)

        dialog.exec()

    def on_date_selected(self, date):
        selected_date = date.toString("yyyy-MM-dd")
        print("Selected Date:", selected_date)

if __name__ == '__main__':
    app = QApplication([])
    window = QMainWindow()

    date_entry = DateEntry("C:/Users/ellio_6/Desktop/Coding/etasksV2-main/calendar_icon.jpg")
    window.setCentralWidget(date_entry)

    window.show()
    app.exec()
