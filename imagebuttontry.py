from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QIcon
import sys
from quickbarframe import QuickBarFrame
from get_current_date import get_month, get_cdaymnth, get_cday, update_time
from getweather import get_weather
import asyncio
from ImageButton import ImageButton


app = QApplication(sys.argv)
window = QMainWindow()
button = ImageButton('Home_Icon.png')
window.setCentralWidget(button)
window.show()
sys.exit(app.exec())
