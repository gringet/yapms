from PySide6.QtWidgets import QWidget, QHBoxLayout

from kanban_column import KanbanColumn


class KanbanBoard(QWidget):
  def __init__(self):
    super().__init__()

    mainLayout = QHBoxLayout()

    self.todoColumn = KanbanColumn("todo", "To Do")
    mainLayout.addWidget(self.todoColumn)

    self.inProgressColumn = KanbanColumn("in_progress", "In Progress")
    mainLayout.addWidget(self.inProgressColumn)

    self.doneColumn = KanbanColumn("done", "Done")
    mainLayout.addWidget(self.doneColumn)

    self.setLayout(mainLayout)

