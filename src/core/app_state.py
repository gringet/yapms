from typing import Optional, Any


class AppState:
  def __init__(self):
    self.currentView = "tasks"
    self.currentTab = "Kanban"
    self.contentArea = None
    self.tabs = None
    self.tasksList = None
    self.draggedCard = None
    self.searchQuery = ""
  
  def setView(self, view: str):
    self.currentView = view
  
  def setTab(self, tab: str):
    self.currentTab = tab
  
  def setContentArea(self, contentArea):
    self.contentArea = contentArea
  
  def setTabs(self, tabs):
    self.tabs = tabs
  
  def setTasksList(self, tasksList):
    self.tasksList = tasksList
  
  def setDraggedCard(self, card):
    self.draggedCard = card
  
  def getDraggedCard(self):
    return self.draggedCard
  
  def setSearchQuery(self, query: str):
    self.searchQuery = query.lower().strip()
  
  def getSearchQuery(self):
    return self.searchQuery
  
  def filterTasks(self, tasks):
    """Filter tasks based on search query"""
    query = self.getSearchQuery()
    if not query:
      return tasks
    
    filtered = []
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

  def filterStakeholders(self, stakeholders):
    """Filter stakeholders for display in stakeholder view, excluding system stakeholder"""
    # Always exclude the "Not Assigned" system stakeholder from the stakeholder management view
    visible_stakeholders = [s for s in stakeholders if not (s.name == "Not" and s.surname == "Assigned")]
    
    # Apply search filtering only to visible stakeholders
    query = self.getSearchQuery()
    if not query:
      return visible_stakeholders
    
    filtered = []
    for stakeholder in visible_stakeholders:
      # Search in name, surname, email, and type
      searchable_text = f"{stakeholder.name} {stakeholder.surname} {stakeholder.email} {stakeholder.type}".lower()
      if query in searchable_text:
        filtered.append(stakeholder)
    
    return filtered


appState = AppState()