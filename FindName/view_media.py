# media_view.py
import os
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QUrl
from PySide6.QtMultimedia import QMediaPlayer
import actions

def main_media(self, filepath,ext,ord):
    self.player.setVideoOutput(self.video_widget)
    self.player.setAudioOutput(self.audio_output)
    try:
        self.player.setSource(QUrl.fromLocalFile(filepath))
        self.player.setPosition(0)
    except Exception as e:
        self.play_button.setText("Play")
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
    show_media_thumbnail(self.full_path)
#-------------Sound Control ----------------------------------
def on_volume_changed(self, value ):
    normalized = value / self.MAX_VOL
    volume = min(1.0, normalized ** 1.5)
    self.audio_output.setVolume(volume)
#----------------------------------------
def toggle_mute(self, checked):
    self.audio_output.setMuted(checked)
    self.mute_button.setText("Unmute" if checked else "Mute")


#-------------Elapsed Timer --------------------------------------
def on_slider_pressed(self):
    self.is_seeking = True
    self.was_playing = (
        self.player.playbackState() == QMediaPlayer.PlayingState
    )
    self.player.pause()
#----------------------------------------
def on_slider_released(self):
    self.is_seeking = False
    self.player.setPosition(self.seek_slider.value())
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
    print("update_time_label called with:", position)
    cur = format_time(self,position)
    total = format_time(self,self.player.duration())
    self.timer.setText(f"{cur} / {total}")  

def on_position_changed(self, pos):
    if self.is_seeking:
        return
    self.seek_slider.setValue(pos)
    update_time_label(self, pos)


def show_media_thumbnail(self,filepath):
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