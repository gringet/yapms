from __future__ import annotations

from typing import List, Optional

from nicegui import ui

from ...data.task import Task
from ...data.stakeholder import getStakeholderById
from .dialogs import addUpdateTaskDialog
from ...core.app_state import appState
from ...core.styles import KanbanColumn, Kanban, Card as CardStyles, applyGlobalStyles

applyGlobalStyles()


@ui.refreshable
def build(tasks: List[Task]):
  filtered_tasks = appState.filterTasks(tasks)
  with ui.row().classes("w-full flex flex-nowrap"):
    for columnName in ["Backlog", "To Do", "In Progress", "Done"]:
      with Column(columnName):
        column_tasks = sorted([task for task in filtered_tasks if task.status == columnName], key=lambda t: t.sort_key)
        for task in column_tasks:
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
    from ...data import database
    draggedCard = appState.getDraggedCard()
    if draggedCard and not self == draggedCard.parent_slot.parent:
      # Check if task has start date for active statuses
      if self.name in ["To Do", "In Progress", "Done"] and not draggedCard.task.startdate:
        ui.notify("Tasks must have a start date to be moved to active status", type="warning")
        self._onDragLeave()
        appState.setDraggedCard(None)
        return
      
      # Get current tasks in this column to determine position
      current_tasks = [task for task in appState.tasksList if task.status == self.name and task.id != draggedCard.task.id]
      current_tasks.sort(key=lambda t: t.sort_key)
      
      # For now, add to the end. Later we can implement more sophisticated positioning
      new_position = len(current_tasks)
      
      # Use reorderTask to update sort_key and status
      database.reorderTask(draggedCard.task.id, new_position, self.name)
      
      # Update the task object
      draggedCard.task.status = self.name
      # Get updated sort_key from database
      updated_task = database.getTask(draggedCard.task.id)
      if updated_task:
        draggedCard.task.sort_key = updated_task['sort_key']
      
      # Remove old card and create new one
      draggedCard.parent_slot.parent.remove(draggedCard)
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
      
      with ui.row().classes(Kanban.TASK_ROW + " items-center"):
        # Startdate and Effort together
        if task.startdate:
          with ui.row().classes(Kanban.TASK_ICON_ROW):
            ui.icon('event').classes(Kanban.TASK_ICON)
            ui.label(task.startdate).classes(Kanban.TASK_LABEL)
        
        with ui.row().classes(Kanban.TASK_ICON_ROW):
          ui.icon('schedule').classes(Kanban.TASK_ICON)
          ui.label(f"{task.effort}d").classes(Kanban.TASK_LABEL)

        # Space between info and assignee
        ui.space()
        
        # Assignee on the right
        stakeholder = getStakeholderById(task.assigned_stakeholder_id)
        if stakeholder:
          ui.label(stakeholder.getAcronym()).style('background-color: white; font-size: 0.9rem; color: black; padding: 1px 6px; display: inline-block; text-align: center; font-weight: 600;')

    self.on("dragstart", self._onDragStart)
    self.on("dragend", self._onDragEnd)
    self.on("click", lambda: addUpdateTaskDialog(self.task))

  def _onDragStart(self) -> None:
    appState.setDraggedCard(self)

  def _onDragEnd(self) -> None:
    appState.setDraggedCard(None)