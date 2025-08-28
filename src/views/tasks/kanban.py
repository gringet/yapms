from __future__ import annotations

from typing import List, Optional

from nicegui import ui

from ...data.task import Task
from .dialogs import addUpdateTaskDialog
from ...core.app_state import appState
from ...core.styles import KanbanColumn, Kanban, Card as CardStyles, applyGlobalStyles

applyGlobalStyles()


@ui.refreshable
def build(tasks: List[Task]):
  with ui.row():
    for columnName in ["Backlog", "To Do", "In Progress", "Done"]:
      with Column(columnName):
        for task in [task for task in tasks if task.status == columnName]:
          Card(task)


class Column(ui.column):
  highlighted = KanbanColumn.HIGHLIGHTED
  unhighlighted = KanbanColumn.UNHIGHLIGHTED

  def __init__(self, name: str) -> None:
    super().__init__()
    with self.classes(f"{self.unhighlighted} kanban-column {KanbanColumn.BASE}"):
      ui.label(name).classes(Kanban.COLUMN_HEADER)
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
    
    with self.props("draggable").classes(CardStyles.DRAGGABLE):
      ui.label(task.title).classes(Kanban.TASK_TITLE)
      if task.description:
        ui.label(task.description).classes(Kanban.TASK_DESCRIPTION)
      
      with ui.row().classes(Kanban.TASK_ROW):
        if task.startdate:
          with ui.row().classes(Kanban.TASK_ICON_ROW):
            ui.icon('event').classes(Kanban.TASK_ICON)
            ui.label(task.startdate).classes(Kanban.TASK_LABEL)
        else:
          ui.space()
        
        with ui.row().classes(Kanban.TASK_ICON_ROW):
          ui.icon('schedule').classes(Kanban.TASK_ICON)
          ui.label(f"{task.duration}d").classes(Kanban.TASK_LABEL)

    self.on("dragstart", self._onDragStart)
    self.on("dragend", self._onDragEnd)
    self.on("click", lambda: addUpdateTaskDialog(self.task))

  def _onDragStart(self) -> None:
    appState.setDraggedCard(self)

  def _onDragEnd(self) -> None:
    appState.setDraggedCard(None)