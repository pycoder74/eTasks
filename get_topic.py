import sqlite3
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute("SELECT DISTINCT topic FROM tasks")
print(c.fetchall())
conn.commit()
