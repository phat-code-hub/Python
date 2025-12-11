from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton,QApplication
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import Qt, QUrl
import os,sys


class MediaPreview(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        self.player = None
        self.video_widget = None
        self.audio_output = None

    def clear_preview(self):
        """Remove old widgets and media player."""
        if self.player:
            self.player.stop()
            self.player.deleteLater()
            self.player = None

        for i in reversed(range(self.layout.count())):
            item = self.layout.takeAt(i)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def preview(self, filepath: str):
        """Show preview based on file type."""
        self.clear_preview()

        ext = os.path.splitext(filepath)[1].lower()

        if ext in [".mp3", ".wav", ".ogg", ".flac"]:
            self.preview_audio(filepath)
        elif ext in [".mp4", ".mkv", ".avi", ".mov"]:
            self.preview_video(filepath)
        else:
            self.layout.addWidget(QLabel("This file type is not supported here."))

    # ---------------------------
    # AUDIO PREVIEW
    # ---------------------------
    def preview_audio(self, filepath):
        self.player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.player.setAudioOutput(self.audio_output)

        play_button = QPushButton("Play / Pause")
        play_button.clicked.connect(
            lambda: self.player.play() if self.player.playbackState() == QMediaPlayer.StoppedState else
                    (self.player.pause() if self.player.playbackState() == QMediaPlayer.PlayingState else self.player.play())
        )

        self.layout.addWidget(QLabel(f"Audio file: {os.path.basename(filepath)}"))
        self.layout.addWidget(play_button)

        self.player.setSource(QUrl.fromLocalFile(filepath))

    # ---------------------------
    # VIDEO PREVIEW
    # ---------------------------
    def preview_video(self, filepath):
        self.player = QMediaPlayer(self)
        self.video_widget = QVideoWidget(self)
        self.audio_output = QAudioOutput(self)
        self.player.setAudioOutput(self.audio_output)

        self.layout.addWidget(QLabel(f"Video file: {os.path.basename(filepath)}"))
        self.layout.addWidget(self.video_widget)

        self.player.setVideoOutput(self.video_widget)
        self.player.setSource(QUrl.fromLocalFile(filepath))
        self.player.play()


# app = QApplication(sys.argv)
# form = MediaPreview
# form.show()
# sys.exit(app.exec())
if __name__ == "__main__":
    pp = QApplication(sys.argv)
    preview = MediaPreview()
    file  ="C:\MyData\example\\Pic1.mp3"
    # when user clicks an item in list box
    # preview.preview(file)
    preview.show()
    sys.exit(pp.exec())