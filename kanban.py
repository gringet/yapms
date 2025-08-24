from __future__ import annotations

from typing import List, Optional

from nicegui import ui

from task import Task


dragged: Optional[Card] = None

@ui.refreshable
def build(tasks: List[Task]):
  with ui.row():
    for columnName in ["To Do", "In Progress", "Done"]:
      with Column(columnName):
        for task in [task for task in tasks if task._status == columnName]:
          Card(task)


class Column(ui.column):
  highlighted = "bg-blue-grey-2"
  unhighlighted = "bg-blue-grey-3"

  def __init__(self, name: str) -> None:
    super().__init__()
    with self.classes(f"{self.highlighted} w-96 full-height p-3 rounded"):
      ui.label(name).classes("text-bold ml-1")
    self.name = name
    self.on("dragover.prevent", self.highlight)
    self.on("dragleave", self.unhighlight)
    self.on("drop", self.moveCard)

  def highlight(self) -> None:
    self.classes(remove=self.highlighted, add=self.unhighlighted)

  def unhighlight(self) -> None:
    self.classes(remove=self.unhighlighted, add=self.highlighted)

  def moveCard(self) -> None:
    global dragged  # pylint: disable=global-statement # noqa: PLW0603
    self.unhighlight()
    dragged.parent_slot.parent.remove(dragged)
    with self:
      Card(dragged.task)
    dragged.task.status = self.name
    dragged = None


class Card(ui.card):
  def __init__(self, task: Task) -> None:
    super().__init__()
    self.task = task
    with self.props("draggable").classes("w-full cursor-pointer bg-grey-1"):
      ui.label(task._title).classes("text-weight-bold")
      ui.label(task._description)
    self.on("dragstart", self.handleDragStart)

  def handleDragStart(self) -> None:
    global dragged  # pylint: disable=global-statement # noqa: PLW0603
    dragged = self