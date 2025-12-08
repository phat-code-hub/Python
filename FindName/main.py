# main.py
import sys
from pc_system import PCSettings
from PySide6.QtWidgets import QApplication
from ui_main import CheckForm ,FileSearchHandler
from actions import check_registration
def main():
    # app = QApplication(sys.argv)
    # # is_OK = check_registration(InitInfo())
    # is_OK = check_registration(pc_system())
    # form = FileSearchHandler() if is_OK else CheckForm()
    # form.show()
    # sys.exit(app.exec())
    infos = PCSettings()
    print(infos.OS)
    print(infos.locale)
if __name__ == "__main__":
    main()