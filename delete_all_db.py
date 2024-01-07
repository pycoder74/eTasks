import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Delete all records from the 'tasks' table
cursor.execute("DELETE FROM tasks")
print('All tasks deleted')

# Delete all records from the 'users' table
cursor.execute("DELETE FROM users")
print('All users deleted')

# Commit the changes and close the connection
conn.commit()
conn.close()
