from PySide6.QtWidgets import (
    QApplication, QWidget, QListWidget, QLabel, QVBoxLayout,
    QSplitter, QListWidgetItem
)
from PySide6.QtCore import Qt
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Two-Pane File Preview UI")
        self.resize(800, 500)

        # --- Splitter ---
        splitter = QSplitter(Qt.Horizontal, self)

        # --- Left: List Box A ---
        self.list_widget = QListWidget()
        splitter.addWidget(self.list_widget)

        # Add sample items (files)
        for name in ["test1.txt", "image.png", "notes.pdf"]:
            QListWidgetItem(name, self.list_widget)

        # --- Right: Preview Control B ---
        self.preview_label = QLabel("Select a file to preview")
        self.preview_label.setAlignment(Qt.AlignCenter)
        splitter.addWidget(self.preview_label)

        # --- Layout ---
        layout = QVBoxLayout(self)
        layout.addWidget(splitter)

        # --- Connect event ---
        self.list_widget.itemClicked.connect(self.show_preview)

    def show_preview(self, item):
        filename = item.text()
        # simple preview for example
        self.preview_label.setText(f"Previewing:\n{filename}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
