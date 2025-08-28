import os
import sqlite3

from typing import List

DB_FILE = "db.db"
TASK_COLUMNS = ["title", "description", "status", "effort", "startdate", "assigned_stakeholder_id", "sort_key"]
TASK_COLUMNS_STR = ", ".join(TASK_COLUMNS)
VALID_STATUSES = ["Backlog", "To Do", "In Progress", "Done"]

STAKEHOLDER_COLUMNS = ["name", "surname", "email", "type"]
STAKEHOLDER_COLUMNS_STR = ", ".join(STAKEHOLDER_COLUMNS)
VALID_STAKEHOLDER_TYPES = ["strategy", "subject matter expert", "sponsor", "executant", "system"]

def _getConnection() -> sqlite3.Connection:
  conn = sqlite3.connect(DB_FILE)
  conn.row_factory = sqlite3.Row
  return conn


def _migrateDatabase() -> None:
  """Add sort_key column if it doesn't exist"""
  with _getConnection() as conn:
    cursor = conn.cursor()
    # Check if sort_key column exists
    cursor.execute("PRAGMA table_info(tasks)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'sort_key' not in columns:
      # Add sort_key column
      cursor.execute("ALTER TABLE tasks ADD COLUMN sort_key REAL")
      # Update existing tasks to have sort_key equal to their id
      cursor.execute("UPDATE tasks SET sort_key = id WHERE sort_key IS NULL")

def createDummy() -> None:
  with _getConnection() as conn:
    cursor = conn.cursor()
    cursor.execute("""
      CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT NOT NULL,
        effort INTEGER DEFAULT 1,
        startdate DATE,
        assigned_stakeholder_id INTEGER,
        sort_key REAL
      )""")

    cursor.execute("""
      CREATE TRIGGER IF NOT EXISTS set_default_sort_key
      AFTER INSERT ON tasks
      WHEN NEW.sort_key IS NULL
      BEGIN
        UPDATE tasks SET sort_key = NEW.id WHERE id = NEW.id;
      END
    """)

    cursor.execute("""
      CREATE TABLE IF NOT EXISTS stakeholders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        email TEXT NOT NULL,
        type TEXT NOT NULL
      )""")

    stakeholderCommand = f"INSERT INTO stakeholders ({STAKEHOLDER_COLUMNS_STR}) VALUES (?, ?, ?, ?)"
    # Insert "Not Assigned" stakeholder first (will have ID = 1)
    cursor.execute(stakeholderCommand, ("Not", "Assigned", "not.assigned@system", "system"))
    cursor.execute(stakeholderCommand, ("John", "Doe", "john.doe@company.com", "strategy"))
    cursor.execute(stakeholderCommand, ("Jane", "Smith", "jane.smith@company.com", "subject matter expert"))
    cursor.execute(stakeholderCommand, ("Bob", "Johnson", "bob.johnson@company.com", "sponsor"))
    cursor.execute(stakeholderCommand, ("Alice", "Wilson", "alice.wilson@company.com", "executant"))

    command = f"INSERT INTO tasks ({TASK_COLUMNS_STR}) VALUES (?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(command, ("First Task", "This is the first task.", "To Do", 1, "2024-01-01", 1, None))  # Assigned to "Not Assigned"
    cursor.execute(command, ("In-Progress Task", "This task is being worked on.", "In Progress", 3, "2024-01-02", 2, None))  # Assigned to John
    cursor.execute(command, ("Completed Task", "This task is finished.", "Done", 5, "2024-01-03", 3, None))  # Assigned to Jane

def addTask(title: str, description: str, status: str, effort: int, startdate: str = None, assigned_stakeholder_id: int = 1, sort_key: float = None) -> int:
  if not title.strip():
    print("Error: Task title cannot be empty")
    return None
  if status not in VALID_STATUSES:
    print(f"Error: Invalid status. Must be one of: {VALID_STATUSES}")
    return None
  if effort <= 0:
    print("Error: Effort must be a positive integer")
    return None
  
  with _getConnection() as conn:
    cursor = conn.cursor()
    command = f"INSERT INTO tasks ({TASK_COLUMNS_STR}) VALUES (?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(command, (title, description, status, effort, startdate, assigned_stakeholder_id, sort_key))
    return cursor.lastrowid

def getTasks() -> List[sqlite3.Row]:
  with _getConnection() as conn:
    command = f"SELECT id, {TASK_COLUMNS_STR} FROM tasks ORDER BY sort_key"
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
  if 'effort' in kwargs and kwargs['effort'] <= 0:
    print("Error: Effort must be a positive integer")
    return
  
  with _getConnection() as conn:
    command = ", ".join([f"{key} = ?" for key in kwargs.keys()])
    command = f"UPDATE tasks SET {command} WHERE id = ?"
    conn.execute(command, (*list(kwargs.values()), taskId))

def addStakeholder(name: str, surname: str, email: str, type: str) -> int:
  if not name.strip():
    print("Error: Stakeholder name cannot be empty")
    return None
  if not surname.strip():
    print("Error: Stakeholder surname cannot be empty")
    return None
  if not email.strip():
    print("Error: Stakeholder email cannot be empty")
    return None
  if type not in VALID_STAKEHOLDER_TYPES:
    print(f"Error: Invalid stakeholder type. Must be one of: {VALID_STAKEHOLDER_TYPES}")
    return None
  
  with _getConnection() as conn:
    cursor = conn.cursor()
    command = f"INSERT INTO stakeholders ({STAKEHOLDER_COLUMNS_STR}) VALUES (?, ?, ?, ?)"
    cursor.execute(command, (name, surname, email, type))
    return cursor.lastrowid

def getStakeholders() -> List[sqlite3.Row]:
  with _getConnection() as conn:
    command = f"SELECT id, {STAKEHOLDER_COLUMNS_STR} FROM stakeholders ORDER BY name, surname"
    return conn.execute(command).fetchall()

def getStakeholder(stakeholderId: int) -> sqlite3.Row:
  with _getConnection() as conn:
    command = f"SELECT id, {STAKEHOLDER_COLUMNS_STR} FROM stakeholders WHERE id = ?"
    return conn.execute(command, (stakeholderId,)).fetchone()

def updateStakeholder(stakeholderId: int, **kwargs):
  if not kwargs:
    return
  
  if 'name' in kwargs and not kwargs['name'].strip():
    print("Error: Stakeholder name cannot be empty")
    return
  if 'surname' in kwargs and not kwargs['surname'].strip():
    print("Error: Stakeholder surname cannot be empty")
    return
  if 'email' in kwargs and not kwargs['email'].strip():
    print("Error: Stakeholder email cannot be empty")
    return
  if 'type' in kwargs and kwargs['type'] not in VALID_STAKEHOLDER_TYPES:
    print(f"Error: Invalid stakeholder type. Must be one of: {VALID_STAKEHOLDER_TYPES}")
    return
  
  with _getConnection() as conn:
    command = ", ".join([f"{key} = ?" for key in kwargs.keys()])
    command = f"UPDATE stakeholders SET {command} WHERE id = ?"
    conn.execute(command, (*list(kwargs.values()), stakeholderId))

def calculateNewSortKey(position: int, tasks_in_status: List[sqlite3.Row] = None) -> float:
  """Calculate new sort_key for fractional indexing"""
  if tasks_in_status is None:
    with _getConnection() as conn:
      command = f"SELECT id, sort_key FROM tasks ORDER BY sort_key"
      tasks_in_status = conn.execute(command).fetchall()
  
  if not tasks_in_status:
    return 1.0
  
  if position <= 0:  # Insert at the beginning
    first_sort_key = tasks_in_status[0]['sort_key']
    return first_sort_key / 2
  
  if position >= len(tasks_in_status):  # Insert at the end
    last_sort_key = tasks_in_status[-1]['sort_key']
    return last_sort_key + 1
  
  # Insert between two tasks
  prev_sort_key = tasks_in_status[position - 1]['sort_key']
  next_sort_key = tasks_in_status[position]['sort_key']
  return (prev_sort_key + next_sort_key) / 2

def reorderTask(taskId: int, new_position: int, status: str = None):
  """Reorder a task to a new position using fractional indexing"""
  with _getConnection() as conn:
    cursor = conn.cursor()
    
    # Get current task info
    current_task = cursor.execute(f"SELECT id, {TASK_COLUMNS_STR} FROM tasks WHERE id = ?", (taskId,)).fetchone()
    if not current_task:
      print(f"Error: Task with id {taskId} not found")
      return
    
    # If status is provided, update it first
    if status and status != current_task['status']:
      cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, taskId))
      current_status = status
    else:
      current_status = current_task['status']
    
    # Get all tasks in the same status, excluding the current task
    command = f"SELECT id, sort_key FROM tasks WHERE status = ? AND id != ? ORDER BY sort_key"
    tasks_in_status = cursor.execute(command, (current_status, taskId)).fetchall()
    
    # Calculate new sort_key
    new_sort_key = calculateNewSortKey(new_position, tasks_in_status)
    
    # Update the task's sort_key
    cursor.execute("UPDATE tasks SET sort_key = ? WHERE id = ?", (new_sort_key, taskId))

