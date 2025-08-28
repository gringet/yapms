from typing import List

from nicegui import ui

from ...data.task import Task
from ...core.styles import Table

@ui.refreshable
def build(tasks: List[Task]):
  columns = [
    {'name': 'id', 'label': 'ID', 'field': 'id', 'sortable': True, 'align': 'left', 'classes': 'w-1/12'},
    {'name': 'title', 'label': 'Title', 'field': 'title', 'sortable': True, 'align': 'left', 'classes': 'w-3/12'},
    {'name': 'description', 'label': 'Description', 'field': 'description', 'align': 'left', 'classes': 'w-3/12'},
    {'name': 'status', 'label': 'Status', 'field': 'status', 'sortable': True, 'align': 'left', 'classes': 'w-2/12'},
    {'name': 'duration', 'label': 'Duration', 'field': 'duration', 'sortable': True, 'align': 'left', 'classes': 'w-1/12'},
    {'name': 'startdate', 'label': 'Start Date', 'field': 'startdate', 'sortable': True, 'align': 'left', 'classes': 'w-2/12'},
  ]
  tasks = [task.dict() for task in tasks]
  ui.table(columns=columns, rows=tasks, row_key='id').classes(Table.DEFAULT).props(Table.PROPS)