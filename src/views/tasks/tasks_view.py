from nicegui import ui
from .kanban_view import build as kanban_build
from . import gantt
from . import task_list


@ui.refreshable
def build(tasks, currentTab="Kanban"):
  with ui.column().classes('w-full bg-gray-50'):
    if currentTab == "Kanban":
      kanban_build(tasks)
      tasks.on_change(kanban_build.refresh)
    elif currentTab == "Gantt":
      gantt.build()
    elif currentTab == "List":
      task_list.build(tasks)
      tasks.on_change(task_list.build.refresh)