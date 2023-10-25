import sys
import sqlite3
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QFrame, QHBoxLayout, QSizePolicy
from task_obj import Task  
from PyQt6.QtCore import Qt

QWIDGETSIZE_MAX = 2**31 - 1

class Group(QWidget):
    def __init__(self, name, parent=None):
        super().__init__(parent)
        
        # Layout for the entire group widget
        mainLayout = QVBoxLayout(self)

        # The chevron button
        self.toggleButton = QPushButton('v', self)
        self.toggleButton.setFlat(True)  # Flat appearance
        self.toggleButton.clicked.connect(self.toggleContent)

        # A label for the group name
        self.titleLabel = QLabel(name)
        
        # Header contains the toggle button and the group title
        headerLayout = QHBoxLayout()
        headerLayout.addWidget(self.toggleButton)
        headerLayout.addWidget(self.titleLabel)
        mainLayout.addLayout(headerLayout)

        # Content loading from the database
        self.scrollArea = QScrollArea(self)
        self.contentFrame = QFrame(self.scrollArea)
        self.contentLayout = QVBoxLayout(self.contentFrame)

        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE task_group=?', (name,))
        
        for row in cursor.fetchall():
            taskname, user, priority, topic, task_group, sD, eD, sT, eT = row
            loaded_task = Task(taskname, sD, eD)
            self.contentLayout.addWidget(loaded_task)

        conn.close()
        
        self.scrollArea.setWidget(self.contentFrame)
        self.scrollArea.setWidgetResizable(True)
        mainLayout.addWidget(self.scrollArea)
        self.scrollArea.setVisible(False)  # Initially hide the content

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
    group = Group(name='group4', parent=window)
    group2 = Group(name='group', parent=window)
    main_layout.addWidget(group2)
    main_layout.addWidget(group)
    window.show()
    app.exec()
