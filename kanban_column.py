from typing import List

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QDialog, QLineEdit, QTextEdit
from PySide6.QtCore import Qt, Signal

from flashcard import Flashcard, FlashcardDetailsDialog
from task import Task

from data_storage import getDataStorage

class KanbanColumn(QWidget):
  taskCreated = Signal(Task)
  flashcardsReordered = Signal(str, list)

  def __init__(self, columnId: str, title: str, parent=None):
    super().__init__(parent)

    storage = getDataStorage()
    self.taskCreated.connect(storage.addTask)
    self.flashcardsReordered.connect(storage.reorderKanban)

    self._columnId = columnId

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
  
    self._loadFromStorage()

  def _handleAddTask(self):
    task = Task("", "")
    dialog = FlashcardDetailsDialog(task, self)
    if dialog.exec() == QDialog.Accepted:
      self.taskCreated.emit(task)
      self.addFlashcard(Flashcard(task))

  def _loadFromStorage(self):
    storage = getDataStorage()
    tasks = storage.tasks
    ordering = storage.kanban[self._columnId]

    for taskId in ordering[::-1]:
      task = tasks[taskId]
      task = Task(task["title"], task["description"], task["id"])
      flashcard = Flashcard(task)
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
    else:
      # Column switch
      flashcard.kanbanColumn.removeFlashcard(flashcard)
      self.addFlashcard(flashcard, dropIndex)

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
