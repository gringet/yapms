from __future__ import annotations

from typing import List, Optional

from nicegui import ui

from task import Task, addUpdateTaskDialog

ui.add_head_html("""
<style>
.dragging * {
  pointer-events: none !important;
}
</style>
""")


dragged: Optional[Card] = None

@ui.refreshable
def build(tasks: List[Task]):
  with ui.row():
    for columnName in ["To Do", "In Progress", "Done"]:
      with Column(columnName):
        for task in [task for task in tasks if task.status == columnName]:
          Card(task)


class Column(ui.column):
  highlighted = "bg-gray-100 border-2 border-black"
  unhighlighted = "bg-white border border-gray-300"

  def __init__(self, name: str) -> None:
    super().__init__()
    with self.classes(f"{self.unhighlighted} w-96 max-w-[calc(32vw-8rem)] h-screen min-h-screen p-3 rounded-none"):
      ui.label(name).classes("text-bold ml-1 text-black font-bold uppercase tracking-wide")
    self.name = name
    self._dragCount = 0
    self.on("dragenter", self._onDragEnter)
    self.on("dragover.prevent", lambda: None)
    self.on("dragleave", self._onDragLeave)
    self.on("drop", self._onDrop)

  def _onDragEnter(self) -> None:
    self._dragCount += 1
    if self._dragCount == 1:
      self.classes(add="dragging")
      self.classes(remove=self.unhighlighted, add=self.highlighted)

  def _onDragLeave(self) -> None:
    self._dragCount -= 1
    if self._dragCount == 0:
      self.classes(remove="dragging")
      self.classes(remove=self.highlighted, add=self.unhighlighted)

  def _onDrop(self) -> None:
    global dragged  # pylint: disable=global-statement # noqa: PLW0603
    if not self == dragged.parent_slot.parent:
      dragged.parent_slot.parent.remove(dragged)
      dragged.task.status = self.name
      with self:
        Card(dragged.task)
    self._onDragLeave()
    dragged = None


class Card(ui.card):
  def __init__(self, task: Task) -> None:
    super().__init__()
    self.task = task
    with self.props("draggable").classes("w-full cursor-pointer bg-white border border-black rounded-none shadow-none hover:bg-gray-50"):
      ui.label(task.title).classes("text-weight-bold text-black")
      ui.label(task.description).classes("text-gray-600")
      if task.startdate:
        ui.label(f"Start: {task.startdate}").classes("text-gray-500 text-sm")
      with ui.row().classes("w-full justify-end items-center"):
        ui.icon("schedule").classes("text-black")
        ui.label(f"{task.duration} {'days' if task.duration > 1 else 'day'}").classes("text-black font-mono text-sm")

    self.on("dragstart", self._onDragStart)
    self.on("dragend", self._onDragEnd)
    self.on("click", lambda: addUpdateTaskDialog(self.task))

  def _onDragStart(self) -> None:
    global dragged  # pylint: disable=global-statement # noqa: PLW0603
    dragged = self

  def _onDragEnd(self) -> None:
    global dragged
    dragged = None