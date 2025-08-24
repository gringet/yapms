from dataclasses import dataclass

from nicegui import ui
from nicegui.observables import ObservableList

import database


tasks = ObservableList()


@dataclass
class Task:
  def __init__(self, id: int, title: str, description: str="", status: str="To Do", duration: int=1):
    self._id = id
    self._title = title
    self._description = description
    self._status = status
    self._duration = duration

  def dict(self):
    return {"id": self.id, "title": self.title, "description": self.description, "status": self.status,
            "duration": self.duration}

  @property
  def id(self):
    return self._id

  @property
  def title(self):
    return self._title

  @title.setter
  def title(self, title: str):
    database.updateTask(self._id, title=title)
    self._title = title

  @property
  def description(self):
    return self._description

  @description.setter
  def description(self, description: str):
    database.updateTask(self._id, description=description)
    self._description = description

  @property
  def status(self):
    return self._status

  @status.setter
  def status(self, status: str):
    database.updateTask(self._id, status=status)
    self._status = status

  @property
  def duration(self):
    return self._duration

  @duration.setter
  def duration(self, duration: int):
    database.updateTask(self._id, duration=duration)
    self._duration = duration


def addUpdateTaskDialog(task: Task=None):
  def addUpdateTask(title: str, description: str, duration: int):
    if task is None:
      taskId = database.addTask(title, description, "To Do", duration)
      tasks.append(Task(taskId, title, description, "To Do", duration))
    else:
      database.updateTask(task.id, title=title, description=description, duration=duration)

  with ui.dialog() as dialog, ui.card().classes("w-[32rem]"):
    title = ui.input("Title", value=task.title if task is not None else "").props("autofocus").classes("w-full")
    description = ui.textarea("Description", value=task.description if task is not None else "").classes('w-full')
    duration = ui.number("Duration (days)", value=task.duration if task is not None else 1, min=1, step=1).classes('w-full')
    with ui.row().classes("w-full justify-end"):
      ui.button("Cancel", on_click=dialog.close, color="secondary")
      ui.button("Save", on_click=lambda: (
        addUpdateTask(title.value, description.value, duration.value),
        dialog.close()
      ))
  dialog.open()