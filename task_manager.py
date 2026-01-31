from typing import Dict, Optional

from PySide6.QtCore import QObject, Signal

from task import Task


class _TaskManager(QObject):
  """Central manager for all Task objects in the application."""

  taskCreated = Signal(str)  # Emits task ID
  taskDeleted = Signal(str)  # Emits task ID

  def __init__(self):
    super().__init__()
    self._tasks: Dict[str, Task] = {}

  def createTask(self, title: str, description: str, status: str="todo") -> Task:
    """Create a new task and register it with the manager."""
    task = Task(title, description, status=status)
    self._tasks[task.id] = task
    self.taskCreated.emit(task.id)
    return task

  def addTask(self, task: Task):
    """Register an existing task with the manager."""
    self._tasks[task.id] = task

  def getTask(self, taskId: str) -> Optional[Task]:
    """Retrieve a task by its ID."""
    return self._tasks.get(taskId)

  def requestTaskDeletion(self, taskId: str):
    """Request deletion of a task. This should be called by UI components."""
    if taskId in self._tasks:
      self.deleteTask(taskId)

  def deleteTask(self, taskId: str):
    """Remove a task from the manager and notify listeners."""
    if taskId in self._tasks:
      del self._tasks[taskId]
      self.taskDeleted.emit(taskId)

  def getAllTasks(self) -> Dict[str, Task]:
    """Get all tasks as a dictionary."""
    return self._tasks.copy()


_taskManagerInstance = None


def getTaskManager() -> _TaskManager:
  """Get the singleton TaskManager instance."""
  global _taskManagerInstance
  if _taskManagerInstance is None:
    _taskManagerInstance = _TaskManager()
  return _taskManagerInstance
