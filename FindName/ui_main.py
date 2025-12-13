# ui_main.py
import os
import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget

# Your project modules (must exist)
from actions import *
from languages import *
import txt_view
import media_view

# ---------------------------
# Lightweight helper: InitInfo
# ---------------------------
class InitInfo:
    def __init__(self):
        # Keep simple: only collect values you need right away
        self.REG_KEY = REG_KEY
        self.OS, self.LANG = PC_Info(self)
# ---------------------------
# Valid Confirmation
# ---------------------------
class CheckForm(QWidget):
    def __init__(self):
        super().__init__()
        self.REG_KEY = InitInfo().REG_KEY
        self.OS = InitInfo().OS
        self.LANG = InitInfo().LANG
        self.setWindowTitle(LICENSE[self.LANG]["Title"])
        self.setGeometry(100, 100, 300, 150)
        self.setup_ui()
        move_to_center(self)
    def setup_ui(self):
        layout = QVBoxLayout()
        self.label = QLabel(LICENSE[self.LANG]["Prompt"])
        layout.addWidget(self.label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.show_hide_checkbox = QCheckBox(LICENSE[self.LANG]["Display"])
        layout.addWidget(self.show_hide_checkbox)
        
        self.check_button = QPushButton(LICENSE[self.LANG]["Button"])
        layout.addWidget(self.check_button)

        self.setLayout(layout)
        # Connect the button to the check_license function
        self.check_button.clicked.connect(lambda pw:check_license(self,self.password_input.text().strip().lower()))
        self.password_input.returnPressed.connect(lambda pw:check_license(self,self.password_input.text().strip().lower()))
        self.show_hide_checkbox.stateChanged.connect(lambda state:toggle_password_visibility(self,self.show_hide_checkbox.checkState()))
# ---------------------------
# Ensure Error of main path
# ---------------------------
def resource_path(self,relative_path):
        """Get absolute path to resource (works for dev and PyInstaller)."""
        if hasattr(sys, "_MEIPASS"):
            # When running as a bundled EXE
            base_path = sys._MEIPASS
        else:
            # When running as a normal Python script
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, relative_path)

