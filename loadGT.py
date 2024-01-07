import sqlite3

def get_topics():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT topic FROM tasks')
    topics = cursor.fetchall()
    conn.close()
    available_topics = [topic[0] for topic in topics]
    return available_topics

def get_groups(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT DISTINCT task_group FROM tasks WHERE user = ? AND task_group IS NOT NULL', [user_id])
    groups = cursor.fetchall()
    available_groups = [group[0] for group in groups]
    
    conn.close()
    return available_groups

def get_tasks(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("""SELECT COUNT(*) FROM tasks WHERE user = ?""", [user_id])
    tasks_num = cursor.fetchone()[0]

    cursor.execute('SELECT  taskname FROM tasks WHERE user = ?', [user_id])
    tasks = cursor.fetchall()
    available_tasks = [task[0] for task in tasks]
    return available_tasks
if __name__ == '__main__':
    topics = get_topics()
    groups = get_groups('1')
    tasks = get_tasks('1')
    print(f"""Available topics: {topics}\nAvailable groups: {groups}\nTasks: {tasks}""")
