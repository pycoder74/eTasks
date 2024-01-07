from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QFormLayout
import sys
from Entries import Entry
class SignUp(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Sign up to eos')
        self.central_widget = QWidget(self)  # Central widget to hold the layout
        self.setCentralWidget(self.central_widget)
        
        self.layout = QFormLayout(self.central_widget)  # Set layout to the central_widget

        self.layout.setVerticalSpacing(0)  # Set vertical spacing to 0
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.username_entry = Entry.InfoEntry(text='Username:')
        self.layout.addRow(self.username_entry)

        self.password_entry = Entry.PasswordEntry()
        self.layout.addRow(self.password_entry)


        self.show()

if __name__ == '__main__':
    app = QApplication([])

    signUpWindow = SignUp()

    signUpWindow.show()
    sys.exit(app.exec())

