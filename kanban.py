from typing import Callable, Dict, List, Optional
from nicegui import ui
import database

# Define the columns for the Kanban board
COLUMNS = ['To Do', 'In Progress', 'Done']

# Common styling for dialog titles to ensure consistency.
DIALOG_TITLE_CLASSES = 'text-h6'

class KanbanState:
    """A state object to hold the tasks for the Kanban board."""
    def __init__(self):
        self.tasks: Dict[str, List[Dict]] = {}

    def load_tasks(self) -> Dict[str, List[Dict]]:
        """Loads tasks from the database and organizes them by status."""
        tasks_by_status = {column: [] for column in COLUMNS}
        for task in database.get_tasks():
            task_dict = dict(task)
            if task_dict['status'] in tasks_by_status:
                tasks_by_status[task_dict['status']].append(task_dict)
        return tasks_by_status

# --- Single-User State Management ---
# A single, shared state for the application.
kanban_state = KanbanState()

# A reference to the single UI board's refresh function.
_board_refresher: Optional[Callable] = None

# The ID of the task currently being dragged.
_dragged_task_id: Optional[int] = None

def _refresh_board():
    """Reloads data from the database and triggers a UI refresh if the board exists."""
    kanban_state.tasks = kanban_state.load_tasks()
    if _board_refresher:
        _board_refresher()

def init_state():
    """Loads the initial state from the database."""
    kanban_state.tasks = kanban_state.load_tasks()

def move_task(task_id: int, new_status: str):
    """Moves a task to a new column/status and refreshes the board."""
    database.update_task_status(task_id, new_status)
    ui.notify(f"Moved task to '{new_status}'")
    _refresh_board()

def update_task_details(task_id: int, title: str, content: str, duration: int):
    """Updates the details of an existing task."""
    if title:
        database.update_task_details(task_id, title, content, duration)
        ui.notify(f"Updated task '{title}'")
        _refresh_board()
    else:
        ui.notify("Title is required.", color='negative')

def open_edit_task_dialog(task_id: int):
    """Opens a dialog for editing an existing task."""
    task = database.get_task(task_id)
    if not task:
        ui.notify("Task not found.", color='negative')
        return

    with ui.dialog() as dialog, ui.card().classes('w-[32rem]'):
        ui.label('Edit Task').classes(DIALOG_TITLE_CLASSES)
        title_input = ui.input('Title', value=task['title']).props('autofocus').classes('w-full')
        content_input = ui.textarea('Content', value=task['content']).classes('w-full')
        duration_input = ui.number('Duration (days)', value=task['duration'], min=1, step=1).classes('w-full')
        with ui.row().classes('w-full justify-end'):
            ui.button('Cancel', on_click=dialog.close, color='secondary')
            ui.button('Save', on_click=lambda: (
                update_task_details(task_id, title_input.value, content_input.value, int(duration_input.value or 1)),
                dialog.close()
            ))
    dialog.open()

class KanbanColumn(ui.column):
    """A column in the Kanban board that can be a drop target for tasks."""
    def __init__(self, status: str) -> None:
        super().__init__()
        self.status = status
        # Add 'kanban-column' class for CSS targeting.
        self.classes('kanban-column w-1/3 bg-gray-200 p-4 rounded-md h-full min-h-[10rem]')
        # The 'dragover.prevent' event is crucial to allow dropping.
        self.on('dragover.prevent', self.highlight)
        self.on('dragleave', self.unhighlight)
        self.on('drop', self.handle_drop)

    def highlight(self) -> None:
        self.classes(remove='bg-gray-200', add='bg-gray-300')

    def unhighlight(self) -> None:
        self.classes(remove='bg-gray-300', add='bg-gray-200')

    def handle_drop(self) -> None:
        """Handles a task being dropped into this column."""
        global _dragged_task_id
        self.unhighlight()
        # On a successful drop, we immediately remove the dragging class to re-enable
        # pointer events. This is crucial because the UI will be rebuilt, and the
        # original task's 'dragend' event might not fire on the removed element.
        ui.run_javascript('document.body.classList.remove("dragging-active")')
        dragged_task_id = _dragged_task_id
        _dragged_task_id = None  # Clear the state after the drop
        if dragged_task_id is not None:
            move_task(dragged_task_id, self.status)

class KanbanTask(ui.card):
    """A draggable task in the Kanban board."""
    def __init__(self, task_data: Dict) -> None:
        super().__init__()
        self.task_id = task_data['id']
        self.classes('w-full mb-2 cursor-pointer hover:shadow-lg').props('draggable=true')
        self.on('dragstart', self._handle_drag_start)
        self.on('dragend', self._handle_drag_end)
        self.on('click', lambda: open_edit_task_dialog(self.task_id))
        with self:
            ui.label(task_data['title']).classes('font-bold truncate')
            with ui.label(task_data['content']).classes('text-sm text-gray-600 my-1') as content_label:
                if task_data['content']:
                    ui.tooltip(task_data['content']).style('max-width: 28rem; overflow-wrap: break-word;')
                content_label.style(
                    'display: -webkit-box;'
                    '-webkit-box-orient: vertical;'
                    '-webkit-line-clamp: 2;'  # Limit to 2 lines
                    'overflow: hidden;')
            if task_data.get('duration'):
                with ui.row().classes('w-full items-center justify-end text-xs text-gray-500'):
                    ui.icon('timer', size='xs').classes('mr-1')
                    ui.label(f"{task_data['duration']} day(s)")

    def _handle_drag_start(self) -> None:
        """Set the dragged task ID in our module-level state and apply dragging styles."""
        global _dragged_task_id
        _dragged_task_id = self.task_id
        ui.run_javascript('document.body.classList.add("dragging-active")')

    def _handle_drag_end(self) -> None:
        """Clear the dragged task ID and remove dragging styles.
        This event is essential for cleanup when a drag operation is canceled or
        the task is dropped on an invalid target."""
        global _dragged_task_id
        _dragged_task_id = None
        ui.run_javascript('document.body.classList.remove("dragging-active")')

@ui.refreshable
def _kanban_board_ui():
    """The main UI component for the Kanban board."""
    with ui.row().classes('w-full no-wrap bg-gray-100 rounded-lg gap-4'):
        for status in COLUMNS:
            with KanbanColumn(status=status):
                ui.label(status).classes('text-lg font-semibold mb-4 text-gray-700')
                # The board now reads from the global state object
                for task in kanban_state.tasks.get(status, []):
                    KanbanTask(task)

def build_content() -> Callable[[], None]:
    """Builds the UI content for the Kanban board and returns a refresh function."""
    global _board_refresher
    # Add CSS to the page to prevent flickering during drag-and-drop.
    # When a drag is active, we disable pointer events on the children of the columns.
    ui.add_head_html('''
    <style>
    body.dragging-active .kanban-column > * {
        pointer-events: none;
    }
    </style>
    ''')

    # Create the board UI.
    _kanban_board_ui()

    # Store its refresh method for internal use within this module.
    _board_refresher = _kanban_board_ui.refresh

    # Return the refresh function so the main page can call it for external updates (e.g., new task added).
    return _refresh_board
