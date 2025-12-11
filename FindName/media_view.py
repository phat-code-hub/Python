import os
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import QUrl, QCoreApplication
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget


# ---------------------------------------------------------------------------
#  Audio Player Widget (Self-contained)
# ---------------------------------------------------------------------------
class AudioPlayerWidget(QWidget):
    def __init__(self, file_path, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.player = QMediaPlayer()
        self.output = QAudioOutput()
        self.player.setAudioOutput(self.output)

        self.player.setSource(QUrl.fromLocalFile(file_path))

        btnPlay = QPushButton("Play")
        btnPause = QPushButton("Pause")
        btnStop = QPushButton("Stop")

        btnPlay.clicked.connect(self.player.play)
        btnPause.clicked.connect(self.player.pause)
        btnStop.clicked.connect(self.player.stop)

        layout.addWidget(btnPlay)
        layout.addWidget(btnPause)
        layout.addWidget(btnStop)

# ---------------------------------------------------------------------------
#  Layout clearing helper
# ---------------------------------------------------------------------------
def clear_layout(layout):
    if layout is None:
        return
    while layout.count():
        item = layout.takeAt(0)
        w = item.widget()
        if w:
            w.deleteLater()


# ---------------------------------------------------------------------------
#  Clear preview system (top + bottom)
# ---------------------------------------------------------------------------
def clear_preview(self):
    # Stop old media player
    if hasattr(self, "player") and self.player:
        try:
            self.player.stop()
        except:
            pass
        self.player.deleteLater()
        self.player = None

    if hasattr(self, "audio_output") and self.audio_output:
        self.audio_output.deleteLater()
        self.audio_output = None

    # ----- TOP PREVIEW -----
    # Remove all child widgets
    for child in self.preview.findChildren(QWidget):
        child.setParent(None)
        child.deleteLater()
        
    if self.preview.layout() is None:
        self.preview.setLayout(QVBoxLayout())
    else:
        clear_layout(self.preview.layout())
        
    # Clear bottom preview
    # Remove all child widgets
    for child in self.bottom_area.findChildren(QWidget):
        child.setParent(None)
        child.deleteLater()
    if self.bottom_area.layout() is None:
        self.bottom_area.setLayout(QVBoxLayout())
    else:
        clear_layout(self.bottom_area.layout())


    QCoreApplication.processEvents()


# ---------------------------------------------------------------------------
#  Main controller
# ---------------------------------------------------------------------------
def main_media(self, filepath, ext, order):
    clear_preview(self)

    # =============================== AUDIO ===============================
    if order == 10:
        # Ensure top preview layout exists
        if self.preview.layout() is None:
            self.preview.setLayout(QVBoxLayout())

        # Ensure bottom layout exists
        # HARD RESET bottom_area: remove ALL child widgets
        for child in self.bottom_area.findChildren(QWidget):
            child.setParent(None)
            child.deleteLater()
        if self.bottom_area.layout() is None:
            self.bottom_area.setLayout(QVBoxLayout())
        else:
            clear_layout(self.bottom_area.layout())

        # CLEAR old filename before showing new one
        clear_layout(self.preview.layout())

        # Clear old bottom (important)
        clear_layout(self.bottom_area.layout())

        # Add audio controls widget (one only)
        audio_widget = AudioPlayerWidget(filepath, self.bottom_area)
        self.bottom_area.layout().addWidget(audio_widget)

        return

    # =============================== VIDEO ===============================
    elif order == 7:
        preview_video(self, filepath)
        return

    # ======================= Unsupported Files ==========================
    if self.preview.layout() is None:
        self.preview.setLayout(QVBoxLayout())
    # Clear preview (top)
    clear_layout(self.preview.layout())
    # Clear bottom-area (audio/video widgets)
    if self.bottom_area.layout():
        clear_layout(self.bottom_area.layout())
    
    # Show unsupported message
    msg = QLabel("[Unsupported file type]")
    self.preview.layout().addWidget(msg)
    
    # self.preview.setText("[Unsupported file type]")


# ---------------------------------------------------------------------------
#  Video Preview
# ---------------------------------------------------------------------------
def preview_video(self, filepath):
    # Ensure top preview has layout
    if not self.preview.layout():
        self.preview.setLayout(QVBoxLayout())

    # Video widget
    video_widget = QVideoWidget(self)
    self.preview.layout().addWidget(video_widget)

    # Ensure bottom layout exists
    if self.bottom_area.layout() is None:
        self.bottom_area.setLayout(QVBoxLayout())

    # Create player
    self.player = QMediaPlayer(self)
    self.audio_output = QAudioOutput(self)
    self.player.setAudioOutput(self.audio_output)
    self.player.setVideoOutput(video_widget)
    self.player.setSource(QUrl.fromLocalFile(filepath))
    self.player.play()

    self.bottom_area.layout().addWidget(QLabel(os.path.basename(filepath)))
