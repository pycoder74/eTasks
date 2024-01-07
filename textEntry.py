class ComboText(QWidget):
    def __init__(self, text, *args, **kwargs):
    super().__init__(*args, **kwargs)
    layout = QHBoxLayout()
    self.label = QLabel(text)
    layout.addWidget(self.label)
    
