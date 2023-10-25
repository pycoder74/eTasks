from quickbarV2 import QuickBar
from PyQt6.QtWidgets import QMainWindow, QApplication, QVBoxLayout

app = QApplication([])
win = QMainWindow()

# Create QuickBar instance
quickbar = QuickBar()

# Set QuickBar as central widget
win.setCentralWidget(quickbar)

win.show()
app.exec()
