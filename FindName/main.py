
from PySide6 import QtWidgets,QtCore, QtGui
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import re
import sys
import os
import winreg
#-----------------------------------------------------------------------

    
class FileSearch(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    #-----------------------------------------------------------------------
    def default_Values(self):
        self.language,self.search_path = self.get_default_values()
        self.lang={"English":{"ENG":"English","JP":"Japanese","VN"  :"Vietnamese"},"Japanese":{"ENG":"英語","JP":"日本語","VN"  :"ベトナム語"},
                "Vietnamese":{"ENG":"Tiếng Anh","JP":"Tiếng Nhật","VN"  :"Tiếng Việt"}}
        self.search={"English":{"AND":"All","OR":"Contain","NOT"  :"Not contain"},"Japanese":{"AND":"全て","OR":"いずれか","NOT"  :"いずれか除外"},
                "Vietnamese":{"AND":"Tất cả","OR":"Bao hàm","NOT"  :"Không bao hàm"}}
        self.place_holder={"English":"Input search keywords","Japanese":"検索キーワードを入力","Vietnamese":"Nhập từ khóa tìm kiếm"}
        self.open_dialog_hint={"English":"Click to change search folder","Japanese":"クリックして検索フォルダを変更","Vietnamese":"Click để thay đổi đường dẫn tìm kiếm"}
        self.search_hint={"English":"Multiple keywords are separated by ',:;' or spaces",
                        "Japanese":"複数のキーワードは英字、数字、記号とし',:;'または空白で区切って入力",
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
        self.type_hint = {"English":"Select file type","Japanese":"ファイルタイプを選択","Vietnamese":"Chọn loại tập tin"}
        self.label ={"English": {
                        "Title": "File Search",
                        "Search Path:":"Search Path:","Search keyword:":"Search keyword:",
                        "File Type:":"File Type:","Folders:":"Folders:","Files:":"Files:",
                        "SearchButton":"Search",
                        "SelectFolder":"Select Folder",
                        "Info":"File Information:",
                        },
            "Japanese":{
                        "Title": "ファイル検索",
                        "Search Path:":"検索パス:","Search keyword:":"検索キーワード:",
                        "File Type:":"ファイルタイプ:","Folders:":"フォルダ:","Files:":"ファイル:",
                        "SearchButton":"検索",
                        "SelectFolder":"フォルダを選択",
                        "Info":"ファイル情報:",
                        },
            "Vietnamese":{
                        "Title": "Tìm kiếm tập tin",
                        "Search Path:":"Đường dẫn:","Search keyword:":"Từ Khóa:",
                        "File Type:":"Kiểu tập tin:","Folders:":"Thư mục:","Files:":"Tập tin   :",
                        "SearchButton":"Tìm kiếm",
                        "SelectFolder":"Chọn thư mục",
                        "Info":"Chi tiết tập tin:", 
                        }
            }
        self.type ={
            0:{"English": 'All', 'Japanese': '全て',"Vietnamese": "Tất cả"},
            1:{"English": 'CAD Files', 'Japanese': 'CAD ファイル',  "Vietnamese": "Tập tin CAD"},
            2:{"English": 'Excel Files', 'Japanese': 'Excel ファイル',  "Vietnamese": "Tập tin Excel"},
            3:{"English": 'PDF Files', 'Japanese': 'PDF ファイル',  "Vietnamese": "Tập tin PDF"},
            4:{"English": 'DXF Files', 'Japanese': 'DXF ファイル',  "Vietnamese": "Tập tin DXF"},
            5:{"English": 'Image Files', 'Japanese': '画像 ファイル',"Vietnamese": "Tập tin hình ảnh"},
            6:{"English": 'Video Files', 'Japanese': '動画 ファイル',"Vietnamese": "Tập tin video"},
            7:{"English": 'Word Files', 'Japanese': 'Word ファイル',  "Vietnamese": "Tập tin Word"},
            8:{"English": 'Text Files', 'Japanese': 'テキスト ファイル',"Vietnamese": "Tập tin text"},
            9:{"English": 'Audio Files', 'Japanese': '音声 ファイル',"Vietnamese": "Tập tin âm thanh"},
            10:{"English": 'Executable Files', 'Japanese': '実行可能 ファイル', "Vietnamese": "Tập tin thực thi"}
        }
        self.ext_type ={
            0: [],
            1: [".vwx",".sta",".mcd",".dwg", ".step", ".stp","dxf",
                        ".CAT",".iges", ".igs", ".sldprt", ".sldasm", ".prt"],
            2: [".xl",".xlsx",".xlsm",".xlsb",".xltx",".xltm",".xlt",".csv",".numbers"],
            3: [".pdf"],
            4: ["dxf"],
            5: [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg"],
            6: [".mp4", ".avi", ".mkv", ".mov", ".wmv"],
            7: [ ".doc", ".docx", ".odt", ".rtf",".dot","docm","dotx"],
            8: [".txt", ".doc", ".docx", ".odt", ".rtf",".ini",".log" ,".csv" ,".json"],
            9: [".mp3", ".wav", ".aac", ".flac", ".ogg"],
            10: [".exe", ".msi", ".bat", ".cmd",".pkg",".sh", ".app", ".jar", ".py", ".pyw", ".pyc"]
        }
        self.logics ={
            "OR":0,
            "AND":1,
            "NOT":2
        }
        
#------------------------------------------------------------------------------------------------------------------     
    def initUI(self):
        self.default_Values()
        self.setWindowTitle(self.label[self.language]["Title"])
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
        self.search_folder_change.setFixedSize(30, 20)  # Set the size of the button
        # self.search_folder_change.setStyleSheet("background-color: lightpink;")  # Set the background color
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
        self.setLayout(layout)
    #---------------------------------------------------------------------------
    def get_default_values(self):
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\FileSearchApp")
            language,default_path= winreg.QueryValueEx(reg_key, "Language"), winreg.QueryValueEx(reg_key, "SearchPath")
            winreg.CloseKey(reg_key)
            return language[0],default_path[0]
        except FileNotFoundError:
            return  "English",os.path.expanduser("~")
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
        self.folder_list.currentItemChanged.connect(lambda : self.change_search_source(source=2))
        # self.folder_list.itemDoubleClicked.connect(self.open_folder_location)
        #Show file info
        self.file_list.currentItemChanged.connect(self.show_file_info)
        self.file_list.itemDoubleClicked.connect(self.open_file_location)
    #----------------------------------------------------------------
    def change_tooltips(self,item =0):
        self.search_folder_change.setToolTip(self.open_dialog_hint[self.language])
        self.file_type_combo.setToolTip(self.type_hint[self.language])
        if item == 0 or item == 1: #Search Input
            self.search_input.setToolTip(self.search_hint[self.language])
        elif item == 0 or item == 2:#Logic
            logic = self.logic_hint[self.language] 
            self.or_radio.setToolTip(logic[0])
            self.and_radio.setToolTip(logic[1])
            self.not_radio.setToolTip(logic[2])
        elif item == 0 or item == 3:#Type
            pass
        elif item == 0 or item == 4:#Folder
            pass
        elif item == 0 or item == 5:#File
            pass

    #----------------------------------------------------------------
    def logic_tooltips(self):
        self.or_radio.setToolTip(self.logic[0])
        self.and_radio.setToolTip(self.logic[1])
        self.not_radio.setToolTip(self.logic[2])
    #----------------------------------------------------------------
    def open_file_dialog(self):
        select_folder = self.label[self.language]["SelectFolder"]
        folder_path = QFileDialog.getExistingDirectory(self, select_folder,self.search_path)
        if folder_path:
            self.search_path = folder_path
            self.search_folder_path.setText(folder_path)
            self.saved_path_to_registry()
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
        self.save_before_close(changed_item=1)
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
        self.file_type_combo.clear()
        for _ in range(len(self.type)):
            self.file_type_combo.addItem(types[_][self.language])
        self.change_tooltips(1)
        self.change_logic()
        self.change_type()
    #----------------------------------------------------------------
    def reset_data(self):
        self.keywords = ""
        self.condition = None
        self.found_files = []
        self.found_folders = set()
        self.found_files_short = []
        self.found_folders_short = set()
    #----------------------------------------------------------------
    def change_search_source(self,source =1):
        if source == 2:
            if self.folder_list.currentItem() is None:
                return
            else:
                self.search_path = self.folder_list.selectedItems()[0].text()
        self.search_folder_path.setText(self.search_path)
        self.saved_path_to_registry()
        self.reset_data()
        if self.search_input.text().strip() :
            self.search_files(source = source)
        else:
            self.show_data()
    #----------------------------------------------------------------
    def change_logic(self):
        if self.and_radio.isChecked():
            self.logic_index = self.logics["AND"]
        elif self.or_radio.isChecked():
            self.logic_index = self.logics["OR"]
        else:
            self.logic_index = self.logics["NOT"]
        self.change_tooltips(2)
        self.reset_data()
        self.search_files()
    #----------------------------------------------------------------
    def change_type(self):
        if self.file_type_combo.currentIndex() == -1:
            self.type_index =0
        else:
            self.type_index =self.file_type_combo.currentIndex()
        self.search_type =self.ext_type[self.type_index]
        self.reset_data()
        self.search_files()
    #----------------------------------------------------------------
    def saved_path_to_registry(self):
        self.save_before_close(changed_item=2)
    #----------------------------------------------------------------
    def save_before_close(self,changed_item=0):
        reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\FileSearchApp")
        if changed_item != 2: #Language changed
            winreg.SetValueEx(reg_key, "Language", 0, winreg.REG_SZ, self.language)
        if changed_item != 1: #Search Path changed
            winreg.SetValueEx(reg_key, "SearchPath", 0, winreg.REG_SZ, self.search_path)
        winreg.CloseKey(reg_key)
#-----------------------------------------------------------------------
    def search_files(self,source =1): 
        keyword = self.search_input.text().strip()
        if keyword:
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
        else:#Nothing selected 
            self.file_list.clear()
            self.folder_list.clear()
            self.reset_data()
        self.show_data(source)
#-----------------------------------------------------------------------
    def search_by_logic(self):
        if  self.filtered_files is None: 
            return
        else:
            if self.logic_index == 0: #OR:
                self.filtered_files = self.found_files
                self.filtered_folders =self.found_folders
            else:
                for file in self.found_files:
                    if self.logic_index == 1:#AND
                        found_files = []
                        found_folders = set()
                        self.condition =all(part in file for part in self.keywords)
                        if os.path.isfile(file):
                            found_files.append(file)
                            found_folders.add(os.path.dirname(file))
                        elif os.path.isdir(file):
                            found_folders.add(file)
                        self.filtered_files = found_files
                        self.filtered_folders = found_folders #.intersection(self.filtered_folders)
                    elif self.logic_index ==2:#NOT
                        set_files = set(self.filtered_files)
                        self.filtered_files = [item for item in self.found_files if item not in set_files]
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
            short_path =fm.elidedText(self.found_files[self.file_list.row(current)],Qt.ElideMiddle,400)
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
    app = QtWidgets.QApplication(sys.argv)
    form = FileSearchHandler()
    form.show()
    sys.exit(app.exec())