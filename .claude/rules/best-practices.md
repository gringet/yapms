# Best Practices

## Code Quality

### Keep It Simple
- Avoid over-engineering solutions
- Don't add features that weren't requested
- Three similar lines are better than a premature abstraction
- Only refactor when asked

### Function Design
- Keep functions small and focused
- Each function should do one thing well
- Use descriptive names that explain what the function does
- Limit parameters to 3-4 when possible

### Error Handling
- Only validate at system boundaries (user input, external APIs)
- Trust internal code and framework guarantees
- Don't add error handling for scenarios that can't happen
- Use try/except blocks for external operations (file I/O, network calls)

Example:
```python
def loadUserData(filePath):
  try:
    with open(filePath, 'r') as file:
      return json.load(file)
  except FileNotFoundError:
    return None
  except json.JSONDecodeError:
    return None
```

## PySide6 / Qt Specific

### Signal and Slots
- Use camelCase for custom signals
- Connect signals in initialization methods
- Disconnect signals when widgets are destroyed if needed

### Widget Creation
- Initialize UI components in `__init__` or dedicated setup methods
- Keep UI logic separate from business logic
- Use layouts instead of absolute positioning

## Version Control

### Commits
- Only commit when explicitly requested
- Write clear commit messages that explain why, not what
- Don't commit sensitive files (.env, credentials, etc.)

## Testing

### Before Committing
- Test changes manually
- Verify the application runs without errors
- Check that existing functionality still works

## Documentation

- Don't create documentation files unless explicitly requested
- Code should be self-documenting through clear naming
- Add docstrings for complex classes or public APIs only when needed
