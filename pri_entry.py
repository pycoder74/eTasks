from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QHBoxLayout, QRadioButton

class PriEntry(QWidget):
    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QHBoxLayout()
        self.label = QLabel(text)
        layout.addWidget(self.label)
        priChoices = ["High", "Medium", "Low"]
        self.radiobuttons = []
        for i in priChoices:
            radiobutton = QRadioButton(text=i)
            self.radiobuttons.append(radiobutton)
            layout.addWidget(radiobutton)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication([])
    window = QMainWindow()

    priority = PriEntry('Priority:')
    window.setCentralWidget(priority)

    window.show()
    app.exec()
