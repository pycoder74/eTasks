from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QFormLayout, QTimeEdit

class TimeEntry(QWidget):
    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QFormLayout()
        
        self.label = QLabel(text)
        self.time_edit = QTimeEdit()
        
        layout.addRow(self.label, self.time_edit) 
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication([])
    window = QMainWindow()
    
    time_entry = TimeEntry('Time:')
    window.setCentralWidget(time_entry)
    
    window.show()
    app.exec()
