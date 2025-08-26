from typing import Dict, Any


class Stakeholder:
  def __init__(self, name: str, surname: str, email: str, type: str, **kwargs):
    self.name = name
    self.surname = surname
    self.email = email
    self.type = type
  
  def toDict(self) -> Dict[str, Any]:
    return {
      'name': self.name,
      'surname': self.surname,
      'email': self.email,
      'type': self.type
    }