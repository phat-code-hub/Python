# actions.py
#--------------------------------------------------------------------------------------
import os
import openpyxl
import platform
import ui_main
import locale
import media_view
from view_txt  import *

# from media_view import *
from languages import *
from PySide6.QtWidgets import (QLabel,QWidget,QVBoxLayout,QListWidgetItem,
                                QMessageBox,QFileDialog,
                                QLineEdit,QApplication)
from PySide6.QtCore import Qt,QUrl
from PySide6.QtGui import QFontMetrics,QDesktopServices,QPixmap,QImageReader 
# from media_view import main_media,clear_preview
#--------------------------------------------------------------------------------------
def PC_Info(self):
    system = platform.system()

    # Detect OS
    if system == "Windows":
        os_name = "WIN"
        lang, _ = locale.getdefaultlocale()
        lang_code = lang or "en_US"

    elif system == "Darwin":  # macOS
        os_name = "MAC"
        lang_code = os.environ.get("LANG", "")
        lang_code = lang_code.split(".")[0] if "." in lang_code else lang_code

        if not lang_code:
            lang_code, _ = locale.getdefaultlocale()

    elif system == "Linux":
        os_name = "LINUX"
        lang_code = os.environ.get("LANG", "")
        lang_code = lang_code.split(".")[0] if "." in lang_code else lang_code

        if not lang_code:
            lang_code, _ = locale.getdefaultlocale()
    else:
        os_name = "UNKNOWN"
        lang_code = "en_US"

    return os_name, MAPPING.get(lang_code, "English")
#--------------------------------------------------------------------------------------
def check_registration(self): #For UnitFrom
    passed = False
    # Windows
    if self.OS == "WIN":
        import winreg
        try:
            winreg.OpenKey(winreg.HKEY_CURRENT_USER,f"Software\\{self.REG_KEY}")
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,f"Software\\{self.REG_KEY}")
            is_passed = winreg.QueryValueEx(reg_key, "Passed")
            if is_passed[0] == "True":
                self.LANG = winreg.QueryValueEx(reg_key, "Language")
                self.PATH = winreg.QueryValueEx(reg_key, "SearchPath")
                passed = True
                winreg.CloseKey(reg_key)   
        except Exception as e:
            pass
    # MAC
    elif self.OS == "MAC":
        from pathlib import Path
        import plistlib
        plist_path = Path("~/Library/Preferences").expanduser() / f"{self.REG_KEY}.plist"
        if  plist_path.exists():
            with open(plist_path, "rb") as f:
                data = plistlib.load(f)
                if data.get("Passed") == "True":
                    self.LANG = data.get("Language")
                    self.PATH = data.get("SearchPath")
                    passed = True
    # Linux
    elif self.OS == "LINUX":
        import json
        file = Path("~/.config").expanduser() / self.REG_KEY / "settings.json"
        if file.exists():
            with open(file, "r") as f:
                data = json.load(f)
                if data.get("Passed") == "True":
                    self.LANG = data.get("Language")
                    self.PATH = data.get("SearchPath")
                    passed = True
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
    if "0" in password:
        self.close()
        # ui_main.CheckForm().close()
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
    lang,path = "English",os.path.expanduser("~")
    # Windows
    if self.OS =="WIN":
        import winreg
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, f"Software\\{self.REG_KEY}")
            language,default_path= winreg.QueryValueEx(reg_key, "Language"), winreg.QueryValueEx(reg_key, "SearchPath")
            winreg.CloseKey(reg_key)
            lang,path = language[0],default_path[0]
        except FileNotFoundError:
            pass
    # MAC
    elif self.OS == "MAC":
        from pathlib import Path
        import plistlib
        plist_path = Path("~/Library/Preferences").expanduser() / f"{self.REG_KEY}.plist"
        if  plist_path.exists():
            with open(plist_path, "rb") as f:
                data = plistlib.load(f)
                lang,path = data.get("Language"),data.get("SearchPath")
        else:
            pass
    # Linux
    else:
        import json
        file = Path("~/.config").expanduser() /f"{self.REG_KEY} / settings.json"
        if file.exists():
            with open(file, "r") as f:
                data = json.load(f)
                lang,path = data.get("Language"),data.get("SearchPath")
        else:
            pass
    return lang,path
