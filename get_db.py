import sqlite3
import pandas as pd
from tabulate import tabulate
def insert(data):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # You should provide an SQL statement to insert data into the database.
    # Below is an example of how you can insert data into a table named 'tasks':
    cursor.execute("INSERT INTO tasks (column1, column2) VALUES (?, ?)", data)
    
    conn.commit()
    print('Data saved')
    conn.close()

def get_data():
    conn = sqlite3.connect('users.db')
    
    # Use pandas to read data from the database into a DataFrame
    try:
        data = pd.read_sql("SELECT * FROM tasks", conn)
        
        conn.close()
        
        # Convert the DataFrame to a formatted table string
        table = tabulate(data, headers='keys', tablefmt='grid')
        
        return table
    except pd.errors.DatabaseError:
        return('No tasks found')


def delete_all():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # To delete all records from a table, use the DELETE statement without specifying columns
    cursor.execute("DELETE FROM tasks")
    cursor.execute("DELETE FROM users")
    
    conn.commit()
    print('Database cleared')
    conn.close()

