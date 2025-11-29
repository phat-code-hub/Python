from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
import sys

class A(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("No sys.argv Demo")
        self.label = QLabel("Hello")
        self.button = QPushButton("Click Me")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

app = QApplication([])  # ✅ no sys.argv here
window = A()
window.show()
app.exec()
