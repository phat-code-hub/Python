import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QUrl


class MediaPlayerUI(QWidget):
    def __init__(self, media_path):
        super().__init__()

        self.setWindowTitle("PySide6 Media Player")
        self.resize(800, 500)

        # ===== Media objects =====
        self.player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.player.setAudioOutput(self.audio_output)

        self.video_widget = QVideoWidget(self)
        self.player.setVideoOutput(self.video_widget)

        self.player.setSource(QUrl.fromLocalFile(media_path))

        # ===== Buttons =====
        self.play_button = QPushButton("Play")
        self.stop_button = QPushButton("Stop")

        self.play_button.clicked.connect(self.toggle_play)
        self.stop_button.clicked.connect(self.stop_media)

        # ===== Layout =====
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.stop_button)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.video_widget)
        main_layout.addLayout(button_layout)

        # ===== Initial state =====
        self.player.pause()   # start paused
        self.play_button.setText("Play")

    # ==============================
    # Slots
    # ==============================
    def toggle_play(self):
        if self.player.playbackState() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.play_button.setText("Play")
        else:
            self.player.play()
            self.play_button.setText("Pause")

    def stop_media(self):
        self.player.stop()
        self.play_button.setText("Play")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # CHANGE THIS PATH TO YOUR MEDIA FILE
    media_file = r"D:\\Yamazaki\\Test Sample\\hong.mov"   # .mp3 or .avi also works

    window = MediaPlayerUI(media_file)
    window.show()

    sys.exit(app.exec())
