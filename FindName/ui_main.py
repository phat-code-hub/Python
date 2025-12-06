# ui_main.py

import os,sys
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt,QTimer
from PySide6.QtGui import QIcon
from actions import *
from languages import *
class CheckForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Check")
        self.setGeometry(100, 100, 300, 150)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.label = QLabel("Enter your password:")
        layout.addWidget(self.label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.show_hide_checkbox = QCheckBox("Show/Hide")
        
        layout.addWidget(self.show_hide_checkbox)
        
        self.check_button = QPushButton("Check Password")
        layout.addWidget(self.check_button)

        self.setLayout(layout)
        # Connect the button to the check_password function
        self.check_button.clicked.connect(lambda pw:check_password(self,self.password_input.text().strip().lower()))
        self.password_input.returnPressed.connect(lambda pw:check_password(self,self.password_input.text().strip().lower()))
        self.show_hide_checkbox.stateChanged.connect(lambda state:toggle_password_visibility(self,self.show_hide_checkbox.checkState()))

#------------------------------------------------------------------------------------------------
class FileSearch(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    #---------------------------------------------------------------------------
    def init_values(self):
        import platform
        if platform.system() == "Windows":
            self.OS ="WIN"
        elif platform.system() == "Darwin":
            self.OS = "MAC"
        elif platform.system() == "Linux":
            self.OS = "LINUX"
        self.REG_KEY  = "FileSearch"
        if self.OS =="WIN":
            import winreg
            try:
                reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, f"Software\\{self.REG_KEY}")
                language,default_path= winreg.QueryValueEx(reg_key, "Language"), winreg.QueryValueEx(reg_key, "SearchPath")
                winreg.CloseKey(reg_key)
                return language[0],default_path[0]
            except FileNotFoundError:
                return  "English",os.path.expanduser("~")
        elif self.OS == "MAC":
            # elif sys.platform == "darwin":
            # macOS: use NSUserDefaults
            # from Foundation import NSUserDefaults
            # self.defaults = NSUserDefaults.alloc().initWithSuiteName_(f"com.mycompany.{self.REG_KEY}")
            # self.defaults = NSUserDefaults.alloc().initWithSuiteName_(f"com.mycompany.FileSearchApp")
            # language = self.defaults.stringForKey_("Language")
            # default_path = self.defaults.stringForKey_("SearchPath")
            # language = "English"
            # default_path = "~"
            # return language, default_path
            return "English",os.path.expanduser("~")
        else:
            return "English",os.path.expanduser("~") 
    #-----------------------------------------------------------------------
    def default_values(self):
        # import platform
        self.language,self.search_path = self.init_values()
        self.limit_timer  = 200
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
#-----------------------------------------------------
    def initUI(self):
        self.default_values()
        self.setWindowTitle(self.APP_NAME)
        self.icon = self.resource_path("favicon.ico")
        self.setWindowIcon(QIcon(self.icon))
        self.setGeometry(100, 100, 500, 300)
        self.timer =QTimer()
        
        layoutL = QVBoxLayout()
        layoutR = QVBoxLayout()
        
        #Languages choice
        lang_layout = QHBoxLayout()
        self.language_radio = QButtonGroup()
        self.english_radio = QRadioButton(self.lang[self.language]["ENG"])
        self.japanese_radio = QRadioButton(self.lang[self.language]["JP"])
        self.vietnamese_radio = QRadioButton(self.lang[self.language]["VN"])
        self.language_radio.addButton(self.japanese_radio,0)
        self.language_radio.addButton(self.english_radio,1)
        self.language_radio.addButton(self.vietnamese_radio,2)
        lang_layout.addWidget(self.japanese_radio)
        lang_layout.addWidget(self.english_radio)
        lang_layout.addWidget(self.vietnamese_radio)
        
        layoutL.addLayout(lang_layout)
        
        self.japanese_radio.setChecked(True)
        #Folder Search path
        search_folder_layout = QHBoxLayout()
        self.search_folder_label = QLabel(self.label[self.language]["SearchPath"])
        self.search_folder_path = QLabel()
        self.search_folder_path.setText(self.search_path)
        # self.search_folder_path.setStyleSheet("color: dark_blue; font-style: italic;text-align: left;")
        self.search_folder_change = QPushButton("...")
        self.search_folder_change.setFixedSize(50,30)  # Set the size of the button
        self.search_folder_change.setStyleSheet("background-color: lightpink;")  # Set the background color
        search_folder_layout.addWidget(self.search_folder_label)
        search_folder_layout.addWidget(self.search_folder_path)
        search_folder_layout.addWidget(self.search_folder_change)
        
        layoutL.addLayout(search_folder_layout)
        # keyword input
        keyword_layout = QHBoxLayout()
        self.search_label = QLabel(self.label[self.language]["SearchKeyword"])
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(self.place_holder[self.language])
        self.search_button = QPushButton(self.label[self.language]["SearchButton"])
        
        keyword_layout.addWidget(self.search_label)
        keyword_layout.addWidget(self.search_input)
        keyword_layout.addWidget(self.search_button)
        
        layoutL.addLayout(keyword_layout)
        
        search_layout = QHBoxLayout()
        self.search_radio = QButtonGroup()
        self.or_radio = QRadioButton(self.options[self.language]["OR"])
        self.and_radio = QRadioButton(self.options[self.language]["AND"])
        self.not_radio = QRadioButton(self.options[self.language]["NOT"])
        
        self.search_radio.addButton(self.or_radio,0)
        self.search_radio.addButton(self.and_radio,1)
        self.search_radio.addButton(self.not_radio,2)
        
        search_layout.addWidget(self.or_radio)
        search_layout.addWidget(self.and_radio)
        search_layout.addWidget(self.not_radio)
        
        layoutL.addLayout(search_layout)
        
        self.or_radio.setChecked(True)
        # Create the combo box for file types
        file_type_layout = QHBoxLayout()
        self.file_type_label = QLabel(self.label[self.language]["FileType"])
        self.file_type_combo = QComboBox()
        file_type_layout.addWidget(self.file_type_label)
        file_type_layout.addWidget(self.file_type_combo)
        # Add file types to the combo box
        for _ in range(len(self.type)):
            self.file_type_combo.addItem(self.type[_][self.language])
        self.file_type_combo.setCurrentIndex(0) # Set default selection to 'All'
        
        layoutL.addLayout(file_type_layout)
        
        # Create the listbox for folders and files
        list_layout = QHBoxLayout()
        folder_layout = QVBoxLayout()
        self.folder_label = QLabel(self.label[self.language]["Folders"])
        self.folder_list = QListWidget()
        folder_layout.addWidget(self.folder_label)
        folder_layout.addWidget(self.folder_list)
        list_layout.addLayout(folder_layout)
        
        file_layout = QVBoxLayout()
        self.file_label = QLabel(self.label[self.language]["Files"])
        self.file_list = QListWidget()
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_list)
        list_layout.addLayout(file_layout) 
        
        layoutL.addLayout(list_layout)
        
        info_layout = QHBoxLayout()
        self.info_label = QLabel(self.label[self.language]["Info"])
        self.info = QLabel()
        # self.info.setStyleSheet("color: red; font-style: italic;text-align: left;")
        info_layout.addWidget(self.info_label)
        info_layout.addWidget(self.info)
        
        layoutL.addLayout(info_layout)
        
        self.cancel_button = QPushButton(self.label[self.language]["Cancel"])
        self.cancel_button.setMaximumWidth(80)  # Won't grow beyond 80px
        layoutL.addWidget(self.cancel_button,alignment=Qt.AlignCenter)
        
        self.preview  = QLabel("Preview Area")
        self.preview.setStyleSheet("border: 1px solid gray;")
        self.preview.setMinimumHeight(250)
        self.preview.setWordWrap(True)
        self.preview.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Set size policy to expand in both directions
        self.preview.setContentsMargins(0, 0, 0, 0)  # Remove margins to allow resizing
        self.preview.setAlignment(Qt.AlignCenter)
        
        layoutR.addWidget(self.preview)
        
        splitter = QSplitter(Qt.Horizontal)
        left_panel = QWidget()
        right_panel =QWidget()
        
        left_panel.setLayout(layoutL)
        right_panel.setLayout(layoutR)

        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([700, 300])
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)
    #---------------------------------------------------------------------------  
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            QApplication.quit()
    
    #---------------------------------------------------------------------------
    def resource_path(self,relative_path):
        """Get absolute path to resource (works for dev and PyInstaller)."""
        if hasattr(sys, "_MEIPASS"):
            # When running as a bundled EXE
            base_path = sys._MEIPASS
        else:
            # When running as a normal Python script
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, relative_path)
    #---------------------------------------------------------------------------
