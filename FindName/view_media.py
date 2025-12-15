# media_view.py
import os
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QUrl
from PySide6.QtMultimedia import QMediaPlayer
import actions

def main_media(self, filepath,ext,ord):
    try:
        #Enabled controls 
        actions.SetBottomView(self,True)
        self.media_player.setSource(QUrl.fromLocalFile(filepath))
        self.media_player.setPosition(0)
        # self.media_player.stop()
        try:
            self.play_button.clicked.disconnect()
            self.stop_button.clicked.disconnect()
        except TypeError:
            pass    
        self.media_player.play()
        print("Play:",self.play_button.inEnabled())
        print("Stop:",self.stop_button.inEnabled())
        # self.play_button.clicked.connect(lambda:on_play_clicked(self)) 
        # self.stop_button.clicked.connect(lambda:on_stop_clicked(self))
        # self.volume_slider.valueChanged.connect(
        #     lambda v: self.audio_output.setVolume(v / 100.0)
        # )
        # self.media_player.positionChanged.connect(
        #     lambda pos:on_position_changed(self,pos))
        # self.media_player.durationChanged.connect(
        #     lambda dur: on_duration_changed(self,dur))
    except Exception as e:
        self.text_view.setText("[Cannot prepare media]")
        self.preview_top.setCurrentWidget(self.text_view)
        actions.SetBottomView(self,False)
#------------------------------------------------------------------------


def on_play_clicked(self):
    if self.media_player.playbackState() == QMediaPlayer.PlayingState:
        self.media_player.pause()
        self.play_button.setText("Play")
    else:
        self.media_player.play()
        self.play_button.setText("Pause")
#------------------------------------------------------------------------
def on_stop_clicked(self):
    self.media_player.stop()
    self.play_button.setText("Play")

def on_position_changed(self, pos =5000):
    if self.media_player.duration() > 0:
        # val = int(pos * 1000 / self.media_player.duration())
        self.seek_slider.setRange(0,self.media_player.duration())
        self.seek_slider.blockSignals(True)
        self.seek_slider.setValue(pos)
        self.seek_slider.blockSignals(False)

def on_duration_changed(self, dur=100):
    # duration known - can be used to update UI (optional)
    if dur <= 0:
        self.seek_slider.setEnabled(False)
        return

    self.seek_slider.setEnabled(True)
    self.seek_slider.setRange(0, dur)

def on_seek_slider_moved(self, value):
    if self.media_player.duration() > 0:
        position = int(self.media_player.duration() * (value / 1000.0))
        self.media_player.setPosition(position)

def on_volume_changed(self, value):
    self.audio_output.setVolume(max(0.0, min(1.0, value / 100.0)))


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