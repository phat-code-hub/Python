from PySide6 import QtWidgets
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt,QUrl
from PySide6.QtGui import QIcon,QFontMetrics,QDesktopServices

import platform
import re
import sys
import os
#-----------------------------------------------------------------------

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

        self.check_button = QPushButton("Check Password")
        self.check_button.clicked.connect(self.check_password)
        layout.addWidget(self.check_button)

        self.setLayout(layout)
    def check_password(self):
        entered_password = self.password_input.text()
        if "11" in entered_password and "3" in entered_password:
            self.open_main_form()
        else:
            QMessageBox.critical(self, "Error", "Incorrect password.")
            self.close()

    def open_main_form(self):
        self.main_form = FileSearchHandler()
        self.main_form.show()
        self.close()

#----------------------------------------------------------------------------
    
class FileSearch(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    #-----------------------------------------------------------------------
    def default_Values(self):
        #Some Constants
        self.APP_NAME = {
            "English": "FileSearch",
            "Japanese": "ファイル検索",
            "Vietnamese": "Search File"
            }
        # APP_DOMAIN = f"com.mycompany.{APP_NAME}"  # used on macOS
        self.DEFAULT_LANGUAGE = "English"
        self.DEFAULT_PATH = os.path.expanduser("~/Documents")
        #Get default values
        self.language,self.search_path = self.get_default_values()
        self.lang={"English":{"ENG":"English","JP":"Japanese","VN"  :"Vietnamese"},"Japanese":{"ENG":"英語","JP":"日本語","VN"  :"ベトナム語"},
                "Vietnamese":{"ENG":"Tiếng Anh","JP":"Tiếng Nhật","VN"  :"Tiếng Việt"}}
        self.search={"English":{"AND":"All matched","OR":"Contain","NOT"  :"Not contain"},"Japanese":{"AND":"全て一致","OR":"いずれか","NOT"  :"いずれか除外"},
                "Vietnamese":{"AND":"Tất cả","OR":"Bao hàm","NOT"  :"Không bao hàm"}}
        self.place_holder={"English":"Input search keywords","Japanese":"検索キーワードを入力","Vietnamese":"Nhập từ khóa tìm kiếm"}
        self.open_dialog_hint={"English":"Click to change search folder","Japanese":"クリックして検索フォルダを変更","Vietnamese":"Click để thay đổi đường dẫn tìm kiếm"}
        self.search_hint={"English":"Multiple keywords are separated by ',:;' or spaces",
                        "Japanese":"複数のキーワードは半角で英字、数字、記号とし',:;'または空白で区切って入力",
                        "Vietnamese":"Các từ khóa cách nhau bởi ',:;' hoặc khoảng trắng"}
        self.logic_hint = {"English":
                                {0: "Any of the keywords matches",
                                1: "All of the keywords matches, ignore order",
                                2: "Not contain all keywords"},
                        "Japanese":{0: "いずれかのキーワードに一致",
                                1: "順番問わず、全てのキーワードに一致",
                                2: "全てのキーワードに一致しない"},
                        "Vietnamese":{0: "Có ít nhất một từ khóa ",
                                1: "Tất cả đều tìm thấy , không cần thứ tự",
                                2: "Không chứa tất cả các từ khóa này"}}
        self.type_hint = {"English":"Select file type","Japanese":"ファイルタイプを選択","Vietnamese":"Chọn Lodi tập tin"}
        self.folder_hint = {"English":"Double Click to change search folder",
                            "Japanese":"ダブルクリックしてフォルダを選択、再検索",
                            "Vietnamese":"Click đúp để chọn đường dẫn tìm kiếm, tìm kiếm lại"}
        self.file_hint = {"English":"Double Click to go file location",
                            "Japanese":"ダブルクリックしてファイルの場所を開く",
                            "Vietnamese":"Click đúp để đi tới vị trí tập tin"}
        self.label ={"English": {
                        "Title": "File Search",
                        "Search Path:":"Search Path:","Search keyword:":"Search keyword:",
                        "File Type:":"File Type:","Folders:":"Folders:","Files:":"Files:",
                        "SearchButton":"Search",
                        "SelectFolder":"Select Folder",
                        "Info":"File Information:",
                        "message":"Searching, please wait...",
                        "finish":"Search finished!",
                        "Cancel":"Cancel"
                        },
            "Japanese":{
                        "Title": "ファイル検索",
                        "Search Path:":"検索パス:","Search keyword:":"検索キーワード:",
                        "File Type:":"ファイルタイプ:","Folders:":"フォルダ:","Files:":"ファイル:",
                        "SearchButton":"検索",
                        "SelectFolder":"フォルダを選択",
                        "Info":"ファイル情報:",
                        "message":"検索中、お待ちください...",
                        "finish":"検索完了!",
                        "Cancel":"キャンセル"
                        },
            "Vietnamese":{
                        "Title": "Tìm kiếm tập tin",
                        "Search Path:":"Đường dẫn:","Search keyword:":"Từ Khóa:",
                        "File Type:":"Kiểu tập tin:","Folders:":"Thư mục:","Files:":"Tập tin   :",
                        "SearchButton":"Tìm kiếm",
                        "SelectFolder":"Chọn thư mục",
                        "Info":"Chi tiết tập tin:",
                        "message":"Đang tìm, vui lòng đợi...",
                        "finish":"Hoàn Thành tìm kiếm!",
                        "Cancel":"Hủy"
                        }
            }
        self.type ={
            0:{"English": 'All', 'Japanese': '全て',"Vietnamese": "Tất cả"},
            1:{"English": 'VectorWorks Files', 'Japanese': 'VectorWorks ファイル',  "Vietnamese": "Tập tin VectorWorks"},
            2:{"English": 'CAD Files', 'Japanese': 'CAD ファイル',  "Vietnamese": "Tập tin CAD"},
            3:{"English": 'Excel Files', 'Japanese': 'Excel ファイル',  "Vietnamese": "Tập tin Excel"},
            4:{"English": 'PDF Files', 'Japanese': 'PDF ファイル',  "Vietnamese": "Tập tin PDF"},
            5:{"English": 'DXF Files', 'Japanese': 'DXF ファイル',  "Vietnamese": "Tập tin DXF"},
            6:{"English": 'Image Files', 'Japanese': '画像 ファイル',"Vietnamese": "Tập tin hình ảnh"},
            7:{"English": 'Video Files', 'Japanese': '動画 ファイル',"Vietnamese": "Tập tin video"},
            8:{"English": 'Word Files', 'Japanese': 'Word ファイル',  "Vietnamese": "Tập tin Word"},
            9:{"English": 'Text Files', 'Japanese': 'テキスト ファイル',"Vietnamese": "Tập tin text"},
            10:{"English": 'Audio Files', 'Japanese': '音声 ファイル',"Vietnamese": "Tập tin âm thanh"},
            11:{"English": 'Executable Files', 'Japanese': '実行可能 ファイル', "Vietnamese": "Tập tin thực thi"}
        }
        self.ext_type ={
            0: [],
            1: [".vwx",".vwxp",".vwxw",".sta"],
            2: [".vwx",".sta",".mcd",".dwg", ".step", ".stp","dxf",
                        ".CAT",".iges", ".igs", ".sldprt", ".sldasm", ".prt"],
            3: [".xl",".xlsx",".xlsm",".xlsb",".xltx",".xltm",".xlt",".csv",".numbers"],
            4: [".pdf"],
            5: ["dxf"],
            6: [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg"],
            7: [".mp4", ".avi", ".mkv", ".mov", ".wmv"],
            8: [ ".doc", ".docx", ".odt", ".rtf",".dot","docm","dotx"],
            9: [".txt", ".doc", ".docx", ".odt", ".rtf",".ini",".log" ,".csv" ,".json"],
            10: [".mp3", ".wav", ".aac", ".flac", ".ogg"],
            11: [".exe", ".msi", ".bat", ".cmd",".pkg",".sh", ".app", ".jar", ".py", ".pyw", ".pyc"]
        }
        self.logics ={
            "OR":0,
            "AND":1,
            "NOT":2
        }
        self.init =True
#-----------------------------------------------------
    def initUI(self):
        self.default_Values()
        self.setWindowTitle(self.APP_NAME[self.DEFAULT_LANGUAGE])
        # basedir = os.path.dirname(os.path.abspath(__file__))
        self.icon = self.resource_path("favicon.ico")
        self.setWindowIcon(QIcon(self.icon))
        self.setGeometry(100, 100, 500, 300)
        layout = QVBoxLayout()
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
        layout.addLayout(lang_layout)
        self.japanese_radio.setChecked(True)
        #Folder Search path
        search_folder_layout = QHBoxLayout()
        self.search_folder_label = QLabel(self.label[self.language]["Search Path:"])
        self.search_folder_path = QLabel()
        self.search_folder_path.setText(self.search_path)
        # self.search_folder_path.setStyleSheet("color: dark_blue; font-style: italic;text-align: left;")
        self.search_folder_change = QPushButton("...")
        self.search_folder_change.setFixedSize(50,30)  # Set the size of the button
        self.search_folder_change.setStyleSheet("background-color: lightpink;")  # Set the background color
        search_folder_layout.addWidget(self.search_folder_label)
        search_folder_layout.addWidget(self.search_folder_path)
        search_folder_layout.addWidget(self.search_folder_change)
        
        layout.addLayout(search_folder_layout)
        
        # keyword input
        keyword_layout = QHBoxLayout()
        self.search_label = QLabel(self.label[self.language]["Search keyword:"])
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(self.place_holder[self.language])
        self.search_button = QPushButton(self.label[self.language]["SearchButton"])
        
        keyword_layout.addWidget(self.search_label)
        keyword_layout.addWidget(self.search_input)
        keyword_layout.addWidget(self.search_button)
        layout.addLayout(keyword_layout)
        
        search_layout = QHBoxLayout()
        self.search_radio = QButtonGroup()
        self.or_radio = QRadioButton(self.search[self.language]["OR"])
        self.and_radio = QRadioButton(self.search[self.language]["AND"])
        self.not_radio = QRadioButton(self.search[self.language]["NOT"])
        
        self.search_radio.addButton(self.or_radio,0)
        self.search_radio.addButton(self.and_radio,1)
        self.search_radio.addButton(self.not_radio,2)
        
        search_layout.addWidget(self.or_radio)
        search_layout.addWidget(self.and_radio)
        search_layout.addWidget(self.not_radio)
        
        layout.addLayout(search_layout)
        self.or_radio.setChecked(True)
        # Create the combo box for file types
        file_type_layout = QHBoxLayout()
        self.file_type_label = QLabel(self.label[self.language]["File Type:"])
        self.file_type_combo = QComboBox()
        file_type_layout.addWidget(self.file_type_label)
        file_type_layout.addWidget(self.file_type_combo)
        # Add file types to the combo box
        for _ in range(len(self.type)):
            self.file_type_combo.addItem(self.type[_][self.language])
        self.file_type_combo.setCurrentIndex(0) # Set default selection to 'All'
        layout.addLayout(file_type_layout)
        # Create the listbox for folders and files
        list_layout = QHBoxLayout()
        folder_layout = QVBoxLayout()
        self.folder_label = QLabel(self.label[self.language]["Folders:"])
        self.folder_list = QListWidget()
        folder_layout.addWidget(self.folder_label)
        folder_layout.addWidget(self.folder_list)
        list_layout.addLayout(folder_layout)
        
        file_layout = QVBoxLayout()
        self.file_label = QLabel(self.label[self.language]["Files:"])
        self.file_list = QListWidget()
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_list)
        list_layout.addLayout(file_layout)  
        layout.addLayout(list_layout)
        
        info_layout = QHBoxLayout()
        self.info_label = QLabel(self.label[self.language]["Info"])
        self.info = QLabel()
        # self.info.setStyleSheet("color: red; font-style: italic;text-align: left;")
        info_layout.addWidget(self.info_label)
        info_layout.addWidget(self.info)
        layout.addLayout(info_layout)
        
        self.cancel_button = QPushButton(self.label[self.language]["Cancel"])
        self.cancel_button.setMaximumWidth(80)  # Won't grow beyond 80px
        layout.addWidget(self.cancel_button,alignment=Qt.AlignCenter)
        
        self.setLayout(layout)
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
    def get_default_values(self):
        import sys
        self.name  = self.APP_NAME[self.DEFAULT_LANGUAGE]
        if platform.system() == "Windows":
            import winreg
            try:
                reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, f"Software\\{self.name}")
                language,default_path= winreg.QueryValueEx(reg_key, "Language"), winreg.QueryValueEx(reg_key, "SearchPath")
                winreg.CloseKey(reg_key)
                return language[0],default_path[0]
            except FileNotFoundError:
                return  self.name,os.path.expanduser("~")
        elif platform.system() == "Darwin":
        # elif sys.platform == "darwin":
            # macOS: use NSUserDefaults
            # from Foundation import NSUserDefaults
            # self.defaults = NSUserDefaults.alloc().initWithSuiteName_(f"com.mycompany.{self.name}")
            # self.defaults = NSUserDefaults.alloc().initWithSuiteName_(f"com.mycompany.FileSearchApp")
            # language = self.defaults.stringForKey_("Language")
            # default_path = self.defaults.stringForKey_("SearchPath")
            
            language = "English"
            default_path = "~"
            return language, default_path
