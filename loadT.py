from PyQt6.QtCore import QThread, pyqtSignal
import sqlite3
from group_obj import Group
from task_obj import Task
class TaskLoaderThread(QThread):
    tasksLoaded = pyqtSignal(list)
    groupsLoaded = []  # Class-level variable to track loaded groups
    unsorted_group_created = False  # Variable to track if 'Unsorted' group has been created

    def __init__(self, user_id, load_complete: bool, parent_layout):
        super().__init__()
        self.user_id = user_id
        self.num_of_tasks = 0  # Initialize num_of_tasks in the constructor
        self.load_complete = load_complete
        self.parent_layout = parent_layout  # Added parent_layout as an instance variable
    def load_tasks(self, user_id, load_complete):
        self.load_complete = load_complete
        tasks = []
        try:
            with sqlite3.connect('users.db') as conn:
                print('Connected to the database')

                cursor = conn.cursor()
                cursor.execute(
                    """SELECT COUNT(*) FROM tasks """
                )
                self.num_of_tasks = int(cursor.fetchone()[0])
                print(f"Number of tasks to load: {self.num_of_tasks}")
                if not self.load_complete:
                    query = 'SELECT taskname, sD, eD, task_group FROM tasks WHERE user = ? AND (complete = 0)'
                else:
                    query = 'SELECT taskname, sD, eD, task_group FROM tasks WHERE user = ? AND (complete = 1)'
                print(f"Executing query: {query}")

                cursor.execute(query, [user_id][0])
                self.tasks = cursor.fetchall()
                print(f"Fetched tasks: {self.tasks}")  # Print fetched tasks
        except sqlite3.Error as e:
            print(f"Error loading tasks: {e}")

        return self.tasks

    def emit(self, load_complete=bool):
        tasks = self.load_tasks(self.user_id[0], load_complete=load_complete)
        self.tasksLoaded.emit(tasks)

    def add_tasks_to_layout(self, tasks, parent_layout):
        for i in tasks:
            nTask = Task(i[0], i[1], i[2], is_complete = False, parent = parent_layout)
        

    def run_task_thread(self):
        tasks = self.load_tasks(self.user_id, self.load_complete)
        self.add_tasks_to_layout(tasks, self.parent_layout)  # Use self.parent_layout
        self.finished.emit()  # Emit the finished signal when the thread is complete
    def on_thread_finished(self):
        print("Thread finished.")