#----------------------------------------------------------------
def create_registry(self):
    data = {
            "Language": "English",
            "SearchPath": "~/Documents",
            "Passed": "True"
            }
    # Windows
    if self.OS == "WIN":
        import winreg
        reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\{self.REG_KEY}")
        winreg.SetValueEx(reg_key, "Language", 0, winreg.REG_SZ,"English")
        winreg.SetValueEx(reg_key, "SearchPath", 0, winreg.REG_SZ, os.path.expanduser("~")+"\\Documents")
        winreg.SetValueEx(reg_key, "Passed", 0, winreg.REG_SZ, "True")
        winreg.CloseKey(reg_key)
    # MAC
    elif self.OS == "MAC":
        # macOS: use plist
        from pathlib import Path
        import plistlib
        plist_path = Path("~/Library/Preferences").expanduser() / f"{self.REG_KEY.lower()}.plist"
        try:
            with open(plist_path, "wb") as f:
                plistlib.dump(data, f)
        except Exception as e:
            print("macOS plist save error:", e)
    # Linux
    else:
        import json
        config_dir = Path("~/.config").expanduser() / self.REG_KEY
        config_dir.mkdir(parents=True, exist_ok=True)
        
        file = Path("~/.config").expanduser() / f"{self.REG_KEY} / settings.json"
        try:
            with file.open("w", encoding="utf-8") as f:
                json.dump(data, f)
        except Exception as e:
                print("Linux save error:", e)
#----------------------------------------------------------------   
def saved_to_registry(self):
        data = {
                "Language": self.language,
                "SearchPath": self.search_path,
                "Passed": "True"
            }
        # Windows
        if self.OS == "WIN":
            import winreg
            reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\{self.REG_KEY}")
            winreg.SetValueEx(reg_key, "Language", 0, winreg.REG_SZ, self.language)
            winreg.SetValueEx(reg_key, "SearchPath", 0, winreg.REG_SZ, self.search_path)
            winreg.SetValueEx(reg_key, "Passed", 0, winreg.REG_SZ, "True")
            winreg.CloseKey(reg_key)
        # MAC
        elif self.OS == "MAC":
            from pathlib import Path
            import plistlib
            plist_path = Path("~/Library/Preferences").expanduser() / f"{self.REG_KEY}.plist"
            try:
                with open(plist_path, "wb") as f:
                    plistlib.dump(data, f)
            except Exception as e:
                print("macOS save error:", e)
        # Linux
        else:
            import json
            file = Path("~/.config").expanduser() / f"{self.REG_KEY} / settings.json"
            data = {
                "Language": "English",
                "SearchPath": "~/Documents",
                "Passed": "True"
                }
            try:
                with file.open("w", encoding="utf-8") as f:
                    json.dump(data, f)
            except Exception as e:
                    print("Linux save error:", e)
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

