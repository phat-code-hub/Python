# main.py
import sys
from pc_system import PCSettings
from PySide6.QtWidgets import QApplication
from ui_main import InitInfo,CheckForm ,FileSearchHandler
from actions import check_registration
def main():
    app = QApplication(sys.argv)
    is_OK = check_registration(InitInfo())
    form = FileSearchHandler() if is_OK else CheckForm()
    form.show()
    sys.exit(app.exec())
if __name__ == "__main__":
    main()