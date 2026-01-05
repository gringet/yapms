import uuid

from PySide6.QtCore import QObject, Signal

from data_storage import getDataStorage


class Task(QObject):
  titleChanged = Signal(str)
  descriptionChanged = Signal(str)

  def __init__(self, title: str, description: str, id: str=None):
    super().__init__()
    if id is None:
      self._id = str(uuid.uuid4())
    else:
      self._id = id
    self._title = title
    self._description = description

  @property
  def id(self) -> str:
    return self._id
  
  @property
  def title(self) -> str:
    return self._title

  @title.setter
  def title(self, value: str):
    self._title = value
    self.titleChanged.emit(value)
    getDataStorage().editTask(self)

  @property
  def description(self) -> str:
    return self._description

  @description.setter
  def description(self, value: str):
    self._description = value
    self.descriptionChanged.emit(value)
    getDataStorage().editTask(self)

