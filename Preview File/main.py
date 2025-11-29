import sys
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QListWidget, QLabel, QPushButton,
    QVBoxLayout, QTextEdit, QMessageBox
)
from PySide6.QtGui import QPixmap,QImageReader
from PySide6.QtCore import Qt

import docx
import openpyxl

# import FreeCAD
# import FreeCADGui
# import Part

class PreviewForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Preview Demo")
        self.resize(500, 600)

        # ----- UI Controls -----
        self.listbox = QListWidget()
        self.preview = QLabel("Preview Area")
        self.preview.setStyleSheet("border: 1px solid gray;")
        self.preview.setMinimumHeight(250)
        self.preview.setWordWrap(True)

        self.cancel_btn = QPushButton("Cancel")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.listbox)
        layout.addWidget(self.preview)
        layout.addWidget(self.cancel_btn)
        self.setLayout(layout)

        # Files
        self.add_demo_files()

        # Events
        self.listbox.currentItemChanged.connect(self.on_file_selected)
        self.cancel_btn.clicked.connect(self.close)

    # -----------------------------------------
    # Add sample files
    # -----------------------------------------
    def add_demo_files(self):
        # Replace with your real full paths
        files = [
            r"C:\MyData\example\Pic.jpg",
            r"C:\MyData\example\Pic.pdf",
            r"C:\MyData\example\Pic.xlsx",
            r"C:\MyData\example\Pic.png",
            r"C:\MyData\example\Pic.txt",
            r"C:\MyData\example\Pic.docx",
            r"C:\MyData\example\原紙.xlsx",
            r"C:\MyData\example\Pic2.xlsx",
        ]
        for f in files:
            self.listbox.addItem(f)

    # -----------------------------------------
    # File selected → Preview
    # -----------------------------------------
    def on_file_selected(self, current, previous):
        if not current:
            self.clear_preview()
            return

        filepath = current.text()
        ext = os.path.splitext(filepath)[1].lower()
        # Check supported types
        #Check if it  is image, pdf
        supported_ext = [b"." + fmt for fmt in QImageReader.supportedImageFormats()]
        if ext.encode() in supported_ext:
            self.preview_image(filepath)
        #Check if it is plaintext
        TEXT_EXT = [
            ".txt",
            ".ini",
            ".md",
            ".csv",
            ".yml",
            ".yaml",
            ".log",
            ".json"
        ]
        # CAD_EXT = ['.step', '.stp', '.iges', '.igs']
        CAD_EXT = ['.vwx', '.dwg', '.dxf']
        self.clear_preview
        if ext in  TEXT_EXT:
            self.preview_text(filepath)
        if ext == ".docx":
            self.preview_word(filepath)
        if ext == ".xlsx":
            self.preview_excel(filepath)
    # -----------------------------------------
    # Preview Methods
    # -----------------------------------------
    def preview_text(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            self.preview.setText(content)
        except:
            self.preview.setText("[Cannot read text file]")
    # -----------------------------------------
    def preview_image(self, filepath):
        pixmap = QPixmap(filepath)
        if pixmap.isNull():
            self.preview.setText("[Cannot load image]")
        else:
            scaled = pixmap.scaled(self.preview.width(), self.preview.height(),
                                Qt.KeepAspectRatio)
            self.preview.setPixmap(scaled)
    # ----------------------------------------- 
    def preview_word(self, filepath):
        from docx import Document
        try:
            doc = Document(filepath)
            text = "\n".join([p.text for p in doc.paragraphs])
            self.preview.setText(text if text else "[Empty Word document]")
        except:
            self.preview.setText("[Cannot preview Word file]")
    # -----------------------------------------
    def preview_excel(self, filepath, max_rows=10):
        try:
            wb = openpyxl.load_workbook(filepath, read_only=True)
            ws = wb.active
            text = ""
            for i, row in enumerate(ws.iter_rows(values_only=True)):
                text += "\t".join([str(cell) if cell is not None else "" for cell in row]) + "\n"
                if i + 1 >= max_rows:
                    break
            self.preview.setText(text if text else "[Empty Excel sheet]")
        except:
            self.preview.setText("[Cannot preview Excel file]")
    # -----------------------------------------
    # -----------------------------------------
    def clear_preview(self):
        self.preview.clear()
        self.preview.setText("")


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = PreviewForm()
    w.show()
    sys.exit(app.exec())
