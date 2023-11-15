from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QScrollArea, QFrame, QLabel, QSizePolicy
from PyQt6.QtCore import Qt

class Group(QWidget):
    groups_loaded = []

    def __init__(self, name, color, parent_layout):
        super(Group, self).__init__()
        if name not in Group.groups_loaded:
            self.name = name  # Store the name as an instance variable
            self.color = color
            self.parent_layout = parent_layout

            # The chevron button
            self.toggleButton = QPushButton('v', self)
            self.toggleButton.setFlat(True)  # Flat appearance
            self.toggleButton.clicked.connect(self.toggleContent)

            # A label for the group name
            self.titleLabel = QLabel(name, self)

            # Header contains the toggle button and the group title
            headerFrame = QFrame(self)
            headerLayout = QVBoxLayout(headerFrame)
            headerLayout.addWidget(self.toggleButton)
            headerLayout.addWidget(self.titleLabel)

            # Create a colored frame to hold tasks
            self.contentFrame = QFrame(self)
            self.content_layout = QVBoxLayout(self.contentFrame)  # Add this line to define content_layout

            self.scrollArea = QScrollArea(self)
            self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.scrollArea.setWidgetResizable(True)
            self.scrollArea.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

            self.scrollArea.setWidget(self.contentFrame)
            self.scrollArea.setVisible(False)  # Initially hide the content

            self.layout = QVBoxLayout(self)
            self.layout.addWidget(headerFrame)
            self.layout.addWidget(self.scrollArea)

            self.parent_layout.addWidget(self)
            Group.groups_loaded.append(name)

    def toggleContent(self):
        if self.scrollArea.isVisible():
            self.scrollArea.setVisible(False)
            self.toggleButton.setText('^')
        else:
            self.scrollArea.setVisible(True)
            self.toggleButton.setText('v')

    def add_task(self, task):
        # Add the task to the content_layout of the group
        self.content_layout.addWidget(task)
