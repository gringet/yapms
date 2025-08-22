import sqlite3
from typing import List

DB_FILE = 'kanban.db'

def get_db_connection():
    """Establishes a connection to the database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database and creates the tasks table if it doesn't exist."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                status TEXT NOT NULL,
                duration INTEGER DEFAULT 1
            )
        ''')
        # Add some dummy data if the table is newly created and empty
        cursor.execute('SELECT COUNT(id) FROM tasks')
        if cursor.fetchone()[0] == 0:
            cursor.execute('INSERT INTO tasks (title, content, status, duration) VALUES (?, ?, ?, ?)',
                           ("First Task", "This is the first task.", "To Do", 1))
            cursor.execute('INSERT INTO tasks (title, content, status, duration) VALUES (?, ?, ?, ?)',
                           ("In-Progress Task", "This task is being worked on.", "In Progress", 3))
            cursor.execute('INSERT INTO tasks (title, content, status, duration) VALUES (?, ?, ?, ?)',
                           ("Completed Task", "This task is finished.", "Done", 5))

def add_task(title: str, content: str, status: str, duration: int) -> int:
    """Adds a new task to the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (title, content, status, duration) VALUES (?, ?, ?, ?)',
                       (title, content, status, duration))
        return cursor.lastrowid

def get_tasks() -> List[sqlite3.Row]:
    """Retrieves all tasks from the database."""
    with get_db_connection() as conn:
        return conn.execute('SELECT id, title, content, status, duration FROM tasks ORDER BY id').fetchall()

def update_task_status(task_id: int, new_status: str):
    """Updates the status (column) of a specific task."""
    with get_db_connection() as conn:
        conn.execute('UPDATE tasks SET status = ? WHERE id = ?', (new_status, task_id))