# ---------------------------
# UI-only class (no signals)
# ---------------------------
class FileSearch(QWidget):
    """
    UI-only: create widgets, layouts and preview areas.
    Do NOT connect signals or implement logic here.
    FileSearchHandler will subclass this and attach behavior.
    """
    def __init__(self):
        super().__init__()
        self.default_values()
        self._build_ui()
        # Prepare containers for values that handler will set later
        # self.language = None
        # self.search_path = None
        # self.search_type = None

        # Call methods to build UI
        # self._default_values_placeholder()
    def default_values(self):
        self.REG_KEY = InitInfo().REG_KEY
        self.OS = InitInfo().OS
        self.LOCALE = InitInfo().LANG
        self.language,self.search_path = get_registry_values(self)
        self.APP_NAME = TITLE[self.language]
        self.lang = LANGUAGES
        self.options = OPTIONS
        self.place_holder =PLACE_HOLDER
        self.hint_dialog = HINT["Dialog"]
        self.hint_search = HINT["Search"]
        self.hint_logic = HINT["Logic"]
        self.hint_type = HINT["Type"]
        self.hint_folder = HINT["Folder"]
        self.hint_file = HINT["File"]
        self.label = LABELS
        self.type = TYPES
        self.ext_type = EXTENSIONS
        self.logics = LOGICS
        self.readable_text_ext = TEXT_EXT
        self.readable_cad_ext =CAD_EXT
        self.init =True
    # def _default_values_placeholder(self):
        """
        Minimal placeholders — FileSearchHandler will override with real values.
        This prevents attribute errors if handler later accesses them.
        """
        # self.APP_NAME = "App"
        # self.audio_exts = {".mp3", ".wav", ".ogg", ".m4a", ".flac"}
        # self.video_exts = {".mp4", ".avi", ".mkv", ".mov", ".wmv"}
        # self.readable_text_ext = {".txt", ".md", ".py", ".json"}
        # self.readable_cad_ext = set()

    def _build_ui(self):
        # Hold basic Info
        # Basic window
        self.setWindowTitle(self.APP_NAME)
        self.setGeometry(100, 100, 1000, 600)
        self.icon = resource_path(self,"favicon.ico")
        # ---------- LEFT PANEL (file controls) ----------
        layoutL = QVBoxLayout()

        # Language radios (actual labels will be set by handler)
        lang_layout = QHBoxLayout()
        self.language_radio = QButtonGroup()
        self.english_radio = QRadioButton("English")
        self.japanese_radio = QRadioButton("Japanese")
        self.vietnamese_radio = QRadioButton("Vietnamese")
        self.language_radio.addButton(self.japanese_radio, 0)
        self.language_radio.addButton(self.english_radio, 1)
        self.language_radio.addButton(self.vietnamese_radio, 2)
        lang_layout.addWidget(self.japanese_radio)
        lang_layout.addWidget(self.english_radio)
        lang_layout.addWidget(self.vietnamese_radio)
        layoutL.addLayout(lang_layout)

        # Search folder row
        search_folder_layout = QHBoxLayout()
        self.search_folder_label = QLabel("Search Path")
        self.search_folder_path = QLabel("")
        self.search_folder_change = QPushButton("...")
        self.search_folder_change.setFixedSize(50, 30)
        search_folder_layout.addWidget(self.search_folder_label)
        search_folder_layout.addWidget(self.search_folder_path)
        search_folder_layout.addWidget(self.search_folder_change)
        layoutL.addLayout(search_folder_layout)

        # Keyword row
        keyword_layout = QHBoxLayout()
        self.search_label = QLabel("Keyword")
        self.search_input = QLineEdit()
        self.search_button = QPushButton("Search")
        keyword_layout.addWidget(self.search_label)
        keyword_layout.addWidget(self.search_input)
        keyword_layout.addWidget(self.search_button)
        layoutL.addLayout(keyword_layout)

        # Search logic radios
        search_logic_layout = QHBoxLayout()
        self.search_radio = QButtonGroup()
        self.or_radio = QRadioButton("OR")
        self.and_radio = QRadioButton("AND")
        self.not_radio = QRadioButton("NOT")
        self.search_radio.addButton(self.or_radio, 0)
        self.search_radio.addButton(self.and_radio, 1)
        self.search_radio.addButton(self.not_radio, 2)
        search_logic_layout.addWidget(self.or_radio)
        search_logic_layout.addWidget(self.and_radio)
        search_logic_layout.addWidget(self.not_radio)
        layoutL.addLayout(search_logic_layout)

        # File type combo
        file_type_layout = QHBoxLayout()
        self.file_type_label = QLabel("File Type")
        self.file_type_combo = QComboBox()
        file_type_layout.addWidget(self.file_type_label)
        file_type_layout.addWidget(self.file_type_combo)
        layoutL.addLayout(file_type_layout)

        # Folders and files list widgets
        list_layout = QHBoxLayout()
        # Folders
        folder_layout = QVBoxLayout()
        self.folder_label = QLabel("Folders")
        self.folder_list = QListWidget()
        folder_layout.addWidget(self.folder_label)
        folder_layout.addWidget(self.folder_list)
        list_layout.addLayout(folder_layout)
        # Files
        file_layout = QVBoxLayout()
        self.file_label = QLabel("Files")
        self.file_list = QListWidget()
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_list)
        list_layout.addLayout(file_layout)
        layoutL.addLayout(list_layout)

        # Info & Cancel
        info_layout = QHBoxLayout()
        self.info_label = QLabel("Info")
        self.info = QLabel()
        info_layout.addWidget(self.info_label)
        info_layout.addWidget(self.info)
        layoutL.addLayout(info_layout)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setMaximumWidth(80)
        layoutL.addWidget(self.cancel_button, alignment=Qt.AlignCenter)

        # ---------- RIGHT PANEL: PREVIEW TOP + BOTTOM ----------
        # Top preview: QStackedWidget (image, text, CAD placeholder)
        self.preview_top = QStackedWidget()
        # Index 0: image view
        self.image_view = QLabel("No preview")
        self.image_view.setAlignment(Qt.AlignCenter)
        self.image_view.setWordWrap(True)
        self.image_view.setStyleSheet("border: 1px solid lightgray;")
        self.preview_top.addWidget(self.image_view)
        # Index 1: text view
        self.text_view = QTextEdit()
        self.text_view.setReadOnly(True)
        self.preview_top.addWidget(self.text_view)
        # Index 2: CAD / placeholder
        self.cad_view = QLabel("CAD preview not implemented")
        self.cad_view.setAlignment(Qt.AlignCenter)
        self.cad_view.setStyleSheet("border: 1px dashed gray;")
        self.preview_top.addWidget(self.cad_view)

        # Bottom preview: media controls (created, but hidden by handler until used)
        self.preview_bottom = QWidget()
        self.preview_bottom.setMinimumHeight(120)
        self.preview_bottom.setStyleSheet("border: 1px solid lightgray; background: #fafafa;")
        pb_layout = QHBoxLayout()
        pb_layout.setContentsMargins(6, 6, 6, 6)

        # Video widget and simple controls (handler will hook behavior)
        self.video_widget = QVideoWidget()
        self.video_widget.setMinimumSize(200, 100)
        self.media_player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.media_player.setAudioOutput(self.audio_output)

        # Control placeholders - handler wires actual signals
        controls_layout = QVBoxLayout()
        controls_row = QHBoxLayout()
        self.play_button = QPushButton("Play")
        self.stop_button = QPushButton("Stop")
        self.seek_slider = QSlider(Qt.Horizontal)
        self.seek_slider.setRange(0, 1000)
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        controls_row.addWidget(self.play_button)
        controls_row.addWidget(self.stop_button)
        controls_row.addWidget(QLabel("Seek"))
        controls_row.addWidget(self.seek_slider)
        controls_row.addWidget(QLabel("Vol"))
        controls_row.addWidget(self.volume_slider)
        controls_layout.addLayout(controls_row)
        controls_layout.addStretch()

        pb_layout.addWidget(self.video_widget, stretch=3)
        pb_layout.addLayout(controls_layout, stretch=5)
        self.preview_bottom.setLayout(pb_layout)
        # Do not connect media output here — handler will call:
        # self.media_player.setVideoOutput(self.video_widget)

        # Vertical splitter (top and bottom)
        right_splitter = QSplitter(Qt.Vertical)
        right_splitter.addWidget(self.preview_top)
        right_splitter.addWidget(self.preview_bottom)
        right_splitter.setSizes([400, 120])

        # Left-right splitter assembly
        splitter = QSplitter(Qt.Horizontal)
        left_panel = QWidget()
        left_panel.setLayout(layoutL)
        right_panel = QWidget()
        right_panel_layout = QVBoxLayout()
        right_panel_layout.addWidget(right_splitter)
        right_panel.setLayout(right_panel_layout)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([400, 600])

        main_layout = QVBoxLayout()
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

        # Hide bottom area initially
        self.preview_bottom.setVisible(False)

    # Small utility helpers (handler can use)
    def _set_file_item(self, filename, fullpath):
        item = QListWidgetItem(filename)
        item.setData(Qt.UserRole, fullpath)
        return item

    def _add_file_list_items(self, list_widget, files, base_path=None):
        list_widget.clear()
        for f in files:
            full = f if (base_path is None or os.path.isabs(f)) else os.path.join(base_path, f)
            item = self._set_file_item(os.path.basename(f), os.path.abspath(full))
            list_widget.addItem(item)
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            QApplication.quit()
        super().keyPressEvent(event)
    #----------------------------------------------------------------
