import sys
from PyQt6.QtWidgets import QApplication, QSizePolicy, QFrame, QWidget, QVBoxLayout, QLabel, QCheckBox, QHBoxLayout
from PyQt6.QtCore import Qt

class Task(QWidget):
    def __init__(self, taskname, startDate, endDate, parent=None):
        super(Task, self).__init__(parent)

        # Store the task name
        self.taskname = taskname
        self.startDate = startDate
        self.endDate = endDate

        # Main Layout
        mainLayout = QVBoxLayout(self)
        mainLayout.setSpacing(5)                 # Adjust spacing between widgets to 5 pixels
        mainLayout.setContentsMargins(0, 0, 0, 0)  # Set margins to 10 pixels on all sides

        mainframe = QFrame(self)
        mainframe.setFrameShape(QFrame.Shape.Box)
        mainLayout.addWidget(mainframe, alignment=Qt.AlignmentFlag.AlignTop)
        mainframeLayout = QHBoxLayout(mainframe)

        # Check Box
        checkBox = QCheckBox(self)
        mainframeLayout.addWidget(checkBox)

        # Task Name Frame & Label
        tasknameFrame = QFrame(self)
        tasknameFrame.setFrameShape(QFrame.Shape.Box)
        tasknameFrameLayout = QVBoxLayout(tasknameFrame)
        tasknameLabel = QLabel(self.taskname, tasknameFrame)
        tasknameFrameLayout.addWidget(tasknameLabel)
        mainframeLayout.addWidget(tasknameFrame)

        # Start Date Frame & Label
        sDateFrame = QFrame(self)
        sDateFrame.setFixedSize(320, 40)
        sDateFrame.setFrameShape(QFrame.Shape.Box)
        sDateLayout = QHBoxLayout(sDateFrame)
        if startDate is None:
            sDateLabel = QLabel(f'Starts: No Start Date')
        else:
            sDateLabel = QLabel(f'Starts: {startDate}')
        sDateLayout.addWidget(sDateLabel)
        mainframeLayout.addWidget(sDateFrame)

        # End Date Frame & Label
        dDateFrame = QFrame(self)
        dDateFrame.setFixedSize(320, 40)
        dDateFrame.setFrameShape(QFrame.Shape.Box)
        dDateLayout = QHBoxLayout(dDateFrame)
        if endDate is None:
            endDateLabel = QLabel('Starts: No End Date')
        else:
            endDateLabel = QLabel(f"Ends: {endDate}")
        dDateLayout.addWidget(endDateLabel)
        mainframeLayout.addWidget(dDateFrame)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

  # sets both horizontal and vertical policies to Fixed



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = Task('Task Name', 'sdate', 'edate')
    mainWindow.showMaximized()
    sys.exit(app.exec())