#-----------------------------------------------------------------------
class FileSearchHandler(FileSearch):
    def __init__(self):
        super().__init__()
        # Set default values
        self.logic_index = self.logics["OR"] # 0 for OR, 1 for AND, 2 for NOT
        self.type_index =0 # For ALL file type
        #Control default values
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
        self.reset_data()
        self.connect_signals()
        self.change_logic()
        self.change_tooltips()
    #----------------------------------------------------------------
    def connect_signals(self):
        #Change language
        self.language_radio.buttonClicked.connect(self.change_language)
        # self.english_radio.toggled.connect(self.change_language)
        # Change Search Folder
        self.search_folder_change.clicked.connect(self.open_file_dialog)
        # Search Folder and Files
        self.search_input.returnPressed.connect(lambda:self.change_search_source(source=1))
        self.search_button.clicked.connect(lambda:self.change_search_source(source=1))
        # Connect the combo box's currentIndexChanged signal to the search_files method
        self.file_type_combo.currentIndexChanged.connect(self.change_type)
        #Search logic
        self.search_radio.buttonClicked.connect(self.change_logic)
        #CLick self.Folder_list
        self.folder_list.itemDoubleClicked.connect(lambda : self.change_search_source(source=2))
        #Show file info
        self.file_list.currentItemChanged.connect(self.show_file_info)
        self.file_list.itemDoubleClicked.connect(self.open_file_location)
        #Quit Program
        self.cancel_button.clicked.connect(QApplication.quit)
    #----------------------------------------------------------------
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            QApplication.quit()
        super().keyPressEvent(event)
    #----------------------------------------------------------------
    def closeEvent(self, event):
        # Save to Windows Registry before closing
        try:
            self.saved_to_registry()
        except Exception as e:
            print(f"Registry write failed: {e}")

        super().closeEvent(event)  # Call the default close event handler event.accept()  # Allow the window to close

    #----------------------------------------------------------------
    def change_tooltips(self):
        self.search_folder_change.setToolTip(self.open_dialog_hint[self.language])
        self.file_type_combo.setToolTip(self.type_hint[self.language])
        self.folder_list.setToolTip(self.folder_hint[self.language])
        self.file_list.setToolTip(self.file_hint[self.language])
        self.search_input.setToolTip(self.search_hint[self.language])
        logic = self.logic_hint[self.language] 
        self.or_radio.setToolTip(logic[0])
        self.and_radio.setToolTip(logic[1])
        self.not_radio.setToolTip(logic[2])
    #----------------------------------------------------------------
    def open_file_dialog(self):
        select_folder = self.label[self.language]["SelectFolder"]
        folder_path = QFileDialog.getExistingDirectory(self, select_folder,self.search_path)
        if folder_path:
            self.search_path = folder_path
            self.search_folder_path.setText(folder_path)
            self.search_files()
        else:
            self.show_empty()
    #----------------------------------------------------------------
    def change_language(self):
        langs,labels,types,search =self.lang,self.label,self.type,self.search
        if self.english_radio.isChecked():
            self.language = 'English'
        elif self.japanese_radio.isChecked():
            self.language = 'Japanese'
        else:
            self.language = 'Vietnamese'
        #Update changed language to registry
        self.saved_to_registry()
        #Set the labels and combo box items based on the selected language
        self.setWindowTitle(labels[self.language]["Title"])
        self.english_radio.setText(langs[self.language]["ENG"])  
        self.japanese_radio.setText(langs[self.language]["JP"])
        self.vietnamese_radio.setText(langs[self.language]["VN"])
        self.search_folder_label.setText(labels[self.language]["Search Path:"])
        self.search_label.setText(labels[self.language]["Search keyword:"])
        self.search_input.setPlaceholderText(self.place_holder[self.language])
        self.search_button.setText(labels[self.language]["SearchButton"])
        self.and_radio.setText(search[self.language]["AND"])
        self.or_radio.setText(search[self.language]["OR"])
        self.not_radio.setText(search[self.language]["NOT"])
        self.file_type_label.setText(labels[self.language]["File Type:"])
        self.folder_label.setText(labels[self.language]["Folders:"])
        self.file_label.setText(labels[self.language]["Files:"])
        self.cancel_button.setText(labels[self.language]["Cancel"])
        self.info_label.setText(self.label[self.language]["Info"])
        self.info.setText("")
        self.file_type_combo.clear()
        for _ in range(len(self.type)):
            self.file_type_combo.addItem(types[_][self.language])
        self.change_tooltips()
    #----------------------------------------------------------------
    def reset_data(self):
        self.keywords = ""
        self.condition = None
        self.found_files = []
        self.found_folders = set()
        self.found_files_short = []
        self.found_folders_short = set()
    #----------------------------------------------------------------
    #Search from search pattern
    def change_search_source(self,source =1):
        # self.init = True
        if self.search_input.text().strip() :
            if source == 2:
                if self.folder_list.currentItem() is None:
                    return
                else:
                    self.search_path = os.path.join(self.search_path,self.folder_list.selectedItems()[0].text())
            self.search_folder_path.setText(self.search_path)
            self.info.setText(self.label[self.language]["message"])
            self.search_files(source = source)
        else:
            if not self.init:
                self.show_empty()
    #----------------------------------------------------------------
    def change_logic(self):
        if self.and_radio.isChecked():
            self.logic_index = self.logics["AND"]
        elif self.or_radio.isChecked():
            self.logic_index = self.logics["OR"]
        else:
            self.logic_index = self.logics["NOT"]
        self.search_files()
    #----------------------------------------------------------------
    def change_type(self):
        if self.file_type_combo.currentIndex() == -1:
            self.type_index =0
        else:
            self.type_index =self.file_type_combo.currentIndex()
        self.search_type =self.ext_type[self.type_index]
        self.search_files()
    #----------------------------------------------------------------
    def saved_to_registry(self):
        if platform.system() == "Windows":
            import winreg
            reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\{self.APP_NAME[self.DEFAULT_LANGUAGE]}")
            winreg.SetValueEx(reg_key, "Language", 0, winreg.REG_SZ, self.language)
            winreg.SetValueEx(reg_key, "SearchPath", 0, winreg.REG_SZ, self.search_path)
            winreg.CloseKey(reg_key)
        elif platform.system() == "Darwin":
            # macOS: use NSUserDefaults
            pass
