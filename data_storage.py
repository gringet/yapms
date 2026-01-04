import pickle
import os
from typing import Any, Dict, List, Tuple

from task import Task


class DataStorage:
  def __init__(self, filePath: str=".data.pkl"):
    self._filePath = filePath
  
    if not os.path.exists(self._filePath):
      self._data = self._empty()
    else:
      try:
        with open(self._filePath, "rb") as f:
          self._data = pickle.load(f)
      except:
        self._data = self._empty()
  
  @property
  def tasks(self) -> Dict[str, Dict[str, str]]:
    return self._data["tasks"]

  @property
  def kanban(self) -> Dict[str, List[str]]:
    return self._data["kanban"]

  def _empty(self):
    return {
      "tasks": dict(),
      "kanban": {"todo": list(), "in_progress": list(), "done": list()}
    }

  def addTask(self, task: Task):
    self._data["tasks"][task.id] = {
      "id": task.id,
      "title": task.title,
      "description": task.description
    }
    self.save()

  def reorderKanban(self, columnId: str, ordering: List[str]):
    self._data["kanban"][columnId] = ordering
    self.save()

  def save(self) -> bool:
    try:
      with open(self._filePath, "wb") as f:
        pickle.dump(self._data, f)
      return True
    except:
      return False


_storageInstance = None


def getDataStorage(filePath: str=".data.pkl") -> DataStorage:
  global _storageInstance
  if _storageInstance is None:
    _storageInstance = DataStorage(filePath)
  return _storageInstance