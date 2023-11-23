from PyQt6.QtCore import QThread, pyqtSignal
import sqlite3
from group_obj import Group

class TaskLoaderThread(QThread):
    tasksLoaded = pyqtSignal(list)
    groupsLoaded = []  # Class-level variable to track loaded groups
    unsorted_group_created = False  # Variable to track if 'Unsorted' group has been created

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.num_of_tasks = 0  # Initialize num_of_tasks in the constructor

    def load_tasks(self, user_id, load_complete : bool):
        self.load_complete = load_complete
        tasks = []
        try:
            with sqlite3.connect('users.db') as conn:
                print('Connected to the database')  # Add this line


                cursor = conn.cursor()
                cursor.execute(
                    """SELECT COUNT(*) FROM tasks """
                )
                self.num_of_tasks = int(cursor.fetchone()[0])
                print(f"Number of tasks to load: {self.num_of_tasks}")
                if not load_complete:
                    query = 'SELECT taskname, sD, eD, task_group FROM tasks WHERE user = ? AND (task_group IS NULL) AND (complete IS NULL OR complete = 0)'
                else:
                    query = 'SELECT taskname, sD, eD, task_group FROM tasks WHERE user = ? AND (task_group IS NULL) AND (complete = 1)'
                print(f"Executing query: {query}")
                
                cursor.execute(query, [user_id][0])
                tasks = cursor.fetchall()
                print(f"Fetched tasks: {tasks}")  # Print fetched tasks
        except sqlite3.Error as e:
            print(f"Error loading tasks: {e}")

        return tasks

    def emit(self, load_complete = bool):
        tasks = self.load_tasks(self.user_id[0], load_complete = load_complete)
        self.tasksLoaded.emit(tasks)

    def add_tasks_to_layout(self, tasks, parent_layout):
        if not self.unsorted_group_created and self.num_of_tasks > 0:
            unsorted_group = Group('Unsorted', '#FFFFFF', parent_layout)
            parent_layout.addWidget(unsorted_group)
            self.unsorted_group_created = True
        else:
            # Try to find 'Unsorted' group by name
            unsorted_group = None
            for group in parent_layout.children():
                if isinstance(group, Group) and group.name is None:
                    unsorted_group = group
                    break

        if unsorted_group:
            for loaded_task in tasks:
                print(f"Adding task {loaded_task} to group {unsorted_group.name}")
                unsorted_group.add_task(loaded_task)
        else:
            return

        print("Groups after adding tasks:")
        for group in parent_layout.children():
            if isinstance(group, Group):
                print(f"Group name: {group.name}")
                print(f"Number of tasks in {group.name}: {len(group.tasks)}")

    def on_thread_finished(self):
        print("Thread finished.")
