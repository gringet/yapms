import uuid

from PySide6.QtCore import QObject, Signal

from data_storage import getDataStorage


class Task(QObject):
  titleChanged = Signal(str)
  descriptionChanged = Signal(str)
  statusChanged = Signal(str)
  orderingChanged = Signal(int)

  def __init__(self, title: str, description: str, id: str=None, status: str="todo", ordering: int=0):
    super().__init__()
    if id is None:
      self._id = str(uuid.uuid4())
    else:
      self._id = id
    self._title = title
    self._description = description
    self._status = status
    self._ordering = ordering

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

  @property
  def status(self) -> str:
    return self._status

  @status.setter
  def status(self, value: str):
    if self._status != value:
      self._status = value
      self.statusChanged.emit(value)
      getDataStorage().editTask(self)

  @property
  def ordering(self) -> int:
    return self._ordering

  @ordering.setter
  def ordering(self, value: int):
    if self._ordering != value:
      self._ordering = value
      self.orderingChanged.emit(value)
      getDataStorage().editTask(self)

