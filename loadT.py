from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import sqlite3
from task_obj import Task
from group_obj import Group

class TaskLoaderThread(QThread):
    tasksLoaded = pyqtSignal(list)
    groupsLoaded = []  # Class-level variable to track loaded groups

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

    def add_tasks_to_group(self, tasks, layout):
        unsorted_group = None  # Initialize unsorted_group variable
        new_group = None  # Initialize new_group variable outside the loop

        for row in tasks:
            taskname, sD, eD, task_group = row  # Unpack task details
            group_name = 'NULL'

            # Check if the group has already been loaded
            if group_name not in TaskLoaderThread.groupsLoaded:
                new_group = Group(name=group_name, color='#000000', parent_layout=layout)
                TaskLoaderThread.groupsLoaded.append(group_name)

            loaded_task = Task(taskname, startDate=sD, endDate=eD)

            if group_name == 'NULL':
                unsorted_group = new_group  # Assign the 'Unsorted' group

            if new_group and new_group is not unsorted_group:
                new_group.add_task(loaded_task)

        if unsorted_group:
            unsorted_group.add_tasks([loaded_task for row in tasks if not row[3]])


    def on_thread_finished(self):
        print("Thread finished.")

