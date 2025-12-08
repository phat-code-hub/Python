# actions.py
#--------------------------------------------------------------------------------------
import os
import sys
import openpyxl
import platform
import ui_main
from  languages import ERROR
from PySide6.QtWidgets import QMessageBox,QFileDialog,QLineEdit,QApplication
from PySide6.QtCore import Qt,QUrl
from languages import *
from PySide6.QtGui import QFontMetrics,QDesktopServices,QPixmap,QImageReader 

#--------------------------------------------------------------------------------------
def check_PC(self):
    if platform.system() == "Windows":
        os = "WIN"
    elif platform.system() == "Darwin":
        os = "MAC"
    else:
        os = "LINUX"
    lang = get_system_language(self,os)
    return os, lang
#--------------------------------------------------------------------------------------
def normalize_lang(code: str) -> str:
    """Convert Windows style (en_US) to BCP-47 (en-US)."""
    if not code:
        return None
    return code.replace("_", "-")
#--------------------------------------------------------------------------------------
def lang_to_name(lang_code: str) -> str:
    """Map language code to readable name."""
    mapping = {
        "en-US": "English",
        "ja-JP": "Japanese",
        "vi-VN": "Vietnamese",
    }
    return mapping.get(lang_code, lang_code)  # fallback → return original code
#--------------------------------------------------------------------------------------
def  get_system_language(self,os ="WIN") -> str:
    import ctypes,locale,plistlib,subprocess
    if os == "WIN":
        try:
            lang_id = ctypes.windll.kernel32.GetUserDefaultUILanguage()
            lang = normalize_lang(locale.windows_locale.get(lang_id))
            return lang_to_name(lang)
        except Exception:
            pass

        try:
            lang = normalize_lang(locale.getdefaultlocale()[0])
            return lang_to_name(lang)
        except Exception:
            pass
    elif os == "MAC":
        try:
            plist_path = os.path.expanduser(
                "~/Library/Preferences/.GlobalPreferences.plist"
            )
            with open(plist_path, "rb") as f:
                plist = plistlib.load(f)
            lang = normalize_lang(plist.get("AppleLanguages", [None])[0])
            return lang_to_name(lang)
        except Exception:
            pass

        try:
            result = subprocess.run(
                ["defaults", "read", "-g", "AppleLanguages"],
                capture_output=True, text=True
            )
            lines = result.stdout.strip().split("\n")
            if lines:
                lang = normalize_lang(lines[0].strip().strip('"'))
                return lang_to_name(lang)
        except Exception:
            pass
    else: #LINUX
        try:
            lang = normalize_lang(locale.getdefaultlocale()[0])
            return lang_to_name(lang)
        except Exception:
            return  None
    #--------------------------------------------------------------------------------------
def check_registration(self): #For UnitFrom
    passed = False
    if self.OS == "WIN":
        import winreg
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, f"Software\\{self.REG_KEY}")
            is_passed = winreg.QueryValueEx(reg_key, "Passed")
            if is_passed[0] == "True":
                passed = True
                self.LANG = winreg.QueryValueEx(reg_key, "Language")
                self.PATH = winreg.QueryValueEx(reg_key, "SearchPath")
            winreg.CloseKey(reg_key)
        except Exception:
            pass
    elif self.OS == "MAC":
        pass
    else: #self.OS = "LINUX"
        pass
    return passed
#--------------------------------------------------------------------------------------
def toggle_password_visibility(self,state):
    if state == Qt.Checked:
        self.password_input.setEchoMode(QLineEdit.Normal)
    else:
        self.password_input.setEchoMode(QLineEdit.Password)
#--------------------------------------------------------------------------------------
def check_license(self,password):
    import re
    # if re.match(r"^0\w*",password):
    # if ("11" in password) and ("3" in password):
    if "0" in password:
        self.close()
        create_registry(self)
        ui_main.FileSearchHandler().show()
    else:
        QMessageBox.critical(None, ERROR[self.LANG]["Title"],ERROR[self.LANG]["Message"])
        self.close()
#--------------------------------------------------------------------------------------
def move_to_center(self):
        # Get the screen geometry of the primary screen
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        # Get the geometry of the window
        window_geometry = self.frameGeometry()

        # Move center of window geometry to center of screen
        window_geometry.moveCenter(screen_geometry.center())

        # Move the top-left of the window to match the new center
        self.move(window_geometry.topLeft())

#--------------------------------------------------------------------------------------
def get_registry_values(self):
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
            # language = self.defaults.stringForKey_("Language")
            # default_path = self.defaults.stringForKey_("SearchPath")
            # language = "English"
            # default_path = "~"
            # return language, default_path
            return "English",os.path.expanduser("~")
        else:
            return "English",os.path.expanduser("~")
