from PyQt6.QtWidgets import QMessageBox, QApplication
import sys

from PyQt6.QtWidgets import QMessageBox

class MessageBox(QMessageBox):
    def __init__(self, type_, text, parent=None):
        super().__init__(parent)
        self.setIcon(type_)
        self.setText(text)
        self.setWindowTitle("eTasks")



if __name__ == "__main__":
    app = QApplication(sys.argv)

    box = MessageBox(QMessageBox.Icon.Information, "Hello, World")
    box.exec()
    sys.exit(app.exec())
