from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PySide6.QtGui import QFont, QColor
import sys


# --- A: defines the form (UI) ---
class A(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Car Form - Class A")
        self.resize(300, 150)

        # UI components
        self.label = QLabel("Engine: OFF")
        self.label.setFont(QFont("Arial", 14))
        self.label.setStyleSheet("color: blue;")

        self.button = QPushButton("Start Engine")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)


# --- B: extends A, adds behavior ---
class B(A):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Car Form - Class B (Behavior)")

        # Modify A's label property
        self.label.setStyleSheet("color: red;")

        # Connect button click event
        self.button.clicked.connect(self.on_button_click)

    def on_button_click(self):
        self.label.setText("Engine: RUNNING")
        self.button.setText("Stop Engine")
        # You can also change behavior later, for example:
        self.button.clicked.disconnect() # Disconnect previous connection
        self.button.clicked.connect(self.on_stop_click)

    def on_stop_click(self):
        self.label.setText("Engine: OFF")
        self.button.setText("Start Engine")
        self.button.clicked.disconnect() # Disconnect previous connection
        self.button.clicked.connect(self.on_button_click)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = B()
    window.show()
    sys.exit(app.exec())
