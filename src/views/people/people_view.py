from nicegui import ui
from typing import List
from ...data.stakeholder import Stakeholder

stakeholders: List[Stakeholder] = [
  Stakeholder("John", "Doe", "john.doe@company.com", "strategy"),
  Stakeholder("Jane", "Smith", "jane.smith@company.com", "subject matter expert"),
  Stakeholder("Bob", "Johnson", "bob.johnson@company.com", "sponsor"),
  Stakeholder("Alice", "Wilson", "alice.wilson@company.com", "executant")
]


def addStakeholderDialog():
  with ui.dialog() as dialog, ui.card().style('min-width: 400px'):
    ui.label('Add New Stakeholder').classes('text-h6 mb-4')
    
    nameInput = ui.input('Name').props('outlined')
    surnameInput = ui.input('Surname').props('outlined')
    emailInput = ui.input('Email').props('outlined')
    typeSelect = ui.select(['strategy', 'subject matter expert', 'sponsor', 'executant'], 
                           label='Type').props('outlined')
    
    with ui.row().classes('w-full justify-end'):
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
  with ui.column().classes('w-full p-4'):
    if not stakeholders:
      ui.label('No stakeholders added yet.').classes('text-grey-6 text-center mt-8')
    else:
      with ui.grid(columns=3).classes('w-full gap-4'):
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
  
  with ui.card().classes('min-h-[160px] cursor-pointer hover:shadow-lg transition-shadow flex flex-col'):
    ui.label(f'{stakeholder.name} {stakeholder.surname}').classes('text-h6 font-semibold')
    ui.chip(stakeholder.type, color=color).props('size=sm').classes('-mt-2 flex-1')
    
    with ui.row().classes('w-full justify-between items-end mt-0 p-0 pt-0'):
      with ui.row().classes('items-center gap-1'):
        ui.icon('email').classes('text-grey-6')
        ui.label(stakeholder.email).classes('text-sm text-grey-8')
      ui.space()