# Python Code Style Guide

## Naming Conventions

### Variables and Functions
- **Always use camelCase** for variable names and function names
- Examples:
  ```python
  userName = "John"
  totalCount = 0

  def calculateTotal(items):
    return sum(items)

  def getUserData(userId):
    return fetchData(userId)
  ```

### Classes
- Use PascalCase for class names
- Examples:
  ```python
  class UserManager:
    pass

  class DataProcessor:
    pass
  ```

### Constants
- Use UPPER_CASE_WITH_UNDERSCORES for constants
- Examples:
  ```python
  MAX_CONNECTIONS = 100
  DEFAULT_TIMEOUT = 30
  API_BASE_URL = "https://api.example.com"
  ```

## Indentation and Formatting

### Spacing
- **Use spaces instead of tabs**
- **Use 2 spaces for indentation** (not 4)
- Examples:
  ```python
  def processData(data):
    if data:
      for item in data:
        print(item)
  ```

### Line Length
- Keep lines under 120 characters when practical
- Break long lines at logical points

### Blank Lines
- Use one blank line between functions
- Use two blank lines between classes

## Import Statements

- Group imports in this order:
  1. Standard library imports
  2. Third-party imports (PySide6, etc.)
  3. Local application imports
- Separate groups with a blank line

Example:
```python
import os
import sys

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt

from utils.helpers import formatData
```

## String Formatting

- Prefer f-strings for string formatting
- Examples:
  ```python
  userName = "Alice"
  age = 30
  message = f"User {userName} is {age} years old"
  ```

## Comments

- Add comments only when logic isn't self-evident
- Use clear variable names that reduce need for comments
- For complex algorithms, add a brief explanation above the code

Example:
```python
# Calculate weighted average based on user preferences
weightedSum = sum(value * weight for value, weight in zip(values, weights))
averageValue = weightedSum / sum(weights)
```
