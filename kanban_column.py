from typing import Dict

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea
from PySide6.QtCore import Qt, Signal

from flashcard import Flashcard
from task import Task

class KanbanColumn(QWidget):
  taskCreationRequested = Signal()  # Request to create a new task
  taskCreated = Signal(str)  # Notify that a task was created (emit task ID)
  taskDeletionRequested = Signal(str)  # Request deletion of a task (emit task ID)

  def __init__(self, columnId: str, title: str, parent=None):
    super().__init__(parent)

    self._columnId = columnId
    self._tasks: Dict[str, Task] = {}

    self.setAcceptDrops(True)
    self.setMinimumWidth(300)

    layout = QVBoxLayout()

    headerLayout = QVBoxLayout()
    titleLabel = QLabel(title)
    titleLabel.setStyleSheet("font-size: 13pt")
    headerLayout.addWidget(titleLabel)

    addButton = QPushButton("+ Add Task")
    addButton.clicked.connect(self._handleAddTask)
    headerLayout.addWidget(addButton)

    layout.addLayout(headerLayout)

    scrollArea = QScrollArea()
    scrollArea.setWidgetResizable(True)

    self._flashcardsWidget = QWidget()
    self._flashcardsLayout = QVBoxLayout()
    self._flashcardsLayout.setSpacing(8)
    self._flashcardsLayout.addStretch()
    self._flashcardsWidget.setLayout(self._flashcardsLayout)

    scrollArea.setWidget(self._flashcardsWidget)
    layout.addWidget(scrollArea)

    self.setLayout(layout)

  def _handleAddTask(self):
    self.taskCreationRequested.emit()

  def addTask(self, task: Task):
    """Add a task to this column's internal registry."""
    self._tasks[task.id] = task

  def createFlashcardForTask(self, task: Task):
    """Create and add a flashcard for the given task."""
    # Set ordering to add at the top (position 0)
    task.ordering = 0
    flashcard = Flashcard(task)
    flashcard.deletionRequested.connect(self.taskDeletionRequested)
    self.addFlashcard(flashcard)
    # Update ordering for all existing tasks
    self.updateTaskOrdering()

  def loadTasksFromStorage(self, tasks: Dict[str, Task]):
    """Load tasks into the column that match this column's status."""
    # Filter tasks that belong to this column
    columnTasks = [task for task in tasks.values() if task.status == self._columnId]

    # Sort by ordering
    columnTasks.sort(key=lambda t: t.ordering)

    # Create flashcards in order
    for task in columnTasks:
      self._tasks[task.id] = task
      flashcard = Flashcard(task)
      flashcard.deletionRequested.connect(self.taskDeletionRequested)
      self._flashcardsLayout.insertWidget(self._flashcardsLayout.count() - 1, flashcard)
      flashcard.kanbanColumn = self

  def addFlashcard(self, flashcard: Flashcard, position=None):
    if position is None:
      position = 0
    else:
      position = min(position, self._flashcardsLayout.count() - 1)
      position = max(0, position)

    self._flashcardsLayout.insertWidget(position, flashcard)
    flashcard.kanbanColumn = self

    # Update task status when flashcard is added to this column
    task = self._tasks.get(flashcard.taskId)
    if task and task.status != self._columnId:
      task.status = self._columnId

  def removeFlashcard(self, flashcard: Flashcard):
    self._flashcardsLayout.removeWidget(flashcard)
    flashcard.setParent(None)
    flashcard.kanbanColumn = None

  def updateTaskOrdering(self):
    """Update the ordering field for all tasks in this column based on their position."""
    for i in range(self._flashcardsLayout.count() - 1):
      flashcard = self._flashcardsLayout.itemAt(i).widget()
      task = self._tasks.get(flashcard.taskId)
      if task:
        task.ordering = i

  def dragEnterEvent(self, event):
    if event.mimeData().property("flashcard") is not None:
      event.acceptProposedAction()

  def dragMoveEvent(self, event):
    if event.mimeData().property("flashcard") is not None:
      event.acceptProposedAction()

  def dropEvent(self, event):
    flashcard: Flashcard = event.mimeData().property("flashcard")

    if flashcard is None:
      return

    dropIndex = self._getDropIndex(event)
    currentIndex = self._flashcardsLayout.indexOf(flashcard)

    if currentIndex >= 0:
      # Reordering within same column
      if not dropIndex == currentIndex:
        self._flashcardsLayout.removeWidget(flashcard)
        # special case to handle when reordering at the end of the list
        if self._flashcardsLayout.count() == dropIndex:
          dropIndex -= 1
        self._flashcardsLayout.insertWidget(dropIndex, flashcard)
        # Update ordering for all tasks in this column
        self.updateTaskOrdering()
    else:
      # Moving to different column
      oldColumn = flashcard.kanbanColumn

      # Get the task before removing from old column
      task = oldColumn._tasks.get(flashcard.taskId)

      # Remove from old column
      oldColumn.removeFlashcard(flashcard)
      if flashcard.taskId in oldColumn._tasks:
        del oldColumn._tasks[flashcard.taskId]

      # Update ordering in old column
      oldColumn.updateTaskOrdering()

      # Add to this column
      if task:
        self._tasks[task.id] = task
      self.addFlashcard(flashcard, dropIndex)

      # Update ordering in new column
      self.updateTaskOrdering()

    event.acceptProposedAction()

  def _getDropIndex(self, event) -> int:
    nFlashcards = self._flashcardsLayout.count() - 1
    if nFlashcards < 1:
      return 0

    pos = event.pos()
    dropPos = self._flashcardsWidget.mapFrom(self, pos)

    for i in range(nFlashcards):
      flashcard = self._flashcardsLayout.itemAt(i).widget()
      if dropPos.y() < flashcard.pos().y() + flashcard.height():
        return i

    return nFlashcards

  def handleTaskDeletion(self, taskId: str):
    """Remove the flashcard for the given task ID."""
    # Remove from internal registry
    if taskId in self._tasks:
      del self._tasks[taskId]

    # Find and remove the flashcard widget
    for i in range(self._flashcardsLayout.count() - 1):
      flashcard = self._flashcardsLayout.itemAt(i).widget()
      if flashcard.taskId == taskId:
        self.removeFlashcard(flashcard)
        flashcard.deleteLater()
        break
