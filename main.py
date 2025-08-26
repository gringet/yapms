import os
import time

from nicegui import ui

import database
import gantt
import kanban
import task
import task_list


if not os.path.exists(database.DB_FILE):
  database.createDummy()


def refresher():
  kanban.build.refresh()
  task_list.build.refresh()

task.tasks.extend([task.Task(**dict(t), onChange=refresher) for t in database.getTasks()])
tasks = task.tasks


ui.add_head_html('<script src="https://cdn.jsdelivr.net/npm/frappe-gantt@0.6.1/dist/frappe-gantt.min.js"></script>')

with ui.header().classes(replace="row items-center bg-black text-white") as header:
  ui.button(on_click=lambda: leftDrawer.toggle(), icon="menu").props("flat color=white")
  with ui.tabs() as tabs:
    ui.tab("Kanban").classes("text-white")
    ui.tab("Gantt").classes("text-white")
    ui.tab("List").classes("text-white") 
  ui.space()
  ui.button(icon="add", on_click=task.addUpdateTaskDialog).classes("mr-3 text-black bg-white").props("round size=12px")


with ui.left_drawer().classes("bg-white border-r border-black w-32") as leftDrawer:
  ui.label("Project Manager").classes("text-h5 mx-auto text-black font-bold")
  ui.separator().classes("bg-black")


with ui.tab_panels(tabs, animated=False, value="Kanban").classes("w-full bg-gray-50"):
  with ui.tab_panel("Kanban"):
    kanban.build(tasks)
    tasks.on_change(kanban.build.refresh)
  with ui.tab_panel("Gantt"):
    gantt.build()
  with ui.tab_panel("List"):
    task_list.build(tasks)
    tasks.on_change(task_list.build.refresh)


leftDrawer.hide()

ui.run()