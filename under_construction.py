from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class UnderConstruction(QWidget):
  def __init__(self, featureName="This feature", parent=None):
    super().__init__(parent)

    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignCenter)

    iconLabel = QLabel("🚧")
    iconLabel.setStyleSheet("font-size: 72px;")
    iconLabel.setAlignment(Qt.AlignCenter)
    layout.addWidget(iconLabel)

    titleLabel = QLabel("Under Construction")
    titleLabel.setStyleSheet("font-size: 24px; font-weight: bold; margin-top: 20px;")
    titleLabel.setAlignment(Qt.AlignCenter)
    layout.addWidget(titleLabel)

    messageLabel = QLabel(f"{featureName} is coming soon!")
    messageLabel.setStyleSheet("font-size: 16px; color: #666; margin-top: 10px;")
    messageLabel.setAlignment(Qt.AlignCenter)
    layout.addWidget(messageLabel)

    self.setLayout(layout)
