import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt
from main_window import MainWindow

def main():
  app = QApplication(sys.argv)

  darkPalette = QPalette()
  darkPalette.setColor(QPalette.Window, QColor(53, 53, 53))
  darkPalette.setColor(QPalette.WindowText, Qt.white)
  darkPalette.setColor(QPalette.Base, QColor(35, 35, 35))
  darkPalette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
  darkPalette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
  darkPalette.setColor(QPalette.ToolTipText, Qt.white)
  darkPalette.setColor(QPalette.Text, Qt.white)
  darkPalette.setColor(QPalette.Button, QColor(53, 53, 53))
  darkPalette.setColor(QPalette.ButtonText, Qt.white)
  darkPalette.setColor(QPalette.BrightText, Qt.red)
  darkPalette.setColor(QPalette.Link, QColor(42, 130, 218))
  darkPalette.setColor(QPalette.Highlight, QColor(42, 130, 218))
  darkPalette.setColor(QPalette.HighlightedText, Qt.black)
  app.setPalette(darkPalette)
  app.setStyle("Fusion")

  app.setStyleSheet(open("style.css", "r").read())

  window = MainWindow()
  window.show()

  sys.exit(app.exec())

if __name__ == '__main__':
  main()
