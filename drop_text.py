from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QFormLayout, QComboBox

class DropEntry(QWidget):
    def __init__(self, text, items, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QFormLayout()
        self.label = QLabel(text)
        self.drop = QComboBox()
        self.items = items
        self.drop.addItems(self.items)
        layout.addRow(self.label, self.drop)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication([])
    window = QMainWindow()

    entry = DropEntry('Combobox:', ['1', '2', '3'])
    window.setCentralWidget(entry)

    window.show()
    app.exec()
