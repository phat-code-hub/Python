
from PySide6 import QtWidgets,QtCore, QtGui
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import re
import sys
import os
import winreg
#-----------------------------------------------------------------------
class FileSearchHandler:
    def __init__(self):
        pass
    
        
    def search_files(self, search_criteria):
        # Search logic goes here
        default_path = self.get_default_folder_path_from_registry()
        if not default_path:
            default_path = os.path.expanduser("~")
        # Perform search using the search criteria
        # ...

    # def get_default_folder_path_from_registry(self):
        # Get default folder path from registry
        # ... 
    
    
        
    def open_file_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.search_folder_path.setText(folder_path)
            self.saved_path_to_registry()


def saved_path_to_registry(searchFolder):
        reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\FileSearchApp")
        winreg.SetValueEx(reg_key, "DefaultPath", 0, winreg.REG_SZ, searchFolder)
        winreg.CloseKey(reg_key)
    
class FileSearch(QWidget):
    # handler = FileSearchHandler(search_folder_path=None)
    def __init__(self):
        super().__init__()
        self.search_path = self.get_search_folder_path_from_registry()
        self.initUI()
        self.handler = FileSearchHandler()
    def get_search_folder_path_from_registry(self):
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\FileSearchApp")
            search_path, _ = winreg.QueryValueEx(reg_key, "DefaultPath")
            winreg.CloseKey(reg_key)
            return search_path
        except FileNotFoundError:
            return os.path.expanduser("~")
    def initUI(self):
        self.setWindowTitle("File Search")
        self.setGeometry(100, 100, 500, 300)
        layout = QVBoxLayout()
        #Languages choice
        lang_layout = QHBoxLayout()
        self.language_radio = QButtonGroup()
        self.english_radio = QRadioButton('ENG')
        self.japanese_radio = QRadioButton('JP')
        self.language_radio.addButton(self.english_radio)
        self.language_radio.addButton(self.japanese_radio)
        
        self.english_radio.setChecked(True)
        self.language_radio.buttonToggled.connect(self.update_language)
    
        # Add the radio buttons to the layout
        lang_layout.addWidget(self.english_radio)
        lang_layout.addWidget(self.japanese_radio)
        layout.addLayout(lang_layout)
        
        search_folder_layout = QHBoxLayout()
        self.search_folder_label = QLabel('Search Path:')
        self.search_folder_path = QLabel(self.search_path)
        self.search_folder_path.setStyleSheet("color: blue; font-style: italic;text-align: left;")
        search_folder_layout.addWidget(self.search_folder_label)
        search_folder_layout.addWidget(self.search_folder_path)
        
        layout.addLayout(search_folder_layout)
        
        # keyword input
        keyword_layout = QHBoxLayout()
        self.search_label = QLabel('Search keyword:')
        self.search_input = QLineEdit()
        self.search_folder_change = QPushButton("...")
        self.search_button = QPushButton('Search')
        ### Event Handlers
        self.search_folder_change.clicked.connect(self.open_file_dialog)
        # Connect the search input's returnPressed signal to the search_files method
        # self.search_input.returnPressed.connect(self.search_files)
        # self.search_button.clicked.connect(self.search_files)

        self.search_folder_change.setFixedSize(30, 20)  # Set the size of the button
        self.search_folder_change.setStyleSheet("background-color: lightpink;")  # Set the background color
        # self.search_folder_change.clicked.connect(self.open_file_dialog)
        # self.search_folder_change.clicked.connect(self.change_folder)
        
        keyword_layout.addWidget(self.search_label)
        keyword_layout.addWidget(self.search_input)
        keyword_layout.addWidget(self.search_folder_change)
        keyword_layout.addWidget(self.search_button)
        layout.addLayout(keyword_layout)
        # Create the combo box for file types
        file_type_layout = QHBoxLayout()
        self.file_type_label = QLabel('File Type:')
        self.file_type_combo = QComboBox()
        file_type_layout.addWidget(self.file_type_label)
        file_type_layout.addWidget(self.file_type_combo)

        # Add file types to the combo box
        file_types = ['All','CAD Files','PDF Files',  'Text Files','Image Files', 'Audio Files', 'Video Files', 'Executable Files']
        # file_types = types[self.language].values()
        for file_type in file_types:
            self.file_type_combo.addItem(file_type)

        # Connect the combo box's currentIndexChanged signal to the search_files method
        # self.file_type_combo.currentIndexChanged.connect(self.search_files)
        layout.addLayout(file_type_layout)
        
        # Create the listbox for folders and files
        list_layout = QHBoxLayout()
        
        folder_layout = QVBoxLayout()
        self.folder_label = QLabel('Folders:')
        self.folder_list = QListWidget()
        folder_layout.addWidget(self.folder_label)
        folder_layout.addWidget(self.folder_list)
        list_layout.addLayout(folder_layout)
        
        file_layout = QVBoxLayout()
        self.file_label = QLabel('Files:')
        self.file_list = QListWidget()
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_list)
        list_layout.addLayout(file_layout)  

        layout.addLayout(list_layout)
        self.setLayout(layout)
