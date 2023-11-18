from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import sqlite3
from task_obj import Task
from group_obj import Group

class TaskLoaderThread(QThread):
    tasksLoaded = pyqtSignal(list)
    groupsLoaded = []  # Class-level variable to track loaded groups
    unsorted_group_created = False  # Variable to track if 'Unsorted' group has been created

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    def load_tasks(self, user_id):
        tasks = []
        try:
            with sqlite3.connect('users.db') as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT taskname, sD, eD, task_group FROM tasks WHERE user = ? AND (task_group IS NULL) AND (complete IS NULL OR complete = 0)',
                    [user_id]
                )
                tasks = cursor.fetchall()
                print(tasks)
        except sqlite3.Error as e:
            print(f"Error loading tasks: {e}")
        return tasks

    def run(self):
        tasks = self.load_tasks(self.user_id[0])
        self.tasksLoaded.emit(tasks)

    def add_tasks_to_group(self, tasks, parent_layout):
        if not self.unsorted_group_created:
            # If 'Unsorted' group is not found, create it
            unsorted_group = Group('Unsorted', '#FFFFFF', parent_layout)
            parent_layout.insertWidget(0, unsorted_group)
            self.unsorted_group_created = True
        else:
            # Try to find 'Unsorted' group by name
            unsorted_group = None
            for group in parent_layout.children():
                if isinstance(group, Group) and group.name == 'Unsorted':
                    unsorted_group = group
                    break

        if unsorted_group:
            for loaded_task in tasks:
                print(f"Adding task {loaded_task} to group {unsorted_group.name}")
                unsorted_group.add_task(loaded_task)
        else:
            print("Error: 'Unsorted' group not found.")

        print("Groups after adding tasks:")
        for group in parent_layout.children():
            if isinstance(group, Group):
                print(f"Group name: {group.name}")
                print(f"Number of tasks in {group.name}: {len(group.tasks)}")


    def on_thread_finished(self):
        print("Thread finished.")
