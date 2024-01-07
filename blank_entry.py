from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QFormLayout, QPushButton
from Entries import Entry

class Window(QMainWindow):
    def __init__ (self, parent = None):
        super().__init__(parent)

        self.layout = QFormLayout()

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        self.entry = Entry.InfoEntry('')
        self.layout.addRow(self.entry)

        self.valuebtn = QPushButton(text = 'Get text')
        self.valuebtn.clicked.connect(self.get_value)
        self.layout.addRow(self.valuebtn)

    def get_value(self):
        value = self.entry.entry.text()
        if value:
            print(value)
        else:
            print('empty')
            
if __name__ == '__main__':

    app = QApplication([])
    win = Window()
    win.show()
    app.exec()

