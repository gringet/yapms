from nicegui import ui
import database
from typing import Callable

def build_content() -> Callable[[], None]:
    """Builds the UI for the task list view and returns a refresh function."""
    def get_rows():
        """Helper function to fetch and format tasks for the table."""
        tasks = database.get_tasks()
        return [dict(task) for task in tasks]

    columns = [
        {'name': 'id', 'label': 'ID', 'field': 'id', 'sortable': True, 'align': 'left', 'classes': 'w-1/12'},
        {'name': 'title', 'label': 'Title', 'field': 'title', 'sortable': True, 'align': 'left', 'classes': 'w-3/12'},
        {'name': 'content', 'label': 'Content', 'field': 'content', 'align': 'left', 'classes': 'w-4/12'},
        {'name': 'status', 'label': 'Status', 'field': 'status', 'sortable': True, 'align': 'left', 'classes': 'w-2/12'},
        {'name': 'duration', 'label': 'Duration', 'field': 'duration', 'sortable': True, 'align': 'left', 'classes': 'w-2/12'},
    ]

    task_table = ui.table(columns=columns, rows=get_rows(), row_key='id').classes('w-full').props('flat bordered')

    def refresh():
        """Fetches the latest tasks and updates the table rows."""
        task_table.rows = get_rows()

    return refresh