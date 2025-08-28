from nicegui import ui
from .kanban import build as kanban_build
from . import gantt
from . import tasks_list
from ...core.styles import Layout, Colors


@ui.refreshable
def build(tasks, currentTab="Kanban"):
  with ui.column().classes(f"{Layout.FULL_WIDTH} {Colors.GRAY_LIGHT}"):
    if currentTab == "Kanban":
      kanban_build(tasks)
      tasks.on_change(kanban_build.refresh)
    elif currentTab == "Gantt":
      gantt.build()
    elif currentTab == "List":
      tasks_list.build(tasks)
      tasks.on_change(tasks_list.build.refresh)