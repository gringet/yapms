from typing import TYPE_CHECKING

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QDialog, QTextEdit, QPushButton, QLineEdit
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag

from task import Task

if TYPE_CHECKING:
  from kanban_column import KanbanColumn


class FlashcardDetailsDialog(QDialog):

  def __init__(self, task: Task, parent: QWidget=None):
    self._task = task
    
    super().__init__(parent)
    self.setWindowTitle("Task Details")
    self.setModal(True)
    self.setMinimumSize(400, 300)

    layout = QVBoxLayout()

    layout.addWidget(QLabel("<b>Title:</b>"))
    self._title = QLineEdit(text=task.title)
    self._title.setText(task.title)
    layout.addWidget(self._title)

    layout.addWidget(QLabel("<b>Description:</b>"))
    self._description = QTextEdit()
    self._description.setPlainText(task.description)
    layout.addWidget(self._description)

    buttonLayout = QVBoxLayout()
    saveButton = QPushButton("Save")
    saveButton.clicked.connect(self.accept)
    buttonLayout.addWidget(saveButton)

    cancelButton = QPushButton("Cancel")
    cancelButton.clicked.connect(self.reject)
    buttonLayout.addWidget(cancelButton)

    layout.addLayout(buttonLayout)
    self.setLayout(layout)

  def accept(self):
    self._task.title = self._title.text()
    self._task.description = self._description.toPlainText()
    return super().accept()


class Flashcard(QWidget):

  def __init__(self, task: Task, parent: QWidget=None):
    self._task = task
    self._kanbanColumn = None
    
    super().__init__(parent)
    self.setAttribute(Qt.WA_StyledBackground, True)
    self.setFixedHeight(40)
    self.setStyleSheet("""
      Flashcard {
        background-color: white;
        border: 2px solid #ccc;
        border-radius: 6px;
      }
      Flashcard:hover {
        background-color: #f0f0f0;
        border: 2px solid #999;
      }
    """)

    layout = QVBoxLayout()

    titleLabel = QLabel(task.title)
    titleLabel.setWordWrap(True)
    titleLabel.setStyleSheet("font-weight: bold;")
    layout.addWidget(titleLabel)
    task.titleChanged.connect(lambda: titleLabel.setText(task.title))

    self.setLayout(layout)
  
  @property
  def kanbanColumn(self) -> KanbanColumn:
    return self._kanbanColumn
  
  @kanbanColumn.setter
  def kanbanColumn(self, column: KanbanColumn):
    self._kanbanColumn = column

  def mousePressEvent(self, event):
    if event.button() == Qt.LeftButton:
      self._dragStartPos = event.pos()

  def mouseMoveEvent(self, event):
    if not (event.buttons() & Qt.LeftButton):
      return

    if (event.pos() - self._dragStartPos).manhattanLength() < 10:
      return

    drag = QDrag(self)
    mimeData = QMimeData()
    mimeData.setProperty("flashcard", self)
    drag.setMimeData(mimeData)
    drag.exec(Qt.MoveAction)

  def mouseDoubleClickEvent(self, event):
    dialog = FlashcardDetailsDialog(self._task, self)
    dialog.exec()

  @property
  def taskId(self):
    return self._task.id