#-----------------------------------------------------------------------
    def search_files(self,source =1):
        self.reset_data()
        keyword = self.search_input.text().strip()
        self.info.setText(self.label[self.language]["message"])
        if keyword:
            self.init = False
            self.keywords = re.split(r'[ ,;:/|]+', self.search_input.text().strip().lower())
            for root, dirs, files in os.walk(self.search_path):
                # Check if any file or folder name matches any part of the search pattern
                for name in files + dirs:
                    if self.logic_index == 0: #OR
                        self.condition =any(part in name.lower() for part in self.keywords)
                    elif self.logic_index == 1:#AND
                        self.condition =all(part in name.lower() for part in self.keywords)
                    else:#NOT
                        self.condition =not all(part in name.lower() for part in self.keywords)
                    if self.condition:
                        if os.path.isfile(os.path.join(root, name)):
                            self.found_files.append(os.path.join(root, name))
                            self.found_folders.add(os.path.dirname(os.path.join(root, name)))             
            # Filter by file type
            if self.search_type or len(self.search_type)>0:
                self.found_files,folders = self.filter_type()
                self.found_folders = folders.intersection(self.found_folders)
            self.filtered_files, self.filtered_folders = self.found_files, self.found_folders
            self.show_data(source)
        else:#Nothing selected 
            self.file_list.clear()
            self.folder_list.clear()
            if not self.init:
                self.show_empty()
