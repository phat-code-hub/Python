import sys
from PySide6.QtCore import Qt
# from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QListWidget, QListWidgetItem, QPushButton, QFileDialog, QMessageBox, QLabel
from PySide6.QtWidgets import *
import re
import fnmatch
import os
class FileSearchForm(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('File Search and Rename')
        layout = QVBoxLayout()
        # Create a layout for the language selection
        language_layout = QHBoxLayout()
        language_label = QLabel('Language:')
        self.language_label = language_label
        language_layout.addWidget(language_label)

        # Create radio buttons for English and Japanese
        self.language_radio = QButtonGroup()
        self.english_radio = QRadioButton('Eng')
        self.japanese_radio = QRadioButton('JP')
        self.language_radio.addButton(self.english_radio)
        self.language_radio.addButton(self.japanese_radio)


        language_layout.addWidget(self.english_radio)
        language_layout.addWidget(self.japanese_radio)
        # Add the language layout to the main layout
        layout.addLayout(language_layout)
        
        
        # keyword input
        keyword_layout = QHBoxLayout()
        self.keyword_label = QLabel('Pattern:')
        self.keyword_input = QLineEdit()
        self.keyword_input.returnPressed.connect(self.search_files)
        self.search_button = QPushButton('Search')
        self.search_button.clicked.connect(self.search_files)
    
        keyword_layout.addWidget(self.keyword_label)
        keyword_layout.addWidget(self.keyword_input)
        keyword_layout.addWidget(self.search_button)
        layout.addLayout(keyword_layout)

        # search folder input Group
        search_folder_layout = QHBoxLayout()
        self.folder_label = QLabel('Folder:') # Label Title
        self.path_label = QLabel('')  #Show Default Path
        self.browse_button = QPushButton('Browse')
        self.browse_button.clicked.connect(self.browse_folder) #Browse Button click event handle
        search_folder_layout.addWidget(self.folder_label)
        search_folder_layout.addWidget(self.path_label)
        search_folder_layout.addWidget(self.browse_button)
        
        layout.addLayout(search_folder_layout)
        
        
        #Full Path Layout Group
        full_path_layout = QHBoxLayout()
        self.full_path_label = QLabel('Selected Path:')
        self.full_path = QLabel ('FullPath')
        full_path_layout.addWidget(self.full_path_label)
        full_path_layout.addWidget(self.full_path)
        layout.addLayout(full_path_layout)
        
        # file list
        list_layout = QHBoxLayout()
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
    
        list_layout.addWidget(self.file_list)
        
        #Buttons Layout Group
        button_layout = QVBoxLayout()
        self.open_button = QPushButton('Open')
        # self.open_button.clicked.connect(self.open_file)
        self.rename_button = QPushButton('Rename')
        #self.rename_button.clicked.connect(self.rename_file)
        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.close) # Close Button click event handle
        button_layout.addWidget(self.open_button)
        button_layout.addWidget(self.rename_button)
        button_layout.addWidget(self.cancel_button)
        
        button_list_layout = QHBoxLayout()
        button_list_layout.addLayout(list_layout)
        button_list_layout.addLayout(button_layout)
        layout.addLayout(button_list_layout)
        
        self.setLayout(layout)
        # Events Handler
        self.english_radio.toggled.connect(self.update_language)
        self.japanese_radio.toggled.connect(self.update_language)
        self.english_radio.setChecked(True)  # Set English as the default language
        self.file_list.itemSelectionChanged.connect(self.update_button_states)
        self.open_button.clicked.connect(self.open_selected_file_location)

        self.open_button.setEnabled(False)
        self.rename_button.setEnabled(False)
        
    def search_files(self):
        keyword = self.keyword_input.text()
        if (keyword[0] not in [".", "*","?"]):
            keyword = "*"+keyword
        if (keyword[-1] not in [".", "*","?"]):
            keyword += "*"
        search_folder = self.path_label.text()
        self.default_folder_path = search_folder
        # Use Helper function
        full_paths = self.search_files_helper(search_folder, keyword)
        self.full_paths = full_paths
        self.file_list.clear()
        for file in full_paths:
            # path,file_name = os.path.dirname(file).split("\\")[-2],os.path.basename(file)
            file_name = os.path.basename(file)
            item = QListWidgetItem(file_name)
            self.file_list.addItem(item)
        self.open_button.setEnabled(len(self.full_paths) > 0)

    #-------------------------------------
    # Language Selection
    def update_language(self):
        if self.english_radio.isChecked():
            # Update the UI to use English
            self.setWindowTitle('File Search and Rename')
            self.language_label.setText('Language:')
            self.english_radio.setText('English')
            self.japanese_radio.setText('Japanese')
            self.keyword_label.setText('Pattern:')
            self.search_button.setText('Search')
            self.folder_label.setText('Folder:')
            self.browse_button.setText('Browse')
            self.full_path_label.setText('Selected Path:')
            self.full_path.setText('')
            self.open_button.setText('Open')
            self.rename_button.setText('Rename')
            self.cancel_button.setText('Cancel')
            
        elif self.japanese_radio.isChecked():
            # Update the UI to use Japanese
            self.setWindowTitle('ファイル検索と改称')
            self.language_label.setText('言語')
            self.english_radio.setText('英語')
            self.japanese_radio.setText('日本語')
            self.keyword_label.setText('検索パータン')
            self.search_button.setText('検索')
            self.folder_label.setText('検索フォルダー')
            self.browse_button.setText('参照')
            self.full_path_label.setText('選択ファイルパス')
            self.full_path.setText('')
            self.open_button.setText('開く')
            self.rename_button.setText('改称')
            self.cancel_button.setText('中止')
    
    #-------------------------------------
    # Change Default Folder
    def browse_folder(self):
        if self.english_radio.isChecked():
            title ="Select DefaultSearch Folder"
        elif self.japanese_radio.isChecked():
            title ="検索フォルダーを選択してください"
        folder_path = QFileDialog.getExistingDirectory(self, title)
        # self.search_folder_input.setText(folder_path)
        self.path_label.setText(folder_path)
    
    
    
    def search_files_helper(self, search_folder, keyword):
        file_list = []
        for root, dirs, files in os.walk(search_folder):
            for file in files:
                if fnmatch.fnmatch(file, keyword):
                    file_list.append(os.path.join(root, file))
                    # file_list.append(file)
        # return [os.path.basename(file) for file in file_list]
        return file_list
            
    def update_button_states(self):
        selected_items = self.file_list.selectedItems()
        num_selected = len(selected_items)
        if num_selected == 0:
            selected_index = -1
            self.open_button.setEnabled(False)
            self.rename_button.setEnabled(False)
        elif num_selected == 1:
            selected_index =self.file_list.currentRow()
            self.open_button.setEnabled(True)
            self.rename_button.setEnabled(True)
        else:
            selected_index = self.file_list.currentRow()
            self.open_button.setEnabled(False)
            self.rename_button.setEnabled(True)
        if selected_index != -1:
            self.full_path.setText(self.full_paths[selected_index])
        # Disable "Open" and "Rename" buttons if the file list is empty
        self.open_button.setEnabled(len(self.file_list) > 0)
        self.rename_button.setEnabled(len(self.file_list) > 0)   
    #Open Selected File
    def open_selected_file_location(self):
        selected_index = self.file_list.currentRow()
        if selected_index != -1:
            file_path = self.full_paths[selected_index]
            import os
            import platform
            import subprocess
            if platform.system() == 'Windows':
                # os.startfile(os.path.dirname(file_path))
                os.startfile(os.path.dirname(file_path),'explore','/select') #Locate and Open
                # os.startfile(file_path,'explore') #Error
                # subprocess.call(['explorer', '/select,', file_path])
            elif platform.system() == 'Darwin':  # macOS
                subprocess.call(('open', os.path.dirname(file_path)))
            else:  # Linux
                # import subprocess
                subprocess.call(('xdg-open', os.path.dirname(file_path)))

    def rename_file(self):
        # invoke Rename Form
        rename_form = RenameForm(self)
        
        # Show the form
        rename_form.show()
        
        # Connect the rename signal to the parent form
        rename_form.accepted.connect(self.rename_file_accepted)
    def rename_file_accepted(self):
        # Close the RenameForm
        self.rename_form.close()
    
class RenameForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rename File")
        self.setGeometry(200, 200, 300, 200)
        
        # Create the controls
        self.list_file2 = QListWidget(self)
        
        # Add the selected items from the main form to the list
        selected_items = self.parent().file_list.selectedItems()
        for item in selected_items:
            self.list_file2.addItem(item.text())
        
        # Create the radio buttons for "Rename" and "Add"
        self.rename_radio = QRadioButton("Rename", self)
        self.add_radio = QRadioButton("Add", self)
        self.rename_radio.setChecked(True)
        
        # Connect the signals to the slots
        self.rename_radio.toggled.connect(self.toggle_rename)
        self.add_radio.toggled.connect(self.toggle_add)
        
        # Create the layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.list_file2)
        layout.addWidget(self.rename_radio)
        layout.addWidget(self.add_radio)
        
    def toggle_rename(self, checked):
        if checked:
            self.add_radio.setChecked(False)
            if self.list_file2.count() == 1:
                self.rename_radio.setEnabled(True)
            else:
                self.rename_radio.setEnabled(False)
            # Enable/disable the controls related to renaming
            # ...
    
    def toggle_add(self, checked):
        if checked:
            self.rename_radio.setChecked(False)
            # Enable/disable the controls related to adding
            # ...
    
    def rename_file(self):
        # Get the selected file path from the parent form
        selected_index = self.parent().file_list.currentRow()
        if selected_index != -1:
            selected_path = self.parent().full_paths[selected_index]
            
            # Get the new name from the input field
            new_name = self.new_name_input.text()
            
            # Rename the file
            try:
                os.rename(selected_path, os.path.join(os.path.dirname(selected_path), new_name))
                QMessageBox.information(self, "Success", "File renamed successfully!")
            except FileNotFoundError:
                QMessageBox.critical(self, "Error", "File not found!")
            except PermissionError:
                QMessageBox.critical(self, "Error", "Permission denied!")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
            
            # Close the form
            self.close()
    
    def rename_file_accepted(self):
        # Perform the rename operation
        self.rename_file()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = FileSearchForm()
    form.show()
    sys.exit(app.exec())