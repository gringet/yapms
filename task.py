from dataclasses import dataclass
import datetime

from nicegui import ui
from nicegui.observables import ObservableList

import database

from typing import Callable


tasks = ObservableList()


def openDatePickerDialog(inputField: ui.input, currentValue=None):
  """Opens a date picker dialog and updates the input field with the selected date"""
  with ui.dialog() as dateDialog, ui.card().classes("bg-white border-2 border-black rounded-none shadow-none"):
    ui.label("Select Date").classes("text-lg font-bold text-black mb-4")
    datePicker = ui.date(value=currentValue or inputField.value).props("minimal")
    with ui.row().classes("w-full justify-end mt-4"):
      ui.button("Cancel", on_click=dateDialog.close).classes("bg-white text-black border border-black rounded-none hover:bg-gray-100 mr-2")
      ui.button("Select", on_click=lambda: (
        setattr(inputField, 'value', datePicker.value),
        dateDialog.close()
      )).classes("bg-black text-white border border-black rounded-none hover:bg-gray-800")
  dateDialog.open()


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


def addUpdateTaskDialog(task: Task=None):
  def _addUpdateTask(*args):
    if addUpdateTask(*args):
      dialog.close()

  with ui.dialog() as dialog, ui.card().classes("w-[48rem] bg-white border-2 border-black rounded-none shadow-none"):
    title = ui.input("Title", value=task.title if task is not None else "").props("autofocus outlined").classes("w-full")
    description = ui.textarea("Description", value=task.description if task is not None else "").props("outlined").classes('w-full')
    defaultDate = task.startdate if task is not None else datetime.date.today().strftime('%Y-%m-%d')
    
    with ui.row().classes("w-full items-end"):
      startdate = ui.input("Start Date", value=defaultDate).props("outlined").classes("flex-grow")
      ui.button("Select Date", on_click=lambda: openDatePickerDialog(startdate)).classes("bg-white text-black border border-black rounded-none hover:bg-gray-100 ml-2")
    duration = ui.number("Duration (days)", value=task.duration if task is not None else 1, min=1, step=1).props("outlined").classes('w-full')
    with ui.row().classes("w-full justify-end"):
      ui.button("Cancel", on_click=dialog.close).classes("bg-white text-black border border-black rounded-none hover:bg-gray-100")
      ui.button("Save", on_click=lambda: (
        _addUpdateTask(task, title.value, description.value, duration.value, startdate.value)
      )).classes("bg-black text-white border border-black rounded-none hover:bg-gray-800")
  dialog.open()


def addUpdateTask(task: Task, title: str, description: str, duration: int, startdate: str) -> bool:
  if not title.strip():
    ui.notify("Task title cannot be empty", type="negative")
    return False
  if duration <= 0:
    ui.notify("Duration must be a positive integer", type="negative") 
    return False
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
    ui.notify("Invalid date format", type="negative")
    return False
    
  if task is None:
    taskId = database.addTask(title, description, "To Do", duration, startdate)
    if taskId:
      tasks.append(Task(taskId, title, description, "To Do", duration, startdate))
  else:
    task.title = title
    task.description = description
    task.duration = duration
    task.startdate = startdate
  return True