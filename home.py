from PyQt6.QtWidgets import QScrollArea, QSizePolicy, QMenu, QMainWindow, QApplication, QFrame, QWidget, QVBoxLayout, QLabel, QToolButton, QLineEdit, QHBoxLayout
from quickbarV2 import QuickBar
from PyQt6.QtCore import Qt, pyqtSignal
from addtaskwin import AddTaskWindow
from PyQt6.QtGui import QAction, QFont
from addgroupwin import AddGroupWindow
from task_obj import Task
import sqlite3
from group_obj import Group
from splashscreen import SplashScreen
from loadT import TaskLoaderThread
import sys

class Home(QMainWindow):
    loadingProgress = pyqtSignal(int)

    def __init__(self, fname='', app=None, parent=None):
        super().__init__(parent)
        self.app = app
        self.notasklabelshown = False  # Corrected initialization
        self.stretch_added = False
        self.child_wins = []
        self.fname = fname
        self.setWindowTitle("Home")
        self.widgets = []
        self.task_layout = QVBoxLayout()

        self.setup_ui()
        print('Loading incomplete tasks...')
        self.load_tasks(load_complete=False)
        print('Loading completed tasks...')
        self.load_tasks(load_complete=True)
        print('setting up signals...')
        self.setup_signals()
        print('Signals set')
        self.show()

    def setup_ui(self):
        self.connected_tasks = []
        self.splashscreen = SplashScreen(self, span_ang=10)
        self.loadingProgress.connect(self.splashscreen.updateLoadingProgress)
        self.splashscreen.resize(400, 400)
        screen_size = self.app.primaryScreen().size()
        x = (screen_size.width() - self.splashscreen.width()) // 2
        y = (screen_size.height() - self.splashscreen.height()) // 2
        self.app.processEvents()
        self.splashscreen.show()
        self.loadingProgress.emit(40)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        self.setCentralWidget(scroll_area)
        self.widget = QWidget()
        self.layout = QVBoxLayout()

        # Quickbar setup
        self.qb = QuickBar(self)
        self.layout.addWidget(self.qb)
        self.loadingProgress.emit(60)

        self.task_frame = QFrame()
        self.task_frame.setObjectName('task_frame')
        self.task_frame.setStyleSheet(
            """#task_frame{
            border: 2px solid #000000
            }"""
        )
        self.task_frame.setLayout(self.task_layout)

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("""SELECT id FROM users WHERE fname = ?""", (self.fname,))
        self.user_id = cursor.fetchone()

        # Title setup
        self.loadingProgress.emit(80)
        self.title = QLabel(f'Welcome, {self.fname}')
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("""
            padding-left: 20px; 
            padding-right: 20px;
            font-size: 30px;
            text-decoration: underline;
            font-weight: bold;
            color: #000000;
        """)
        self.layout.addWidget(self.title)

        # Add button setup
        self.setup_add_button()

        # Search bar setup
        self.setup_search_bar()

        # Top action layout for search and add button
        top_action_layout = QHBoxLayout()
        top_action_layout.addWidget(self.addbtn)
        top_action_layout.addWidget(self.search_bar)
        if top_action_layout.parent() is None:
            self.layout.addLayout(top_action_layout)
        self.layout.addWidget(self.task_frame)

        self.app.processEvents()

        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        self.layout.addStretch(1)
        self.loadingProgress.emit(100)

    def setup_add_button(self):
        self.addbtn = QToolButton()
        self.addbtn.setText('+')
        self.addbtn.setStyleSheet("""QToolButton::menu-indicator { image: none; }
                                     QToolButton {
                                      background-color: white;
                                      border-radius: 4px;
                                      }""")
        self.addbtn.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.addbtn.clicked.connect(self.showMenu)
        self.addbtn.setFixedSize(50, 50)
        self.atFont = self.addbtn.font()
        self.atFont.setPointSize(18)
        self.addbtn.setFont(self.atFont)

        # Dropdown menu setup
        dropdown = QMenu()
        dropdown.setStyleSheet("""
QMenu::item {
    background-color: white;
}
QMenu::item:selected {
    background-color: blue;
}
""")
        addtaskaction = QAction('Task', self)
        addtaskaction.triggered.connect(self.addTask)
        dropdown.addAction(addtaskaction)

        addgroupaction = QAction('Group', self)
        addgroupaction.triggered.connect(self.addGroup)
        dropdown.addAction(addgroupaction)
        addtopicaction = QAction('Topic', self)
        dropdown.addAction(addtopicaction)

        self.addbtn.setMenu(dropdown)

    def setup_search_bar(self):
        self.search_bar = QLineEdit(self)
        font_size = int(self.search_bar.height() * 0.5)
        font = QFont()
        font.setPointSize(font_size)
        self.search_bar.setFont(font)
        search_bar_height = self.addbtn.size().height()
        self.search_bar.setFixedHeight(search_bar_height)
        self.search_bar.setPlaceholderText("Search tasks...")
        self.search_bar.setStyleSheet("""QLineEdit { padding-left: 10px; }
                                         QLineEdit {
                                          background-color: white;
                                          border-radius: 4px;
                                          }""")
        self.search_bar.textChanged.connect(self.update_display)

    def update_display(self, text):
        any_task_visible = False

        for widget in self.widgets:
            if (text.lower() in str(widget.taskname).lower()) or \
                    (text.lower() in str(widget.startDate).lower()) or \
                    (text.lower() in str(widget.endDate).lower()):
                widget.show()
                any_task_visible = True
            else:
                widget.hide()

    def showMenu(self):
        menu_position = self.addbtn.mapToGlobal(self.addbtn.rect().bottomLeft())
        self.addbtn.menu().exec(menu_position)

    def addTask(self):
        self.win = AddTaskWindow(self.fname, home_ref=self)
        self.win.taskAdded.connect(self.add_task_to_gui)
        self.win.show()

    def add_task_to_gui(self, task_name, start_date, end_date):
        new_task = Task(task_name, start_date, end_date, complete=False)
        new_task.taskCompleted.connect(self.reload_tasks)
        new_task.taskIncompleted.connect(self.reload_tasks)
        if self.notasklabelshown is True:
            self.notasklabel.destroy()
            self.notasklabelshown = False

        # Retrieve the group information from the database
        group_name = self.get_group_from_database(new_task.taskname)

        # If the task has a group, add it to the corresponding group
        if group_name:
            # Find the group with the matching name
            matching_group = next((group for group in self.task_frame.children() if isinstance(group, Group) and group.name == group_name), None)

            if matching_group:
                matching_group.add_task(new_task)

            # Print group names after adding the task
            print("Group Names:", [group.name for group in self.task_frame.children()])

    def get_group_from_database(self, taskname):
        try:
            with sqlite3.connect('users.db') as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT task_group FROM tasks WHERE taskname = ?', [taskname])
                group_name = cursor.fetchone()
                return group_name[0] if group_name else None
        except sqlite3.Error as e:
            print(f"Error retrieving group information: {e}")
            return None

    def addGroup(self):
        self.win = AddGroupWindow(self.user_id[0])
        self.win.groupAdded.connect(self.add_group_to_gui)
        self.win.show()

    def add_group_to_gui(self, group_name, color):
        # Check if the group already exists
        existing_group = next((group for group in self.task_frame.children() if isinstance(group, Group) and group.name == group_name), None)

        if existing_group:
            print(f"Group '{group_name}' already exists.")
        else:
            new_group = Group(group_name, color, self.task_layout)
            self.layout.insertWidget(4, new_group)

    def load_tasks(self, load_complete: bool):
        print("Starting task loader thread at home.py")
        self.task_loader = TaskLoaderThread(self.user_id, load_complete, parent_layout=self.task_layout)
        self.task_loader.run_task_thread()
        # Create a group based on completion status
        group_name = 'Completed' if load_complete else 'Not Completed'
        group_color = '#00FF00' if load_complete else '#FF0000'

        self.status_group = Group(name=group_name, color=group_color, parent_layout=self.task_layout)

        if self.task_loader.num_of_tasks > 0:
            for i in self.task_loader.tasks:
                print(f"\n{i} in home.py")
                nTask = Task(i[0], i[1], i[2], i[3])
                if load_complete:
                    self.status_group.add_task(task_name=nTask.taskname, start_date=nTask.startDate,
                                               end_date=nTask.endDate, complete=True)
                else:
                    self.status_group.add_task(task_name=nTask.taskname, start_date=nTask.startDate,
                                               end_date=nTask.endDate, complete=False)

            # Connect the thread's finished signal to the cleanup function
            self.task_loader.finished.connect(self.task_loader.on_thread_finished)

            # Connect a new signal to add all tasks to the 'Unsorted' group
            self.task_loader.tasksLoaded.connect(lambda tasks: self.load_tasks)

            # Start the thread
            self.task_loader.run_task_thread()

        else:
            text = f'No {"completed" if load_complete else "incomplete"} tasks found'
            self.notasklabel = QLabel(text)
            self.notasklabel.setStyleSheet(
                """font-weight: bold;"""
            )

            self.status_group.add_task_to_group(self.notasklabel)


    def setup_signals(self):
        for widget in self.findChildren(Task):
            widget.taskCompleted.connect(lambda: self.handle_completion_change(widget, completed=False))
            widget.taskIncompleted.connect(lambda: self.handle_completion_change(widget, completed=True))

    def handle_completion_change(self, widget: Task, completed: bool):
        print('Task has been marked as complete. Reloading tasks...')
        self.clear_tasks()
        self.clear_groups()
        if completed:
            widget.complete_task()
        else:
            widget.incomplete_task()
        self.reload_tasks()

    def reload_tasks(self):
        print('Clearing tasks...')
        self.clear_tasks()
        print('Clearing groups...')
        self.clear_groups()
        print('Reloading at home.py')
        # Reload incomplete tasks
        print('Reloading incomplete tasks...')
        self.load_tasks(load_complete=False)
        # Reload completed tasks
        print('Reloading completed tasks...')
        self.load_tasks(load_complete=True)
        self.setup_signals()

    def clear_tasks(self):
        for widget in self.findChildren(Task):
            print(f"Task widget: {widget}")
            widget.setParent(None)

    def clear_groups(self):
        for widget in self.findChildren(Group):
            if isinstance(widget, Group):
                widget.setParent(None)


if __name__ == '__main__':
    app = QApplication([])
    main_win = Home('Elliott', app)
    main_win.show()
    sys.exit(app.exec())
