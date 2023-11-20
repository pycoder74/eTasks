import sys
from PyQt6.QtWidgets import QMessageBox, QMainWindow, QApplication, QSizePolicy, QFrame, QWidget, QVBoxLayout, QLabel, QCheckBox, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt, QTimer
from etasksMessageBox import MessageBox
import sqlite3
from ImageButton import ImageButton
class Task(QWidget):
    def __init__(self, taskname, startDate, endDate, parent=None):
        super(Task, self).__init__(parent)

        # Store the task name
        self.taskname = taskname
        self.startDate = startDate
        self.endDate = endDate
        self.parent = parent

        # Main Layout
        mainLayout = QVBoxLayout(self)
        mainLayout.setSpacing(5)
        mainLayout.setContentsMargins(0, 0, 0, 0)

        mainframe = QFrame(self)
        mainframe.setObjectName("mainframe")
        mainframe.setStyleSheet(
    """ #mainframe {
        border: 2px solid #000000;
        }"""
)

        mainframe.setFrameShape(QFrame.Shape.Box)
        mainLayout.addWidget(mainframe, alignment=Qt.AlignmentFlag.AlignTop)
        mainframeLayout = QHBoxLayout(mainframe)

        # Check Box
        self.checkBox = QCheckBox(self)
        mainframeLayout.addWidget(self.checkBox)
        self.checkBox.stateChanged.connect(self.checkbox_state_changed)  # Connect to the slot

        self.bin_icon = QPushButton(text = 'Delete')
        self.bin_icon.clicked.connect(self.delete)
        mainframeLayout.addWidget(self.bin_icon)
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
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute(""" UPDATE tasks SET complete = TRUE WHERE taskname = ?""",(self.taskname,))
            conn.commit()
            conn.close()
            completion = MessageBox(type_= QMessageBox.Icon.Information, text = "Task Complete")
            completion.exec()
    def delete(self):
        msgBox = MessageBox(QMessageBox.Icon.Warning, "Are you sure you want to delete this task?")
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

        result = msgBox.exec()

        if result == QMessageBox.StandardButton.Ok:
            # Close the widget before deleting
            self.close()

            doublecheck = MessageBox(QMessageBox.Icon.Warning, 'Task Deleted')
            undo_btn = QPushButton("Undo")
            ok_btn = QPushButton("OK")
            doublecheck.addButton(undo_btn, QMessageBox.ButtonRole.RejectRole)
            doublecheck.addButton(ok_btn, QMessageBox.ButtonRole.AcceptRole)
            result = doublecheck.exec()

            if result == QMessageBox.ButtonRole.AcceptRole:
                with sqlite3.connect('users.db') as conn:
                    c = conn.cursor()
                    c.execute(""" DELETE FROM tasks WHERE taskname = ?""", (self.taskname,))
                    conn.commit()
            elif result == QMessageBox.ButtonRole.RejectRole:
                # If the user cancels, show the widget again
                self.show()
                cancelled = MessageBox(QMessageBox.Icon.Information, 'Cancelled')
                cancelled.exec()



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
