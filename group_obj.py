import sys
import sqlite3
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QFrame, QSizePolicy
from task_obj import Task
from PyQt6.QtCore import Qt

class Group(QWidget):
    def __init__(self, name, color, parent=None):
        super().__init__(parent)
        self.color = color

        # Layout for the entire group widget
        mainLayout = QVBoxLayout(self)

        # The chevron button
        self.toggleButton = QPushButton('v', self)
        self.toggleButton.setFlat(True)  # Flat appearance
        self.toggleButton.clicked.connect(self.toggleContent)

        # A label for the group name
        self.titleLabel = QLabel(name)

        # Header contains the toggle button and the group title
        headerLayout = QVBoxLayout()
        headerLayout.addWidget(self.toggleButton)
        headerLayout.addWidget(self.titleLabel)
        headerFrame = QFrame(self)
        headerFrame.setLayout(headerLayout)
        headerFrame.setStyleSheet(f"border: 2px solid {self.color};")  # Set the border color for the header frame

        # Create a colored frame to hold tasks
        self.contentFrame = QFrame(self)

        # Content loading from the database
        self.contentLayout = QVBoxLayout(self.contentFrame)
        self.scrollArea = QScrollArea(self)

        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE task_group=?', (name,))

        for row in cursor.fetchall():
            print(row)
            ntask = Task(row[0], row[4], row[5])
            self.contentLayout.addWidget(ntask)  # Add the Task widget to the contentLayout

        conn.close()

        self.scrollArea.setWidget(self.contentFrame)
        self.scrollArea.setVisible(False)  # Initially hide the content

        mainLayout.addWidget(headerFrame)
        mainLayout.addWidget(self.scrollArea)

    def toggleContent(self):
        if self.scrollArea.isVisible():
            self.scrollArea.setVisible(False)
            self.toggleButton.setText('^')
        else:
            self.scrollArea.setVisible(True)
            self.toggleButton.setText('v')

if __name__ == '__main__':
    app = QApplication([])
    window = QMainWindow()

    central_widget = QWidget()
    main_layout = QVBoxLayout(central_widget)
    main_layout.setContentsMargins(0, 0, 0, 0)  # Left, Top, Right, Bottom
    main_layout.setSpacing(10)  # Adjust as needed
    window.setCentralWidget(central_widget)
    group = Group(name='group4', color='blue', parent=window)
    group2 = Group(name='group', color='green', parent=window)
    main_layout.addWidget(group2)
    main_layout.addWidget(group)
    window.show()
    app.exec()
