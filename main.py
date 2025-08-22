from nicegui import ui, app
import database
import kanban
import gantt

@app.on_startup
def init():
    """Initialize the database and the initial state when the app starts."""
    database.init_db()
    # Load the initial state from the database after it has been initialized.
    kanban.init_state()

@ui.page('/')
def main_page():
    """The main page of the Kanban board application."""
    # Main layout
    with ui.header(elevated=True).classes('items-center justify-between'):
        with ui.row().classes('items-center'):
            ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=white')
            header_title = ui.label('Kanban Board').classes('text-h5')
        header_actions = ui.row()  # Placeholder for view-specific buttons

    with ui.left_drawer(value=False).classes('bg-gray-100') as left_drawer:
        ui.label('Views').classes('p-4 text-lg font-semibold')
        ui.menu_item('Kanban Board', on_click=lambda: show_view('kanban'))
        ui.menu_item('Gantt Chart', on_click=lambda: show_view('gantt'))

    content_area = ui.column().classes('w-full p-4')

    def show_view(view_name: str):
        """Clears the content and header actions, then builds the selected view."""
        content_area.clear()
        header_actions.clear()
        if view_name == 'kanban':
            header_title.text = 'Kanban Board'
            with header_actions:
                ui.button(icon='add', on_click=kanban.open_new_task_dialog).props('flat color=white')
            with content_area:
                kanban.build_content()
        elif view_name == 'gantt':
            header_title.text = 'Gantt Chart'
            with content_area:
                gantt.build_content()
        left_drawer.hide()

    show_view('kanban')

ui.run(storage_secret='a_very_secret_key_for_kanban')