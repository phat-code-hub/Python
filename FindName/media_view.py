# media_view.py
import os
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QUrl

def show_media_thumbnail(self, filepath):
    base, ext = os.path.splitext(filepath)
    for candidate_ext in (".jpg", ".jpeg", ".png", ".bmp"):
        candidate = base + candidate_ext
        if os.path.exists(candidate):
            pix = QPixmap(candidate)
            self.image_view.setPixmap(pix.scaled(
                max(1, self.preview_top.width()),
                max(1, self.preview_top.height()),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation))
            self.preview_top.setCurrentWidget(self.image_view)
            return
    self.text_view.setText(f"[Media file]\n{os.path.basename(filepath)}")
    self.preview_top.setCurrentWidget(self.text_view)

def prepare_media_player(self, filepath):
    try:
        url = QUrl.fromLocalFile(os.path.abspath(filepath))
        self.media_player.setSource(url)
        self.preview_bottom.setVisible(True)
        self.media_player.pause()
        self.play_button.setText("Play")
    except Exception as e:
        print("Media prepare error:", e)
        self.text_view.setText("[Cannot prepare media]")
        self.preview_top.setCurrentWidget(self.text_view)
        self.preview_bottom.setVisible(False)
