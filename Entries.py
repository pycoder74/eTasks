import typing
from PyQt6 import QtCore
from PyQt6.QtWidgets import (QApplication, QListWidget, QLabel, QCheckBox, QWidget, QMainWindow, QFormLayout, QToolButton, QPushButton,
                             QMenu, QCalendarWidget, QDialog, QVBoxLayout, QLineEdit, QHBoxLayout, QRadioButton, QTimeEdit, QComboBox,
                             QColorDialog)
from PyQt6.QtCore import QDate, Qt, QEvent
from PyQt6.QtGui import QPixmap, QIcon, QColor


class Entry:
    class DateEntry(QWidget):
        def __init__(self, image_path, *args, **kwargs):
            super().__init__(*args, **kwargs)
            layout = QFormLayout()

            self.image_button = QToolButton()
            self.set_image(image_path)
            self.image_button.clicked.connect(self.open_calendar_dialog)
            layout.addRow(self.image_button)
            self.setLayout(layout)

            self.selected_date = None  # Initialize with None

        def set_image(self, image_path):
            pixmap = QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(50, 50)
            icon = QIcon(scaled_pixmap)
            self.image_button.setStyleSheet("background-color: transparent")
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
            self.selected_date = date.toString("yyyy-MM-dd")
            print("Selected Date:", self.selected_date)

        def get_value(self):
            return self.selected_date

    class InfoEntry(QWidget):
        def __init__(self, text, *args, **kwargs):
            super().__init__(*args, **kwargs)
            layout = QFormLayout()
            self.label = QLabel(text)
            self.entry = QLineEdit()
            layout.addRow(self.label, self.entry)
            self.setLayout(layout)

        def get_value(self):
            return self.entry.text()

    class PriEntry(QWidget):
        def __init__(self, text, *args, **kwargs):
            super().__init__(*args, **kwargs)
            layout = QHBoxLayout()
            self.label = QLabel(text)
            layout.addWidget(self.label)
            priChoices = ["High", "Medium", "Low"]
            self.radiobuttons = []
            for i in priChoices:
                radiobutton = QRadioButton(text=i)
                self.radiobuttons.append(radiobutton)
                layout.addWidget(radiobutton)
            self.setLayout(layout)

        def get_value(self):
            for rb in self.radiobuttons:
                if rb.isChecked():
                    return rb.text()
            return None

    class TimeEntry(QWidget):
        def __init__(self, text, *args, **kwargs):
            super().__init__(*args, **kwargs)
            layout = QFormLayout()

            self.label = QLabel(text)
            self.time_edit = QTimeEdit()

            layout.addRow(self.label, self.time_edit)
            self.setLayout(layout)

        def get_value(self):
            return self.time_edit.time().toString()

    class DropEntry(QWidget):
        def __init__(self, text, items, *args, **kwargs):
            super().__init__(*args, **kwargs)
            layout = QFormLayout()
            self.label = QLabel(text)
            self.drop = QComboBox()
            self.items = items
            self.drop.addItems([str(item) for item in self.items])

            layout.addRow(self.label, self.drop)
            self.setLayout(layout)

        def get_value(self):
            return self.drop.currentText()

    class DateTimeEntry(QWidget):
        def __init__(self, text, image_path, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.timeEntry = Entry.TimeEntry(text)
            self.dateEntry = Entry.DateEntry(image_path=image_path)

            time_layout = QVBoxLayout()
            time_layout.addWidget(self.timeEntry)
            time_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            date_layout = QVBoxLayout()
            date_layout.addWidget(self.dateEntry)
            date_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            layout = QHBoxLayout()
            layout.setSpacing(5)
            layout.addLayout(time_layout)
            layout.addLayout(date_layout)
            self.setLayout(layout)

        def get_time_value(self):
            return self.timeEntry.get_value()

        def get_date_value(self):
            return self.dateEntry.get_value()

        def get_value(self):
            return {
                'time': self.get_time_value(),
                'date': self.get_date_value()
            }

    class PasswordEntry(QWidget):
        def __init__(self, shown=False, verify=False, required=False, *args, **kwargs):
            super().__init__(*args, **kwargs)

            layout = QHBoxLayout()

            label_text = 'Verify Password:' if verify else 'Password:'
            if required:
                label_text = '* ' + label_text

            self.password_box = Entry.InfoEntry(text=label_text)
            self.password_box.entry.setEchoMode(QLineEdit.EchoMode.Password if not shown else QLineEdit.EchoMode.Normal)

            self.hide_password_box = QCheckBox('Hide')
            self.hide_password_box.setChecked(not shown)
            self.hide_password_box.toggled.connect(self.toggle_password_visibility)

            layout.addWidget(self.password_box, alignment=Qt.AlignmentFlag.AlignVCenter)
            layout.addWidget(self.hide_password_box, alignment=Qt.AlignmentFlag.AlignVCenter)

            self.setLayout(layout)

        def get_value(self):
            return self.password_box.get_value()

        def toggle_password_visibility(self, checked):
            if checked:
                self.password_box.entry.setEchoMode(QLineEdit.EchoMode.Password)
            else:
                self.password_box.entry.setEchoMode(QLineEdit.EchoMode.Normal)

    class StayOpenMenu(QMenu):
        def mouseReleaseEvent(self, event):
            action = self.activeAction()
            if action and action.isCheckable():
                action.setChecked(not action.isChecked())
            else:
                super().mouseReleaseEvent(event)

        def mousePressEvent(self, event):
            action = self.activeAction()
            if action and action.isCheckable():
                return
            super().mousePressEvent(event)




    class MultiSelectDropEntry(QWidget):
        def __init__(self, text, items, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            layout = QFormLayout()

            self.label = QLabel(text)
            self.button = QPushButton("Select Items")
            
            # Use the StayOpenMenu class here
            self.button.setMenu(Entry.StayOpenMenu(self.button))
            
            for item in items:
                action = self.button.menu().addAction(item)
                action.setCheckable(True)
                action.toggled.connect(self.updateButtonText)

            layout.addRow(self.label, self.button)
            self.setLayout(layout)
            
            # Initially set the button text
            self.updateButtonText()

        def updateButtonText(self):
            checked_items = [action.text() for action in self.button.menu().actions() if action.isChecked()]
            if checked_items:
                self.button.setText(", ".join(checked_items))
            else:
                self.button.setText("Select Items")

        def get_value(self):
            return [action.text() for action in self.button.menu().actions() if action.isChecked()]
    class ColorPicker(QWidget):
        def __init__(self, parent = None):
            super().__init__()

            self.initUI()

        def initUI(self):
            layout = QVBoxLayout()

            self.color_button = QPushButton("Pick a Color", self)
            self.color_button.clicked.connect(self.showColorDialog)

            self.color_label = QLabel("Selected Color: None", self)

            layout.addWidget(self.color_button)
            layout.addWidget(self.color_label)

            self.setLayout(layout)

        def showColorDialog(self):
            color = QColorDialog.getColor()
            if color.isValid():
                self.color_label.setText(f"Selected Color: {color.name()}")
    class ColorEntry(QWidget):
            def __init__(self, text, *args, **kwargs):
                super().__init__(*args, **kwargs)

                layout = QFormLayout()
                self.label = QLabel(text)
                self.color_picker = Entry.ColorPicker()  # Create an instance of the ColorPicker widget

                layout.addRow(self.label, self.color_picker)
                self.setLayout(layout)

            def get_value(self):
                return self.color_picker.color_label.text()

if __name__ == '__main__':
    app = QApplication([])

    window = QMainWindow()
    window.setWindowTitle("Color Picker Integration")
    window.setGeometry(100, 100, 400, 200)

    entry = Entry.ColorEntry("Select Color:")

    window.setCentralWidget(entry)
    window.show()

    app.exec()
