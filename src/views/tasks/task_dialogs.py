import datetime
from nicegui import ui
from ...data.task import Task, addUpdateTask


def openDatePickerDialog(inputField: ui.input, currentValue=None):
  """Opens a date picker dialog and updates the input field with the selected date"""
  with ui.dialog() as dateDialog, ui.card().classes("bg-white border-2 border-black rounded-none shadow-none"):
    ui.label("Select Date").classes("text-lg font-bold text-black mb-4")
    datePicker = ui.date(value=currentValue or inputField.value).props("minimal")
    with ui.row().classes("w-full justify-end mt-4"):
      ui.button("Cancel", on_click=dateDialog.close).classes("bg-white text-black border border-black rounded-none hover:bg-gray-100 mr-2")
      ui.button("Select", on_click=lambda: (
        setattr(inputField, 'value', datePicker.value),
        dateDialog.close()
      )).classes("bg-black text-white border border-black rounded-none hover:bg-gray-800")
  dateDialog.open()


def addUpdateTaskDialog(task: Task=None):
  def _addUpdateTask(*args):
    success, message = addUpdateTask(*args)
    if success:
      dialog.close()
    else:
      ui.notify(message, type="negative")

  with ui.dialog() as dialog, ui.card().classes("w-[48rem] bg-white border-2 border-black rounded-none shadow-none"):
    title = ui.input("Title", value=task.title if task is not None else "").props("autofocus outlined").classes("w-full")
    description = ui.textarea("Description", value=task.description if task is not None else "").props("outlined").classes('w-full')
    defaultDate = task.startdate if task is not None else datetime.date.today().strftime('%Y-%m-%d')
    
    with ui.row().classes("w-full items-end"):
      startdate = ui.input("Start Date", value=defaultDate).props("outlined").classes("flex-grow")
      ui.button("Select Date", on_click=lambda: openDatePickerDialog(startdate)).classes("bg-white text-black border border-black rounded-none hover:bg-gray-100 ml-2")
    duration = ui.number("Duration (days)", value=task.duration if task is not None else 1, min=1, step=1).props("outlined").classes('w-full')
    with ui.row().classes("w-full justify-end"):
      ui.button("Cancel", on_click=dialog.close).classes("bg-white text-black border border-black rounded-none hover:bg-gray-100")
      ui.button("Save", on_click=lambda: (
        _addUpdateTask(task, title.value, description.value, duration.value, startdate.value)
      )).classes("bg-black text-white border border-black rounded-none hover:bg-gray-800")
  dialog.open()