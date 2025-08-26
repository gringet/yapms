import os
import time

from nicegui import ui

from .data import database
from .data.task import Task, addUpdateTaskDialog
from .views.tasks_view import build as tasks_build
from .components.people import build as people_build, addStakeholderDialog
from .core.app_state import appState


if not os.path.exists(database.DB_FILE):
  database.createDummy()


def refresher():
  from .components.kanban import build as kanban_build
  from .components.task_list import build as task_list_build
  kanban_build.refresh()
  task_list_build.refresh()


task_list = []
for task_data in database.getTasks():
  task_obj = Task(**dict(task_data), onChange=refresher)
  task_list.append(task_obj)

appState.setTasksList(task_list)


ui.add_head_html('<script src="https://cdn.jsdelivr.net/npm/frappe-gantt@0.6.1/dist/frappe-gantt.min.js"></script>')

with ui.header().classes(replace="row items-center bg-black text-white").style("height: 48px; min-height: 48px") as header:
  ui.button(on_click=lambda: leftDrawer.toggle(), icon="menu").props("flat color=white")
  with ui.tabs() as tabs:
    kanbanTab = ui.tab("Kanban").classes("text-white")
    ganttTab = ui.tab("Gantt").classes("text-white")
    listTab = ui.tab("List").classes("text-white") 
  ui.space()
  def handleAddButton():
    if appState.currentView == "tasks":
      addUpdateTaskDialog()
    elif appState.currentView == "people":
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


with ui.left_drawer().classes("bg-white border-r border-black w-32") as leftDrawer:
  with ui.column().classes("w-full mt-4 gap-2"):
    def showTasks():
      appState.setView("tasks")
      appState.tabs.set_visibility(True)
      appState.contentArea.clear()
      with appState.contentArea:
        tasks_build(appState.tasksList, appState.currentTab)
    
    def showPeople():
      appState.setView("people")
      appState.tabs.set_visibility(False)
      appState.contentArea.clear()  
      with appState.contentArea:
        people_build()
    
    ui.button("People", on_click=showPeople).classes("w-full justify-start").props("flat color=black")
    ui.button("Tasks", on_click=showTasks).classes("w-full justify-start").props("flat color=black")


contentArea = ui.column().classes("w-full")
appState.setContentArea(contentArea)

with contentArea:
  tasks_build(appState.tasksList, appState.currentTab)


leftDrawer.hide()

ui.run()