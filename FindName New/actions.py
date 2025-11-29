# actions.py
import os
import sys
import platform
import winreg
from PySide6.QtWidgets import QMessageBox,QFileDialog,QApplication
from PySide6.QtCore import Qt,QUrl
import ui_main
from languages import *
from PySide6.QtGui import QIcon,QFontMetrics,QDesktopServices
#--------------------------------------------------------------------------------------
def check_registration():
    passed = False
    if platform.system() == "Windows":
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\\FileSearch")
            is_passed = winreg.QueryValueEx(reg_key, "Passed")
            if is_passed[0] == "True":
                passed = True
        except Exception:
            pass
        winreg.CloseKey(reg_key)
    return passed
#--------------------------------------------------------------------------------------
def check_password(password):
    import re
    # if re.match(r"^0\w*",password):
    if ("11" in password) and ("3" in password):
        form = ui_main.FileSearchHandler()
        form.show()
    else:
        QMessageBox.critical(None, "Error", "Incorrect password.")
#--------------------------------------------------------------------------------------
def change_language(self):
    langs,labels,types,search =LANGUAGES,LABELS,TYPES,OPTIONS
    if self.english_radio.isChecked():
        self.language = 'English'
    elif self.japanese_radio.isChecked():
        self.language = 'Japanese'
    else:
        self.language = 'Vietnamese'
    #Update changed language to registry
    saved_to_registry(self)
    #Set the labels and combo box items based on the selected language
    self.setWindowTitle(labels[self.language]["Title"])
    self.english_radio.setText(langs[self.language]["ENG"])  
    self.japanese_radio.setText(langs[self.language]["JP"])
    self.vietnamese_radio.setText(langs[self.language]["VN"])
    self.search_folder_label.setText(labels[self.language]["SearchPath"])
    self.search_label.setText(labels[self.language]["SearchKeyword"])
    self.search_input.setPlaceholderText(self.place_holder[self.language])
    self.search_button.setText(labels[self.language]["SearchButton"])
    self.and_radio.setText(search[self.language]["AND"])
    self.or_radio.setText(search[self.language]["OR"])
    self.not_radio.setText(search[self.language]["NOT"])
    self.file_type_label.setText(labels[self.language]["FileType"])
    self.folder_label.setText(labels[self.language]["Folders"])
    self.file_label.setText(labels[self.language]["Files"])
    self.cancel_button.setText(labels[self.language]["Cancel"])
    self.info_label.setText(self.label[self.language]["Info"])
    self.info.setText("")
    self.file_type_combo.clear()
    for _ in range(len(self.type)):
        self.file_type_combo.addItem(types[_][self.language])
    change_tooltips(self)
    
#----------------------------------------------------------------   
def saved_to_registry(self):
        
        if platform.system() == "Windows":
            import winreg
            reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\{self.APP_NAME}")
            winreg.SetValueEx(reg_key, "Language", 0, winreg.REG_SZ, self.language)
            winreg.SetValueEx(reg_key, "SearchPath", 0, winreg.REG_SZ, self.search_path)
            winreg.CloseKey(reg_key)
        elif platform.system() == "Darwin":
            # macOS: use NSUserDefaults
            pass
        
#----------------------------------------------------------------
def open_file_dialog(self):
    select_folder = self.label[self.language]["SelectFolder"]
    folder_path = QFileDialog.getExistingDirectory(self, select_folder,self.search_path)
    if folder_path:
        self.search_path = folder_path
        self.search_folder_path.setText(folder_path)
        search_files(self)
    else:
        self.show_empty()
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
        search_files(self,source = source)
    else:
        if not self.init:
            self.show_empty()
#----------------------------------------------------------------
def change_type(self):
        if self.file_type_combo.currentIndex() == -1:
            self.type_index =0
        else:
            self.type_index =self.file_type_combo.currentIndex()
        self.search_type =self.ext_type[self.type_index]
        search_files(self)
#----------------------------------------------------------------
def change_logic(self):
    if self.and_radio.isChecked():
        self.logic_index = self.logics["AND"]
    elif self.or_radio.isChecked():
        self.logic_index = self.logics["OR"]
    else:
        self.logic_index = self.logics["NOT"]
    search_files(self)
#----------------------------------------------------------------
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
def change_tooltips(self):
    self.search_folder_change.setToolTip(self.hint_dialog[self.language])
    self.file_type_combo.setToolTip(self.hint_type[self.language])
    self.folder_list.setToolTip(self.hint_folder[self.language])
    self.file_list.setToolTip(self.hint_file[self.language])
    self.search_input.setToolTip(self.hint_search[self.language])
    logic = self.hint_logic[self.language] 
    self.or_radio.setToolTip(logic[0])
    self.and_radio.setToolTip(logic[1])
    self.not_radio.setToolTip(logic[2])
#----------------------------------------------------------------
def reset_data(self):
    self.keywords = ""
    self.condition = None
    self.found_files = []
    self.found_folders = set()
    self.found_files_short = []
    self.found_folders_short = set()
#-----------------------------------------------------------------------
def show_empty(self):
        reset_data(self)
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
    self.file_label.setText(self.label[self.language]["Files"]+" "+ str(self.file_list.count()))
    if len(self.found_folders)>0:
        for folder in self.found_folders_short:
            self.folder_list.addItem(folder)
    self.folder_label.setText(self.label[self.language]["Folders"]+" "+ str(self.folder_list.count()))
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
def search_files(self,source =1):
    import re
    if source == 1:
        reset_data(self)
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
                self.found_files,folders = filter_type(self)
                self.found_folders = folders.intersection(self.found_folders)
            self.filtered_files, self.filtered_folders = self.found_files, self.found_folders
            show_data(self,source)
        else:#Nothing selected 
            self.file_list.clear()
            self.folder_list.clear()
            if not self.init:
                show_empty(self)
#----------------------------------------------------------------------