import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QDialog
)
from PySide6.QtCore import QTimer, Qt


class TimePopup(QDialog):
    """Popup window showing elapsed time — no buttons."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Elapsed Time")
        self.setWindowFlags(Qt.Tool | Qt.WindowStaysOnTopHint)

        self.label = QLabel("Elapsed: 0s")
        self.label.setStyleSheet("font-size: 18px; padding: 10px;")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    def update_time(self, sec):
        self.label.setText(f"Elapsed: {sec}s")


class MainForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Alphabet Loop App")

        self.label = QLabel("a")
        self.label.setStyleSheet("font-size: 30px;")

        self.btn = QPushButton("Start")
        self.btn.clicked.connect(self.start_process)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.btn)
        self.setLayout(layout)

        # Timers
        self.alphabet_timer = QTimer()
        self.alphabet_timer.timeout.connect(self.update_alphabet)

        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self.update_time_counter)

        # Counters
        self.elapsed = 0
        self.limit_seconds = 100
        self.alphabet_index = 0
        self.alphabet = [chr(i) for i in range(ord("a"), ord("z") + 1)]

        # Popup window
        self.popup = TimePopup()

    def start_process(self):
        self.btn.setEnabled(False)
        self.elapsed = 0
        self.alphabet_index = 0

        # Show popup
        self.popup.update_time(0)
        self.popup.show()

        # Start timers
        self.alphabet_timer.start(1000)   # ← alphabet loop EVERY 1 second
        self.time_timer.start(100)       # elapsed time every 1 second

    def update_alphabet(self):
        self.label.setText(self.alphabet[self.alphabet_index])
        self.alphabet_index = (self.alphabet_index + 1) % len(self.alphabet)

    def update_time_counter(self):
        self.elapsed += 1
        self.popup.update_time(self.elapsed)

        if self.elapsed >= self.limit_seconds:
            self.stop_all()
        

    def stop_all(self):
        self.alphabet_timer.stop()
        self.time_timer.stop()
        self.popup.close()
        self.btn.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = MainForm()
    form.show()
    sys.exit(app.exec())
