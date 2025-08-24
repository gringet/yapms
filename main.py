import kanban
import task_list

from nicegui import ui

import os

import database
import task


if not os.path.exists(database.DB_FILE):
  database.createDummy()


task.tasks.extend([task.Task(**t) for t in database.getTasks()])
tasks = task.tasks


with ui.header().classes(replace="row items-center") as header:
  ui.button(on_click=lambda: leftDrawer.toggle(), icon="menu").props("flat color=white")
  with ui.tabs() as tabs:
    ui.tab("Kanban")
    ui.tab("Gantt")
    ui.tab("List")
  ui.space()
  ui.button(icon="add", on_click=task.addUpdateTaskDialog).classes("mr-3").props("round color=black")


with ui.left_drawer().classes("bg-blue-100") as leftDrawer:
  ...

with ui.tab_panels(tabs, animated=False, value="Kanban").classes("w-full"):
  with ui.tab_panel("Kanban"):
    kanban.build(tasks)
    tasks.on_change(kanban.build.refresh)
  with ui.tab_panel("Gantt"):
    ui.label("Gantt")
  with ui.tab_panel("List"):
    task_list.build(tasks)
    tasks.on_change(task_list.build.refresh)



leftDrawer.hide()

ui.run()