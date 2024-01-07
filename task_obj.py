import sys
from PyQt6.QtWidgets import (
    QMessageBox, QMainWindow, QApplication, QSizePolicy,
    QFrame, QWidget, QVBoxLayout, QLabel, QCheckBox,
    QHBoxLayout, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSlot, pyqtSignal
import sqlite3
from etasksMessageBox import MessageBox

class Task(QWidget):
    taskCompleted = pyqtSignal()
    taskIncompleted = pyqtSignal()

    def __init__(self, taskname, startDate, endDate, is_complete: bool, parent=None):
        super(Task, self).__init__()

        self.taskname = taskname
        self.startDate = startDate
        self.endDate = endDate
        self.parent = parent
        self.is_complete = is_complete

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

        self.checkBox = QCheckBox(self)
        self.checkBox.clicked.connect(self.on_checkbox_clicked)
        if self.is_complete:
            self.checkBox.setChecked(True)
        else:
            self.checkBox.setChecked(False)
        mainframeLayout.addWidget(self.checkBox)

        self.bin_icon = QPushButton(text='Delete')
        self.bin_icon.clicked.connect(self.delete)
        mainframeLayout.addWidget(self.bin_icon)

        tasknameFrame = QFrame(self)
        tasknameFrame.setFrameShape(QFrame.Shape.Box)
        tasknameFrameLayout = QVBoxLayout(tasknameFrame)
        tasknameLabel = QLabel(self.taskname, tasknameFrame)
        tasknameFrameLayout.addWidget(tasknameLabel)
        mainframeLayout.addWidget(tasknameFrame)

        sDateFrame = QFrame(self)
        sDateFrame.setFixedSize(320, 40)
        sDateFrame.setFrameShape(QFrame.Shape.Box)
        sDateLayout = QHBoxLayout(sDateFrame)
        sDateLabel = QLabel(f'Starts: {startDate}' if startDate is not None else 'Starts: No Start Date')
        sDateLayout.addWidget(sDateLabel)
        mainframeLayout.addWidget(sDateFrame)

        dDateFrame = QFrame(self)
        dDateFrame.setFixedSize(320, 40)
        dDateFrame.setFrameShape(QFrame.Shape.Box)
        dDateLayout = QHBoxLayout(dDateFrame)
        endDateLabel = QLabel(f'Ends: {endDate}' if endDate is not None else 'Ends: No End Date')
        dDateLayout.addWidget(endDateLabel)
        mainframeLayout.addWidget(dDateFrame)

        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

    @pyqtSlot()
    def on_checkbox_clicked(self):
        if self.checkBox.isChecked():
            self.complete_task()
        else:
            self.incomplete_task()

    @pyqtSlot()
    def complete_task(self):
        print('Running complete task func at task_obj.py')
        with sqlite3.connect('users.db') as conn:
            c = conn.cursor()
            c.execute("UPDATE tasks SET complete = TRUE WHERE taskname = ?", (self.taskname,))
        self.is_complete = True

        # Disconnect all slots connected to the clicked signal
        self.checkBox.clicked.disconnect()

        self.show_completion_message()

        # Connect the specific slot again
        self.checkBox.clicked.connect(self.incomplete_task)

    @pyqtSlot()
    def incomplete_task(self):
        print('Running incomplete task func at task_obj.py')
        with sqlite3.connect('users.db') as conn:
            c = conn.cursor()
            c.execute("UPDATE tasks SET complete = FALSE WHERE taskname = ?", (self.taskname,))
        self.is_complete = False

        self.show_completion_message()

        # Connect the signals again
        self.checkBox.setChecked(False)
        self.checkBox.clicked.connect(self.complete_task)

    def show_completion_message(self):
        message_text = "Task marked as complete" if self.is_complete else "Task marked as incomplete"
        completion = MessageBox(QMessageBox.Icon.Information, text=message_text)
        completion.exec()

    def delete(self):
        result = QMessageBox.question(
            self, 'Delete Task', 'Are you sure you want to delete this task?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if result == QMessageBox.StandardButton.Yes:
            doublecheck = MessageBox(QMessageBox.Icon.Warning, 'Task Deleted')
            undo_btn = QPushButton("Undo")
            ok_btn = QPushButton("OK")
            doublecheck.addButton(undo_btn, QMessageBox.ButtonRole.RejectRole)
            doublecheck.addButton(ok_btn, QMessageBox.ButtonRole.AcceptRole)
            result = doublecheck.exec()

            if result == QMessageBox.StandardButton.No:
                try:
                    with sqlite3.connect('users.db') as conn:
                        c = conn.cursor()
                        c.execute("DELETE FROM tasks WHERE taskname = ?", (self.taskname,))
                        conn.commit()
                except sqlite3.Error as e:
                    print(f"Error deleting task: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    central_widget = QWidget(mainWindow)
    layout = QHBoxLayout(central_widget)
    mainWindow.setCentralWidget(central_widget)
    task = Task('task', 'sdate', 'edate', False, mainWindow)
    layout.addWidget(task)
    mainWindow.showMaximized()
    sys.exit(app.exec())
