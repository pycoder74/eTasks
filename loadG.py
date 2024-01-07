from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
import sqlite3
from task_obj import Task
from group_obj import Group

def loadG(user_id, parent=None):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute("""SELECT COUNT(*) FROM tasks WHERE user = ? AND "group" IS NOT NULL""", (user_id,))
    count = cursor.fetchone()[0]
    
    if count > 0:
        cursor.execute("""SELECT * FROM tasks WHERE user = ? AND "group" IS NOT NULL""", (user_id,))
        groups = cursor.fetchall()
        print('Groups:', groups)
        for group in groups:
            return groups
        conn.close()
    else:
        conn.close()
        return 'No groups found'

if __name__ == '__main__':
    app = QApplication([])
    win = QMainWindow()
    result = loadG('1', win)
    print(result)
