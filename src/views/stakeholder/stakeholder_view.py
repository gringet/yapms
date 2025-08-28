from nicegui import ui
from typing import List
from ...data.stakeholder import Stakeholder, addUpdateStakeholder, stakeholders
from ...core.styles import Layout, Text, Input, Card, Kanban, Button
from ...core.app_state import appState


def addUpdateStakeholderDialog(stakeholder: Stakeholder = None):
  def _addUpdateStakeholder(*args):
    success, message = addUpdateStakeholder(*args)
    if success:
      build.refresh()
      dialog.close()
    else:
      ui.notify(message, type="negative")

  # Don't allow editing of the "Not Assigned" stakeholder
  if stakeholder and stakeholder.name == "Not" and stakeholder.surname == "Assigned":
    ui.notify("Cannot edit the 'Not Assigned' system stakeholder", type="warning")
    return
    
  with ui.dialog() as dialog, ui.card().classes(f"{Layout.DIALOG_WIDTH} {Card.DIALOG}"):
    nameInput = ui.input('Name', value=stakeholder.name if stakeholder else "").props(f"autofocus {Input.OUTLINED}").classes(Input.DEFAULT)
    surnameInput = ui.input('Surname', value=stakeholder.surname if stakeholder else "").props(Input.OUTLINED).classes(Input.DEFAULT)
    emailInput = ui.input('Email', value=stakeholder.email if stakeholder else "").props(Input.OUTLINED).classes(Input.DEFAULT)
    
    stakeholder_types = ['strategy', 'subject matter expert', 'sponsor', 'executant']
    default_type = stakeholder.type if stakeholder and stakeholder.type in stakeholder_types else None
    typeSelect = ui.select(stakeholder_types, 
                           label='Type', value=default_type).props(Input.OUTLINED).classes(Input.DEFAULT)
    
    with ui.row().classes(Layout.ROW):
      ui.button('Cancel', on_click=dialog.close).classes(Button.CANCEL)
      ui.button('Save', on_click=lambda: (
        _addUpdateStakeholder(stakeholder, nameInput.value, surnameInput.value, emailInput.value, typeSelect.value)
      )).classes(Button.PRIMARY)
  
  dialog.open()

# Keep the old function name for backward compatibility
def addStakeholderDialog():
  addUpdateStakeholderDialog()


@ui.refreshable
def build():
  with ui.column().classes(Layout.COLUMN):
    filtered_stakeholders = appState.filterStakeholders(stakeholders)
    
    # Check if we have any non-system stakeholders (excluding "Not Assigned")
    visible_stakeholders = [s for s in stakeholders if not (s.name == "Not" and s.surname == "Assigned")]
    
    if not visible_stakeholders:
      ui.label('No stakeholders added yet.').classes(Text.CENTER_GRAY)
    elif not filtered_stakeholders:
      ui.label('No stakeholders match your search.').classes(Text.CENTER_GRAY)
    else:
      with ui.row().classes(Layout.GRID_4_RESPONSIVE):
        for stakeholder in filtered_stakeholders:
          createStakeholderCard(stakeholder)


def createStakeholderCard(stakeholder: Stakeholder):
  with ui.card().classes(Card.STAKEHOLDER).on('click', lambda: addUpdateStakeholderDialog(stakeholder)):
    ui.label(f'{stakeholder.name} {stakeholder.surname}').classes(Text.H6_BOLD).style('font-size: 1.2rem')
    ui.label(stakeholder.type).classes('-mt-2 flex-1').style('background-color: white; font-size: 1rem; color: black; padding: 2px 8px; display: inline-block; text-align: center; font-weight: 500;')
    
    with ui.row().classes(Kanban.TASK_ROW):
      with ui.row().classes(Kanban.TASK_ICON_ROW):
        ui.icon('email').classes(Kanban.TASK_ICON)
        ui.label(stakeholder.email).classes(Kanban.TASK_LABEL).style('font-size: 0.95rem')
      ui.space()