class FileSearchHandler(FileSearch):
    def __init__(self):
        super().__init__()
        # Set default values
        self.logic_index = self.logics["OR"] # 0 for OR, 1 for AND, 2 for NOT
        self.type_index =0 # For ALL file type
        if self.language == 'English':
            self.english_radio.setChecked(True)
        elif self.language == 'Japanese':
            self.japanese_radio.setChecked(True)
        else:
            self.vietnamese_radio.setChecked(True)  

        self.search_radio.button(self.logic_index).setChecked(True)
        self.file_type_combo.setCurrentIndex(self.type_index)        
        #initialize values
        self.search_folder_path.setText(self.search_path)
        self.search_type = self.ext_type[self.type_index]
        reset_data(self)
        self.connect_signals()
        change_logic(self)
        change_tooltips(self)
    #----------------------------------------------------------------
    def connect_signals(self):
        
        #Change language
        self.language_radio.buttonClicked.connect(lambda: change_language(self))
        # Change Search Folder
        self.search_folder_change.clicked.connect(lambda:open_file_dialog(self))
        # Search Folder and Files
        self.search_input.returnPressed.connect(lambda:change_search_source(self,source=1))
        self.search_button.clicked.connect(lambda:change_search_source(self,source=1))
        # Connect the combo box's currentIndexChanged signal to the search_files method
        self.file_type_combo.currentIndexChanged.connect(lambda:change_type(self))
        #Search logic
        self.search_radio.buttonClicked.connect(lambda:change_logic(self))
        #CLick self.Folder_list
        self.folder_list.itemDoubleClicked.connect(lambda : change_search_source(self,source=2))
        #Show file info
        self.file_list.currentItemChanged.connect(lambda current:show_file_info(self,current))
        self.file_list.itemDoubleClicked.connect(lambda item:open_file_location(self,item))
        #Quit Program
        self.cancel_button.clicked.connect(QApplication.quit)
    #----------------------------------------------------------------s
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            QApplication.quit()
        super().keyPressEvent(event)
    #----------------------------------------------------------------
    def closeEvent(self, event):
        # Save to Windows Registry before closing
        try:
            saved_to_registry(self)
        except Exception as e:
            print(f"Registry write failed: {e}")

        super().closeEvent(event)  # Call the default close event handler event.accept()  # Allow the window to close
#-----------------------------------------------------------------------