#-----------------------------------------------------------------------
    def show_empty(self):
        self.reset_data()
        for root, dirs, _ in os.walk(self.search_path):
            if dirs:
                for dir in dirs:
                    self.found_folders.add(os.path.join(root, dir))
        if self.found_folders:
            for folder in self.found_folders:
                partial_path = folder.removeprefix(self.search_path)
                if partial_path.startswith(os.path.sep):
                    partial_path = partial_path[1:]
                self.found_folders_short.add(partial_path)    
        self.show_data()
#-----------------------------------------------------------------------
    def filter_type(self):
        filtered_files = []
        filtered_folders =  set()
        if self.search_type or len(self.search_type)>0:
            for file in self.found_files:
                if any(file.lower().endswith(ext) for ext in self.search_type):
                    filtered_files.append(file)
                    dirname= os.path.dirname(file)
                    if dirname.startswith(os.path.sep):
                        partial_path = partial_path[1:]
                        dirname = dirname[1:]
                    filtered_folders.add(dirname)
        return filtered_files, filtered_folders
    #-----------------------------------------------------------------------
    def show_data(self,source=1):
        self.file_list.clear()
        self.folder_list.clear()
        if source == 1:
            if self.found_folders or self.found_files:
                self.info.setText(self.label[self.language]["finish"])
            else:
                self.info.setText("")
            if self.found_folders:
                folders = list(self.found_folders)
                for folder in folders:
                    partial_path = folder.removeprefix(self.search_path)
                    if partial_path.startswith(os.path.sep):
                        partial_path = partial_path[1:]
                    self.found_folders_short.add(partial_path)    
            if self.found_files:
                for file in self.found_files:
                    filename = os.path.basename(file)
                    self.found_files_short.append(filename)    
        else:
            if self.found_files:
                for file in self.found_files:
                    filename = os.path.basename(file)
                    self.found_files_short.append(filename)
        #----------------------------------------------------------------------
        if len(self.found_files)>0:
            for file in self.found_files_short:
                self.file_list.addItem(file)
        self.file_label.setText(self.label[self.language]["Files:"]+" "+ str(self.file_list.count()))
        if len(self.found_folders)>0:
            for folder in self.found_folders_short:
                self.folder_list.addItem(folder)
        self.folder_label.setText(self.label[self.language]["Folders:"]+" "+ str(self.folder_list.count()))
