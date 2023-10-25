from PyQt6.QtWidgets import QApplication, QPushButton, QLabel, QWidget, QMainWindow, QFormLayout, QMessageBox
from Entries import Entry
import sqlite3
from etasksMessageBox import MessageBox
from PyQt6.QtCore import Qt
import bcrypt
from create_task_table import create_table
from PyQt6.QtGui import QShortcut, QKeySequence
class RegisterWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QFormLayout()

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        self.setWindowTitle('Create eTasks Account')


        self.title = QLabel('Register for eTasks')
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

        self.FnameEntry = Entry.InfoEntry('* First Name:')
        self.layout.addRow(self.FnameEntry)

        self.SnameEntry = Entry.InfoEntry('* Surname: ')
        self.layout.addRow(self.SnameEntry)

        self.usernameEntry = Entry.InfoEntry('* Username: ')
        self.layout.addRow(self.usernameEntry)

        self.passwordEntry = Entry.PasswordEntry(verify=False)
        self.layout.addRow(self.passwordEntry)

        self.VerifyPasswordEntry = Entry.PasswordEntry(verify=True)
        self.layout.addRow(self.VerifyPasswordEntry)

        self.addAccount = QPushButton('Register')
        self.addAccount.clicked.connect(self.Register)
        self.layout.addRow(self.addAccount)

        self.Loginbtn = QPushButton('Already have an account? Login')
        self.Loginbtn.clicked.connect(self.login)
        self.layout.addRow(self.Loginbtn)
        shortcut = QShortcut(QKeySequence(Qt.Key.Key_Return), self)
        shortcut.activated.connect(self.addAccount.click)

    def Register(self):
        if not all([self.FnameEntry.get_value(), self.SnameEntry.get_value(), self.usernameEntry.get_value(), self.passwordEntry.get_value()]):
            warning = MessageBox(QMessageBox.Icon.Warning, "Please fill out all fields")
            warning.exec()
            return
            
        fname = self.FnameEntry.entry.text()
        sname = self.SnameEntry.entry.text()
        username = self.usernameEntry.entry.text()
        password = self.passwordEntry.password_box.entry.text()
        verify_password = self.VerifyPasswordEntry.password_box.entry.text()
        
        if password != verify_password:
            warning = MessageBox(QMessageBox.Icon.Warning, "The passwords are not the same")
            warning.exec()
            return
        else:
            password_encoded = password.encode('utf-8')
            salt = bcrypt.gensalt()
            saltstr = salt.decode('utf-8')
            hashed_password = bcrypt.hashpw(password_encoded, salt)

        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        # Create table if it doesn't exist
        c.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fname TEXT NOT NULL,
            sname TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            salt TEXT NOT NULL
        )""")
        
        # Check if username exists
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user_exists = c.fetchone()
        
        if user_exists:
            message = MessageBox(QMessageBox.Icon.Information, "Username is already taken")
            message.exec()
            return
        
        
        
        # Insert user data
        c.execute("INSERT INTO users (fname, sname, username, password, salt) VALUES (?, ?, ?, ?, ?)",
                  (fname, sname, username, hashed_password, saltstr))
        create_table(c)
        conn.commit()
        conn.close()

        success = MessageBox(QMessageBox.Icon.Information, "Registration Success. Directing you to login page")
        success.exec()
        self.login()
        
    def login(self):
        self.close()
        from Login import LoginWindow
        self.window = LoginWindow(self)
        self.window.show()

if __name__ == '__main__':

    app = QApplication([])
    win = RegisterWindow()
    win.show()
    app.exec()

