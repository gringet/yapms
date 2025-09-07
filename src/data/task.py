from __future__ import annotations
from dataclasses import dataclass
import datetime
from nicegui.observables import ObservableList
from . import database
from typing import Callable, Dict, Any, Tuple, Optional


tasks: ObservableList = ObservableList()


@dataclass
class Task:
  def __init__(self, id: int, title: str, description: str = "", status: str = "Backlog", effort: int = 1, startdate: Optional[str] = None, assigned_stakeholder_id: Optional[int] = None, sort_key: Optional[float] = None, onChange: Callable | None = None) -> None:
    self._id = id
    self._title = title
    self._description = description
    self._status = status
    self._effort = effort
    self._startdate = startdate
    self._assigned_stakeholder_id = assigned_stakeholder_id if assigned_stakeholder_id is not None else 1
    self._sort_key = sort_key if sort_key is not None else float(id)
    self._onChange = onChange

  def dict(self) -> Dict[str, Any]:
    return {"id": self.id, "title": self.title, "description": self.description, "status": self.status,
            "effort": self.effort, "startdate": self.startdate, "assigned_stakeholder_id": self.assigned_stakeholder_id, "sort_key": self.sort_key}

  @property
  def id(self) -> int:
    return self._id

  @property
  def title(self) -> str:
    return self._title

  def _update_field(self, field_name: str, new_value: Any, current_value: Any) -> None:
    if current_value == new_value:
      return
    database.updateTask(self._id, **{field_name: new_value})
    setattr(self, f"_{field_name}", new_value)
    if self._onChange:
      self._onChange()

  @title.setter
  def title(self, title: str) -> None:
    self._update_field("title", title, self._title)

  @property
  def description(self) -> str:
    return self._description

  @description.setter
  def description(self, description: str) -> None:
    self._update_field("description", description, self._description)

  @property
  def status(self) -> str:
    return self._status

  @status.setter
  def status(self, status: str) -> None:
    self._update_field("status", status, self._status)

  @property
  def effort(self) -> int:
    return self._effort

  @effort.setter
  def effort(self, effort: int) -> None:
    self._update_field("effort", effort, self._effort)

  @property
  def startdate(self) -> Optional[str]:
    return self._startdate

  @startdate.setter
  def startdate(self, startdate: Optional[str]) -> None:
    self._update_field("startdate", startdate, self._startdate)

  @property
  def assigned_stakeholder_id(self) -> int:
    return self._assigned_stakeholder_id

  @assigned_stakeholder_id.setter
  def assigned_stakeholder_id(self, assigned_stakeholder_id: int) -> None:
    self._update_field("assigned_stakeholder_id", assigned_stakeholder_id, self._assigned_stakeholder_id)

  @property
  def sort_key(self) -> float:
    return self._sort_key

  @sort_key.setter
  def sort_key(self, sort_key: float) -> None:
    self._update_field("sort_key", sort_key, self._sort_key)


def addUpdateTask(task: Task | None, title: str, description: str, effort: int, startdate: Optional[str], assigned_stakeholder_id: int = 1) -> tuple[bool, str]:
  """Pure business logic for adding/updating tasks without UI dependencies"""
  if not title.strip():
    return False, "Task title cannot be empty"
  if effort <= 0:
    return False, "Effort must be a positive integer"
  
  # Check if task is in active status and requires start date
  if task and task.status in ["To Do", "In Progress", "Done"] and (not startdate or not startdate.strip()):
    return False, "Tasks in active status must have a start date"
  
  # Validate start date only if provided
  if startdate and startdate.strip():
    try:
      parts = startdate.split('-')
      if len(parts) == 3:
        year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
        # Validate the date exists
        datetime.date(year, month, day)
        # Format with zero-padding
        startdate = f"{year:04d}-{month:02d}-{day:02d}"
      else:
        raise ValueError
    except (ValueError, TypeError):
      return False, "Invalid date format"
  else:
    # Allow empty start date only for new tasks or backlog tasks
    startdate = None
    
  if task is None:
    taskId = database.addTask(title, description, "Backlog", effort, startdate, assigned_stakeholder_id)
    if taskId:
      tasks.append(Task(taskId, title, description, "Backlog", effort, startdate, assigned_stakeholder_id, float(taskId)))
  else:
    task.title = title
    task.description = description
    task.effort = effort
    task.startdate = startdate
    task.assigned_stakeholder_id = assigned_stakeholder_id
  return True, "Success"
