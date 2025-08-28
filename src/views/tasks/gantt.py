import datetime
import json

from nicegui import ui

from ...data import database
from ...core.styles import Text, Layout

@ui.refreshable
def build():
    return
    """Builds the interactive Gantt chart view using Frappe Gantt."""

    tasks = database.getTasks()

    if not tasks:
        ui.label('No tasks to display.').classes(Text.LARGE_GRAY)
        ui.label('Add some tasks in the Kanban board view.').classes(Text.SMALL_LIGHT_GRAY)
        return

    # --- Task Processing for Gantt Chart ---
    gantt_tasks = []
    # We'll sequence tasks one after another starting from today for a clear timeline.
    start_of_timeline = datetime.date.today()

    # Map Kanban status to a numerical progress value for the Gantt chart.
    progress_map = {
        'To Do': 0,
        'In Progress': 50,  # Assumption: 'In Progress' is 50% complete.
        'Done': 100,
    }

    for task in tasks:
        duration = task['duration'] if task['duration'] > 0 else 1
        end_of_task = start_of_timeline + datetime.timedelta(days=duration - 1)

        gantt_tasks.append({
            'id': str(task['id']),
            'name': task['title'],
            'start': start_of_timeline.strftime('%Y-%m-%d'),
            'end': end_of_task.strftime('%Y-%m-%d'),
            'progress': progress_map.get(task['status'], 0),
            'dependencies': ''  # Dependencies are not part of our current data model.
        })

        # The next task starts the day after the current one ends.
        start_of_timeline = end_of_task + datetime.timedelta(days=1)

    # --- UI and JavaScript Initialization ---

    # The container for the Gantt chart. Frappe-Gantt renders into an SVG element.
    ui.html('<svg id="gantt-container"></svg>').classes(Layout.GANTT_SVG)

    # Convert the Python list of tasks into a JSON string.
    tasks_json = json.dumps(gantt_tasks)

    # Run JavaScript to initialize the Gantt chart with a small delay to ensure DOM is ready
    ui.run_javascript(f'''
        setTimeout(() => {{
            const tasks = {tasks_json};
            const gantt_container = document.getElementById("gantt-container");

            if (gantt_container && tasks && tasks.length > 0) {{
                gantt_container.innerHTML = '';
                new Gantt(gantt_container, tasks, {{
                    view_mode: 'Week',
                    language: 'en'
                }});
            }}
        }}, 100);
    ''')