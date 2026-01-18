from PySide6.QtWidgets import QWidget, QHBoxLayout, QDialog

from kanban_column import KanbanColumn
from task_manager import getTaskManager
from data_storage import getDataStorage
from flashcard import FlashcardDetailsDialog


class KanbanBoard(QWidget):
  def __init__(self):
    super().__init__()

    self._taskManager = getTaskManager()
    self._storage = getDataStorage()

    # Wire TaskManager to DataStorage
    self._taskManager.taskDeleted.connect(self._storage.deleteTask)

    mainLayout = QHBoxLayout()

    self.todoColumn = KanbanColumn("todo", "To Do")
    self._wireColumnSignals(self.todoColumn)
    mainLayout.addWidget(self.todoColumn)

    self.inProgressColumn = KanbanColumn("in_progress", "In Progress")
    self._wireColumnSignals(self.inProgressColumn)
    mainLayout.addWidget(self.inProgressColumn)

    self.doneColumn = KanbanColumn("done", "Done")
    self._wireColumnSignals(self.doneColumn)
    mainLayout.addWidget(self.doneColumn)

    self.setLayout(mainLayout)

    self._loadTasksFromStorage()

  def _wireColumnSignals(self, column: KanbanColumn):
    """Wire up signals for a column."""
    # Column requests task creation
    column.taskCreationRequested.connect(lambda: self._handleTaskCreationRequest(column))

    # Column requests task deletion
    column.taskDeletionRequested.connect(self._taskManager.requestTaskDeletion)

    # TaskManager notifies deletion - column handles UI cleanup
    self._taskManager.taskDeleted.connect(column.handleTaskDeletion)

  def _loadTasksFromStorage(self):
    """Load all tasks from storage and distribute to columns."""
    tasks = self._storage.tasks

    # Register all tasks with TaskManager
    for task in tasks.values():
      self._taskManager.addTask(task)

    # Load tasks into each column
    self.todoColumn.loadTasksFromStorage(tasks)
    self.inProgressColumn.loadTasksFromStorage(tasks)
    self.doneColumn.loadTasksFromStorage(tasks)

  def _handleTaskCreationRequest(self, column: KanbanColumn):
    """Handle a request to create a new task in a specific column."""
    task = self._taskManager.createTask("", "")
    dialog = FlashcardDetailsDialog(task, self)
    if dialog.exec() == QDialog.Accepted:
      # Save to storage
      self._storage.addTask(task)
      # Add to column
      column.addTask(task)
      column.createFlashcardForTask(task)
      column.taskCreated.emit(task.id)


