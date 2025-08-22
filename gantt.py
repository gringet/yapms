from nicegui import ui

def build_content():
    """Builds the placeholder UI for the Gantt Chart view."""
    ui.label('Gantt Chart View').classes('text-2xl')
    ui.label('This is a placeholder for the Gantt chart.').classes('text-gray-600 mb-2')
    ui.label('It will display tasks with their durations.').classes('text-sm text-gray-500')