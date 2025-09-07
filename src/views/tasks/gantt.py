from nicegui import ui

from ...core.styles import applyGlobalStyles


@ui.refreshable
def build() -> None:
  """Builds the Gantt chart view placeholder."""

  # Apply global styles
  applyGlobalStyles()

  ui.label('gantt here')
