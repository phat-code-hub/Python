# main.py
import sys
from PySide6.QtWidgets import QApplication
from ui_main import CheckForm,FileSearch ,FileSearchHandler
from actions import check_registration

def main():
    app = QApplication(sys.argv)
    form0=FileSearch()
    is_OK = check_registration(form0)
    form = FileSearchHandler() if is_OK else CheckForm()
    form0.close()
    form.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