# def on_file_selected(self, current, previous=None):
        # self.info.setTextInteractionFlags(self.info.textInteractionFlags() | Qt.TextSelectableByMouse)
        # fm = QFontMetrics(self.info.font())
        # """Routing: decide how to preview a selected file and whether to show media controls."""
        # try:
        #     if current is None:
        #         return
        #     file_index = self.file_list.currentRow()
        #     # get absolute path from item data if present
        #     filename = current.data(Qt.UserRole) or current.text()
        #     if not filename:
        #         filename = current.text()
        #     file_path = os.path.dirname(self.found_files[file_index]).lower()
        #     file_path = file_path.removeprefix(self.search_path).removeprefix(os.path.sep)
        #     foundFolders =[i.text().lower() for i in self.folder_list.findItems("",Qt.MatchContains)]
        #     index = list(filter(lambda i:foundFolders[i] in file_path,range(len(foundFolders))))
        #     if index:
        #         self.folder_list.setCurrentRow(index[0])
                    
            # # try to resolve relative path against search_path
            # if not os.path.isabs(filename) and getattr(self, "search_path", None):
            #     candidate = os.path.join(self.search_path, filepath)
            #     if os.path.exists(candidate):
            #         filepath = candidate

            # if not os.path.exists(filepath):
            #     self.text_view.setText("[File not found]")
            #     self.preview_top.setCurrentWidget(self.text_view)
            #     self.preview_bottom.setVisible(False)
            #     return
            #Get selected file folder path
            # file_path = file_path.removeprefix(self.search_path).removeprefix(os.path.sep)
            # foundFolders =[i.text().lower() for i in self.folder_list.findItems("",Qt.MatchContains)]
            # index = list(filter(lambda i:foundFolders[i] in file_path,range(len(foundFolders))))
            # if index:
            #     self.folder_list.setCurrentRow(index[0])
            
            # print(filepath)
            # fpath, ext = os.path.splitext(file_path)
            # ext = ext.lower()
            # print(fpath,ext)

            # Media: audio/video -> thumbnail top + enable bottom controls
        #     if ext in getattr(self, "audio_exts", set()) or ext in getattr(self, "video_exts", set()):
        #         media_view.show_media_thumbnail(self, filepath)
        #         media_view.prepare_media_player(self, filepath)
        #         # media_view.prepare_media_player will show preview_bottom
        #         return

        #     # Text/document/images handled by txt_view functions
        #     if ext in getattr(self, "readable_text_ext", set()) or ext in (".txt", ".md", ".py", ".log", ".json"):
        #         txt_view.preview_text_file(self, filepath)
        #         self.preview_bottom.setVisible(False)
        #         return

        #     # images (use QImageReader supported formats)
        #     try:
        #         from PySide6.QtGui import QImageReader
        #         supported_exts = {("." + bytes(fmt).decode()).lower() for fmt in QImageReader.supportedImageFormats()}
        #     except Exception:
        #         supported_exts = {".png", ".jpg", ".jpeg", ".bmp", ".gif"}

        #     if ext in supported_exts:
        #         txt_view.preview_image_file(self, filepath)
        #         self.preview_bottom.setVisible(False)
        #         return

        #     # docx / xlsx
        #     if ext == ".docx" or ext == ".xlsx":
        #         txt_view.preview_document_file(self, filepath)
        #         self.preview_bottom.setVisible(False)
        #         return

        #     # CAD placeholder
        #     if ext in getattr(self, "readable_cad_ext", set()):
        #         self.cad_view.setText(f"CAD preview not available for {os.path.basename(filepath)}")
        #         self.preview_top.setCurrentWidget(self.cad_view)
        #         self.preview_bottom.setVisible(False)
        #         return

        #     # fallback
        #     self.text_view.setText("[Unsupported file type]")
        #     self.preview_top.setCurrentWidget(self.text_view)
        #     self.preview_bottom.setVisible(False)

        # except Exception as e:
        #     print("Preview routing error:", e)
        #     self.text_view.setText("[Preview error]")
        #     self.preview_top.setCurrentWidget(self.text_view)
        #     self.preview_bottom.setVisible(False)

#----------------------------------------------------------------
def show_file_info(self,current):
    self.info.setTextInteractionFlags(self.info.textInteractionFlags() | Qt.TextSelectableByMouse)
    fm = QFontMetrics(self.info.font())
    try:
        if current is None:
            self.info.setText("")
            return
        file_index = self.file_list.currentRow()
        filename = current.data(Qt.UserRole) or current.text()
        if not filename:
            filename = current.text()
        #Get file full path
        file_path = os.path.dirname(self.found_files[file_index]).lower()
        file_path = file_path.removeprefix(self.search_path).removeprefix(os.path.sep)
        foundFolders =[i.text().lower() for i in self.folder_list.findItems("",Qt.MatchContains)]
        index = list(filter(lambda i:foundFolders[i] in file_path,range(len(foundFolders))))
        if index:
            self.folder_list.setCurrentRow(index[0])
        full_path =self.found_files[self.file_list.row(current)]
        #Get file name
        short_path =fm.elidedText(self.found_files[self.file_list.row(current)],Qt.ElideMiddle,500)
        self.info.setText(short_path)
        preview_file(self,full_path)
    except Exception as e:
            print("Preview routing error:", e)
            self.text_view.setText("[Preview error]")
            self.preview_top.setCurrentWidget(self.text_view)
            self.preview_bottom.setVisible(False)
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
            item = QListWidgetItem(file)
            item.setData(Qt.UserRole, file)
            self.file_list.addItem(item)
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
                if dirname.startswith(os.path.sep) and self.OS != "MAC":
                    partial_path = partial_path[1:]
                    dirname = dirname[1:]
                filtered_folders.add(dirname)
    return filtered_files, filtered_folders
