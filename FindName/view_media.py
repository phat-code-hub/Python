# media_view.py
import math
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QUrl
from PySide6.QtMultimedia import QMediaPlayer
import actions

def main_media(self, filepath,ext,ord):
    # self.player = QMediaPlayer()
    self.player.setVideoOutput(self.video_widget)
    self.player.setAudioOutput(self.audio_output)
    try:
        self.player.setSource(QUrl.fromLocalFile(filepath))
        self.player.setPosition(0)
    except Exception as e:
        self.text_view.setText("[Cannot prepare media]")
        self.preview_top.setCurrentWidget(self.text_view)
#------------------------------------------------------------------------


def on_play(self):
    if self.player.playbackState() == QMediaPlayer.PlayingState:
        self.player.pause()
        self.play_button.setText("Play")
    else:
        self.player.play()
        self.play_button.setText("Pause")
#------------------------------------------------------------------------
def on_stop(self):
    self.player.stop()
    self.play_button.setText("Play")

#-------------Sound Control ----------------------------------
def on_volume_changed(self, value = 10):
    if value == 0:
        volume = 0.0
    else:
        volume = math.pow(value / 100.0, 2.0)
    self.audio_output.setVolume(volume)
#----------------------------------------
def toggle_mute(self, checked):
    self.audio_output.setMuted(checked)
    self.mute_button.setText("undue" if checked else "Mute")


#-------------Elapsed Timer --------------------------------------
def on_slider_pressed(self):
    self.was_playing = (
        self.player.playbackState() == QMediaPlayer.PlayingState
    )
    self.player.pause()
#----------------------------------------
def on_slider_released(self):
    if self.was_playing:
        self.player.play()
#----------------------------------------
def on_duration_changed(self, duration):
    self.seek_slider.setRange(0, duration)
    self.seek_slider.setEnabled(True)
#----------------------------------------
def format_time(self, ms):
    s = ms // 1000
    return f"{s//60:02d}:{s%60:02d}"
#----------------------------------------
def update_time_label(self, position):
    cur = self.format_time(position)
    total = self.format_time(self.player.duration())
    self.timer.setText(f"{cur} / {total}")  








#------------------------------------------------------------------------
# def on_position_changed(self, pos =5000):
#     if self.player.duration() > 0:
#         # val = int(pos * 1000 / self.player.duration())
#         self.seek_slider.setRange(0,self.player.duration())
#         self.seek_slider.blockSignals(True)
#         self.seek_slider.setValue(pos)
#         self.seek_slider.blockSignals(False)

# def on_duration_changed(self, dur=100):
#     # duration known - can be used to update UI (optional)
#     if dur <= 0:
#         self.seek_slider.setEnabled(False)
#         return

#     self.seek_slider.setEnabled(True)
#     self.seek_slider.setRange(0, dur)

# def on_seek_slider_moved(self, value):
#     if self.player.duration() > 0:
#         position = int(self.player.duration() * (value / 1000.0))
#         self.player.setPosition(position)

# def on_volume_changed(self, value):
#     self.audio_output.setVolume(max(0.0, min(1.0, value / 100.0)))


# def show_media_thumbnail(self, filepath):
#     base, ext = os.path.splitext(filepath)
#     for candidate_ext in (".jpg", ".jpeg", ".png", ".bmp"):
#         candidate = base + candidate_ext
#         if os.path.exists(candidate):
#             pix = QPixmap(candidate)
#             self.image_view.setPixmap(pix.scaled(
#                 max(1, self.preview_top.width()),
#                 max(1, self.preview_top.height()),
#                 Qt.KeepAspectRatio,
#                 Qt.SmoothTransformation))
#             self.preview_top.setCurrentWidget(self.image_view)
#             return
#     self.text_view.setText(f"[Media file]\n{os.path.basename(filepath)}")
#     self.preview_top.setCurrentWidget(self.text_view)