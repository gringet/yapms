import datetime
from nicegui import ui
from ...data.task import Task, addUpdateTask
from ...core.styles import Card, Text, Layout, Button, Input


def openDatePickerDialog(inputField: ui.input, currentValue=None):
  """Opens a date picker dialog and updates the input field with the selected date"""
  with ui.dialog() as dateDialog, ui.card().classes(Card.DIALOG):
    ui.label("Select Date").classes(Text.DATE_LABEL)
    datePicker = ui.date(value=currentValue or inputField.value).props("minimal")
    with ui.row().classes(Layout.ROW_END):
      ui.button("Cancel", on_click=dateDialog.close).classes(Button.CANCEL_MR)
      ui.button("Select", on_click=lambda: (
        setattr(inputField, 'value', datePicker.value),
        dateDialog.close()
      )).classes(Button.PRIMARY)
  dateDialog.open()


def addUpdateTaskDialog(task: Task=None):
  def _addUpdateTask(*args):
    success, message = addUpdateTask(*args)
    if success:
      dialog.close()
    else:
      ui.notify(message, type="negative")

  with ui.dialog() as dialog, ui.card().classes(f"{Layout.DIALOG_WIDTH} {Card.DIALOG}"):
    title = ui.input("Title", value=task.title if task is not None else "").props(f"autofocus {Input.OUTLINED}").classes(Input.DEFAULT)
    description = ui.textarea("Description", value=task.description if task is not None else "").props(Input.OUTLINED).classes(Input.DEFAULT)
    defaultDate = task.startdate if task is not None else datetime.date.today().strftime('%Y-%m-%d')
    
    with ui.row().classes(Layout.ROW_ITEMS_END):
      startdate = ui.input("Start Date", value=defaultDate).props(Input.OUTLINED).classes(Input.FLEX_GROW)
      ui.button("Select Date", on_click=lambda: openDatePickerDialog(startdate)).classes(Button.DATE_SELECT)
    duration = ui.number("Duration (days)", value=task.duration if task is not None else 1, min=1, step=1).props(Input.OUTLINED).classes(Input.DEFAULT)
    with ui.row().classes(Layout.ROW):
      ui.button("Cancel", on_click=dialog.close).classes(Button.CANCEL)
      ui.button("Save", on_click=lambda: (
        _addUpdateTask(task, title.value, description.value, duration.value, startdate.value)
      )).classes(Button.PRIMARY)
  dialog.open()