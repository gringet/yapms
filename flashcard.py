from typing import TYPE_CHECKING

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QDialog, QTextEdit, QPushButton, QLineEdit, QMenu
from PySide6.QtCore import Qt, QMimeData, Signal
from PySide6.QtGui import QDrag

if TYPE_CHECKING:
  from kanban_column import KanbanColumn

from task import Task


class FlashcardDetailsDialog(QDialog):

  def __init__(self, task: Task, parent: QWidget=None):
    self._task = task

    super().__init__(parent)
    self.setWindowTitle("Task Details")
    self.setModal(True)
    self.setMinimumSize(400, 300)

    layout = QVBoxLayout()

    layout.addWidget(QLabel("Title:"))
    self._title = QLineEdit(text=self._task.title)
    self._title.setText(self._task.title)
    layout.addWidget(self._title)

    layout.addWidget(QLabel("Description:"))
    self._description = QTextEdit()
    self._description.setPlainText(self._task.description)
    layout.addWidget(self._description)

    buttonLayout = QVBoxLayout()
    saveButton = QPushButton("Save")
    saveButton.setAutoDefault(False)
    saveButton.clicked.connect(self.accept)
    buttonLayout.addWidget(saveButton)

    cancelButton = QPushButton("Cancel")
    cancelButton.setAutoDefault(False)
    cancelButton.clicked.connect(self.reject)
    buttonLayout.addWidget(cancelButton)

    layout.addLayout(buttonLayout)
    self.setLayout(layout)

  def accept(self):
    self._task.title = self._title.text()
    self._task.description = self._description.toPlainText()
    return super().accept()


class Flashcard(QWidget):
  deletionRequested = Signal(str)  # Emits task ID

  def __init__(self, task: Task, parent: QWidget=None):
    super().__init__(parent)

    self._task = task
    self._kanbanColumn = None

    self.setAttribute(Qt.WA_StyledBackground, True)
    self.setFixedHeight(60)

    self.setStyleSheet("""
      Flashcard {
        border: 1px solid palette(text);
      }
      Flashcard:hover {
        border: 1px solid palette(highlight);
      }
      Flashcard[dragging="true"] {
        border: 1px solid palette(highlight);
      }
    """)

    layout = QVBoxLayout()

    titleLabel = QLabel(self._task.title)
    titleLabel.setWordWrap(True)
    layout.addWidget(titleLabel)
    self._task.titleChanged.connect(lambda: titleLabel.setText(self._task.title))

    self.setLayout(layout)
  
  @property
  def kanbanColumn(self) -> 'KanbanColumn':
    return self._kanbanColumn
  
  @kanbanColumn.setter
  def kanbanColumn(self, column: 'KanbanColumn'):
    self._kanbanColumn = column

  def mousePressEvent(self, event):
    if event.button() == Qt.LeftButton:
      self._dragStartPos = event.pos()

  def mouseMoveEvent(self, event):
    if not (event.buttons() & Qt.LeftButton):
      return

    if (event.pos() - self._dragStartPos).manhattanLength() < 10:
      return

    self.setProperty("dragging", "true")
    self.style().polish(self)

    drag = QDrag(self)
    mimeData = QMimeData()
    mimeData.setProperty("flashcard", self)
    drag.setMimeData(mimeData)
    drag.exec(Qt.MoveAction)

    self.setProperty("dragging", "false")
    self.style().polish(self)

  def mouseDoubleClickEvent(self, event):
    dialog = FlashcardDetailsDialog(self._task, self)
    dialog.exec()

  def contextMenuEvent(self, event):
    contextMenu = QMenu(self)

    editAction = contextMenu.addAction("Edit Task")
    deleteAction = contextMenu.addAction("Delete Task")

    action = contextMenu.exec(event.globalPos())

    if action == editAction:
      self._handleEdit()
    elif action == deleteAction:
      self._handleDelete()

  def _handleEdit(self):
    dialog = FlashcardDetailsDialog(self._task, self)
    dialog.exec()

  def _handleDelete(self):
    self.deletionRequested.emit(self._task.id)

  @property
  def taskId(self):
    return self._task.id

