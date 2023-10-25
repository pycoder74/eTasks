from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QFormLayout, QLineEdit


class InfoEntry(QWidget):
    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QFormLayout()
        self.label = QLabel(text)
        self.entry = QLineEdit()
        layout.addRow(self.label, self.entry)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication([])
    window = QMainWindow()

    entry = InfoEntry('Enter:')
    window.setCentralWidget(entry)

    window.show()
    app.exec()
