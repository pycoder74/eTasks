from datetime import datetime
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QLabel
def get_month():
    today = datetime.today()
    cdate = today.strftime("%B")
    return cdate

def get_cdaymnth():
    today = datetime.today()
    cdaymnth = today.strftime("%d")
    return cdaymnth

def get_cday():
    today = datetime.today()
    cday = today.strftime("%A")
    return cday

def get_current_time():
    current_time = datetime.now().strftime('%H:%M:%S')
    return current_time


def update_time(label: QLabel):
    current_time = get_current_time()
    label.setText(current_time)
    QTimer.singleShot(1000, lambda: update_time(label))
