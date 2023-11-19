import sqlite3
try:
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("""
            DELETE FROM tasks
            """)
    conn.commit()
    conn.close()
    print('deletion success')
except sqlite3.Error as error:
    print(f"Error: {error}")