from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import Qt, QUrl
import os
def main_media(self,filepath,ext,ord ):
    pass

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