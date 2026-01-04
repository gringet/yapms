from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget
from navigation_menu import NavigationMenu
from kanban_board import KanbanBoard
from under_construction import UnderConstruction

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("YAPMS - Project Management")
    self.setMinimumSize(1200, 600)

    centralWidget = QWidget()
    self.setCentralWidget(centralWidget)

    mainLayout = QHBoxLayout()
    mainLayout.setSpacing(0)
    mainLayout.setContentsMargins(0, 0, 0, 0)

    self.navigationMenu = NavigationMenu()
    self.navigationMenu.viewChanged.connect(self.handleViewChanged)
    mainLayout.addWidget(self.navigationMenu)

    self.stackedWidget = QStackedWidget()

    self.kanbanView = KanbanBoard()
    self.stackedWidget.addWidget(self.kanbanView)

    self.ganttView = UnderConstruction("Gantt Chart")
    self.stackedWidget.addWidget(self.ganttView)

    mainLayout.addWidget(self.stackedWidget)

    centralWidget.setLayout(mainLayout)

    self.views = {
      'kanban': 0,
      'gantt': 1
    }

    self.stackedWidget.setCurrentIndex(0)

  def handleViewChanged(self, viewId):
    if viewId in self.views:
      self.stackedWidget.setCurrentIndex(self.views[viewId])
