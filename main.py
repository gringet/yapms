import os
import time

from nicegui import ui

import database
import gantt
import kanban
import task
import task_list
import tasks
import people


if not os.path.exists(database.DB_FILE):
  database.createDummy()


def refresher():
  kanban.build.refresh()
  task_list.build.refresh()

task.tasks.extend([task.Task(**dict(t), onChange=refresher) for t in database.getTasks()])
tasksList = task.tasks


ui.add_head_html('<script src="https://cdn.jsdelivr.net/npm/frappe-gantt@0.6.1/dist/frappe-gantt.min.js"></script>')

with ui.header().classes(replace="row items-center bg-black text-white").style("height: 48px; min-height: 48px") as header:
  ui.button(on_click=lambda: leftDrawer.toggle(), icon="menu").props("flat color=white")
  with ui.tabs() as tabs:
    kanbanTab = ui.tab("Kanban").classes("text-white")
    ganttTab = ui.tab("Gantt").classes("text-white")
    listTab = ui.tab("List").classes("text-white") 
  ui.space()
  def handleAddButton():
    if currentView == "tasks":
      task.addUpdateTaskDialog()
    elif currentView == "people":
      people.addStakeholderDialog()
  
  ui.button(icon="add", on_click=handleAddButton).classes("mr-3 text-black bg-white").props("round size=12px")

currentView = "tasks"
currentTab = "Kanban"

def onTabChange():
  global currentTab
  currentTab = tabs.value
  if currentView == "tasks":
    contentArea.clear()
    with contentArea:
      tasks.build(tasksList, currentTab)

tabs.on('update:model-value', onTabChange)


with ui.left_drawer().classes("bg-white border-r border-black w-32") as leftDrawer:
  with ui.column().classes("w-full mt-4 gap-2"):
    def showTasks():
      global currentView, currentTab
      currentView = "tasks"
      tabs.set_visibility(True)
      contentArea.clear()
      with contentArea:
        tasks.build(tasksList, currentTab)
    
    def showPeople():
      global currentView
      currentView = "people"
      tabs.set_visibility(False)
      contentArea.clear()  
      with contentArea:
        people.build()
    
    ui.button("People", on_click=showPeople).classes("w-full justify-start").props("flat color=black")
    ui.button("Tasks", on_click=showTasks).classes("w-full justify-start").props("flat color=black")


contentArea = ui.column().classes("w-full")

with contentArea:
  tasks.build(tasksList, currentTab)


leftDrawer.hide()

ui.run()