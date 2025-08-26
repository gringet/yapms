import os
import sqlite3

from typing import List

DB_FILE = "db.db"
TASK_COLUMNS = ["title", "description", "status", "duration", "startdate"]
TASK_COLUMNS_STR = ", ".join(TASK_COLUMNS)
VALID_STATUSES = ["To Do", "In Progress", "Done"]

def _getConnection() -> sqlite3.Connection:
  conn = sqlite3.connect(DB_FILE)
  conn.row_factory = sqlite3.Row
  return conn

def _migrateDatabase() -> None:
  with _getConnection() as conn:
    cursor = conn.cursor()
    # Check if startdate column exists
    cursor.execute("PRAGMA table_info(tasks)")
    columns = [column[1] for column in cursor.fetchall()]
    if 'startdate' not in columns:
      cursor.execute("ALTER TABLE tasks ADD COLUMN startdate DATE")
      print("Database migrated: added startdate column")

def createDummy() -> None:
  if os.path.exists(DB_FILE):
    _migrateDatabase()
    return

  with _getConnection() as conn:
    cursor = conn.cursor()
    cursor.execute("""
      CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT NOT NULL,
        duration INTEGER DEFAULT 1,
        startdate DATE
      )""")

    command = f"INSERT INTO tasks ({TASK_COLUMNS_STR}) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(command, ("First Task", "This is the first task.", "To Do", 1, "2024-01-01"))
    cursor.execute(command, ("In-Progress Task", "This task is being worked on.", "In Progress", 3, "2024-01-02"))
    cursor.execute(command, ("Completed Task", "This task is finished.", "Done", 5, "2024-01-03"))

def addTask(title: str, description: str, status: str, duration: int, startdate: str = None) -> int:
  if not title.strip():
    print("Error: Task title cannot be empty")
    return None
  if status not in VALID_STATUSES:
    print(f"Error: Invalid status. Must be one of: {VALID_STATUSES}")
    return None
  if duration <= 0:
    print("Error: Duration must be a positive integer")
    return None
  
  with _getConnection() as conn:
    cursor = conn.cursor()
    command = f"INSERT INTO tasks ({TASK_COLUMNS_STR}) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(command, (title, description, status, duration, startdate))
    return cursor.lastrowid

def getTasks() -> List[sqlite3.Row]:
  with _getConnection() as conn:
    command = f"SELECT id, {TASK_COLUMNS_STR} FROM tasks ORDER BY id"
    return conn.execute(command).fetchall()

def getTask(taskId: int) -> sqlite3.Row:
  with _getConnection() as conn:
    command = f"SELECT id, {TASK_COLUMNS_STR} FROM tasks WHERE id = ?"
    return conn.execute(command, (taskId,)).fetchone()

def updateTask(taskId: int, **kwargs):
  if not kwargs:
    return
  
  if 'title' in kwargs and not kwargs['title'].strip():
    print("Error: Task title cannot be empty")
    return
  if 'status' in kwargs and kwargs['status'] not in VALID_STATUSES:
    print(f"Error: Invalid status. Must be one of: {VALID_STATUSES}")
    return
  if 'duration' in kwargs and kwargs['duration'] <= 0:
    print("Error: Duration must be a positive integer")
    return
  
  with _getConnection() as conn:
    command = ", ".join([f"{key} = ?" for key in kwargs.keys()])
    command = f"UPDATE tasks SET {command} WHERE id = ?"
    conn.execute(command, (*list(kwargs.values()), taskId))

