import sqlite3
def create_table(cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS tasks(
        taskname TEXT PRIMARY KEY,
        user TEXT,
        priority TEXT,
        topic   TEXT,
        task_group TEXT,
        sD TEXT,
        eD TEXT,
        sT TEXT,
        eT TEXT
        )
    """)
