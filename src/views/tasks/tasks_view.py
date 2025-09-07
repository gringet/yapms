from __future__ import annotations
from typing import Iterable
from nicegui import ui
from .kanban import build as kanban_build
from . import gantt
from . import tasks_list
from ...core.styles import Layout, Colors
from ...data.task import Task


@ui.refreshable
def build(tasks: Iterable[Task], currentTab: str = "Kanban") -> None:
  with ui.column().classes(f"{Layout.FULL_WIDTH} {Colors.GRAY_LIGHT}"):
    if currentTab == "Kanban":
      kanban_build(tasks)
      tasks.on_change(kanban_build.refresh)
    elif currentTab == "Gantt":
      gantt.build()
    elif currentTab == "List":
      tasks_list.build(tasks)
      tasks.on_change(tasks_list.build.refresh)
