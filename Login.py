from PyQt6.QtWidgets import QApplication, QPushButton, QLabel, QWidget, QMainWindow, QFormLayout, QMessageBox
from Entries import Entry
import sqlite3
from etasksMessageBox import MessageBox
from PyQt6.QtCore import Qt
import bcrypt
from home import Home
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShortcut, QKeySequence
from Register import RegisterWindow
class LoginWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QFormLayout()
        self.home = None
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        self.setWindowTitle('eTasks Login')


        self.title = QLabel('eTasks Login')
        self.title.setStyleSheet("""
    padding-left: 20px; 
    padding-right: 20px;
    font-size: 15px;
    text-decoration: underline;
    font-weight: bold;
    color: #00008B;
    """
                                 )
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)




        self.layout.addWidget(self.title)


        self.usernameEntry = Entry.InfoEntry('Username: ')
        self.layout.addRow(self.usernameEntry)

        self.passwordEntry = Entry.PasswordEntry(verify=False, required = False)
        self.layout.addRow(self.passwordEntry)
        self.noAccount = QPushButton('Create account')
        self.noAccount.clicked.connect(self.new_account)
        self.layout.addRow(self.noAccount)
        self.loginbtn = QPushButton('Login')
        self.loginbtn.clicked.connect(self.login)
        self.layout.addRow(self.loginbtn)
        shortcut = QShortcut(QKeySequence(Qt.Key.Key_Return), self)
        shortcut.activated.connect(self.loginbtn.click)

            
        username = self.usernameEntry.entry.text()
        password = self.passwordEntry.password_box.entry.text()
    def new_account(self):
        window = RegisterWindow(self)
        window.show()
    def login(self):
        if not all([self.usernameEntry.get_value(), self.passwordEntry.get_value()]):
            warning = MessageBox(QMessageBox.Icon.Warning, "Please fill out all fields")
            warning.exec()
            return

        username = self.usernameEntry.entry.text()
        input_password = self.passwordEntry.password_box.entry.text().encode('utf-8')

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        # Fetch the hashed password and salt for the given username
        c.execute("SELECT password, salt FROM users WHERE username=?", (username,))
        result = c.fetchone()

        if result:
            stored_hashed_password, stored_salt = result

            # Hash the user-input password with the stored salt
            hashed_input_password = bcrypt.hashpw(input_password, stored_salt.encode('utf-8'))

            # Compare the hashed input password with the stored hashed password
            if hashed_input_password == stored_hashed_password:

                c.execute("SELECT fname FROM users WHERE username=?", (username,))
                self.fname = c.fetchone()[0]
                self.home = Home(self.fname)
                self.home.show()
                self.close()
                
            else:
                warning = MessageBox(QMessageBox.Icon.Warning, "Invalid password")
                warning.exec()
        else:
            warning = MessageBox(QMessageBox.Icon.Warning, "No account found for this username")
            warning.exec()

        conn.close()


if __name__ == '__main__':

    app = QApplication([])
    win = LoginWindow()
    win.show()
    app.exec()


