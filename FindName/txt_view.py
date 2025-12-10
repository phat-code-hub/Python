# text_view.py
# Preview plain text files
from PySide6.QtGui import QPixmap,QImageReader
from PySide6.QtCore import Qt
import openpyxl
#----------------------------------------------------------------------
def main_txt(self, filepath,ext,kind,type):
    supported_ext = [b"." + fmt for fmt in QImageReader.supportedImageFormats()]
    

def preview_image(self, filepath):
        pixmap = QPixmap(filepath)
        if pixmap.isNull():
            self.preview.setText("[Cannot load image]")
        else:
            self.original_pixmap = pixmap   # ← store original full-quality image
            update_scaled_image(self)
#----------------------------------------------------------------------
def update_scaled_image(self):
        if self.original_pixmap is None:
            return
        scaled = self.original_pixmap.scaled(
            self.preview.width(),
            self.preview.height(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation   # ← smoother resize!
        )
        self.preview.setPixmap(scaled)
#----------------------------------------------------------------------

def preview_text(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            self.preview.setText(content)
        except:
            self.preview.setText("[Cannot read text file]")
#----------------------------------------------------------------------
def preview_word(self, filepath,max_lines=10):
        from docx import Document
        from docx.shared import Pt
        try:
            doc = Document(filepath)
            text =""
            for paragraph in doc.paragraphs:
                for run in paragraph.runs:
                    text += run.text +" "
                text +="\n"
                if max_lines and len(text.splitlines()) >= max_lines:
                    break
            text = text.rstrip()  # Remove trailing newline character
            self.preview.setText(text.rstrip() if text else "[Empty Word document]")
            self.preview.setAlignment(Qt.AlignLeft | Qt.AlignTop)  # Set alignment to left and top
            self.preview.setTextInteractionFlags(Qt.NoTextInteraction)  # Disable text interaction
        except:
            self.preview.setText("[Cannot preview Word file]")
#----------------------------------------------------------------------
def preview_excel(self, filepath, max_rows=10):
        try:
            wb = openpyxl.load_workbook(filepath, read_only=True)
            ws = wb.active
            text = ""
            for i, row in enumerate(ws.iter_rows(values_only=True)):
                text += "\t".join([str(cell) if cell is not None else "" for cell in row]) + "\n"
                if i + 1 >= max_rows:
                    break
            text = text.rstrip()  # Remove trailing newline character
            self.preview.setText(text if text else "[Empty Excel sheet]")
            self.preview.setAlignment(Qt.AlignLeft | Qt.AlignTop)  # Set alignment to left and top
            self.preview.setTextInteractionFlags(Qt.NoTextInteraction)  # Disable text interaction
        except:
            self.preview.setText("[Cannot preview Excel file]")
# -----------------------------------------