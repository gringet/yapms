# PySide6 Conventions

## Widget Naming

Use descriptive camelCase names for widgets:

```python
mainWindow = QMainWindow()
submitButton = QPushButton("Submit")
userNameInput = QLineEdit()
statusLabel = QLabel("Ready")
```

## Layout Structure

### Organizing Layouts
- Use nested layouts for complex UIs
- Prefer QVBoxLayout and QHBoxLayout for most cases
- Use QGridLayout for form-like structures

Example:
```python
def setupUI(self):
  mainLayout = QVBoxLayout()

  # Header section
  headerLayout = QHBoxLayout()
  titleLabel = QLabel("YAPMS")
  headerLayout.addWidget(titleLabel)

  # Content section
  contentLayout = QVBoxLayout()
  # Add content widgets here

  mainLayout.addLayout(headerLayout)
  mainLayout.addLayout(contentLayout)

  self.setLayout(mainLayout)
```

## Signal and Slot Connections

### Connecting Signals
```python
def __init__(self):
  super().__init__()

  self.submitButton = QPushButton("Submit")
  self.submitButton.clicked.connect(self.handleSubmit)

def handleSubmit(self):
  # Handle button click
  pass
```

### Custom Signals
```python
from PySide6.QtCore import Signal

class DataManager(QObject):
  dataLoaded = Signal(dict)  # Custom signal

  def loadData(self):
    data = self.fetchData()
    self.dataLoaded.emit(data)
```

## Resource Management

### Cleaning Up
- Close file handles properly
- Disconnect signals when no longer needed
- Delete widgets that are no longer used

### Using Context Managers
```python
def saveToFile(self, filePath, data):
  with open(filePath, 'w') as file:
    json.dump(data, file, indent=2)
```

## Threading

### Use QThread for Long Operations
- Don't block the UI thread
- Use signals to communicate between threads
- Move heavy operations to worker threads

Example:
```python
from PySide6.QtCore import QThread, Signal

class WorkerThread(QThread):
  finished = Signal(dict)

  def run(self):
    result = self.performHeavyOperation()
    self.finished.emit(result)
```

## Styling

### Using QSS (Qt Style Sheets)
- Keep styling separate from logic when possible
- Use QSS for consistent theming

Example:
```python
submitButton.setStyleSheet("""
  QPushButton {
    background-color: #4CAF50;
    color: white;
    padding: 8px 16px;
    border-radius: 4px;
  }
  QPushButton:hover {
    background-color: #45a049;
  }
""")
```
