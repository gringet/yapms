from typing import List

from nicegui import ui

from ...data.task import Task
from ...core.styles import Table
from ...core.app_state import appState

@ui.refreshable
def build(tasks: List[Task]):
  filtered_tasks = appState.filterTasks(tasks)
  columns = [
    {'name': 'id', 'label': 'ID', 'field': 'id', 'sortable': True, 'align': 'left', 'classes': 'w-1/12'},
    {'name': 'title', 'label': 'Title', 'field': 'title', 'sortable': True, 'align': 'left', 'classes': 'w-3/12'},
    {'name': 'description', 'label': 'Description', 'field': 'description', 'align': 'left', 'classes': 'w-3/12'},
    {'name': 'status', 'label': 'Status', 'field': 'status', 'sortable': True, 'align': 'left', 'classes': 'w-2/12'},
    {'name': 'effort', 'label': 'Effort', 'field': 'effort', 'sortable': True, 'align': 'left', 'classes': 'w-1/12'},
    {'name': 'startdate', 'label': 'Start Date', 'field': 'startdate', 'sortable': True, 'align': 'left', 'classes': 'w-2/12'},
  ]
  sorted_tasks = sorted(filtered_tasks, key=lambda t: t.sort_key)
  task_data = [task.dict() for task in sorted_tasks]
  ui.table(columns=columns, rows=task_data, row_key='id').classes(Table.DEFAULT).props(Table.PROPS)