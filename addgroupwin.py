from PyQt6.QtWidgets import QApplication, QMessageBox, QPushButton, QLabel, QWidget, QMainWindow, QFormLayout
from Entries import Entry  # Assuming Entries module provides Entry class.
from loadGT import get_topics, get_tasks
import sqlite3
import sys
from etasksMessageBox import MessageBox
from task_obj import Task
from group_obj import Group
class AddGroupWindow(QMainWindow):  # Inherit from QMainWindow
    def __init__(self, user_id='', parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.parent = parent
        self.init_ui()
        
    def init_ui(self):
        self.layout = QFormLayout()

        self.setWindowTitle('Create Group')

        # Name Entry
        self.groupEntry = Entry.InfoEntry('Name:')
        self.layout.addRow(self.groupEntry)

        # Topic Dropdown
        available_topics = get_topics()
        self.topic_choose = Entry.DropEntry(text='Topic:', items=available_topics)
        self.layout.addRow(self.topic_choose)

        # Tasks Dropdown
        tasks = get_tasks(self.user_id)
        print(tasks)
        self.task_choose = Entry.MultiSelectDropEntry(text='Tasks:', items=tasks)
        self.layout.addRow(self.task_choose)

        # Save Button
        self.save_button = QPushButton(text='Save')
        self.save_button.clicked.connect(self.save)
        self.layout.addRow(self.save_button)

        # Set Layout
        main_widget = QWidget()
        main_widget.setLayout(self.layout)
        self.setCentralWidget(main_widget)
        
    def save(self):
        # Get the input values
        name = self.groupEntry.get_value()
        topic = self.topic_choose.get_value() 
        selected_tasks = self.task_choose.get_value()  # Assuming this returns a list of task names.

        # Update the database
        self.update_tasks_with_group(name, selected_tasks)

        # Provide feedback to the user
        saved = MessageBox(QMessageBox.Icon.Information, 'Group saved')
        saved.exec()

        # Close this window
        self.close()

    def update_tasks_with_group(self, group_name, tasks):
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            # Update the task_group column for each selected task
            for task in tasks:
                cursor.execute("UPDATE tasks SET task_group = ? WHERE taskname = ? AND user = ?", (group_name, task, self.user_id))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AddGroupWindow('0')
    window.show()
    sys.exit(app.exec())  # Use sys.exit() for a clean exit
