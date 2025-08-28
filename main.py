#!/usr/bin/env python3
"""
Project Manager Application - New Organized Structure
Entry point for the reorganized codebase
"""

import os
import sys
import time
from nicegui import ui

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import modules from organized structure
from src.data import database
from src.data.task import Task, tasks
from src.data.stakeholder import Stakeholder, stakeholders
from src.views.tasks.dialogs import addUpdateTaskDialog
from src.views.tasks import build_tasks as tasks_build
from src.views.stakeholder import build as stakeholder_build, addStakeholderDialog
from src.core.app_state import appState

if not os.path.exists(database.DB_FILE):
  database.createDummy()
else:
  database._migrateDatabase()

def refresher():
  from src.views.tasks import build_kanban, build_task_list
  from src.views.stakeholder import stakeholder_view
  build_kanban.refresh()
  build_task_list.refresh()
  if hasattr(stakeholder_view, 'build'):
    stakeholder_view.build.refresh()

def refreshCurrentView():
  if appState.currentView == "tasks":
    appState.contentArea.clear()
    with appState.contentArea:
      tasks_build(appState.tasksList, appState.currentTab)
  elif appState.currentView == "stakeholder":
    appState.contentArea.clear()
    with appState.contentArea:
      stakeholder_build()

# Use the ObservableList from task module
tasks.extend([Task(**dict(t), onChange=refresher) for t in database.getTasks()])
appState.setTasksList(tasks)

# Load stakeholders from database
stakeholders.extend([Stakeholder(**dict(s), onChange=refresher) for s in database.getStakeholders()])

ui.add_head_html('<script src="https://cdn.jsdelivr.net/npm/frappe-gantt@0.6.1/dist/frappe-gantt.min.js"></script>')

with ui.header().classes(replace="column bg-black text-white").style("min-height: 48px") as header:
  with ui.row().classes("w-full items-center flex-wrap").style("min-height: 48px"):
    ui.button(on_click=lambda: leftDrawer.toggle(), icon="menu").props("flat color=white")
    with ui.tabs() as tabs:
      kanbanTab = ui.tab("Kanban").classes("text-white")
      ganttTab = ui.tab("Gantt").classes("text-white")
      listTab = ui.tab("List").classes("text-white")
    ui.space()
    
    class SearchHandler:
      def __init__(self):
        self.timer = None
      
      def onSearchChange(self, e):
        if self.timer:
          self.timer.cancel()
        
        def performSearch():
          appState.setSearchQuery(e.args)
          refreshCurrentView()
        
        self.timer = ui.timer(0.2, performSearch, once=True)
    
    searchHandler = SearchHandler()
    searchInput = ui.input(placeholder="Search...").props("outlined dense dark").classes("mr-4").style("min-width: 350px;")
    searchInput.on('update:model-value', searchHandler.onSearchChange)
    
    def handleAddButton():
      if appState.currentView == "tasks":
        addUpdateTaskDialog()
      elif appState.currentView == "stakeholder":
        addStakeholderDialog()
    
    ui.button(icon="add", on_click=handleAddButton).classes("mr-3 text-black bg-white").props("round size=12px")

appState.setTabs(tabs)

def onTabChange():
  appState.setTab(tabs.value)
  if appState.currentView == "tasks":
    appState.contentArea.clear()
    with appState.contentArea:
      tasks_build(appState.tasksList, appState.currentTab)

tabs.on('update:model-value', onTabChange)

with ui.left_drawer().classes("bg-white border-r border-black") as leftDrawer:
  with ui.column().classes("w-full gap-0"):
    def showTasks():
      appState.setView("tasks")
      appState.tabs.set_visibility(True)
      appState.contentArea.clear()
      with appState.contentArea:
        tasks_build(appState.tasksList, appState.currentTab)
    
    def showStakeholder():
      appState.setView("stakeholder")
      appState.tabs.set_visibility(False)
      appState.contentArea.clear()  
      with appState.contentArea:
        stakeholder_build()
    
    with ui.button(on_click=showStakeholder).classes("w-full justify-start pl-2").props("flat color=black"):
      ui.icon("group").classes("mr-2")
      ui.label("Stakeholder")
    
    with ui.button(on_click=showTasks).classes("w-full justify-start pl-2").props("flat color=black"):
      ui.icon("task").classes("mr-2") 
      ui.label("Tasks")

contentArea = ui.column().classes("w-full")
appState.setContentArea(contentArea)

with contentArea:
  tasks_build(appState.tasksList, appState.currentTab)

# leftDrawer.hide()

# if __name__ == "__main__":
ui.run()