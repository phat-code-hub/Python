
from PySide6 import QtWidgets,QtCore, QtGui
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import re
import os
import winreg
#-----------------------------------------------------------------------
class FileSearch(QWidget):
    def __init__(self):
        super().__init__()
        self.default_path = self.get_default_folder_path_from_registry()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("File Search")
        self.setGeometry(100, 100, 400, 200)
        layout = QVBoxLayout()
        default_folder_layout = QHBoxLayout()
        self.default_folder_label = QLabel('Default Path:')
        self.default_folder_path = QLabel(self.default_path)
        self.default_folder_path.setStyleSheet("color: blue; font-style: italic;text-align: left;")
        default_folder_layout.addWidget(self.default_folder_label)
        default_folder_layout.addWidget(self.default_folder_path)
        
        layout.addLayout(default_folder_layout)
        
        # keyword input
        keyword_layout = QHBoxLayout()
        self.search_label = QLabel('Pattern:')
        self.search_input = QLineEdit()
        self.search_input.returnPressed.connect(self.search_files)
        self.search_change = QPushButton("...")
        self.search_button = QPushButton('Search')
        self.search_button.clicked.connect(self.search_files)
        # Connect the search input's returnPressed signal to the search_files method
        self.search_input.returnPressed.connect(self.search_files)
        
        
        self.search_change.setFixedSize(30, 20)  # Set the size of the button
        self.search_change.setStyleSheet("background-color: lightpink;")  # Set the background color
        self.search_change.clicked.connect(self.open_file_dialog)
        
        keyword_layout.addWidget(self.search_label)
        keyword_layout.addWidget(self.search_input)
        keyword_layout.addWidget(self.search_change)
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
        for file_type in file_types:
            self.file_type_combo.addItem(file_type)

        # Connect the combo box's currentIndexChanged signal to the search_files method
        self.file_type_combo.currentIndexChanged.connect(self.search_files)
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

    def search_files(self):
        keyword = self.search_input.text()
        if not keyword:
            pattern = f"*{keyword}*"
            file_type = self.file_type_combo.currentText()
            # If the pattern is empty, disable the listboxes
            self.folder_list.setDisabled(True)
            self.file_list.setDisabled(True)
            
        
        
        else:
            # If the pattern is not empty, enable the listboxes
            self.folder_list.setDisabled(False)
            self.file_list.setDisabled(False)
        
        
        
    def open_file_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.default_folder_path.setText(folder_path)
            self.saved_path_to_registry()


    def saved_path_to_registry(self):
        reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\FileSearchApp")
        winreg.SetValueEx(reg_key, "DefaultPath", 0, winreg.REG_SZ, self.default_folder_path.text())
        winreg.CloseKey(reg_key)
        
    def get_default_folder_path_from_registry(self):
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\FileSearchApp")
            default_path, _ = winreg.QueryValueEx(reg_key, "DefaultPath")
            winreg.CloseKey(reg_key)
            return default_path
        except FileNotFoundError:
            return os.path.expanduser("~")
        
        

        
# Run the application, main loop 
# from File_Search_Ui  import FileSearchUI
if __name__ == "__main__":
    app = QApplication([])
    Form = FileSearch()
    Form.show()
    app.exec()