import platform
import os
import locale
import json
import plistlib
from  languages import REG_KEY,MAPPING
from pathlib import Path

class PCSettings:
    def __init__(self) :
        self.REG_KEY = REG_KEY
        self.WIN_KEY = f"Software\\{self.REG_KEY}"
        self.MAC_KEY = f"com.mycompany.{self.REG_KEY.lower()}" # plist file name
        self.LINUX_KEY = f"/etc/{self.REG_KEY.lower()}" # ~/.config/myapp/
        self.OS,self.locale= self.get_os_and_language()
        # self.app_name = app_name
        # self.mac_app_id = mac_app_id
        # self.linux_dir = linux_dir

        # auto-set language
        # self.PC_locale = self.detect_language()
    #-----------------------------------------------------
    def get_os_and_language(self):
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
    #-----------------------------------------------------
    # # 1. Detect OS
    # def get_os(self):
    #     os = platform.system()
    #     if os == "Windows":
    #         return "WIN"
    #     elif os == "Darwin":
    #         return "MAC"
    #     else:
    #         return "LINUX"
        
    # #----------------------------------------------------
    # # 2. Detect DEFAULT locale language
    # def normalize_language(code):
    #     return MAPPING.get(code, "English")  # default
    # #-------------------------------------------------------
    # def detect_language(self):
    #     if self.OS in ["Darwin", "Linux"]:
    #         lang = os.environ.get("LANG", "")
    #         # Example returns: "en_US.UTF-8"
    #         if "." in lang:
    #             prefix = lang.split(".")[0]
    #         return self.normalize_language(prefix)
    #     try:
    #         lang, _ = locale.getdefaultlocale()
    #         return self.normalize_language(lang) or "English"
    #     except:
    #         return "English"

    # =====================================================
    # 3. PUBLIC: Save / Load name + age
    # =====================================================
    def save(self, name, age):
        if self.os == "Windows":
            self._save_windows(name, age)
        elif self.os == "Darwin":
            self._save_macos(name, age)
        elif self.os == "Linux":
            self._save_linux(name, age)

    def load(self):
        if self.os == "Windows":
            return self._load_windows()
        elif self.os == "Darwin":
            return self._load_macos()
        elif self.os == "Linux":
            return self._load_linux()
        return None, None

    # =====================================================
    # WINDOWS — Registry
    # =====================================================
    def _save_windows(self, name, age):
        import winreg
        key_path = f"Software\\{self.app_name}"

        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
            winreg.SetValueEx(key, "name", 0, winreg.REG_SZ, name)
            winreg.SetValueEx(key, "age", 0, winreg.REG_SZ, str(age))
            winreg.CloseKey(key)
        except Exception as e:
            print("Windows save error:", e)

    def _load_windows(self):
        import winreg
        key_path = f"Software\\{self.app_name}"

        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path)
            name = winreg.QueryValueEx(key, "name")[0]
            age = winreg.QueryValueEx(key, "age")[0]
            winreg.CloseKey(key)
            return name, age
        except:
            return None, None

    # =====================================================
    # macOS — plist in ~/Library/Preferences/
    # =====================================================
    def _save_macos(self, name, age):
        plist_path = Path("~/Library/Preferences").expanduser() / f"{self.mac_app_id}.plist"
        data = {"name": name, "age": age}

        try:
            with open(plist_path, "wb") as f:
                plistlib.dump(data, f)
        except Exception as e:
            print("macOS save error:", e)

    def _load_macos(self):
        plist_path = Path("~/Library/Preferences").expanduser() / f"{self.mac_app_id}.plist"
        if not plist_path.exists():
            return None, None

        try:
            with open(plist_path, "rb") as f:
                data = plistlib.load(f)
            return data.get("name"), data.get("age")
        except:
            return None, None

    # =====================================================
    # LINUX — ~/.config/<appname>/settings.json
    # =====================================================
    def _save_linux(self, name, age):
        config_dir = Path("~/.config").expanduser() / self.linux_dir
        config_dir.mkdir(parents=True, exist_ok=True)

        file = config_dir / "settings.json"
        data = {"name": name, "age": age}

        try:
            with open(file, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print("Linux save error:", e)

    def _load_linux(self):
        file = Path("~/.config").expanduser() / self.linux_dir / "settings.json"
        if not file.exists():
            return None, None

        try:
            with open(file, "r") as f:
                data = json.load(f)
            return data.get("name"), data.get("age")
        except:
            return None, None
