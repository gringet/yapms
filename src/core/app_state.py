from __future__ import annotations
from typing import Any, Iterable, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
  from nicegui.observables import ObservableList
  from src.data.task import Task
  from src.data.stakeholder import Stakeholder


class AppState:
  def __init__(self) -> None:
    self.currentView: str = "tasks"
    self.currentTab: str = "Kanban"
    self.contentArea: Any = None
    self.tabs: Any = None
    self.tasksList: Optional[ObservableList[Task]] = None
    self.draggedCard: Any = None
    self.searchQuery: str = ""
  
  def setView(self, view: str) -> None:
    self.currentView = view
  
  def setTab(self, tab: str) -> None:
    self.currentTab = tab
  
  def setContentArea(self, contentArea: Any) -> None:
    self.contentArea = contentArea
  
  def setTabs(self, tabs: Any) -> None:
    self.tabs = tabs
  
  def setTasksList(self, tasksList: ObservableList[Task]) -> None:
    self.tasksList = tasksList
  
  def setDraggedCard(self, card: Any) -> None:
    self.draggedCard = card
  
  def getDraggedCard(self) -> Any:
    return self.draggedCard
  
  def setSearchQuery(self, query: str) -> None:
    self.searchQuery = query.lower().strip()
  
  def getSearchQuery(self) -> str:
    return self.searchQuery
  
  def filterTasks(self, tasks: Iterable[Task]) -> List[Task]:
    """Filter tasks based on search query"""
    query = self.getSearchQuery()
    if not query:
      return list(tasks)
  
    filtered: List[Task] = []
    for task in tasks:
      # Search in title, description, and status
      searchable_text = f"{task.title} {task.description} {task.status}".lower()
      
      # Also search in assigned stakeholder information
      from ..data.stakeholder import getStakeholderById
      stakeholder = getStakeholderById(task.assigned_stakeholder_id)
      if stakeholder:
        stakeholder_text = f"{stakeholder.name} {stakeholder.surname}".lower()
        if stakeholder.name == "Not" and stakeholder.surname == "Assigned":
          stakeholder_text += " not assigned unassigned"  # Add search aliases
        searchable_text += f" {stakeholder_text}"
      
      if query in searchable_text:
        filtered.append(task)
    
    return filtered

  def filterStakeholders(self, stakeholders: Iterable[Stakeholder]) -> List[Stakeholder]:
    """Filter stakeholders for display in stakeholder view, excluding system stakeholder"""
    # Always exclude the "Not Assigned" system stakeholder from the stakeholder management view
    visible_stakeholders = [s for s in stakeholders if not (s.name == "Not" and s.surname == "Assigned")]
    
    # Apply search filtering only to visible stakeholders
    query = self.getSearchQuery()
    if not query:
      return visible_stakeholders
    
    filtered: List[Stakeholder] = []
    for stakeholder in visible_stakeholders:
      # Search in name, surname, email, and type
      searchable_text = f"{stakeholder.name} {stakeholder.surname} {stakeholder.email} {stakeholder.type}".lower()
      if query in searchable_text:
        filtered.append(stakeholder)
    
    return filtered


appState = AppState()
