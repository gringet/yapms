from typing import Optional, Any


class AppState:
  def __init__(self):
    self.currentView = "tasks"
    self.currentTab = "Kanban"
    self.contentArea = None
    self.tabs = None
    self.tasksList = None
    self.draggedCard = None
  
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


appState = AppState()