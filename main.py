#!/usr/bin/env python3
"""
Project Manager Application - Entry point
"""

from __future__ import annotations
import os
import sys
try:
  from dotenv import load_dotenv  # type: ignore
except Exception:  # pragma: no cover
  def load_dotenv(*args, **kwargs):
    return False
from nicegui import ui, app
import datetime as _dt
from typing import Any, Dict
from fastapi import HTTPException

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Load environment from .env
load_dotenv()

# Imports from organized structure
from src.data import database
from src.data.task import Task, tasks
from src.data.stakeholder import Stakeholder, stakeholders
from src.views.tasks.dialogs import addUpdateTaskDialog
from src.views.tasks import build_tasks as tasks_build
from src.views.stakeholder import build as stakeholder_build, addStakeholderDialog
from src.core.app_state import appState

# Ensure database exists and is up-to-date
if not os.path.exists(database.DB_FILE):
  database.createDummy()
else:
  database._migrateDatabase()


def refresher() -> None:
  """Refresh visible views when data changes."""
  from src.views.tasks import build_kanban, build_task_list
  from src.views.stakeholder import stakeholder_view
  build_kanban.refresh()
  build_task_list.refresh()
  if hasattr(stakeholder_view, 'build'):
    stakeholder_view.build.refresh()


def refreshCurrentView() -> None:
  """Re-render content area according to current view and tab."""
  appState.contentArea.clear()
  with appState.contentArea:
    if appState.currentView == "tasks":
      tasks_build(appState.tasksList, appState.currentTab)
    elif appState.currentView == "stakeholder":
      stakeholder_build()


# Load initial data
tasks.extend([Task(**dict(t), onChange=refresher) for t in database.getTasks()])
appState.setTasksList(tasks)
stakeholders.extend([Stakeholder(**dict(s), onChange=refresher) for s in database.getStakeholders()])


# Header with tabs, search and add button
with ui.header().classes(replace="column bg-black text-white").style("min-height: 48px") as header:
  with ui.row().classes("w-full items-center flex-wrap").style("min-height: 48px"):
    ui.button(on_click=lambda: leftDrawer.toggle(), icon="menu").props("flat color=white")
    with ui.tabs() as tabs:
      ui.tab("Kanban").classes("text-white")
      ui.tab("Gantt").classes("text-white")
      ui.tab("List").classes("text-white")
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
    refreshCurrentView()


tabs.on('update:model-value', onTabChange)


# Left drawer navigation
with ui.left_drawer().classes("bg-white border-r border-black") as leftDrawer:
  with ui.column().classes("w-full gap-0"):
    def showTasks():
      appState.setView("tasks")
      appState.tabs.set_visibility(True)
      refreshCurrentView()

    def showStakeholder():
      appState.setView("stakeholder")
      appState.tabs.set_visibility(False)
      refreshCurrentView()

    with ui.button(on_click=showStakeholder).classes("w-full justify-start pl-2").props("flat color=black"):
      ui.icon("group").classes("mr-2")
      ui.label("Stakeholder")

    with ui.button(on_click=showTasks).classes("w-full justify-start pl-2").props("flat color=black"):
      ui.icon("task").classes("mr-2")
      ui.label("Tasks")


# Main content area
contentArea = ui.column().classes("w-full")
appState.setContentArea(contentArea)

with contentArea:
  tasks_build(appState.tasksList, appState.currentTab)


ui.run()
 
 
# --- API: Gantt updates ---
@app.post('/api/gantt/update')
async def api_gantt_update(payload: Dict[str, Any]):
  """Update a task's start date and effort from Gantt drag/resize.
  Expects JSON: {"id": int, "start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}
  """
  try:
    task_id = int(payload.get('id')) if payload.get('id') is not None else None
    start = payload.get('start')
    end = payload.get('end')
    if task_id is None or not start or not end:
      raise HTTPException(status_code=400, detail='Missing id/start/end')

    # Parse dates and compute effort (at least 1 day)
    y1, m1, d1 = [int(x) for x in start.split('-')]
    y2, m2, d2 = [int(x) for x in end.split('-')]
    start_date = _dt.date(y1, m1, d1)
    end_date = _dt.date(y2, m2, d2)
    effort = max((end_date - start_date).days, 1)

    # Update task in memory; setters persist and trigger refresh
    updated = False
    if appState.tasksList:
      for t in appState.tasksList:
        if t.id == task_id:
          t.startdate = start
          t.effort = effort
          updated = True
          break
    if not updated:
      raise HTTPException(status_code=404, detail='Task not found')

    return {'ok': True, 'id': task_id, 'start': start, 'effort': effort}
  except HTTPException:
    raise
  except Exception as ex:
    # Avoid leaking internals; provide generic error
    raise HTTPException(status_code=400, detail=f'invalid payload: {ex}')
