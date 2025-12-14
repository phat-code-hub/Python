import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl

app = QApplication(sys.argv)

player = QMediaPlayer()
audio = QAudioOutput()
audio.setVolume(0.5)

player.setAudioOutput(audio)
player.setSource(QUrl.fromLocalFile(r"C:\Windows\Media\Alarm01.wav"))
player.play()

sys.exit(app.exec())
