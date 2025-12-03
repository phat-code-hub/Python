# main.py
import sys
from PySide6.QtWidgets import QApplication
from ui_main import CheckForm, FileSearchHandler
from actions import check_registration

def main():
    app = QApplication(sys.argv)
    is_OK = check_registration()
    form = FileSearchHandler() if is_OK else CheckForm()
    form.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