#----------------------------------------------------------------
def create_registry(self):
    from pathlib import Path
    if self.OS == "WIN":
        import winreg
        reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\{self.REG_KEY}")
        winreg.SetValueEx(reg_key, "Language", 0, winreg.REG_SZ,"English")
        winreg.SetValueEx(reg_key, "SearchPath", 0, winreg.REG_SZ, os.path.expanduser("~")+"\\Documents")
        winreg.SetValueEx(reg_key, "Passed", 0, winreg.REG_SZ, "True")
        winreg.CloseKey(reg_key)
    elif self.OS == "MAC":
        # macOS: use plist
        plist_path = Path("~/Library/Preferences").expanduser() / f"{self.app_id}.plist"
        data = {"a": a, "b": b}

        try:
            with open(plist_path, "wb") as f:
                plistlib.dump(data, f)
        except Exception as e:
            print("macOS plist save error:", e)
    else:
        pass
#----------------------------------------------------------------   
def saved_to_registry(self):
        if self.OS == "WIN":
            import winreg
            reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\{self.REG_KEY}")
            winreg.SetValueEx(reg_key, "Language", 0, winreg.REG_SZ, self.language)
            winreg.SetValueEx(reg_key, "SearchPath", 0, winreg.REG_SZ, self.search_path)
            winreg.SetValueEx(reg_key, "Passed", 0, winreg.REG_SZ, "True")
            winreg.CloseKey(reg_key)
        elif self.OS == "MAC":
            # macOS: use NSUserDefaults
            pass
        else:
            pass
#----------------------------------------------------------------
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

def open_file_dialog(self):
    select_folder = self.label[self.language]["SelectFolder"]
    folder_path = QFileDialog.getExistingDirectory(self, select_folder,self.search_path)
    if folder_path:
        self.search_path = folder_path
        self.search_folder_path.setText(folder_path)
        search_files(self)
    else:
        show_empty(self)
#----------------------------------------------------------------
#Search from search pattern
def change_search_source(self,source =1):
    if self.search_input.text().strip() :
        if source == 2:
            if self.folder_list.currentItem() is None:
                return
            else:
                self.search_path = os.path.join(self.search_path,self.folder_list.selectedItems()[0].text())
        self.search_folder_path.setText(self.search_path)
        if self.init:
            self.init = False
        if not self.init:
            self.info.setText(self.label[self.language]["message"])
        # start_process(self)
        search_files(self,source = source)
    else:
        if not self.init:
            show_empty(self)
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
        #Get file full path
        file_path = os.path.dirname(self.found_files[file_index]).lower()
        file_path = file_path.removeprefix(self.search_path).removeprefix(os.path.sep)
        foundFolders =[i.text().lower() for i in self.folder_list.findItems("",Qt.MatchContains)]
        index = list(filter(lambda i:foundFolders[i] in file_path,range(len(foundFolders))))
        if index:
            self.folder_list.setCurrentRow(index[0])
        full_path =self.found_files[self.file_list.row(current)]
        #Get file name
        short_path =fm.elidedText(self.found_files[self.file_list.row(current)],Qt.ElideMiddle,600)
        self.info.setText(short_path)
        preview_file(self,full_path)
    else:
        self.info.setText("")
#-----------------------------------------------------------------------   
def open_file_location(self,item):
    import subprocess
    filepath = os.path.dirname(self.found_files[self.file_list.row(item)])
    try:
        if self.OS == "WIN":
        # if sys.platform.startswith("win"):
            QDesktopServices.openUrl(QUrl.fromLocalFile(filepath))
        elif self.OS == "MAC":
            subprocess.run(["open", filepath])
        else:  # Linux and others
            subprocess.run(["xdg-open", filepath])
    except Exception as e:
        pass
        # QMessageBox.critical(self, "Error", f"{ERROR[self.language]["Open"]}:\n{e}")
#-----------------------------------------------------------------------   
def change_tooltips(self):
    self.search_folder_change.setToolTip(HINT["Dialog"][self.language])
    self.file_type_combo.setToolTip(HINT["Type"][self.language])
    self.folder_list.setToolTip(HINT["Folder"][self.language])
    self.file_list.setToolTip(HINT["File"][self.language])
    self.search_input.setToolTip(HINT["Search"][self.language])
    logic = HINT["Logic"][self.language] 
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
        show_data(self)
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
def start_process(self):
    self.elapsed = 0
    # Show popup
    self.popup.update_time(0)
    self.popup.show()
    self.timer.start(0)
