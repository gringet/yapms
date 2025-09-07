"""Views package.

Keep this lightweight to avoid import-time side effects when importing
submodules like `src.views.tasks.dialogs`.
"""

# Expose subpackages without importing their symbols to avoid cycles
__all__ = [
  'tasks',
  'stakeholder',
]
