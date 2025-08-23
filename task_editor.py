from nicegui import ui
import database
from typing import Callable

def open_task_dialog(*, on_save: Callable):
    """Opens a dialog for adding a new task."""
    with ui.dialog() as dialog, ui.card().classes('w-[32rem]'):
        ui.label('Add New Task').classes('text-h6')
        title_input = ui.input('Title').props('autofocus').classes('w-full')
        content_input = ui.textarea('Content').classes('w-full')
        duration_input = ui.number('Duration (days)', value=1, min=1, step=1).classes('w-full')

        def handle_save():
            """Validates input, saves the task, and triggers the refresh callback."""
            if not title_input.value:
                ui.notify('Title cannot be empty.', color='negative')
                return
            database.add_task(title_input.value, content_input.value, 'To Do', int(duration_input.value or 1))
            ui.notify(f"Added task '{title_input.value}'")
            on_save()
            dialog.close()

        with ui.row().classes('w-full justify-end'):
            ui.button('Cancel', on_click=dialog.close, color='secondary')
            ui.button('Add Task', on_click=handle_save)
    dialog.open()