#-----------------------------------------------------------------------
def search_files(self,source = 1):
    import re
    reset_data(self)
    keyword = self.search_input.text().strip()
    self.info.setText(self.label[self.language]["message"])
    if keyword :
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
#----------------------------------------------------------------------
def resizeEvent(self, event):
    if hasattr(self, "original_pixmap") and self.original_pixmap:
        self.update_scaled_image()
    super().resizeEvent(event)
#----------------------------------------------------------------------
def preview_file(self,path):
    ext = os.path.splitext(path)[1].lower()
    # ord_list =[ i  for i,(k,v) in enumerate(EXTENSIONS.items()) if ext in v] or [0]# Index of file in EXTENSIONS
    ord_list =[ i  for i,(k,v) in enumerate(self.ext_type.items()) if ext in v] or [0]# Index of file in EXTENSIONS
    if ord_list[0] == 0 :
        # self.preview.setText("[Unsupported file type]")
        clear_layout = None  # placeholder; top already set by clear_preview
        return
    else:
        ord = ord_list[0]
    # filetype = [k for k,v in VIEW_EXT.items() if ord in v][0]#Type to choose Preview code 
    filetype = [k.lower() for k,v in self.filetype.items() if ord in v][0]#Type to choose Preview code 
    # print(ext,filetype,ord)
    if filetype == "text": #Include image types
        main_text(self,path,ext,ord) # type: ignore
        return
    # if filetype == "cad":
    #     main_txt(self,path,ext,ord) # type: ignore
    #     return
    # if filetype == "prog":
    #     main_txt(self,path,ext,ord) # type: ignore
    #     return
    # elif filetype == "media":
    #     main_media(self,path,ext,ord) # type: ignore
    #     return
    # else:
    #     self.preview.setText("[Unsupported file type]")
    #     return
        
    # IMAGE
    # if filetype == "image":
    #     # Ensure preview has a layout
    #     if self.preview.layout() is None:
    #         self.preview.setLayout(QVBoxLayout())

    #     # Clear any previous top widgets
    #     # (clear_preview already cleaned everything, but keep safe)
    #     for child in self.preview.findChildren(QWidget):
    #         child.setParent(None)

    #     # Create a QLabel inside preview to show the image and store original pixmap
    #     img_label = QLabel(self.preview)
    #     img_label.setAlignment(Qt.AlignCenter)
    #     img_label.setContentsMargins(0, 0, 0, 0)
    #     img_label.setSizePolicy(img_label.sizePolicy().Expanding, img_label.sizePolicy().Expanding)

    #     # load image
    #     reader = QImageReader(path)
    #     qimg = reader.read()
    #     if qimg.isNull():
    #         # fallback to unsupported text
    #         self.preview.layout().addWidget(QLabel("[Cannot display image]"))
    #         return

    #     pixmap = QPixmap.fromImage(qimg)
    #     self.original_pixmap = pixmap  # for resizeEvent handling

    #     # scale to available size
    #     w = max(1, self.preview.width() - 10)
    #     h = max(1, self.preview.height() - 10)
    #     scaled = pixmap.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    #     # img_label.setPixmap(scaled)
    #     self.preview.setPixmap(scaled)
        
    #     self.preview.layout().addWidget(img_label)
    #     return
    
    # OTHER / UNSUPPORTED
    # Leave default preview area (clear_preview put default label)
    return

# Note: removed the prior "clear_preview" definition that treated preview as QLabel.
# The robust clear_preview() from media_view is used everywhere now.