from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton

class MyWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout = QVBoxLayout(central_widget)
        self.widget = QPushButton('foo1')
        self.widget2 = QPushButton('foo2')
        self.layout.addWidget(self.widget)
        self.layout.addWidget(self.widget2)

        self.find_widgets()

    def foo(self, w):
        print('foo at widget', w)
        w.setParent(None)

    def find_widgets(self):
        for widget in self.findChildren(QPushButton):
            print(f"Widget: {widget}")
            if isinstance(widget, QPushButton):
                print(f'Connecting widget {widget} to self.foo()')
                widget.clicked.connect(lambda checked, widget=widget: self.foo(widget))

if __name__ == "__main__":
    app = QApplication([])
    mainWin = MyWindow()
    mainWin.show()
    app.exec()
