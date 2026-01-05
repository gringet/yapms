import uuid

from PySide6.QtCore import QObject, Signal

from data_storage import getDataStorage


class Task(QObject):
  titleChanged = Signal(str)
  descriptionChanged = Signal(str)

  def __init__(self, title: str, description: str, taskId: str=None):
    super().__init__()
    if taskId is None:
      self._id = str(uuid.uuid4())
    else:
      self._id = taskId
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


# class TaskManager(QObject):
#   taskAdded = Signal(Task)
#   taskUpdated = Signal(Task)

#   def __init__(self):
#     super().__init__()
#     self._tasks: List[Task] = list()

#   def addTask(self, task: Task):
#     self._tasks.append(task)
#     task.titleChanged.connect(lambda: self.taskUpdated.emit(task))
#     task.descriptionChanged.connect(lambda: self.taskUpdated.emit(task))

#   def getTask(self):
#     return self._tasks