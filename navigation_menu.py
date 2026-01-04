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
          font-size: 24px;
          border-radius: 3px;
          border: 1px solid palette(highlight);
        }
      """)
    else:
      self.setStyleSheet("""
        MenuButton {
          font-size: 24px;
          border-radius: 3px;
        }
        MenuButton:hover {
          border: 1px solid palette(hover);
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
