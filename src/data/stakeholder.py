from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, Callable, Tuple
from nicegui.observables import ObservableList
from . import database


stakeholders: ObservableList = ObservableList()


@dataclass
class Stakeholder:
  def __init__(self, id: int, name: str, surname: str, email: str, type: str, onChange: Callable | None = None) -> None:
    self._id = id
    self._name = name
    self._surname = surname
    self._email = email
    self._type = type
    self._onChange = onChange

  def dict(self) -> Dict[str, Any]:
    return {"id": self.id, "name": self.name, "surname": self.surname, "email": self.email, "type": self.type}

  @property
  def id(self) -> int:
    return self._id

  @property
  def name(self) -> str:
    return self._name

  def _update_field(self, field_name: str, new_value: Any, current_value: Any) -> None:
    if current_value == new_value:
      return
    database.updateStakeholder(self._id, **{field_name: new_value})
    setattr(self, f"_{field_name}", new_value)
    if self._onChange:
      self._onChange()

  @name.setter
  def name(self, name: str) -> None:
    self._update_field("name", name, self._name)

  @property
  def surname(self) -> str:
    return self._surname

  @surname.setter
  def surname(self, surname: str) -> None:
    self._update_field("surname", surname, self._surname)

  @property
  def email(self) -> str:
    return self._email

  @email.setter
  def email(self, email: str) -> None:
    self._update_field("email", email, self._email)

  @property
  def type(self) -> str:
    return self._type

  @type.setter
  def type(self, type: str) -> None:
    self._update_field("type", type, self._type)

  def toDict(self) -> Dict[str, Any]:
    return {
      'id': self.id,
      'name': self.name,
      'surname': self.surname,
      'email': self.email,
      'type': self.type
    }

  def getAcronym(self) -> str:
    """Generate acronym: first letter of name + first two letters of surname"""
    if self.name == "Not" and self.surname == "Assigned":
      return "N/A"
    
    name_initial = self.name[0] if self.name else ""
    surname_initials = self.surname[:2] if len(self.surname) >= 2 else self.surname
    return (name_initial + surname_initials).upper()


def getStakeholderById(stakeholder_id: int) -> Stakeholder | None:
  """Get stakeholder by ID from the observable list"""
  for stakeholder in stakeholders:
    if stakeholder.id == stakeholder_id:
      return stakeholder
  # Return "Not Assigned" stakeholder if not found
  return stakeholders[0] if stakeholders else None


def addUpdateStakeholder(stakeholder: Stakeholder | None, name: str, surname: str, email: str, type: str) -> tuple[bool, str]:
  """Add or update stakeholder in database"""
  try:
    if stakeholder is None:
      # Add new stakeholder
      stakeholder_id = database.addStakeholder(name, surname, email, type)
      if stakeholder_id:
        new_stakeholder = Stakeholder(stakeholder_id, name, surname, email, type)
        stakeholders.append(new_stakeholder)
        return True, "Stakeholder added successfully"
      else:
        return False, "Failed to add stakeholder"
    else:
      # Update existing stakeholder
      stakeholder.name = name
      stakeholder.surname = surname
      stakeholder.email = email
      stakeholder.type = type
      return True, "Stakeholder updated successfully"
  except Exception as e:
    return False, f"Error: {str(e)}"
