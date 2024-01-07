from PyQt6.QtWidgets import QLabel, QFrame, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QApplication, QMainWindow
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class VLQuickBarFrame(QFrame):
    def __init__(self, parent = None):
        super().__init__()
        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(2)
        self.layout = QVBoxLayout(self)
        self.layout.addStretch(1)  # Push widgets to the center

    def add_widget(self, widget: QWidget):
        self.layout.addWidget(widget)
        font = QFont('Arial', 20, 60)
        widget.setFont(font)
        self.layout.addStretch(1)
        widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

class HLQuickBarFrame(QFrame):
    def __init__(self):
        super().__init__(parent = None)
        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(2)
        self.layout = QHBoxLayout(self)
        self.layout.addStretch(1)  # Push widgets to the center

    def add_widget(self, widget: QWidget):
        self.layout.addWidget(widget)
        font = QFont('Arial', 20, 60)
        widget.setFont(font)
        self.layout.addStretch(1)
        

if __name__ == '__main__':
    app = QApplication([])
    window = QMainWindow()
    
    central_widget = QWidget()
    main_layout = QVBoxLayout(central_widget)  # Main vertical layout
    
    # Create a horizontal layout for the frames
    frames_layout = QHBoxLayout()
    
    frame = VLQuickBarFrame()
    text = QLabel(text='QLabel')
    frame.add_widget(text)  # Add the first frame to the horizontal layout

    newframe = HLQuickBarFrame()
    text = QLabel('HL')
    newframe.add_widget(text)
    frames_layout.addWidget(newframe)  # Add the second frame to the horizontal layout

    # Wrap the horizontal layout with a QWidget so it doesn't stretch
    wrapper_widget = QWidget()
    wrapper_widget.setLayout(frames_layout)

    main_layout.addWidget(wrapper_widget)  # Add the wrapper widget to the main layout
    main_layout.addStretch(1)  # Push frames to the top

    window.setCentralWidget(central_widget)
    window.show()

    app.exec()
