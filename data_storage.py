from typing import TYPE_CHECKING

import os
from typing import Any, Dict, List, Tuple
import sqlite3
import json

if TYPE_CHECKING:
  from task import Task


class DataStorage:
  def __init__(self, filePath: str=".data.db"):
    self._filePath = filePath
    self._conn = None
    self._initializeDatabase()
  
  def _initializeDatabase(self):
    """Initialize the database connection and create tables if they don't exist."""
    self._conn = sqlite3.connect(self._filePath, check_same_thread=False)
    self._conn.row_factory = sqlite3.Row
    
    cursor = self._conn.cursor()

    cursor.execute('''
      CREATE TABLE IF NOT EXISTS tasks (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT
      )
    ''')

    cursor.execute('''
      CREATE TABLE IF NOT EXISTS kanban (
        column_id TEXT PRIMARY KEY,
        ordering TEXT NOT NULL
      )
    ''')

    cursor.execute('SELECT COUNT(*) FROM kanban')
    if cursor.fetchone()[0] == 0:
      default_columns = [
        ('todo', json.dumps([])),
        ('in_progress', json.dumps([])),
        ('done', json.dumps([]))
      ]
      cursor.executemany(
        'INSERT INTO kanban (column_id, ordering) VALUES (?, ?)',
        default_columns
      )
    
    self._conn.commit()
  
  @property
  def tasks(self) -> Dict[str, Dict[str, str]]:
    """Retrieve all tasks as a dictionary."""
    cursor = self._conn.cursor()
    cursor.execute('SELECT id, title, description FROM tasks')
    
    tasks_dict = {}
    for row in cursor.fetchall():
      tasks_dict[row['id']] = {
        'id': row['id'],
        'title': row['title'],
        'description': row['description']
      }
    
    return tasks_dict

  @property
  def kanban(self) -> Dict[str, List[str]]:
    """Retrieve kanban column orderings as a dictionary."""
    cursor = self._conn.cursor()
    cursor.execute('SELECT column_id, ordering FROM kanban')
    
    kanban_dict = {}
    for row in cursor.fetchall():
      kanban_dict[row['column_id']] = json.loads(row['ordering'])
    
    return kanban_dict

  def addTask(self, task: 'Task'):
    """Add a new task to the database."""
    cursor = self._conn.cursor()
    cursor.execute(
      'INSERT OR REPLACE INTO tasks (id, title, description) VALUES (?, ?, ?)',
      (task.id, task.title, task.description)
    )
    self._conn.commit()

  def editTask(self, task: 'Task'):
    """Edit an existing task in the database."""
    cursor = self._conn.cursor()
    cursor.execute(
      'UPDATE tasks SET title = ?, description = ? WHERE id = ?',
      (task.title, task.description, task.id)
    )
    self._conn.commit()

  def reorderKanban(self, columnId: str, ordering: List[str]):
    """Update the ordering of tasks in a kanban column."""
    cursor = self._conn.cursor()
    cursor.execute(
      'UPDATE kanban SET ordering = ? WHERE column_id = ?',
      (json.dumps(ordering), columnId)
    )
    self._conn.commit()

  def save(self) -> bool:
    """
    Save changes to the database.
    Note: With SQLite, changes are committed immediately in each method,
    so this method is kept for API compatibility but doesn't do anything.
    """
    try:
      self._conn.commit()
      return True
    except Exception:
      return False
  
  def close(self):
    """Close the database connection."""
    if self._conn:
      self._conn.close()
      self._conn = None
  
  def __del__(self):
    """Ensure connection is closed when object is destroyed."""
    self.close()


_storageInstance = None


def getDataStorage(filePath: str=".data.db") -> DataStorage:
  global _storageInstance
  if _storageInstance is None:
    _storageInstance = DataStorage(filePath)
  return _storageInstance