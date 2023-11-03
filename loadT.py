from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import sqlite3
from task_obj import Task

class TaskLoaderThread(QThread):
    tasksLoaded = pyqtSignal(list)

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    def run(self):
        tasks = load_tasks(self.user_id)
        self.tasksLoaded.emit(tasks)

def load_tasks(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('SELECT taskname, sD, eD FROM tasks WHERE user = ?', [user_id][0])
    rows = cursor.fetchall()
    print(rows)

    conn.close()
    return rows

def add_tasks_to_layout(tasks, layout):
    if not tasks:
        notasklbl = QLabel("No tasks here. Create a new one by clicking + Add Task button", alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(notasklbl)
    else:
        for row in tasks:
            taskname, sD, eD = row  # Unpack only the taskname
            print(taskname, sD, eD)

            loaded_task = Task(taskname, startDate=sD, endDate=eD)
            layout.addWidget(loaded_task)


if __name__ == '__main__':
    app = QApplication([])

    window = QMainWindow()
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    
    layout = QVBoxLayout()
    central_widget.setLayout(layout)

    task_loader = TaskLoaderThread(user_id='1')
    task_loader.tasksLoaded.connect(lambda tasks: add_tasks_to_layout(tasks, layout))
    task_loader.start()

    window.show()
    app.exec()