#-----------------------------------------------------------------------   
    def show_file_info(self,current):
        self.info.setTextInteractionFlags(self.info.textInteractionFlags() | Qt.TextSelectableByMouse)
        fm = QFontMetrics(self.info.font())
        if current:
            file_index = self.file_list.currentRow()
            file_path = os.path.dirname(self.found_files[file_index]).lower()
            file_path = file_path.removeprefix(self.search_path).removeprefix(os.path.sep)
            foundFolders =[i.text().lower() for i in self.folder_list.findItems("",Qt.MatchContains)]
            index = list(filter(lambda i:foundFolders[i] in file_path,range(len(foundFolders))))
            if index:
                self.folder_list.setCurrentRow(index[0])
            short_path =fm.elidedText(self.found_files[self.file_list.row(current)],Qt.ElideMiddle,600)
            self.info.setText(short_path)
        else:
            self.info.setText("")
#-----------------------------------------------------------------------   
    def open_file_location(self,item):
        import subprocess
        filepath = os.path.dirname(self.found_files[self.file_list.row(item)])
        try:
            # --- use one unified method ---
            if sys.platform.startswith("win"):
                QDesktopServices.openUrl(QUrl.fromLocalFile(filepath))
            elif sys.platform.startswith("darwin"):
                subprocess.run(["open", filepath])
            else:  # Linux and others
                subprocess.run(["xdg-open", filepath])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open folder:\n{e}")

#-----------------------------------------------------------------------         
# Run the application, main loop 
if __name__ == "__main__":
    import sys
    if platform.system() == "Windows":
        import winreg
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\\FileSearch")
            passed= winreg.QueryValueEx(reg_key, "Passed")
            winreg.CloseKey(reg_key)
        except FileNotFoundError:
            passed = False
    elif platform.system() == "Darwin":
        pass
    app = QtWidgets.QApplication(sys.argv)
    if passed[0] == "OK":
        form = FileSearchHandler()
    else:
        form = CheckForm()
    import re
    form.show()
    sys.exit(app.exec())