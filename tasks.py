from nicegui import ui
import kanban
import gantt
import task_list


@ui.refreshable
def build(tasks, currentTab="Kanban"):
  with ui.column().classes('w-full bg-gray-50'):
    if currentTab == "Kanban":
      kanban.build(tasks)
      tasks.on_change(kanban.build.refresh)
    elif currentTab == "Gantt":
      gantt.build()
    elif currentTab == "List":
      task_list.build(tasks)
      tasks.on_change(task_list.build.refresh)