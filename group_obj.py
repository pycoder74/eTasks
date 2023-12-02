from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QScrollArea, QFrame, QLabel, QSizePolicy, QMainWindow, QApplication
from PyQt6.QtCore import Qt
from task_obj import Task  # Assuming task_obj.py contains the Task class

class Group(QWidget):
    groups_loaded = []

    def __init__(self, name, color, parent_layout):
        super(Group, self).__init__()

        self.name = name
        self.color = color
        self.parent_layout = parent_layout


        self.toggleButton = QPushButton('^', self)
        self.toggleButton.setFlat(True)
        self.toggleButton.clicked.connect(self.toggleContent)

        self.contentFrame = QFrame(self)
        self.contentFrame.setObjectName('contentFrame')
        style_sheet = f"""
            #{'contentFrame'} {{
                border: 5px solid {self.color};
            }}
            
        """

        self.setStyleSheet(style_sheet)
        self.content_layout = QVBoxLayout(self.contentFrame)

        self.titleLabel = QLabel(name, self)
        self.content_layout.addWidget(self.titleLabel)

        headerFrame = QFrame(self)
        headerLayout = QVBoxLayout(headerFrame)
        headerLayout.addWidget(self.toggleButton)
        headerLayout.addWidget(self.titleLabel)

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.scrollArea.setWidget(self.contentFrame)
        self.scrollArea.setVisible(False)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(headerFrame)
        self.layout.addWidget(self.scrollArea)

        self.parent_layout.addWidget(self)
        Group.groups_loaded.append(name)

        self.toggle_state = False

    def toggleContent(self):
        self.scrollArea.setVisible(not self.scrollArea.isVisible())
        self.toggle_state = not self.toggle_state
        self.toggleButton.setText('v' if self.toggle_state else '^')

    def add_task_to_group(self, task):
        self.content_layout.addWidget(task)

    def clear_content_layout(self):
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def add_task(self, task_name, start_date, end_date, complete):
        task_widget = Task(task_name, start_date, end_date, complete)
        self.add_task_to_group(task_widget)

if __name__ == '__main__':
    app = QApplication([])
    win = QMainWindow()

    central_widget = QWidget()
    layout = QVBoxLayout(central_widget)
    win.setCentralWidget(central_widget)

    group = Group(name='Hello', color='#FFFFFF', parent_layout=layout)

    win.show()
    app.exec()
