from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QScrollArea, QFrame, QLabel, QSizePolicy, QMainWindow, QApplication
from PyQt6.QtCore import Qt
from task_obj import Task

class Group(QWidget):
    groups_loaded = []

    def __init__(self, name, color, parent_layout):
        super(Group, self).__init__()

        self.name = name  # Store the name as an instance variable
        self.color = color
        self.parent_layout = parent_layout

        # The chevron button
        self.toggleButton = QPushButton('v', self)
        self.toggleButton.setFlat(True)  # Flat appearance
        self.toggleButton.clicked.connect(self.toggleContent)

       # Create a colored frame to hold tasks
        self.contentFrame = QFrame(self)
        self.content_layout = QVBoxLayout(self.contentFrame)  # Add this line to define content_layout

        # A label for the group name
        self.titleLabel = QLabel(name, self)
        self.content_layout.addWidget(self.titleLabel)


        # Header contains the toggle button and the group title
        headerFrame = QFrame(self)
        headerLayout = QVBoxLayout(headerFrame)
        headerLayout.addWidget(self.toggleButton)
        headerLayout.addWidget(self.titleLabel)

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

    def add_task_to_group(self, task):
        self.content_layout.addWidget(task)


    def clear_content_layout(self):
        # Clear the content layout to avoid potential issues
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def add_task(self, task_name, start_date, end_date):
        task_widget = Task(task_name, start_date, end_date)
        self.add_task_to_group(task_widget)
if __name__ == '__main__':
    app = QApplication([])
    win = QMainWindow()

    # Create a central widget for the main window
    central_widget = QWidget()
    layout = QVBoxLayout(central_widget)
    win.setCentralWidget(central_widget)

    # Create an instance of the Group class and add it to the layout
    group = Group(name='Hello', color='#FFFFFF', parent_layout=layout)
    
    win.show()
    app.exec()
