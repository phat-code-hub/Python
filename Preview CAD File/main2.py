"""
embedded_explorer_3pane.py
Three-pane PySide6 app that embeds a REAL Windows Explorer window into the UI.

Requirements:
    pip install PySide6

Run only on Windows.
"""

import sys
import os
import subprocess
import time
import ctypes
from ctypes import wintypes

from PySide6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QTreeView, QListWidget,
    QLabel, QSplitter, QPushButton, QFileSystemModel, QListWidgetItem,
    QMenu, QMessageBox, QToolBar
)
from PySide6.QtCore import Qt, QDir, QTimer, QSize,QEvent
from PySide6.QtGui import QIcon,QAction

# ----------------- Win32 helpers -----------------
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

EnumWindows = user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
GetWindowThreadProcessId = user32.GetWindowThreadProcessId
IsWindowVisible = user32.IsWindowVisible
GetWindowTextLengthW = user32.GetWindowTextLengthW
GetWindowTextW = user32.GetWindowTextW
GetClassNameW = user32.GetClassNameW
SetParent = user32.SetParent
GetWindowLongPtrW = user32.GetWindowLongPtrW
SetWindowLongPtrW = user32.SetWindowLongPtrW
SetWindowPos = user32.SetWindowPos

GWL_STYLE = -16
WS_CHILD = 0x40000000
WS_VISIBLE = 0x10000000

SWP_NOZORDER = 0x0004
SWP_NOACTIVATE = 0x0010

def enum_windows_by_pred(predicate):
    """Return list of HWNDs for which predicate(hwnd) is True."""
    found = []
    @EnumWindowsProc
    def _cb(hwnd, lparam):
        try:
            if predicate(hwnd):
                found.append(hwnd)
        except Exception:
            pass
        return True
    EnumWindows(_cb, 0)
    return found

def hwnd_get_pid(hwnd):
    pid = wintypes.DWORD()
    GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    return pid.value

def hwnd_get_title(hwnd):
    length = GetWindowTextLengthW(hwnd)
    if length == 0:
        return ""
    buf = ctypes.create_unicode_buffer(length + 1)
    GetWindowTextW(hwnd, buf, length + 1)
    return buf.value

def hwnd_get_class(hwnd):
    buf = ctypes.create_unicode_buffer(256)
    GetClassNameW(hwnd, buf, 256)
    return buf.value

def reparent_window_into(hwnd, parent_winid):
    """Set style to child and SetParent to Qt widget window id, then resize to fill parent."""
    style = GetWindowLongPtrW(hwnd, GWL_STYLE)
    # set visible & child bit
    new_style = style | WS_CHILD | WS_VISIBLE
    SetWindowLongPtrW(hwnd, GWL_STYLE, new_style)
    SetParent(hwnd, parent_winid)
    # initial resize handled by caller

def resize_embedded(hwnd, width, height):
    SetWindowPos(hwnd, None, 0, 0, width, height, SWP_NOZORDER | SWP_NOACTIVATE)

# ----------------- Explorer embed / launch logic -----------------
class ExplorerEmbedder:
    """
    Responsible for launching explorer windows (folder or select file),
    locating their top-level HWND, and embedding them into a given parent widget.
    """
    def __init__(self):
        self.last_proc = None
        self.last_hwnd = None
        self.last_target = None

    def launch_explorer_for_folder(self, folder_path):
        # Launch a new Explorer window for folder_path
        # Passing the folder path normally.
        proc = subprocess.Popen(["explorer.exe", folder_path], shell=False)
        self.last_proc = proc
        self.last_target = folder_path
        return proc

    def launch_explorer_select_file(self, file_path):
        # Use /select, to open Explorer and select the file.
        # Note: some Windows versions reuse existing explorer process/window.
        proc = subprocess.Popen(["explorer.exe", "/select,", file_path], shell=False)
        self.last_proc = proc
        self.last_target = file_path
        return proc

    def find_hwnd_for_last_process(self, timeout=3.0):
        """Try to find a top-level HWND for the last launched explorer process."""
        if not self.last_proc:
            return None
        start = time.time()
        target_pid = self.last_proc.pid
        # Try to match by PID first (fast and reliable if a new process was created).
        while time.time() - start < timeout:
            # enumerate windows with matching pid
            hwnds = enum_windows_by_pred(lambda h: hwnd_get_pid(h) == target_pid and IsWindowVisible(h))
            if hwnds:
                return hwnds[0]
            time.sleep(0.08)

        # Fallback: try to find an Explorer window whose title contains a part of the path
        name_fragment = None
        if self.last_target:
            name_fragment = os.path.basename(self.last_target).lower()
        start = time.time()
        while time.time() - start < timeout:
            hwnds = enum_windows_by_pred(lambda h: IsWindowVisible(h) and hwnd_get_class(h) in ("CabinetWClass", "ExploreWClass"))
            for h in hwnds:
                title = hwnd_get_title(h).lower()
                if name_fragment and name_fragment in title:
                    return h
            time.sleep(0.08)
        # give up
        return None

    def embed_target_into(self, parent_winid, timeout=4.0):
        """Wait for target explorer window, then set as child of parent_winid and return HWND."""
        hwnd = self.find_hwnd_for_last_process(timeout=timeout)
        if not hwnd:
            return None
        # Reparent and adjust styles
        try:
            reparent_window_into(hwnd, parent_winid)
        except Exception:
            return None
        self.last_hwnd = hwnd
        return hwnd

    def detach_and_close_last(self):
        """Attempt to close/terminate previous explorer process (best effort)."""
        try:
            if self.last_proc and self.last_proc.poll() is None:
                # Best-effort terminate - some Explorer launches are handled by system shell; safe to ignore errors
                self.last_proc.terminate()
        except Exception:
            pass
        self.last_proc = None
        self.last_hwnd = None
        self.last_target = None

