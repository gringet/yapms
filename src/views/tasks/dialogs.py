import datetime
from nicegui import ui
from ...data.task import Task, addUpdateTask
from ...data.stakeholder import stakeholders
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
    effort = ui.number("Effort (days)", value=task.effort if task is not None else 1, min=1, step=1).props(Input.OUTLINED).classes(Input.DEFAULT)
    
    # Stakeholder assignment dropdown
    stakeholder_options = {}
    for stakeholder in stakeholders:
      display_name = f"{stakeholder.name} {stakeholder.surname}" if stakeholder.name != "Not" else "Not Assigned"
      stakeholder_options[stakeholder.id] = display_name
    
    default_stakeholder_id = task.assigned_stakeholder_id if task is not None else 1
    # Ensure the default value exists in options, fallback to first stakeholder if not
    if default_stakeholder_id not in stakeholder_options and stakeholder_options:
      default_stakeholder_id = list(stakeholder_options.keys())[0]
    
    stakeholder_select = ui.select(
      stakeholder_options,
      label="Assigned to",
      value=default_stakeholder_id
    ).props(f"{Input.OUTLINED} max-height=200px").classes(Input.DEFAULT)
    
    # Start date at the end
    defaultDate = task.startdate if task is not None else ""
    with ui.row().classes(Layout.ROW_ITEMS_END):
      startdate = ui.input("Start Date", value=defaultDate).props(Input.OUTLINED).classes(Input.FLEX_GROW)
      ui.button("Select Date", on_click=lambda: openDatePickerDialog(startdate)).classes(Button.DATE_SELECT)
    
    with ui.row().classes(Layout.ROW):
      ui.button("Cancel", on_click=dialog.close).classes(Button.CANCEL)
      ui.button("Save", on_click=lambda: (
        _addUpdateTask(task, title.value, description.value, int(effort.value) if effort.value else 1, startdate.value, stakeholder_select.value)
      )).classes(Button.PRIMARY)
  dialog.open()