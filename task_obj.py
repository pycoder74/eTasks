import sys
from PyQt6.QtWidgets import QMessageBox, QMainWindow, QApplication, QSizePolicy, QFrame, QWidget, QVBoxLayout, QLabel, QCheckBox, QHBoxLayout
from PyQt6.QtCore import Qt, QTimer
from etasksMessageBox import MessageBox

class Task(QWidget):
    def __init__(self, taskname, startDate, endDate, parent=None):
        super(Task, self).__init__(parent)

        # Store the task name
        self.taskname = taskname
        self.startDate = startDate
        self.endDate = endDate

        # Main Layout
        mainLayout = QVBoxLayout(self)
        mainLayout.setSpacing(5)
        mainLayout.setContentsMargins(0, 0, 0, 0)

        mainframe = QFrame(self)
        mainframe.setFrameShape(QFrame.Shape.Box)
        mainLayout.addWidget(mainframe, alignment=Qt.AlignmentFlag.AlignTop)
        mainframeLayout = QHBoxLayout(mainframe)

        # Check Box
        self.checkBox = QCheckBox(self)
        mainframeLayout.addWidget(self.checkBox)
        self.checkBox.stateChanged.connect(self.checkbox_state_changed)  # Connect to the slot

        # Task Name Frame & Label
        tasknameFrame = QFrame(self)
        tasknameFrame.setFrameShape(QFrame.Shape.Box)
        tasknameFrameLayout = QVBoxLayout(tasknameFrame)
        tasknameLabel = QLabel(self.taskname, tasknameFrame)
        tasknameFrameLayout.addWidget(tasknameLabel)
        mainframeLayout.addWidget(tasknameFrame)

        # Start Date Frame & Label
        sDateFrame = QFrame(self)
        sDateFrame.setFixedSize(320, 40)
        sDateFrame.setFrameShape(QFrame.Shape.Box)
        sDateLayout = QHBoxLayout(sDateFrame)
        if startDate is None:
            sDateLabel = QLabel(f'Starts: No Start Date')
        else:
            sDateLabel = QLabel(f'Starts: {startDate}')
        sDateLayout.addWidget(sDateLabel)
        mainframeLayout.addWidget(sDateFrame)

        # End Date Frame & Label
        dDateFrame = QFrame(self)
        dDateFrame.setFixedSize(320, 40)
        dDateFrame.setFrameShape(QFrame.Shape.Box)
        dDateLayout = QHBoxLayout(dDateFrame)
        if endDate is None:
            endDateLabel = QLabel('Starts: No End Date')
        else:
            endDateLabel = QLabel(f"Ends: {endDate}")
        dDateLayout.addWidget(endDateLabel)
        mainframeLayout.addWidget(dDateFrame)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
    def complete(self):
        if not hasattr(self, 'completed') or not self.completed:
            self.hide()
            self.completed = True  # Use a different variable name
            completion = MessageBox(QMessageBox.Icon.Information, "Task Complete")
            completion.exec()

    def checkbox_state_changed(self, state):
        if state == Qt.CheckState.Unchecked:
            print(f"Checkbox for task '{self.taskname}' is unchecked")
        else:
            print(f"Checkbox for task '{self.taskname}' is checked")
            timer = QTimer(self)
            timer.timeout.connect(self.complete)
            timer.start(500)
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    central_widget = QWidget(mainWindow)
    layout = QHBoxLayout(central_widget)
    mainWindow.setCentralWidget(central_widget)
    task = Task('task', 'sdate', 'edate', mainWindow)
    layout.addWidget(task)
    mainWindow.showMaximized()
    sys.exit(app.exec())
