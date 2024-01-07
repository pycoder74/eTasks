from PyQt6.QtWidgets import QSizePolicy, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from quickbarframe import VLQuickBarFrame, HLQuickBarFrame
from get_current_date import get_month, get_cdaymnth, get_cday, update_time, get_current_time
from getweather import get_weather
import asyncio
from ImageButton import ImageButton
import sys

class QuickBar(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__()
        self.setWindowTitle("Quickbar")

        main_layout = QVBoxLayout(self)  # Main vertical layout
        h_layout = QHBoxLayout()  # Horizontal layout for frames and widgets
        main_layout.addLayout(h_layout)

        timedateframe = HLQuickBarFrame()
        timedateframe.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        

        # Get combined date and time string
        current_date_str = f"{get_cday()}, {get_cdaymnth()} {get_month()} -"
        date = QLabel(current_date_str)
        timedateframe.add_widget(date)
        combined_datetime_str = f"{current_date_str} {get_current_time()}"  # Initial setting

        timelabel = QLabel(combined_datetime_str)
        timelabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        timedateframe.add_widget(timelabel)

        # Set up the timer to update this label every second
        update_time(timelabel)        
        # Create the temp frame and add it to the layout
        tempframe = VLQuickBarFrame()
        ctemp = asyncio.run(get_weather())
        templbl = QLabel(ctemp)
        tempframe.add_widget(templbl)
        tempframe.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        templbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create the app frame and add it to the layout
        appframe = VLQuickBarFrame()
        app = QLabel('eos apps')
        appframe.add_widget(app)

        buttonframe = HLQuickBarFrame()
        buttonframe.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)

        def home_button_clicked():
            home = Home(parent=self)
            home.show()

        def setting_button_clicked():
            settings = SettingWin(self)
            settings.show()

        # Create the home button
        homebutton = ImageButton('Home_Icon.png')
        homebutton.clicked.connect(home_button_clicked)
        homebutton.setFixedSize(50, 50)

        settingbutton = ImageButton('Settings_Icon.png')
        settingbutton.clicked.connect(setting_button_clicked)
        settingbutton.setFixedSize(50, 50)

        buttonframe.add_widget(homebutton)
        buttonframe.add_widget(settingbutton)

        # Add frames and widgets to h_layout
        h_layout.addWidget(timedateframe)
        h_layout.addWidget(tempframe)
        h_layout.addWidget(appframe)
        h_layout.addWidget(buttonframe)

        # Push everything to the top of the main window
        main_layout.addStretch(1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QuickBar()
    window.show()
    sys.exit(app.exec())
