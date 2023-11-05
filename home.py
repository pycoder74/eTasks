from PyQt6.QtWidgets import QSizePolicy, QMenu, QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel, QToolButton, QLineEdit, QHBoxLayout
from quickbarV2 import QuickBar  # Assuming this import is correct
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from addtaskwin import AddTaskWindow  # Assuming this import is correct
from PyQt6.QtGui import QAction, QFont
from addgroupwin import AddGroupWindow
from task_obj import Task
import sqlite3
from group_obj import Group
from splashscreen import SplashScreen
import time
from loadT import TaskLoaderThread

class Home(QMainWindow):
    loadingProgress = pyqtSignal(int)
    def __init__(self, fname='', app = None, parent=None):
        super().__init__(parent)
        self.app = app
        # Initial setups
        self.showMaximized()
        self.stretch_added = False
        self.child_wins = []
        self.fname = fname
        self.setWindowTitle("Home")
        self.widgets = []  
        self.no_task_label = QLabel('No Tasks Found', self)
        self.no_task_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.no_task_label.hide()  
        
        # Setup UI and load tasks
        self.splashscreen = SplashScreen(self, span_ang=10)
        self.loadingProgress.connect(self.splashscreen.updateLoadingProgress)
        self.splashscreen.resize(400, 400)
        screen_size = self.app.primaryScreen().size()
        x = (screen_size.width() - self.splashscreen.width()) // 2
        y = (screen_size.height() - self.splashscreen.height()) // 2

        self.splashscreen.move(x, y)
        self.app.processEvents()
        self.setup_ui()



    def setup_ui(self):
        self.splashscreen.show()
        self.loadingProgress.emit(40)
        self.widget = QWidget()
        self.layout = QVBoxLayout()


        # Quickbar setup
        self.qb = QuickBar(self)
        self.layout.addWidget(self.qb)
        self.loadingProgress.emit(60)

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
        self.layout.addLayout(top_action_layout)

        # Add the no task label to layout
        self.layout.addWidget(self.no_task_label)
        self.app.processEvents()

        print('Loading tasks...')
        self.load_tasks()
        print('tasks loaded')
        
        # Set the main layout
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
                any_task_visible = True  # Mark that at least one task is visible
            else:
                widget.hide()
                
        if not any_task_visible:
            self.no_task_label.show()
        else:
            self.no_task_label.hide()




    def showMenu(self):
        menu_position = self.addbtn.mapToGlobal(self.addbtn.rect().bottomLeft())
        self.addbtn.menu().exec(menu_position)

    def addTask(self):
        self.win = AddTaskWindow(self.fname, home_ref=self)
        self.win.taskAdded.connect(self.add_task_to_gui)
        self.win.show()

    def add_task_to_gui(self, task_name, start_date, end_date):
        new_task = Task(task_name, start_date, end_date)
        self.widgets.append(new_task)
        
        # If stretch is added, insert the task just before the stretch
        if self.stretch_added:
            self.layout.insertWidget(len(self.widgets) - 1, new_task)
        else:
            self.layout.addWidget(new_task)

    def addGroup(self):
        self.win = AddGroupWindow(self.user_id[0])	
        self.win.groupAdded.connect(self.add_group_to_gui)
        self.win.show()
    
    def add_group_to_gui(self, group_name, color):
        new_group = Group(group_name, color, self)
        top_action_layout = self.layout.itemAt(2)  # Index 2 is the top_action_layout
        self.layout.insertLayout(3, top_action_layout)  # Insert the top_action_layout
        self.layout.insertWidget(4, new_group)  # Insert the new group

    def load_tasks(self):
        self.task_loading_thread = TaskLoaderThread(self.user_id)
        self.loadingProgress.emit(50)
        self.task_loading_thread.tasksLoaded.connect(self.display_loaded_tasks)
        self.task_loading_thread.start()
        self.loadingProgress.emit(100)
    def display_loaded_tasks(self, rows):
        for row in rows:
            taskname, sD, eD, = row
            loaded_task = Task(taskname, sD, eD)
            self.widgets.append(loaded_task)
            self.layout.addWidget(loaded_task)
        if not self.stretch_added:
            self.layout.addStretch(1)
            self.stretch_added = True
        QTimer.singleShot(500, self.splashscreen.onFadeOutFinished)


if __name__ == '__main__':
    app = QApplication([])
    window = QMainWindow()
    main_win = Home('Elliott', app, window)
    app.exec()