import os
import sqlite3

from typing import List

DB_FILE = "db.db"
TASKS_COLS = "title, description, status, duration"

def _getConnection() -> sqlite3.Connection:
  conn = sqlite3.connect(DB_FILE)
  conn.row_factory = sqlite3.Row
  return conn

def createDummy() -> None:
  if os.path.exists(DB_FILE):
    return

  with _getConnection() as conn:
    cursor = conn.cursor()
    cursor.execute("""
      CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT NOT NULL,
        duration INTEGER DEFAULT 1
      )""")

    command = f"INSERT INTO tasks ({TASKS_COLS}) VALUES (?, ?, ?, ?)"
    cursor.execute(command, ("First Task", "This is the first task.", "To Do", 1))
    cursor.execute(command, ("In-Progress Task", "This task is being worked on.", "In Progress", 3))
    cursor.execute(command, ("Completed Task", "This task is finished.", "Done", 5))

def addTask(title: str, description: str, status: str, duration: int) -> int:
  with _getConnection() as conn:
    cursor = conn.cursor()
    command = f"INSERT INTO tasks ({TASKS_COLS}) VALUES (?, ?, ?, ?)"
    cursor.execute(command, (title, description, status, duration))
    return cursor.lastrowid

def getTasks() -> List[sqlite3.Row]:
  with _getConnection() as conn:
    command = f"SELECT id, {TASKS_COLS} FROM tasks ORDER BY id"
    return conn.execute(command).fetchall()

def getTask(taskId: int) -> sqlite3.Row:
  with _getConnection() as conn:
    command = f"SELECT id, {TASKS_COLS} FROM tasks WHERE id = ?"
    return conn.execute(command, (taskId,)).fetchone()

def updateTask(taskId: int, **kwargs):
  with _getConnection() as conn:
    command = ", ".join([f"{key} = ?" for key in kwargs.keys()])
    if not command:
      return
    command = f"UPDATE tasks SET {command} WHERE id = ?"
    conn.execute(command, (*list(kwargs.values()), taskId))

