from typing import TYPE_CHECKING, Dict
import sqlite3

if TYPE_CHECKING:
  from task import Task


class _DataStorage:
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
        description TEXT,
        status TEXT DEFAULT 'todo',
        ordering INTEGER DEFAULT 0
      )
    ''')

    self._conn.commit()
    self._runMigrations()

  def _runMigrations(self):
    """Run database migrations to update schema."""
    cursor = self._conn.cursor()

    # Check existing columns
    cursor.execute("PRAGMA table_info(tasks)")
    columns = [column[1] for column in cursor.fetchall()]

    if 'status' not in columns:
      # Migration: Add status column to existing tasks table
      cursor.execute('ALTER TABLE tasks ADD COLUMN status TEXT DEFAULT "todo"')
      self._conn.commit()
      print("Migration: Added 'status' column to tasks table")

    if 'ordering' not in columns:
      # Migration: Add ordering column to existing tasks table
      cursor.execute('ALTER TABLE tasks ADD COLUMN ordering INTEGER DEFAULT 0')
      self._conn.commit()
      print("Migration: Added 'ordering' column to tasks table")

    # Migration: Remove kanban table if it exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='kanban'")
    if cursor.fetchone():
      cursor.execute('DROP TABLE kanban')
      self._conn.commit()
      print("Migration: Removed 'kanban' table")
  
  @property
  def tasks(self) -> Dict[str, Dict[str, 'Task']]:
    """Retrieve all tasks as a dictionary."""
    from task import Task

    cursor = self._conn.cursor()
    cursor.execute('SELECT id, title, description, status, ordering FROM tasks ORDER BY status, ordering')
    return {row["id"]: Task(**dict(row)) for row in cursor.fetchall()}

  def addTask(self, task: 'Task'):
    """Add a new task to the database."""
    cursor = self._conn.cursor()
    cursor.execute(
      'INSERT OR REPLACE INTO tasks (id, title, description, status, ordering) VALUES (?, ?, ?, ?, ?)',
      (task.id, task.title, task.description, task.status, task.ordering)
    )
    self._conn.commit()

  def editTask(self, task: 'Task'):
    """Edit an existing task in the database."""
    cursor = self._conn.cursor()
    cursor.execute(
      'UPDATE tasks SET title = ?, description = ?, status = ?, ordering = ? WHERE id = ?',
      (task.title, task.description, task.status, task.ordering, task.id)
    )
    self._conn.commit()

  def deleteTask(self, taskId: str):
    """Delete a task from the database."""
    cursor = self._conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (taskId,))
    self._conn.commit()
  
  def _close(self):
    """Close the database connection."""
    if self._conn:
      self._conn.close()
      self._conn = None
  
  def __del__(self):
    """Ensure connection is closed when object is destroyed."""
    self._close()


_storageInstance = None


def getDataStorage(filePath: str=".data.db") -> _DataStorage:
  global _storageInstance
  if _storageInstance is None:
    _storageInstance = _DataStorage(filePath)
  return _storageInstance