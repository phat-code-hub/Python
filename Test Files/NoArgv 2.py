from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
import sys

class A(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel("Engine: OFF")
        self.button = QPushButton("Start")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

class B:
    def __init__(self, form: A):
        self.form = form
        self.running = False
        self.form.button.clicked.connect(self.toggle)

    def toggle(self):
        self.running = not self.running
        if self.running:
            self.form.label.setText("Engine: RUNNING")
        else:
            self.form.label.setText("Engine: OFF")

app = QApplication([])  # ✅ again, no sys.argv
form = A()
controller = B(form)
form.show()
app.exec()
