import sys,math
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton,
    QSlider, QVBoxLayout, QHBoxLayout,QLabel
)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QUrl,Qt


class MediaPlayerUI(QWidget):
    def __init__(self, media_path):
        super().__init__()
        self._create_widgets(media_path)
        self._setup_layout()
        self._connect_signals()
    #----------------------------------------------------------------------
    def _create_widgets(self,media_path):
        self.setWindowTitle("Media Player Test")
        self.resize(800, 500)
        # ===== Media objects =====
        self.player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.player.setAudioOutput(self.audio_output)

        self.video_widget = QVideoWidget(self)
        self.player.setVideoOutput(self.video_widget)
        self.player.setSource(QUrl.fromLocalFile(media_path))
        
        # ===== Volume objects =====
        self.volume_label = QLabel("Volume:")
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(10)     # default = 10%
        self.audio_output.setVolume(0.10)   # Qt expects 0.0 → 1.0
        
        self.mute_button = QPushButton("Mute")

        # ===== Elapsed Time objects =====
        self.time_slider =QSlider(Qt.Horizontal)
        self.timer = QLabel("00:00 / 00:00")
        self.timer.setMinimumWidth(100)
    
        
        # ===== Buttons =====
        self.play_button = QPushButton("Play")
        self.stop_button = QPushButton("Stop")
        #====================================================

        # ===== Initial state =====
        self.mute_button.setCheckable(True)
        self.time_slider.setEnabled(False)
        self.player.pause()   # start paused


    #----------------------------------------------------------------------
    def _setup_layout(self):
        #Volume Layout
        volume_layout = QHBoxLayout()
        volume_layout.addWidget(self.volume_label)
        volume_layout.addWidget(self.volume_slider)
        volume_layout.addWidget(self.mute_button)
        #Slider Layout
        slider_layout = QHBoxLayout()
        slider_layout.addWidget(self.timer)
        slider_layout.addWidget(self.time_slider)
        # ===== Buttons =====
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.stop_button)
        # ===== Main Layout =====
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.video_widget)
        main_layout.addLayout(slider_layout)
        main_layout.addLayout(volume_layout)
        main_layout.addLayout(button_layout)
    #----------------------------------------------------------------------
    def _connect_signals(self):
        #Volume Slider
        self.volume_slider.valueChanged.connect(self.on_volume_changed)
        self.mute_button.clicked.connect(self.toggle_mute)
        #Elapsed time Slider
        self.time_slider.sliderPressed.connect(self.on_slider_pressed)
        self.time_slider.sliderReleased.connect(self.on_slider_released)
        self.time_slider.sliderMoved.connect(self.player.setPosition)
        #Player
        self.player.durationChanged.connect(self.on_duration_changed)
        self.player.positionChanged.connect(self.time_slider.setValue)
        self.player.positionChanged.connect(self.update_time_label)
        self.player.durationChanged.connect(self.on_duration_changed)
        #Buttons
        self.play_button.clicked.connect(self.toggle_play)
        self.stop_button.clicked.connect(self.stop_media)
    # ==============================
    # Slots
    # ==============================
    
    #-------------Play ON/OFF--------------------------------------
    def toggle_play(self):
        if self.player.playbackState() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.play_button.setText("Play")  
        else:
            self.player.play()
            self.play_button.setText("Pause")
        self.time_slider.setEnabled(True)    
    #----------------------------------------
    def stop_media(self):
        self.player.stop()
        self.play_button.setText("Play")
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
        self.time_slider.setRange(0, duration)
        self.time_slider.setEnabled(True)
    #----------------------------------------
    def format_time(self, ms):
        s = ms // 1000
        return f"{s//60:02d}:{s%60:02d}"
    #----------------------------------------
    def update_time_label(self, position):
        cur = self.format_time(position)
        total = self.format_time(self.player.duration())
        self.timer.setText(f"{cur} / {total}")  
        
    #-------------Sound Control ----------------------------------
    def on_volume_changed(self, value):
        if value == 0:
            volume = 0.0
        else:
            volume = math.pow(value / 100.0, 2.0)
        self.audio_output.setVolume(volume)
    #----------------------------------------    
    def toggle_mute(self, checked):
        self.audio_output.setMuted(checked)
        self.mute_button.setText("undue" if checked else "Mute")
    
#============================================================          
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # CHANGE THIS PATH TO YOUR MEDIA FILE
    media_file = r"C:\\MyData\\Test Sample\\Nam 2002.mp4"   # .mp3 or .avi also works
    # media_file = r"C:\\MyData\\Test Sample\\006.mp3"
    window = MediaPlayerUI(media_file)
    window.show()

    sys.exit(app.exec())
