from nicegui import ui, app
import database
import kanban
import gantt
import task_editor
import task_list

@app.on_startup
def init():
    """Initialize the database and the initial state when the app starts."""
    database.init_db()
    # Load the initial state from the database after it has been initialized.
    kanban.init_state()

@ui.page('/')
def main_page():
    """The main page of the Kanban board application."""
    # Load the Frappe-Gantt assets globally for the page. This ensures the library
    # is available whenever the Gantt view is built, avoiding race conditions.
    ui.add_head_html('<link href="https://cdn.jsdelivr.net/npm/frappe-gantt@0.6.1/dist/frappe-gantt.css" rel="stylesheet">')
    ui.add_head_html('<script src="https://cdn.jsdelivr.net/npm/frappe-gantt@0.6.1/dist/frappe-gantt.min.js"></script>')

    # Apply a minimalistic black and white theme.
    ui.colors(primary='black')
    ui.query('body').classes('bg-white')

    # Main layout
    with ui.header().classes('items-center justify-between bg-white text-black border-b'):
        with ui.row().classes('items-center'):
            ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=black')
            header_title = ui.label('Tasks').classes('text-h5 text-black')
        header_actions = ui.row()  # Placeholder for view-specific buttons

    with ui.left_drawer(value=False).classes('bg-white border-r') as left_drawer:
        ui.label('Menu').classes('p-4 text-lg font-semibold text-black')
        ui.menu_item('Tasks', on_click=left_drawer.hide)

    content_area = ui.column().classes('w-full p-4')
    # This will hold a reference to the current view's refresh function.
    current_view_refresher = None

    def show_view(view_name: str):
        """Builds the selected view and stores its refresh function."""
        nonlocal current_view_refresher
        app.storage.user['view'] = view_name  # Store the current view
        content_area.clear()
        header_actions.clear()
        with header_actions:
            # This button group acts as a toggle to switch between views.
            # Reverted to simple on_click handlers as requested.
            with ui.button_group().props('flat'):
                ui.button('Kanban', on_click=lambda: show_view('Kanban'))
                ui.button('Gantt', on_click=lambda: show_view('Gantt'))
                ui.button('List', on_click=lambda: show_view('List'))
            # The "add task" button is now always visible and uses the new task editor.
            ui.button(icon='add', on_click=lambda: task_editor.open_task_dialog(on_save=refresh_view)).props('flat color=black')

        with content_area:
            if view_name == 'Kanban':
                header_title.text = 'Kanban Board'
                current_view_refresher = kanban.build_content()
            elif view_name == 'Gantt':
                header_title.text = 'Gantt Chart'
                # NOTE: This assumes gantt.build_content() is refactored to return a refresh function.
                gantt.build_content()
            elif view_name == 'List':
                header_title.text = 'Task List'
                current_view_refresher = task_list.build_content()
        left_drawer.hide()

    def refresh_view():
        """Refreshes the data of the current view without rebuilding the UI."""
        if callable(current_view_refresher):
            current_view_refresher()
        else:
            # Fallback in case there is no refresher available
            ui.notify('Could not refresh view.', color='negative')

    # Show the initial/last-viewed view.
    show_view(app.storage.user.get('view', 'Kanban'))

ui.run()