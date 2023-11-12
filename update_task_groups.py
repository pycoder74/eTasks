import sqlite3
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute(
"""UPDATE tasks
SET task_group = NULL
WHERE task_group = '';
"""
)
conn.commit()
conn.close()
