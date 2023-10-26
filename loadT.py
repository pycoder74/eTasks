from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
import sqlite3
from task_obj import Task

def load_tasks(user_id, parent=None):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute("""SELECT COUNT(*) FROM tasks WHERE user = ?""", [user_id])
    tasks_num = cursor.fetchone()[0]
    
    if tasks_num == 0:
        notasklbl = QLabel("No tasks here. Create a new one by clicking + Add Task button", alignment=Qt.AlignmentFlag.AlignCenter)
        parent.layout.addWidget(notasklbl)
    else:
        cursor.execute('SELECT * FROM tasks WHERE user = ?', [user_id])
        rows = cursor.fetchall()
        print('Rows:', rows)
        
        for row in rows:
            _, taskname, priority, topic, task_group, sD, eD, sT, eT = row
            
            # Assuming `Task` is a PyQt6 widget and it takes taskname, sD, eD as its arguments.
            loaded_task = Task(taskname, sD, eD)
            parent.layout.addWidget(loaded_task)

    conn.close()

if __name__ == '__main__':
    app = QApplication([])

    window = QMainWindow()
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    
    layout = QVBoxLayout()
    central_widget.setLayout(layout)
    
    # Adding a layout attribute to the window for easier access in the load_tasks function
    window.layout = layout

    load_tasks('1', window)
    
    window.show()
    app.exec()
