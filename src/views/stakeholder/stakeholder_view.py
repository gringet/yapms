from nicegui import ui
from typing import List
from ...data.stakeholder import Stakeholder
from ...core.styles import Layout, Text, Input, Card, Kanban

stakeholders: List[Stakeholder] = [
  Stakeholder("John", "Doe", "john.doe@company.com", "strategy"),
  Stakeholder("Jane", "Smith", "jane.smith@company.com", "subject matter expert"),
  Stakeholder("Bob", "Johnson", "bob.johnson@company.com", "sponsor"),
  Stakeholder("Alice", "Wilson", "alice.wilson@company.com", "executant")
]


def addStakeholderDialog():
  with ui.dialog() as dialog, ui.card().style(Layout.DIALOG_MIN_WIDTH):
    ui.label('Add New Stakeholder').classes(Text.H6)
    
    nameInput = ui.input('Name').props(Input.OUTLINED)
    surnameInput = ui.input('Surname').props(Input.OUTLINED)
    emailInput = ui.input('Email').props(Input.OUTLINED)
    typeSelect = ui.select(['strategy', 'subject matter expert', 'sponsor', 'executant'], 
                           label='Type').props(Input.OUTLINED)
    
    with ui.row().classes(Layout.ROW):
      ui.button('Cancel', on_click=dialog.close)
      
      def addStakeholder():
        if nameInput.value and surnameInput.value and emailInput.value and typeSelect.value:
          stakeholder = Stakeholder(
            nameInput.value,
            surnameInput.value,
            emailInput.value,
            typeSelect.value
          )
          stakeholders.append(stakeholder)
          build.refresh()
          dialog.close()
      
      ui.button('Add', on_click=addStakeholder).props('color=primary')
  
  dialog.open()


@ui.refreshable
def build():
  with ui.column().classes(Layout.COLUMN):
    if not stakeholders:
      ui.label('No stakeholders added yet.').classes(Text.CENTER_GRAY)
    else:
      with ui.row().classes(Layout.GRID_4_RESPONSIVE):
        for stakeholder in stakeholders:
          createStakeholderCard(stakeholder)


def createStakeholderCard(stakeholder: Stakeholder):
  typeColors = {
    'strategy': 'blue',
    'subject matter expert': 'green',
    'sponsor': 'purple',
    'executant': 'orange'
  }
  
  color = typeColors.get(stakeholder.type, 'grey')
  
  with ui.card().classes(Card.STAKEHOLDER):
    ui.label(f'{stakeholder.name} {stakeholder.surname}').classes(Text.H6_BOLD)
    ui.chip(stakeholder.type, color=color).props('size=sm').classes('-mt-2 flex-1')
    
    with ui.row().classes(Kanban.TASK_ROW):
      with ui.row().classes(Kanban.TASK_ICON_ROW):
        ui.icon('email').classes(Kanban.TASK_ICON)
        ui.label(stakeholder.email).classes(Kanban.TASK_LABEL)
      ui.space()