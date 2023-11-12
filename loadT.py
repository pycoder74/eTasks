from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import sqlite3
from task_obj import Task
from group_obj import Group

class TaskLoaderThread(QThread):
    tasksLoaded = pyqtSignal(list)

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
    
    def load_tasks_no_group(self, user_id):
        tasks = []
        try:
            with sqlite3.connect('users.db') as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT taskname, sD, eD FROM tasks  WHERE user = ? AND (task_group IS NULL) AND (complete IS NULL OR complete = 0)', [user_id])
                tasks = cursor.fetchall()
                print(tasks)
        except sqlite3.Error as e:
            print(f"Error loading tasks: {e}")
        return tasks

    def run(self):
        tasks = self.load_tasks(self.user_id[0])
        self.tasksLoaded.emit(tasks)

    def on_thread_finished(self):
        print("Thread finished.")

    def add_tasks_to_group(self, tasks, layout):
        if not tasks:
            notasklbl = QLabel("No tasks here. Create a new one by clicking + Add Task button", alignment=Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(notasklbl)
        else:
            for row in tasks:
                taskname, sD, eD = row  # Unpack only the taskname
                print(taskname, sD, eD)
                group = Group(name = 'Not Sorted', color = '#000000', parent = layout)
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
    task_loader.tasksLoaded.connect(lambda tasks: task_loader.add_tasks_to_layout(tasks, layout))

    # Connect the thread's finished signal to the cleanup function
    task_loader.finished.connect(task_loader.on_thread_finished)

    # Start loading tasks after the main window is shown
    window.show()
    task_loader.start()

    app.exec()
