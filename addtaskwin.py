from PyQt6.QtWidgets import QMessageBox, QApplication, QPushButton, QLabel, QWidget, QMainWindow, QFormLayout
from Entries import Entry
from etasksMessageBox import MessageBox
import sqlite3
from task_obj import Task
from PyQt6.QtCore import pyqtSignal
from loadGT import get_topics, get_groups
from addgroupwin import AddGroupWindow

class AddTaskWindow(QMainWindow):
    taskAdded = pyqtSignal(str, str, str)

    def __init__(self, fname='', home_ref=None):
        super().__init__()
        self.fname = fname
        self.home_ref = home_ref
        self.user_id = self.set_user_id()  # fetch the user_id before setting up the UI
        self.setup_ui()

    def set_user_id(self):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("""SELECT id FROM users WHERE fname=?""", (self.fname,))
        result = c.fetchone()
        conn.close()
        return result[0] if result else None

    def addGroup(self):
        self.new_win = AddGroupWindow()
        self.new_win.show()

    def setup_ui(self):
        self.setWindowTitle('Create Task')
        self.layout = QFormLayout()

        self.taskEntry = Entry.InfoEntry('Name:')
        self.layout.addRow(self.taskEntry)

        self.prientry = Entry.PriEntry('Priority:')
        self.layout.addRow(self.prientry)

        available_topics = get_topics()
        self.topic_choose = Entry.MultiSelectDropEntry(text='Topic:', items=available_topics)
        self.layout.addRow(self.topic_choose)

        available_groups = get_groups(self.user_id)
        print(available_groups)
        self.group_choose = Entry.MultiSelectDropEntry(text='Group:', items=available_groups)
        self.layout.addRow(self.group_choose)

        self.add_group = QPushButton(text='Add group')
        self.add_group.clicked.connect(self.addGroup)
        self.layout.addRow(self.add_group)

        calendar_icon_path = 'calendar_icon.jpg'
        self.start_entry = Entry.DateTimeEntry('Start: ', calendar_icon_path)
        self.layout.addRow(self.start_entry)

        self.end_entry = Entry.DateTimeEntry('End: ', calendar_icon_path)
        self.layout.addRow(self.end_entry)

        self.save_button = QPushButton(text="Save")
        self.layout.addRow(self.save_button)
        self.save_button.clicked.connect(self.add_task)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def add_task(self):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        
        taskN = self.taskEntry.get_value()
        pri = self.prientry.get_value()
        topic = ','.join(self.topic_choose.get_value()) if self.topic_choose.get_value() else None
        group = ','.join(self.group_choose.get_value()) if self.group_choose.get_value() else None
        sD = self.start_entry.get_date_value() or None
        eD = self.end_entry.get_date_value() or None
        sT = self.start_entry.get_time_value() or None
        eT = self.end_entry.get_time_value() or None

        try:
            c.execute("""
            INSERT INTO tasks(
                taskname, user, priority, topic, task_group, sD, eD, sT, eT, complete)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (taskN, self.user_id, pri, topic, group, sD, eD, sT, eT, 0))
            conn.commit()
            self.taskAdded.emit(taskN, sD, eD)
            print('Task saved to db')
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
            warning = MessageBox(QMessageBox.type.Warning, text='A task already has the same name.')
            warning.show()
        finally:
            conn.close()

if __name__ == "__main__":
    app = QApplication([])
    window = AddTaskWindow('Elliott')
    window.show()
    app.exec()