#-----------------------------------------------------------------------
def update_time_counter(self):
    self.elapsed += 1
    self.popup.update_time(self.elapsed)

    if self.elapsed >= self.limit_timer:
        self.stop_all()
#-----------------------------------------------------------------------      

def stop_all(self):
    self.timer.stop()
    self.popup.close()
#-----------------------------------------------------------------------
def search_files(self,source = 1):
    import re
    reset_data(self)
    keyword = self.search_input.text().strip()
    self.info.setText(self.label[self.language]["message"])
    if keyword :
        # update_time_counter(self)
        self.init = False
        self.keywords = re.split(r'[ ,;:/|]+', self.search_input.text().strip().lower())
        if  len(self.keywords)==1 and self.keywords[0] in ["*","*.*","."]:
            for root, dirs, files in os.walk(self.search_path):
                for name in files + dirs:
                    if os.path.isfile(os.path.join(root, name)):
                                self.found_files.append(os.path.join(root, name))
                                self.found_folders.add(os.path.dirname(os.path.join(root, name)))
                    elif os.path.isdir(os.path.join(root, name)):
                        self.found_folders.add(os.path.join(root, name))
        else:
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
        reset_data(self)
        if not self.init:
            show_empty(self)
    stop_all(self)
#----------------------------------------------------------------------
def clear_preview(self):
    self.preview.clear()
    self.preview.setText("")
#---------------------------------------------------------------------
def preview_file(self,path)    :
    ext = os.path.splitext(path)[1].lower()
    # Check supported types
    supported_ext = [b"." + fmt for fmt in QImageReader.supportedImageFormats()]
    clear_preview(self)
    if ext.encode() in supported_ext:
        preview_image(self, path)
    elif ext in TEXT_EXT:
        preview_text(self,path)
    elif ext == ".docx":
        preview_word(self,path)
    elif ext == ".xlsx":
        preview_excel(self,path)
    elif ext in CAD_EXT:
        self.preview.setText("[Cannot preview CAD file]")
    else:
        self.preview.setText("[Unsupported file type]")
#----------------------------------------------------------------------
def preview_image(self, filepath):
        pixmap = QPixmap(filepath)
        if pixmap.isNull():
            self.preview.setText("[Cannot load image]")
        else:
            self.original_pixmap = pixmap   # ← store original full-quality image
            update_scaled_image(self)
#----------------------------------------------------------------------
def update_scaled_image(self):
        if self.original_pixmap is None:
            return
        scaled = self.original_pixmap.scaled(
            self.preview.width(),
            self.preview.height(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation   # ← smoother resize!
        )
        self.preview.setPixmap(scaled)
#----------------------------------------------------------------------

def preview_text(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            self.preview.setText(content)
        except:
            self.preview.setText("[Cannot read text file]")
#----------------------------------------------------------------------
def preview_word(self, filepath,max_lines=10):
        from docx import Document
        from docx.shared import Pt
        try:
            doc = Document(filepath)
            text =""
            for paragraph in doc.paragraphs:
                for run in paragraph.runs:
                    text += run.text +" "
                text +="\n"
                if max_lines and len(text.splitlines()) >= max_lines:
                    break
            text = text.rstrip()  # Remove trailing newline character
            self.preview.setText(text.rstrip() if text else "[Empty Word document]")
            self.preview.setAlignment(Qt.AlignLeft | Qt.AlignTop)  # Set alignment to left and top
            self.preview.setTextInteractionFlags(Qt.NoTextInteraction)  # Disable text interaction
        except:
            self.preview.setText("[Cannot preview Word file]")
            
            
            
            
#----------------------------------------------------------------------
def preview_excel(self, filepath, max_rows=10):
        try:
            wb = openpyxl.load_workbook(filepath, read_only=True)
            ws = wb.active
            text = ""
            for i, row in enumerate(ws.iter_rows(values_only=True)):
                text += "\t".join([str(cell) if cell is not None else "" for cell in row]) + "\n"
                if i + 1 >= max_rows:
                    break
            text = text.rstrip()  # Remove trailing newline character
            self.preview.setText(text if text else "[Empty Excel sheet]")
            self.preview.setAlignment(Qt.AlignLeft | Qt.AlignTop)  # Set alignment to left and top
            self.preview.setTextInteractionFlags(Qt.NoTextInteraction)  # Disable text interaction
        except:
            self.preview.setText("[Cannot preview Excel file]")
# -----------------------------------------
def resizeEvent(self, event):
    if hasattr(self, "original_pixmap") and self.original_pixmap:
        self.update_scaled_image()
    super().resizeEvent(event)
#----------------------------------------------------------------------