import sys
from PyQt6.QtWidgets import QSizePolicy, QMenu, QMainWindow, QApplication, QFrame, QWidget, QVBoxLayout, QLabel, QToolButton, QLineEdit, QHBoxLayout
from quickbarV2 import QuickBar
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QThread
from addtaskwin import AddTaskWindow
from PyQt6.QtGui import QAction, QFont
from addgroupwin import AddGroupWindow
from task_obj import Task
import sqlite3
from group_obj import Group
from splashscreen import SplashScreen
from loadT import TaskLoaderThread

class Home(QMainWindow):
    loadingProgress = pyqtSignal(int)
    
    def __init__(self, fname='', app=None, parent=None):
        super().__init__(parent)
        self.app = app
        self.stretch_added = False
        self.child_wins = []
        self.fname = fname
        self.setWindowTitle("Home")
        self.widgets = []
        self.setup_ui()
        self.load_tasks()
        self.show()

    def refresh_application(self):
        # Reset or reload necessary data
        self.widgets = []  # Clear the list of widgets
        self.stretch_added = False  # Reset the stretch flag
        self.load_tasks()  # Reload tasks
    
    def display_loaded_tasks(self, rows):
        for row in rows:
            taskname, sD, eD = row  # Remove the extra comma
            loaded_task = Task(taskname, sD, eD)
            self.widgets.append(loaded_task)
            QTimer.singleShot(0, lambda: self.layout.addWidget(loaded_task))

        if not self.stretch_added:
            QTimer.singleShot(0, lambda: self.layout.addStretch(1))
            self.stretch_added = True

        QTimer.singleShot(500, self.splashscreen.onFadeOutFinished)


    def setup_ui(self):
        self.splashscreen = SplashScreen(self, span_ang=10)
        self.loadingProgress.connect(self.splashscreen.updateLoadingProgress)
        self.splashscreen.resize(400, 400)
        screen_size = self.app.primaryScreen().size()
        x = (screen_size.width() - self.splashscreen.width()) // 2
        y = (screen_size.height() - self.splashscreen.height()) // 2

        self.splashscreen.move(x, y)
        self.app.processEvents()
        self.splashscreen.show()
        self.loadingProgress.emit(40)

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
            border: 2px solid #00008B
            }"""
        )
        self.task_layout = QVBoxLayout()
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

        print('Loading tasks...')
        self.load_tasks()
        print('tasks loaded')

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
        new_task = Task(task_name, start_date, end_date)

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
                
        # Create 'Unsorted' group if it doesn't exist
        unsorted_group = next((group for group in self.task_frame.children() if getattr(group, 'name', None) in (None, 'Unsorted')), None)
        if not unsorted_group:
            unsorted_group = Group('Unsorted', '#FFFFFF', self.task_layout)
            self.layout.insertWidget(4, unsorted_group)

        if unsorted_group:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute("""
                SELECT taskname, start_date, end_date FROM tasks
            """)
            tasks = c.fetchall()
            for task_data in tasks:
                task_name, start_date, end_date = task_data
                task = Task(task_name, start_date, end_date)
                unsorted_group.add_task(task)


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
        new_group = Group(group_name, color, self.task_layout)
        self.layout.insertWidget(4, new_group)

    def load_tasks(self):
        self.task_loader = TaskLoaderThread(user_id=self.user_id)
        self.task_loader.tasksLoaded.connect(lambda tasks: self.task_loader.add_tasks_to_group((Task(row[0], row[1], row[2]) for row in tasks if not row[3]), self.task_layout))

        # Connect the thread's finished signal to the cleanup function
        self.task_loader.finished.connect(self.task_loader.on_thread_finished)

        # Connect a new signal to add all tasks to the 'Unsorted' group
        self.task_loader.tasksLoaded.connect(lambda tasks: self.add_all_tasks_to_unsorted_group(tasks))

        # Start the thread
        self.task_loader.start()

    def add_all_tasks_to_unsorted_group(self, tasks):
        # Create 'Unsorted' group if it doesn't exist
        unsorted_group = next((group for group in self.task_frame.children() if isinstance(group, Group) and group.name == 'Unsorted'), None)
        if not unsorted_group:
            unsorted_group = Group('Unsorted', '#FFFFFF', self.task_layout)
            self.layout.insertWidget(4, unsorted_group)

        # Add all tasks to the 'Unsorted' group
        for task_data in tasks:
            if len(task_data) == 3:
                task_name, start_date, end_date = task_data
            else:
                task_name = str(task_data[0])
                start_date = task_data[1]
                end_date = task_data[2]

            task = Task(task_name, start_date, end_date)
            unsorted_group.add_task(task)


if __name__ == '__main__':
    app = QApplication([])
    window = QMainWindow()
    main_win = Home('Elliott', app, window)
    main_win.show()  
    app.exec()