# ---------------------------
# Logic-heavy subclass
# ---------------------------
class FileSearchHandler(FileSearch):
    """
    Full application handler: sets defaults, hooks signals, and implements behavior.
    Instantiate this class as your main window when app is licensed.
    """
    def __init__(self):
        # Build UI first (from parent)
        super().__init__()
        self._restore_defaults()
        
        # Ensure correct radios are checked
        self.file_type_combo.setCurrentIndex(self.type_index if hasattr(self, "type_index") else 0)
        self.logic_index = self.logics.get("OR", 0) if isinstance(self.logics, dict) else 0
        try:
            btn = self.search_radio.button(self.logic_index)
            if btn:
                btn.setChecked(True)
        except Exception:
            pass
        # Set initial UI values (safe)
        self.search_folder_path.setText(self.search_path or "")
        self.search_type = self.ext_type[self.type_index]
        # Apply initial state: reset data, change logic/tooltips (these are project-specific)
        try:
            reset_data(self)
        except Exception as e:
            print("Warning: reset_data() failed:", e)
        
        try:
            change_logic(self)
        except Exception as e:
            print("Warning: change_logic() failed:", e)
        
        try:
            change_tooltips(self)
        except Exception as e:
            print("Warning: change_tooltips() failed:", e)

        # Wire media output (connect video output to widget)
        try:
            self.media_player.setVideoOutput(self.video_widget)
        except Exception:
            pass
        # Hook media player signals
        self.media_player.positionChanged.connect(self._on_position_changed)
        self.media_player.durationChanged.connect(self._on_duration_changed)

        # Wire all signals here (exactly once)
        self._connect_signals()
    # -- default/state restoration -------------------
    def _restore_defaults(self):
        """
        Load values from registry / languages / actions as you had before.
        This function intentionally mirrors the previous behavior you relied on.
        """
        # Registry, OS, language (InitInfo)
        try:
            info = InitInfo()
            self.REG_KEY = info.REG_KEY
            self.OS = info.OS
            self.LOCALE = info.LANG
            # language and search_path are provided by get_registry_values (your actions.py)
            self.language, self.search_path = get_registry_values(self)
        except Exception:
            # Fallbacks if the above calls fail
            self.language = getattr(self, "language", "English")
            self.search_path = getattr(self, "search_path", os.path.expanduser("~"))
        #Set default for Language Radio Button
        if self.language == 'English':
            self.english_radio.setChecked(True)
        elif self.language == 'Japanese':
            self.japanese_radio.setChecked(True)
        else:
            self.vietnamese_radio.setChecked(True)
        # Create file type combo list 
        self.type_index = 0
        try:
            self.file_type_combo.clear()
            for _ in range(len(self.type)):
                self.file_type_combo.addItem(self.type[_][self.language])
            self.file_type_combo.setCurrentIndex(self.type_index)
        except Exception:
            pass    
        
        # Fill UI label texts (safe guard)
        try:
            # Languages labels
            self.english_radio.setText(self.lang[self.language]["ENG"])
            self.japanese_radio.setText(self.lang[self.language]["JP"])
            self.vietnamese_radio.setText(self.lang[self.language]["VN"])
            # Search labels
            self.search_folder_label.setText(self.label[self.language]["SearchPath"])
            self.search_label.setText(self.label[self.language]["SearchKeyword"])
            self.search_button.setText(self.label[self.language]["SearchButton"])
            self.file_type_label.setText(self.label[self.language]["FileType"])
            self.folder_label.setText(self.label[self.language]["Folders"])
            self.file_label.setText(self.label[self.language]["Files"])
            self.info_label.setText(self.label[self.language]["Info"])
            self.cancel_button.setText(self.label[self.language]["Cancel"])
            # placeholder
            self.search_input.setPlaceholderText(self.place_holder[self.language])
        except Exception:
            pass     

        # Ensure ext sets exist
        # try:
        #     self.audio_exts = {".mp3", ".wav", ".ogg", ".m4a", ".flac"}
        #     self.video_exts = {".mp4", ".avi", ".mkv", ".mov", ".wmv"}
        # except Exception:
        #     pass

    # -- connect all event handlers here ----------------
    def _connect_signals(self):
        # Language selection
        self.language_radio.buttonClicked.connect(lambda: change_language(self))

        # Folder chooser
        self.search_folder_change.clicked.connect(lambda: open_file_dialog(self))

        # Search actions
        self.search_input.returnPressed.connect(lambda: change_search_source(self, source=1))
        self.search_button.clicked.connect(lambda: change_search_source(self, source=1))

        # File type selection
        self.file_type_combo.currentIndexChanged.connect(lambda: change_type(self))

        # Search logic radios
        self.search_radio.buttonClicked.connect(lambda: change_logic(self))

        # Folder double-click triggers search into folder
        self.folder_list.itemDoubleClicked.connect(lambda: change_search_source(self, source=2))

        # File list selection & double-click
        # Route selection through our handler that decides which preview to show
        # self.file_list.currentItemChanged.connect(lambda current:show_file_info(self,current))
        # self.file_list.currentItemChanged.connect(lambda current:on_file_selected(self,current))
        self.file_list.currentItemChanged.connect(lambda current :on_file_selected(self,current))
        self.file_list.itemDoubleClicked.connect(lambda item: open_file_location(self, item))

        # Cancel / quit
        self.cancel_button.clicked.connect(QApplication.quit)

        # Note: do NOT call reset_data/change_logic here (already called in __init__ after wiring)
    #--------------------------------------------------------
    def closeEvent(self, event):
        # Save to Windows Registry before closing
        try:
            saved_to_registry(self)
        except Exception as e:
            print(f"Registry write failed: {e}")

        super().closeEvent(event)  # Call the default close event handler event.accept()  # Allow the window to close

    # -- preview & search routing -----------------------
    def _on_file_selected(self, current, previous=None):
        """Routing: decide how to preview a selected file and whether to show media controls."""
        try:
            if current is None:
                return

            # get absolute path from item data if present
            filepath = current.data(Qt.UserRole) or current.text()
            if not filepath:
                filepath = current.text()

            # try to resolve relative path against search_path
            if not os.path.isabs(filepath) and getattr(self, "search_path", None):
                candidate = os.path.join(self.search_path, filepath)
                if os.path.exists(candidate):
                    filepath = candidate

            if not os.path.exists(filepath):
                self.text_view.setText("[File not found]")
                self.preview_top.setCurrentWidget(self.text_view)
                self.preview_bottom.setVisible(False)
                return

            _, ext = os.path.splitext(filepath)
            ext = ext.lower()

            # Media: audio/video -> thumbnail top + enable bottom controls
            if ext in getattr(self, "audio_exts", set()) or ext in getattr(self, "video_exts", set()):
                media_view.show_media_thumbnail(self, filepath)
                media_view.prepare_media_player(self, filepath)
                # media_view.prepare_media_player will show preview_bottom
                return

            # Text/document/images handled by txt_view functions
            if ext in getattr(self, "readable_text_ext", set()) or ext in (".txt", ".md", ".py", ".log", ".json"):
                txt_view.preview_text_file(self, filepath)
                self.preview_bottom.setVisible(False)
                return

            # images (use QImageReader supported formats)
            try:
                from PySide6.QtGui import QImageReader
                supported_exts = {("." + bytes(fmt).decode()).lower() for fmt in QImageReader.supportedImageFormats()}
            except Exception:
                supported_exts = {".png", ".jpg", ".jpeg", ".bmp", ".gif"}

            if ext in supported_exts:
                txt_view.preview_image_file(self, filepath)
                self.preview_bottom.setVisible(False)
                return

            # docx / xlsx
            if ext == ".docx" or ext == ".xlsx":
                txt_view.preview_document_file(self, filepath)
                self.preview_bottom.setVisible(False)
                return

            # CAD placeholder
            if ext in getattr(self, "readable_cad_ext", set()):
                self.cad_view.setText(f"CAD preview not available for {os.path.basename(filepath)}")
                self.preview_top.setCurrentWidget(self.cad_view)
                self.preview_bottom.setVisible(False)
                return

            # fallback
            self.text_view.setText("[Unsupported file type]")
            self.preview_top.setCurrentWidget(self.text_view)
            self.preview_bottom.setVisible(False)

        except Exception as e:
            print("Preview routing error:", e)
            self.text_view.setText("[Preview error]")
            self.preview_top.setCurrentWidget(self.text_view)
            self.preview_bottom.setVisible(False)

    # -- media player helpers ----------------------------
    def _on_play_clicked(self):
        if self.media_player.playbackState() == QMediaPlayer.PlayingState:
            self.media_player.pause()
            self.play_button.setText("Play")
        else:
            self.media_player.play()
            self.play_button.setText("Pause")

    def _on_stop_clicked(self):
        self.media_player.stop()
        self.play_button.setText("Play")

    def _on_position_changed(self, pos):
        if self.media_player.duration() > 0:
            val = int(pos * 1000 / self.media_player.duration())
            self.seek_slider.blockSignals(True)
            self.seek_slider.setValue(val)
            self.seek_slider.blockSignals(False)

    def _on_duration_changed(self, dur):
        # duration known - can be used to update UI (optional)
        pass

    def _on_seek_slider_moved(self, value):
        if self.media_player.duration() > 0:
            position = int(self.media_player.duration() * (value / 1000.0))
            self.media_player.setPosition(position)

    def _on_volume_changed(self, value):
        self.audio_output.setVolume(max(0.0, min(1.0, value / 100.0)))

    # override to ensure proper cleanup
    def closeEvent(self, event):
        try:
            saved_to_registry(self)
        except Exception as e:
            print(f"Registry write failed: {e}")
        super().closeEvent(event)

# End of ui_main.py
