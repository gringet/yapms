from typing import List, Dict

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea
from PySide6.QtCore import Qt, Signal

from flashcard import Flashcard
from task import Task
from data_storage import getDataStorage

class KanbanColumn(QWidget):
  taskCreationRequested = Signal()  # Request to create a new task
  taskCreated = Signal(str)  # Notify that a task was created (emit task ID)
  taskDeletionRequested = Signal(str)  # Request deletion of a task (emit task ID)
  flashcardsReordered = Signal(str, list)

  def __init__(self, columnId: str, title: str, parent=None):
    super().__init__(parent)

    storage = getDataStorage()
    self.flashcardsReordered.connect(storage.reorderKanban)

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
    flashcard = Flashcard(task)
    flashcard.deletionRequested.connect(self.taskDeletionRequested)
    self.addFlashcard(flashcard)

  def loadTasksFromStorage(self, tasks: Dict[str, Task]):
    """Load tasks into the column from storage."""
    storage = getDataStorage()
    ordering = storage.kanban[self._columnId]

    # Store task references
    for task in tasks.values():
      self._tasks[task.id] = task

    # Create flashcards in order
    for taskId in ordering[::-1]:
      if taskId in self._tasks:
        flashcard = Flashcard(self._tasks[taskId])
        flashcard.deletionRequested.connect(self.taskDeletionRequested)
        self._flashcardsLayout.insertWidget(0, flashcard)
        flashcard.kanbanColumn = self

  def addFlashcard(self, flashcard: Flashcard, position=None):
    if position is None:
      position = 0
    else:
      position = min(position, self._flashcardsLayout.count() - 1)
      position = max(0, position)

    self._flashcardsLayout.insertWidget(position, flashcard)
    flashcard.kanbanColumn = self
    self.handleReordering()

  def removeFlashcard(self, flashcard: Flashcard):
    self._flashcardsLayout.removeWidget(flashcard)
    flashcard.setParent(None)
    flashcard.kanbanColumn = None
    self.handleReordering()
  
  def handleReordering(self):
    ordering = list()
  
    for i in range(self._flashcardsLayout.count() - 1):
      flashcard: Flashcard = self._flashcardsLayout.itemAt(i).widget()
      ordering.append(flashcard.taskId)
    
    self.flashcardsReordered.emit(self._columnId, ordering)

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
      # Reordering
      if not dropIndex == currentIndex:
        self._flashcardsLayout.removeWidget(flashcard)
        # special case to handle when reordering at the end of the list
        if self._flashcardsLayout.count() == dropIndex:
          dropIndex -= 1
        self._flashcardsLayout.insertWidget(dropIndex, flashcard)
        self.handleReordering()
    else:
      # Column switch
      flashcard.kanbanColumn.removeFlashcard(flashcard)
      self.addFlashcard(flashcard, dropIndex)
      self.handleReordering()

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