# ----------------- PySide6 UI -----------------
class Explorer3Pane(QWidget):
    def __init__(self, start_folder=None):
        super().__init__()
        self.setWindowTitle("Professional Explorer Previewer (embedded real Explorer)")
        self.resize(1300, 750)

        if start_folder is None:
            start_folder = QDir.homePath()
        self.start_folder = start_folder

        self.embedder = ExplorerEmbedder()
        self.embedded_hwnd = None

        # Splitter layout (left tree, middle file list, right embedded explorer)
        splitter = QSplitter(Qt.Horizontal, self)

        # ---------------- left: folder tree ----------------
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(6, 6, 6, 6)
        left_layout.setSpacing(6)

        folder_label = QLabel("<b>Folders</b>")
        left_layout.addWidget(folder_label)

        self.folder_model = QFileSystemModel()
        self.folder_model.setRootPath(QDir.rootPath())
        self.folder_model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot)

        self.tree = QTreeView()
        self.tree.setModel(self.folder_model)
        self.tree.setRootIndex(self.folder_model.index(QDir.rootPath()))
        self.tree.setHeaderHidden(True)
        self.tree.clicked.connect(self.on_tree_clicked)
        # Expand the start folder for nicer UX
        start_index = self.folder_model.index(self.start_folder)
        if start_index.isValid():
            self.tree.expand(start_index)
            self.tree.setCurrentIndex(start_index)

        left_layout.addWidget(self.tree)
        splitter.addWidget(left_widget)

        # ---------------- middle: file list + toolbar ----------------
        middle_widget = QWidget()
        middle_layout = QVBoxLayout(middle_widget)
        middle_layout.setContentsMargins(6, 6, 6, 6)
        middle_layout.setSpacing(6)

        top_toolbar = QToolBar()
        btn_refresh = QAction("Refresh", self)
        btn_refresh.triggered.connect(self.on_refresh)
        top_toolbar.addAction(btn_refresh)

        btn_up = QAction("Up", self)
        btn_up.triggered.connect(self.on_up)
        top_toolbar.addAction(btn_up)

        btn_open_ext = QAction("Open in Explorer", self)
        btn_open_ext.triggered.connect(self.on_open_external)
        top_toolbar.addAction(btn_open_ext)

        middle_layout.addWidget(top_toolbar)

        middle_layout.addWidget(QLabel("<b>Files</b>"))
        self.file_list = QListWidget()
        self.file_list.itemClicked.connect(self.on_file_clicked)
        self.file_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.file_list.customContextMenuRequested.connect(self.on_file_list_context_menu)
        middle_layout.addWidget(self.file_list)
        splitter.addWidget(middle_widget)

        # ---------------- right: embedded explorer holder ----------------
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(6, 6, 6, 6)
        right_layout.setSpacing(6)
        right_layout.addWidget(QLabel("<b>Embedded Windows Explorer (with preview pane)</b>"))

        # A placeholder widget we will use as parent for the explorer window
        self.explorer_host = QWidget()
        self.explorer_host.setMinimumSize(QSize(500, 400))
        right_layout.addWidget(self.explorer_host)
        splitter.addWidget(right_widget)

        splitter.setSizes([300, 350, 700])
        main_layout = QHBoxLayout(self)
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

        # initial populate
        self.current_folder = self.start_folder
        self.populate_file_list(self.start_folder)

        # attempt to embed explorer at start folder
        QTimer.singleShot(200, lambda: self.open_and_embed_folder(self.start_folder))

        # handle resize to adjust embedded explorer size
        self.explorer_host.installEventFilter(self)

    # ---------------- UI actions ----------------
    def populate_file_list(self, folder_path):
        self.file_list.clear()
        try:
            entries = sorted(os.listdir(folder_path), key=str.lower)
        except Exception:
            entries = []
        for name in entries:
            full = os.path.join(folder_path, name)
            if os.path.isfile(full):
                item = QListWidgetItem(name)
                item.setData(Qt.UserRole, full)
                self.file_list.addItem(item)
        self.current_folder = folder_path

    def on_tree_clicked(self, index):
        folder_path = self.folder_model.filePath(index)
        if folder_path:
            self.populate_file_list(folder_path)
            self.open_and_embed_folder(folder_path)

    def on_file_clicked(self, item):
        full_path = item.data(Qt.UserRole)
        # Open an explorer window that selects the file and embed it (so preview shows)
        self.open_and_embed_select(full_path)

    def on_file_list_context_menu(self, pos):
        item = self.file_list.itemAt(pos)
        if not item:
            return
        path = item.data(Qt.UserRole)
        menu = QMenu(self)
        act_open = QAction("Open", self)
        act_open.triggered.connect(lambda: self.open_file(path))
        act_show = QAction("Show in external Explorer (select)", self)
        act_show.triggered.connect(lambda: self.open_in_external_explorer(path))
        act_copy = QAction("Copy path", self)
        act_copy.triggered.connect(lambda: QApplication.clipboard().setText(path))
        menu.addAction(act_open)
        menu.addAction(act_show)
        menu.addAction(act_copy)
        menu.exec(self.file_list.mapToGlobal(pos))

    def open_file(self, path):
        try:
            os.startfile(path)
        except Exception as e:
            QMessageBox.warning(self, "Open failed", f"Could not open file:\n{e}")

    def on_refresh(self):
        self.populate_file_list(self.current_folder)
        # optionally re-embed folder so Explorer view updates
        self.open_and_embed_folder(self.current_folder)

    def on_up(self):
        parent = os.path.dirname(self.current_folder.rstrip(os.path.sep))
        if parent and os.path.isdir(parent):
            # update tree and file list
            self.populate_file_list(parent)
            # try to find and set tree index
            idx = self.folder_model.index(parent)
            if idx.isValid():
                self.tree.setCurrentIndex(idx)
                self.tree.scrollTo(idx)
            self.open_and_embed_folder(parent)

    def on_open_external(self):
        # Open current folder in external Explorer
        if os.path.exists(self.current_folder):
            subprocess.Popen(["explorer", self.current_folder])

    # ---------------- embed actions ----------------
    def open_and_embed_folder(self, folder_path):
        # Detach previous embed (best effort)
        self.embedder.detach_and_close_last()
        proc = self.embedder.launch_explorer_for_folder(folder_path)
        # Wait and embed
        QTimer.singleShot(100, lambda: self._try_embed_for_proc(proc, folder_path))

    def open_and_embed_select(self, file_path):
        # Detach previous embed (best effort)
        self.embedder.detach_and_close_last()
        proc = self.embedder.launch_explorer_select_file(file_path)
        QTimer.singleShot(100, lambda: self._try_embed_for_proc(proc, file_path))

    def _try_embed_for_proc(self, proc, target_path, attempts=40):
        # Called via QTimer; try to find window and embed
        hwnd = self.embedder.find_hwnd_for_last_process(timeout=2.0)
        if not hwnd:
            # try again a few times with small delay
            attempts -= 1
            if attempts > 0:
                QTimer.singleShot(150, lambda: self._try_embed_for_proc(proc, target_path, attempts))
            else:
                QMessageBox.warning(self, "Embed failed", "Could not find explorer window to embed.")
            return
        # Reparent and resize
        try:
            reparent_window_into(hwnd, int(self.explorer_host.winId()))
            resize_embedded(hwnd, self.explorer_host.width(), self.explorer_host.height())
            self.embedded_hwnd = hwnd
        except Exception as e:
            QMessageBox.warning(self, "Embed failed", f"Embedding failed: {e}")
            return

    # ---------------- resize handling ----------------
    def eventFilter(self, obj, event):
        # if obj is self.explorer_host and event.type() == event.Resize and self.embedded_hwnd:
        #     resize_embedded(self.embedded_hwnd, self.explorer_host.width(), self.explorer_host.height())
        # return super().eventFilter(obj, event)
        # correct way to detect resize events
        if obj is self.explorer_host and event.type() == QEvent.Resize and self.embedded_hwnd:
            resize_embedded(self.embedded_hwnd, self.explorer_host.width(), self.explorer_host.height())
        return super().eventFilter(obj, event)

    # ---------------- helper: open external explorer and select file/folder ----------------
    def open_in_external_explorer(self, path):
        # Select path in external explorer (doesn't embed)
        if os.path.exists(path):
            subprocess.Popen(["explorer", "/select,", path])

# ----------------- run app -----------------
def main():
    if sys.platform != "win32":
        QMessageBox.critical(None, "Unsupported OS", "This application runs only on Windows.")
        return
    app = QApplication(sys.argv)
    start = QDir.homePath()
    if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
        start = sys.argv[1]
    w = Explorer3Pane(start)
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
