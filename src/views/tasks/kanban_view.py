from __future__ import annotations

from typing import List, Optional

from nicegui import ui

from ...data.task import Task
from .task_dialogs import addUpdateTaskDialog
from ...core.app_state import appState

ui.add_head_html("""
<style>
.dragging * {
  pointer-events: none !important;
}
.kanban-column {
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE and Edge */
}
.kanban-column::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Opera */
}
</style>
""")


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
    with self.classes(f"{self.unhighlighted} kanban-column w-96 max-w-[calc(32vw-8rem)] h-[calc(100vh-100px)] p-3 rounded-none overflow-y-auto"):
      ui.label(name).classes("text-bold ml-1 text-black font-bold uppercase tracking-wide sticky top-0 bg-white z-10 -mx-3 px-3 py-2 mb-2")
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
    draggedCard = appState.getDraggedCard()
    if draggedCard and not self == draggedCard.parent_slot.parent:
      draggedCard.parent_slot.parent.remove(draggedCard)
      draggedCard.task.status = self.name
      with self:
        Card(draggedCard.task)
    self._onDragLeave()
    appState.setDraggedCard(None)


class Card(ui.card):
  def __init__(self, task: Task) -> None:
    super().__init__()
    self.task = task
    
    with self.props("draggable").classes("w-full min-h-[160px] cursor-pointer hover:shadow-lg transition-shadow flex flex-col"):
      ui.label(task.title).classes("text-h6 font-semibold")
      if task.description:
        ui.label(task.description).classes("text-sm text-grey-8 -mt-2 flex-1")
      
      with ui.row().classes("w-full justify-between items-end mt-0 p-0 pt-0"):
        if task.startdate:
          with ui.row().classes("items-center gap-1"):
            ui.icon('event').classes('text-grey-6')
            ui.label(task.startdate).classes("text-sm text-grey-8")
        else:
          ui.space()
        
        with ui.row().classes("items-center gap-1"):
          ui.icon('schedule').classes('text-grey-6')
          ui.label(f"{task.duration}d").classes("text-sm text-grey-8")

    self.on("dragstart", self._onDragStart)
    self.on("dragend", self._onDragEnd)
    self.on("click", lambda: addUpdateTaskDialog(self.task))

  def _onDragStart(self) -> None:
    appState.setDraggedCard(self)

  def _onDragEnd(self) -> None:
    appState.setDraggedCard(None)