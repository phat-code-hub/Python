# media_view.py
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
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(6)

        self.player = QMediaPlayer(self)
        self.output = QAudioOutput(self)
        self.player.setAudioOutput(self.output)

        # set source but do not autoplay
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
    # remove widgets and items
    while layout.count():
        item = layout.takeAt(0)
        w = item.widget()
        if w:
            w.setParent(None)
            w.deleteLater()

# ---------------------------------------------------------------------------
#  Clear preview system (top + bottom)
# ---------------------------------------------------------------------------
def clear_preview(self):
    # Stop and delete any media player if present
    if hasattr(self, "player") and self.player:
        try:
            self.player.stop()
        except Exception:
            pass
        try:
            self.player.deleteLater()
        except Exception:
            pass
        self.player = None

    if hasattr(self, "audio_output") and self.audio_output:
        try:
            self.audio_output.deleteLater()
        except Exception:
            pass
        self.audio_output = None

    # ----- TOP preview -----
    # Remove all child widgets from preview (robust)
    for child in self.preview.findChildren(QWidget):
        child.setParent(None)
        try:
            child.deleteLater()
        except Exception:
            pass

    # Ensure top layout exists and clear it
    if self.preview.layout() is None:
        self.preview.setLayout(QVBoxLayout())
    else:
        clear_layout(self.preview.layout())

    # Put back the default "Preview Area" label if needed
    # If the preview should show default text, caller can add it; we'll keep it blank here.
    default_label = QLabel("Preview Area")
    default_label.setAlignment(default_label.alignment())
    self.preview.layout().addWidget(default_label)

    # ----- BOTTOM preview -----
    # Remove all child widgets from bottom_area (robust)
    for child in self.bottom_area.findChildren(QWidget):
        child.setParent(None)
        try:
            child.deleteLater()
        except Exception:
            pass

    # Ensure bottom layout exists and clear it
    if self.bottom_area.layout() is None:
        self.bottom_area.setLayout(QVBoxLayout())
    else:
        clear_layout(self.bottom_area.layout())

    QCoreApplication.processEvents()

# ---------------------------------------------------------------------------
#  Main controller
# ---------------------------------------------------------------------------
def main_media(self, filepath, ext, order):
    # Use the robust clear_preview from this module
    clear_preview(self)

    # =============================== AUDIO ===============================
    if order == 10:
        # Ensure top preview layout exists (it will already due to clear_preview)
        if self.preview.layout() is None:
            self.preview.setLayout(QVBoxLayout())

        # Ensure bottom layout exists
        if self.bottom_area.layout() is None:
            self.bottom_area.setLayout(QVBoxLayout())

        # Show filename at top
        name_label = QLabel(os.path.basename(filepath))
        name_label.setStyleSheet("font-weight:bold; padding:4px;")
        # Add filename to preview
        self.preview.layout().addWidget(name_label)

        # Add audio controls widget (parented to bottom_area)
        audio_widget = AudioPlayerWidget(filepath, self.bottom_area)
        self.bottom_area.layout().addWidget(audio_widget)

        return

    # =============================== VIDEO ===============================
    elif order == 7:
        preview_video(self, filepath)
        return

    # ======================= Unsupported Files ==========================
    # If not media or video or audio, show unsupported text at top
    if self.preview.layout() is None:
        self.preview.setLayout(QVBoxLayout())

    clear_layout(self.preview.layout())  # clear top
    clear_layout(self.bottom_area.layout())  # clear bottom
    msg = QLabel("[Unsupported file type]")
    msg.setAlignment(msg.alignment())
    self.preview.layout().addWidget(msg)


# ---------------------------------------------------------------------------
#  Video Preview
# ---------------------------------------------------------------------------
def preview_video(self, filepath):
    # Ensure top preview has layout (clear_preview already ensured it)
    if not self.preview.layout():
        self.preview.setLayout(QVBoxLayout())

    # Clear top area for video
    clear_layout(self.preview.layout())

    # Video widget parented to self.preview
    video_widget = QVideoWidget(self.preview)
    video_widget.setMinimumHeight(200)
    self.preview.layout().addWidget(video_widget)

    # Ensure bottom layout exists
    if self.bottom_area.layout() is None:
        self.bottom_area.setLayout(QVBoxLayout())
    else:
        clear_layout(self.bottom_area.layout())

    # Create player
    self.player = QMediaPlayer(self)
    self.audio_output = QAudioOutput(self)
    self.player.setAudioOutput(self.audio_output)
    self.player.setVideoOutput(video_widget)
    self.player.setSource(QUrl.fromLocalFile(filepath))
    self.player.play()

    # Add filename or controls to bottom_area
    self.bottom_area.layout().addWidget(QLabel(os.path.basename(filepath)))