#-----------------------------------------------------------------------
    def update_language(self, button):
        langs,labels,types = Get_Names()
        if button == self.english_radio:
            self.language = 'English'
        elif button == self.japanese_radio:
            self.language = 'Japanese'
        #Set the labels and combo box items based on the selected language
        self.setWindowTitle("File Search" if self.language == "English" else "ファイル検索")
        self.english_radio.setText(langs[self.language]["ENG"])  
        self.japanese_radio.setText(langs[self.language]["JP"])
        self.search_folder_label.setText(labels[self.language]["Search Path:"])
        self.search_label.setText(labels[self.language]["Search keyword:"])
        self.search_button.setText(labels[self.language]["SearchButton"])
        self.file_type_label.setText(labels[self.language]["File Type:"])
        self.folder_label.setText(labels[self.language]["Folders:"])
        self.file_label.setText(labels[self.language]["Files:"])
        self.file_type_combo.clear()
        file_types = types[self.language].values()
        for file_type in file_types:
            self.file_type_combo.addItem(file_type)
    #Change default folder path
    def open_file_dialog(self):
        
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.search_folder_path.setText(folder_path)
            # self.saved_path_to_registry()
            # saved_path_to_registry(self.search_folder_label.text())
            saved_path_to_registry(self.search_path)
    
    # def change_folder(self):
    #     handle = FileSearchHandler()
    #     handle.open_file_dialog()
    #-----------------------------------------------------------------------

    # def search_files(self):
        # keyword = self.search_input.text()
        # if not keyword:
        #     pattern = f"*{keyword}*"
        #     file_type = self.file_type_combo.currentText()
        #     # If the pattern is empty, disable the listboxes
        #     self.folder_list.setDisabled(True)
        #     self.file_list.setDisabled(True)
        
        # else:
        #     # If the pattern is not empty, enable the listboxes
        #     self.folder_list.setDisabled(False)
        #     self.file_list.setDisabled(False)
        
#-----------------------------------------------------------------------   

def Get_Names():
    lang = {"English": {"ENG":"ENG","JP":"JP"},"Japanese":{"ENG":"英語","JP":"日本語"}}
    label ={"English": {
                        "Search Path:":"Search Path:","Search keyword:":"Search keyword:",
                        "File Type:":"File Type:","Folders:":"Folders:","Files:":"Files:",
                        "SearchButton":"Search",
                        },
            "Japanese":{
                        "Search Path:":"検索パス:","Search keyword:":"検索キーワード:",
                        "File Type:":"ファイルタイプ:","Folders:":"フォルダ:","Files:":"ファイル:",
                        "SearchButton":"検索",
                        }}
    # file_types = ['All','CAD Files','PDF Files',  'Text Files','Image Files', 'Audio Files', 'Video Files', 'Executable Files']
    type = {
        "English": {
            'All': 'All',
            'CAD Files': 'CAD Files',
            'PDF Files': 'PDF Files',
            'Text Files': 'Text Files',
            'Image Files': 'Image Files',
            'Audio Files': 'Audio Files',
            'Video Files': 'Video Files',
            'Executable Files': 'Executable Files'
        },
        "Japanese": {
            'All': '全て',
            'CAD Files': 'CAD ファイル',
            'PDF Files': 'PDF ファイル',
            'Text Files': 'テキスト ファイル',
            'Image Files': '画像 ファイル',
            'Audio Files': '音声 ファイル',
            'Video Files': '動画 ファイル',
            'Executable Files': '実行可能 ファイル'
        }
    }
    return lang, label, type
        
# Run the application, main loop 
# from File_Search_Ui  import FileSearchUI
if __name__ == "__main__":
    # app = QApplication([])
    # Form = FileSearch()
    # Form.show()
    # app.exec()
    app = QtWidgets.QApplication(sys.argv)
    form = FileSearch()
    form.show()
    sys.exit(app.exec())