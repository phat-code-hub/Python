# ui_main.py
import os
import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtMultimedia import QMediaDevices

from actions import *
from languages import *

from view_media import *# on_play_clicked

# ---------------------------
# Lightweight  InitInfo
# ---------------------------
class InitInfo:
    def __init__(self):
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
# UI-only class 
# ---------------------------
class FileSearch(QWidget):
    def __init__(self):
        super().__init__()
        self.default_values()
        self._build_ui()
        self._build_layout()
    #-----------------------------------------   
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
        #---------------------------------
        # Classify previewable extensions
        #---------------------------------
        self.filetype = VIEW_EXT
        # self.readable_cad_ext =CAD_EXT
        self.init =True

    def _build_ui(self):
        # Hold basic Info
        self.setWindowTitle(self.APP_NAME)
        self.setGeometry(100, 100, 1000, 600)
        self.icon = resource_path(self,"favicon.ico")
        #================================================
        #      LEFT PANEL (file controls)
        #================================================
        self.layoutL = QVBoxLayout()
        #----------------------------------
        self.language_radio = QButtonGroup()
        self.english_radio = QRadioButton("English")
        self.japanese_radio = QRadioButton("Japanese")
        self.vietnamese_radio = QRadioButton("Vietnamese")
        self.language_radio.addButton(self.japanese_radio, 0)
        self.language_radio.addButton(self.english_radio, 1)
        self.language_radio.addButton(self.vietnamese_radio, 2)

        # Search folder row
        self.search_folder_label = QLabel("Search Path")
        self.search_folder_path = QLabel("")
        self.search_folder_change = QPushButton("...")
        self.search_folder_change.setFixedSize(50, 30)

        # Keyword row
        self.search_label = QLabel("Keyword")
        self.search_input = QLineEdit()
        self.search_button = QPushButton("Search")

        # Search logic radios
        self.search_radio = QButtonGroup()
        self.or_radio = QRadioButton("OR")
        self.and_radio = QRadioButton("AND")
        self.not_radio = QRadioButton("NOT")
        self.search_radio.addButton(self.or_radio, 0)
        self.search_radio.addButton(self.and_radio, 1)
        self.search_radio.addButton(self.not_radio, 2)

        # File type combo
        self.file_type_label = QLabel("File Type")
        self.file_type_combo = QComboBox()

        # Folders and files list widgets
        # Folders
        self.folder_label = QLabel("Folders")
        self.folder_list = QListWidget()
        # Files
        self.file_label = QLabel("Files")
        self.file_list = QListWidget()

        # Info & Cancel
        self.info_label = QLabel("Info")
        self.info = QLabel()
        self.cancel_button = QPushButton("Cancel")

        #================================================
        #      RIGHT PANEL (file Preview)
        #       (Divide 2 panels: top and bottom)
        #================================================
        
        #-----------------------------------------------
        #          Top Preview
        #-----------------------------------------------
        
        # Top preview: QStackedWidget (image, text, CAD placeholder)
        self.preview_top = QStackedWidget()
        # Index 0: image view
        self.image_view = QLabel("No preview")
        self.image_view.setAlignment(Qt.AlignCenter)
        self.image_view.setWordWrap(True)
        self.image_view.setStyleSheet("border: 1px solid lightgray;")
        # Index 1: text view
        self.text_view = QTextEdit()
        self.text_view.setReadOnly(True)
        # Index 2: CAD / placeholder
        self.cad_view = QLabel("CAD preview not implemented")
        self.cad_view.setAlignment(Qt.AlignCenter)
        self.cad_view.setStyleSheet("border: 1px dashed gray;")

        #-----------------------------------------------
        #          Bottom Preview
        #-----------------------------------------------

        self.preview_bottom = QWidget()
        self.preview_bottom.setMinimumHeight(120)
        # self.preview_bottom.setStyleSheet("border: 1px solid lightgray; background: #fafafa;")
        
        # Media Player
        self.player = QMediaPlayer()
        
        self.layoutR = QHBoxLayout()
        self.layoutR.setContentsMargins(6, 6, 6, 6)

        #Audio Component
        self.audio_output = QAudioOutput(self)
        self.audio_output.setDevice(QMediaDevices.defaultAudioOutput())
        self.audio_output.setVolume(0.1) # 10%
        #Info Audio default output device
        # print("Audio device:", QMediaDevices.defaultAudioOutput().description())
        
        # Video widget Component
        self.video_widget = QVideoWidget()
        self.video_widget.setMinimumSize(400, 200)
        self.play_button = QPushButton("Play")
        self.stop_button = QPushButton("Stop")
        self.seek = QLabel("Seek:")
        self.seek_slider = QSlider(Qt.Horizontal)
        self.volume =QLabel("Volume:")
        self.volume_slider = QSlider(Qt.Horizontal)
        
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.seek_slider.setRange(0, 100)
        
        # Video widget
        self.video_widget = QVideoWidget()
        self.video_widget.setMinimumSize(400, 200)

    #----------------------------------------------------------------
    def _build_layout(self):
        #======================================
        #          LEFT SIDE PANEL
        #======================================
        # self.layoutL = QVBoxLayout()
        # L1: Language radios (actual labels will be set by handler)
        lang_layout = QHBoxLayout()
        lang_layout.addWidget(self.japanese_radio)
        lang_layout.addWidget(self.english_radio)
        lang_layout.addWidget(self.vietnamese_radio)
        
        # L2: Search Row
        search_folder_layout = QHBoxLayout()
        search_folder_layout.addWidget(self.search_folder_label)
        search_folder_layout.addWidget(self.search_folder_path)
        search_folder_layout.addWidget(self.search_folder_change)
        # L3: Search Keyword Row
        keyword_layout = QHBoxLayout()
        keyword_layout.addWidget(self.search_label)
        keyword_layout.addWidget(self.search_input)
        keyword_layout.addWidget(self.search_button)
        # L4: Search Logic Row
        search_logic_layout = QHBoxLayout()
        search_logic_layout.addWidget(self.or_radio)
        search_logic_layout.addWidget(self.and_radio)
        search_logic_layout.addWidget(self.not_radio)
        # L5: File Type Row
        file_type_layout = QHBoxLayout()
        file_type_layout.addWidget(self.file_type_label)
        file_type_layout.addWidget(self.file_type_combo)
        
        #L6 List Layout include list and Folder list box layout
        folder_layout = QVBoxLayout()
        folder_layout.addWidget(self.folder_label)
        folder_layout.addWidget(self.folder_list)
        
        file_layout = QVBoxLayout()
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_list)
        #------------O-------------------
        list_layout = QHBoxLayout()
        list_layout.addLayout(folder_layout)
        list_layout.addLayout(file_layout)
        
        # L7 Selected file Information
        info_layout = QHBoxLayout()
        info_layout.addWidget(self.info_label)
        info_layout.addWidget(self.info)
        # L8: Cancel Button
        
        #-----------------------------------------
        # Add all left layout to self.layoutL
        #-----------------------------------------
        self.layoutL.addLayout(lang_layout)
        self.layoutL.addLayout(search_folder_layout)
        self.layoutL.addLayout(keyword_layout)
        self.layoutL.addLayout(search_logic_layout)
        self.layoutL.addLayout(file_type_layout)
        self.layoutL.addLayout(list_layout)
        self.layoutL.addLayout(info_layout)
        self.layoutL.addWidget(self.cancel_button, alignment=Qt.AlignCenter)
        # self.preview_top = QStackedWidget()

        #-----------------------------------------
        # Add all top layouts to self.preview_top
        #-----------------------------------------
        self.preview_top.addWidget(self.image_view)
        self.preview_top.addWidget(self.text_view)
        self.preview_top.addWidget(self.cad_view)
        #======================================
        #          RIGHT SIDE PANEL
        #======================================
        #-----------------------------------------
        # Add all right layout to self.layoutR
        #-----------------------------------------
        controls_layout = QVBoxLayout()
        controls_row1 = QHBoxLayout()
        controls_row2 = QHBoxLayout()
        controls_row3 = QHBoxLayout()
        
        controls_row1.addWidget(self.play_button)
        controls_row1.addWidget(self.stop_button)
        
        controls_row2.addWidget(self.seek)
        controls_row2.addWidget(self.seek_slider)
        
        controls_row3.addWidget(self.volume)
        controls_row3.addWidget(self.volume_slider)
        
        controls_layout.addLayout(controls_row1)
        controls_layout.addLayout(controls_row2)
        controls_layout.addLayout(controls_row3)
        
        controls_layout.addStretch()
        
        self.layoutR = QVBoxLayout()
        
        self.layoutR.addWidget(self.video_widget, stretch=3)
        self.layoutR.addLayout(controls_layout, stretch=5)
        
        #-----------------------------------------
        # Add all bottom layouts to self.preview_bottom
        #-----------------------------------------
        self.preview_bottom.setLayout(self.layoutR)
        
        self.player.setAudioOutput(self.audio_output)
        try:
            self.player.setVideoOutput(self.video_widget)
        except:
            pass

        # Create Left and Right panels
        left_panel = QWidget()
        left_panel.setLayout(self.layoutL)
        
        right_splitter = QSplitter(Qt.Vertical)
        right_splitter.addWidget(self.preview_top)
        right_splitter.addWidget(self.preview_bottom)
        right_splitter.setSizes([400, 120])

        right_panel = QWidget()
        right_panel_layout = QVBoxLayout()
        right_panel_layout.addWidget(right_splitter)
        right_panel.setLayout(right_panel_layout)
        # Create splitter and add panels
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([400, 600])
        # Add splitter to main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)
        #-----------------------------------------
        #Interaction
        # self.mute_button.setCheckable(True)
        self.seek_slider.setEnabled(False)
        self.player.pause()   
    #------------------------------------------------
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
            # get language and search_path
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
        self.file_list.currentItemChanged.connect(lambda current:show_file_info(self,current))
        self.file_list.itemDoubleClicked.connect(lambda item: open_file_location(self, item))
    
        #Volume Slider
        self.volume_slider.valueChanged.connect(lambda value:   on_volume_changed(self,value))
        # self.mute_button.clicked.connect(self.toggle_mute)
        #Player
        self.player.durationChanged.connect(lambda :on_duration_changed(self,50))
        self.player.positionChanged.connect(self.seek_slider.setValue)
        # self.player.positionChanged.connect(update_time_label)
        self.player.durationChanged.connect(lambda :on_duration_changed(self,50))
        #Buttons
        self.play_button.clicked.connect(lambda :on_play(self))
        self.stop_button.clicked.connect(lambda : on_stop(self))
        
    # Cancel / quit
        self.cancel_button.clicked.connect(QApplication.quit)

    #--------------------------------------------------------
    # override to ensure proper cleanup
    def closeEvent(self, event):
        # Save to Windows Registry before closing
        try:
            saved_to_registry(self)
        except Exception as e:
            print(f"Registry write failed: {e}")

        super().closeEvent(event)  # Call the default close event handler event.accept()  # Allow the window to close

# End of ui_main.py