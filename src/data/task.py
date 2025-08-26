from dataclasses import dataclass
import datetime
from nicegui.observables import ObservableList
from . import database
from typing import Callable


tasks = ObservableList()


@dataclass
class Task:
  def __init__(self, id: int, title: str, description: str="", status: str="To Do", duration: int=1, startdate: str=None, onChange: Callable=None):
    self._id = id
    self._title = title
    self._description = description
    self._status = status
    self._duration = duration
    self._startdate = startdate
    self._onChange = onChange

  def dict(self):
    return {"id": self.id, "title": self.title, "description": self.description, "status": self.status,
            "duration": self.duration, "startdate": self.startdate}

  @property
  def id(self):
    return self._id

  @property
  def title(self):
    return self._title

  def _update_field(self, field_name: str, new_value, current_value):
    if current_value == new_value:
      return
    database.updateTask(self._id, **{field_name: new_value})
    setattr(self, f"_{field_name}", new_value)
    if self._onChange:
      self._onChange()

  @title.setter
  def title(self, title: str):
    self._update_field("title", title, self._title)

  @property
  def description(self):
    return self._description

  @description.setter
  def description(self, description: str):
    self._update_field("description", description, self._description)

  @property
  def status(self):
    return self._status

  @status.setter
  def status(self, status: str):
    self._update_field("status", status, self._status)

  @property
  def duration(self):
    return self._duration

  @duration.setter
  def duration(self, duration: int):
    self._update_field("duration", duration, self._duration)

  @property
  def startdate(self):
    return self._startdate

  @startdate.setter
  def startdate(self, startdate: str):
    self._update_field("startdate", startdate, self._startdate)


def addUpdateTask(task: Task, title: str, description: str, duration: int, startdate: str) -> bool:
  """Pure business logic for adding/updating tasks without UI dependencies"""
  if not title.strip():
    return False, "Task title cannot be empty"
  if duration <= 0:
    return False, "Duration must be a positive integer"
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
    
  if task is None:
    taskId = database.addTask(title, description, "To Do", duration, startdate)
    if taskId:
      tasks.append(Task(taskId, title, description, "To Do", duration, startdate))
  else:
    task.title = title
    task.description = description
    task.duration = duration
    task.startdate = startdate
  return True, "Success"