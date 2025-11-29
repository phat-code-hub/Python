"""
embedded_explorer_preview.py

PySide6 app that embeds Windows Explorer (ActiveX) and uses its preview pane.
Left: folder tree
Center: file list
Right: embedded Explorer ActiveX (shows folder/file; uses Windows Preview Handler)

Requirements:
    pip install PySide6 pdf2image   # pdf2image not required but often useful elsewhere
    Run on Windows.

Notes:
- The Preview Pane appears only if Windows has a preview handler for the selected file type.
- Some file types (DWG, VWX, etc.) require their apps' preview handlers to be installed.
"""

import os
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QTreeView, QListWidget,
    QLabel, QSplitter, QMessageBox, QFileSystemModel, QPushButton
)
from PySide6.QtCore import Qt, QDir, QSize
from PySide6.QtGui import QIcon

# ActiveX container (Windows only)
try:
    from PySide6.QtAxContainer import QAxWidget
    AX_AVAILABLE = True
except Exception:
    AX_AVAILABLE = False

class ExplorerPreviewApp(QWidget):
    def __init__(self, start_folder=None):
        super().__init__()
        self.setWindowTitle("Embedded Windows Explorer + Preview Pane")
        self.resize(1200, 700)

        if start_folder is None:
            start_folder = QDir.homePath()

        # Main layout: horizontal splitter
        splitter = QSplitter(Qt.Horizontal, self)

        # Left: Folder tree
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(6, 6, 6, 6)

        self.folder_model = QFileSystemModel()
        self.folder_model.setRootPath(QDir.rootPath())
        # Only show directories in tree
        self.folder_model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot)

        self.tree = QTreeView()
        self.tree.setModel(self.folder_model)
        self.tree.setRootIndex(self.folder_model.index(QDir.rootPath()))
        self.tree.setHeaderHidden(True)
        # Expand user's home
        self.tree.expand(self.folder_model.index(start_folder))
        self.tree.clicked.connect(self.on_tree_clicked)

        left_layout.addWidget(QLabel("<b>Folders</b>"))
        left_layout.addWidget(self.tree)

        # Middle: File list
        middle_widget = QWidget()
        middle_layout = QVBoxLayout(middle_widget)
        middle_layout.setContentsMargins(6, 6, 6, 6)

        middle_layout.addWidget(QLabel("<b>Files</b>"))
        self.file_list = QListWidget()
        self.file_list.itemClicked.connect(self.on_file_clicked)
        middle_layout.addWidget(self.file_list)

        # Quick controls
        btn_layout = QHBoxLayout()
        self.open_in_explorer_btn = QPushButton("Open in external Explorer")
        self.open_in_explorer_btn.clicked.connect(self.open_in_external_explorer)
        btn_layout.addWidget(self.open_in_explorer_btn)

        self.toggle_preview_btn = QPushButton("Toggle Windows Preview Pane (Explorer)")
        self.toggle_preview_btn.clicked.connect(self.notify_preview_toggle)
        btn_layout.addWidget(self.toggle_preview_btn)

        middle_layout.addLayout(btn_layout)

        # Right: embedded Explorer ActiveX (if available) or placeholder
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(6, 6, 6, 6)
        right_layout.addWidget(QLabel("<b>Embedded Explorer (Preview Pane)</b>"))

        if AX_AVAILABLE:
            try:
                self.ax = QAxWidget("Shell.Explorer.2")  # Explorer ActiveX
                # Navigate to start folder
                # Some ActiveX hosts accept file:///
                self.ax.dynamicCall("Navigate(const QString&)", f"file:///{start_folder.replace(os.path.sep, '/')}")
                right_layout.addWidget(self.ax)
                self.ax_available = True
            except Exception as e:
                self.ax = None
                self.ax_available = False
                right_layout.addWidget(QLabel("ActiveX control failed to initialize:\n" + str(e)))
        else:
            self.ax = None
            self.ax_available = False
            right_layout.addWidget(QLabel("Qt ActiveX (QtAxContainer) is not available on this Python installation."))

        # Add panes to splitter
        splitter.addWidget(left_widget)
        splitter.addWidget(middle_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([250, 300, 650])

        # Main layout
        main_layout = QHBoxLayout(self)
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

        # Populate initial file list for start_folder
        self.current_folder = start_folder
        self.populate_file_list(start_folder)

        # Select the tree index of start folder
        idx = self.folder_model.index(start_folder)
        if idx.isValid():
            self.tree.setCurrentIndex(idx)

    def populate_file_list(self, folder_path):
        self.file_list.clear()
        try:
            files = sorted(os.listdir(folder_path))
        except Exception:
            files = []
        for f in files:
            full = os.path.join(folder_path, f)
            if os.path.isfile(full):
                self.file_list.addItem(f)
        self.current_folder = folder_path

    def on_tree_clicked(self, index):
        # Map tree click to folder path and update file list and embedded explorer
        folder_path = self.folder_model.filePath(index)
        if folder_path:
            self.populate_file_list(folder_path)
            # Navigate embedded explorer to the folder
            self.navigate_ax_to_path(folder_path)

    def on_file_clicked(self, item):
        file_name = item.text()
        full_path = os.path.join(self.current_folder, file_name)
        # Ask embedded explorer to navigate to the FILE itself so preview handler shows preview
        if os.path.exists(full_path):
            # Use file:/// URL and forward slashes
            url = f"file:///{full_path.replace(os.path.sep, '/')}"
            self.navigate_ax_to_path(url)

    def navigate_ax_to_path(self, path_or_url):
        if not self.ax_available:
            return
        try:
            # First try BrowseTo with PreviewPane flag (0x40000000) — some hosts honor it.
            # If path is a local file url, pass to Navigate
            if path_or_url.startswith("file:///"):
                # Navigate to file (so preview handler shown)
                self.ax.dynamicCall("Navigate(const QString&)", path_or_url)
            else:
                # For folder paths, try BrowseTo with flag that may enable preview pane
                # 0x40000000 is a common flag for preview pane - host dependent
                try:
                    self.ax.dynamicCall("BrowseTo(const QString&, int)", path_or_url, 0x40000000)
                except Exception:
                    # fallback to navigate using file:/// format
                    url = f"file:///{path_or_url.replace(os.path.sep, '/')}"
                    self.ax.dynamicCall("Navigate(const QString&)", url)
        except Exception as e:
            print("AX navigate error:", e)

    def open_in_external_explorer(self):
        # Open the current folder in regular Windows Explorer
        if os.path.exists(self.current_folder):
            import subprocess
            subprocess.Popen(["explorer", self.current_folder])

    def notify_preview_toggle(self):
        # Show a friendly hint how to toggle the Preview Pane in Explorer
        QMessageBox.information(
            self,
            "Preview Pane Toggle",
            ("To enable/disable the Windows Preview Pane:\n\n"
             "1. Open Windows File Explorer (external).\n"
             "2. View → Preview pane (or press Alt+P).\n\n"
             "Once enabled system-wide, the embedded Explorer should show previews\n"
             "for the selected file types (if a preview handler is installed).")
        )


def main():
    if sys.platform != "win32":
        QMessageBox.critical(None, "Unsupported OS", "This application only runs on Windows.")
        return

    app = QApplication(sys.argv)

    start_folder = QDir.homePath()
    if len(sys.argv) > 1:
        maybe = sys.argv[1]
        if os.path.isdir(maybe):
            start_folder = maybe

    window = ExplorerPreviewApp(start_folder)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
