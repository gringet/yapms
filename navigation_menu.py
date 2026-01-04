from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon

class MenuButton(QPushButton):
  def __init__(self, iconText, viewId, parent=None):
    super().__init__(parent)
    self.viewId = viewId
    self.isActive = False

    self.setText(iconText)
    self.setFixedSize(60, 60)
    self.setCursor(Qt.PointingHandCursor)

    self.updateStyle()

  def updateStyle(self):
    if self.isActive:
      self.setStyleSheet("""
        MenuButton {
          background-color: #4CAF50;
          color: white;
          border: none;
          border-radius: 8px;
          font-size: 24px;
        }
        MenuButton:hover {
          background-color: #45a049;
        }
      """)
    else:
      self.setStyleSheet("""
        MenuButton {
          background-color: #e0e0e0;
          color: #666;
          border: none;
          border-radius: 8px;
          font-size: 24px;
        }
        MenuButton:hover {
          background-color: #d0d0d0;
        }
      """)

  def setActive(self, active):
    self.isActive = active
    self.updateStyle()


class NavigationMenu(QWidget):
  viewChanged = Signal(str)

  def __init__(self, parent=None):
    super().__init__(parent)
    self.buttons = {}
    self.activeButton = None

    self.setFixedWidth(80)
    self.setAttribute(Qt.WA_StyledBackground, True)
    self.setStyleSheet("""
      NavigationMenu {
        background-color: #2c3e50;
        padding: 10px;
      }
    """)

    layout = QVBoxLayout()
    layout.setSpacing(10)
    layout.setContentsMargins(10, 10, 10, 10)
    layout.setAlignment(Qt.AlignTop)

    kanbanButton = MenuButton("📋", "kanban")
    kanbanButton.clicked.connect(lambda: self.handleButtonClick("kanban"))
    self.buttons["kanban"] = kanbanButton
    layout.addWidget(kanbanButton)

    ganttButton = MenuButton("📊", "gantt")
    ganttButton.clicked.connect(lambda: self.handleButtonClick("gantt"))
    self.buttons["gantt"] = ganttButton
    layout.addWidget(ganttButton)

    layout.addStretch()

    self.setLayout(layout)

    self.setActiveView("kanban")

  def handleButtonClick(self, viewId):
    self.setActiveView(viewId)
    self.viewChanged.emit(viewId)

  def setActiveView(self, viewId):
    if self.activeButton:
      self.activeButton.setActive(False)

    if viewId in self.buttons:
      self.buttons[viewId].setActive(True)
      self.activeButton = self.buttons[viewId]
