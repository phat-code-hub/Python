from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PySide6.QtGui import QFont
import sys


# --- A: UI form ---
class A(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Form A (View)")
        self.resize(300, 150)

        self.label = QLabel("Engine: OFF")
        self.label.setFont(QFont("Arial", 14))
        self.label.setStyleSheet("color: blue;")

        self.button = QPushButton("Start Engine")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)


# --- B: Controller (logic/behavior) ---
class B:
    def __init__(self, ui: A):
        self.ui = ui
        # Connect event handler
        self.ui.button.clicked.connect(self.toggle_engine)
        self.running = False

    def toggle_engine(self):
        if not self.running:
            self.ui.label.setText("Engine: RUNNING")
            self.ui.label.setStyleSheet("color: red;")
            self.ui.button.setText("Stop Engine")
            self.running = True
        else:
            self.ui.label.setText("Engine: OFF")
            self.ui.label.setStyleSheet("color: blue;")
            self.ui.button.setText("Start Engine")
            self.running = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = A()
    controller = B(form)
    form.show()
    sys.exit(app.exec())
