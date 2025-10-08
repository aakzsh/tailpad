import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPlainTextEdit, QFileDialog,
    QAction, QMessageBox, QToolBar, QPushButton, QCheckBox, QLabel
)
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon


class Notepad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TailPad")
        self.setWindowIcon(QIcon("logo.ico"))
        self.resize(900, 600)

        # ---- Text Area ----
        self.font_family = "Courier New"        # monospaced font for proper formatting
        self.font_size = 12                      # default size
        self.text_area = QPlainTextEdit(self)
        self.text_area.setFont(QFont(self.font_family, self.font_size))
        self.setCentralWidget(self.text_area)

        # ---- State ----
        self.current_file = None
        self.dark_mode = False
        self.watcher_enabled = False

        # ---- UI ----
        self._create_menu()
        self._create_toolbar()

        # ---- Timer for Watcher ----
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_file)

    # -------------------- Menu --------------------
    def _create_menu(self):
        menu = self.menuBar()
        file_menu = menu.addMenu("File")

        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction("Save As", self)
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    # -------------------- Toolbar --------------------
    def _create_toolbar(self):
        toolbar = QToolBar("Toolbar")
        self.addToolBar(toolbar)

        # Select file to watch
        self.select_btn = QPushButton("Select File")
        self.select_btn.clicked.connect(self.select_file)
        toolbar.addWidget(self.select_btn)

        # Watcher checkbox
        self.watch_checkbox = QCheckBox("Watcher")
        self.watch_checkbox.stateChanged.connect(self.toggle_watcher)
        toolbar.addWidget(self.watch_checkbox)

        # Font controls
        toolbar.addSeparator()
        toolbar.addWidget(QLabel("Font:"))

        self.font_minus_btn = QPushButton("–")
        self.font_minus_btn.clicked.connect(self.decrease_font)
        toolbar.addWidget(self.font_minus_btn)

        self.font_plus_btn = QPushButton("+")
        self.font_plus_btn.clicked.connect(self.increase_font)
        toolbar.addWidget(self.font_plus_btn)

        # Theme toggle
        toolbar.addSeparator()
        self.theme_btn = QPushButton("🌞 Light")
        self.theme_btn.clicked.connect(self.toggle_theme)
        toolbar.addWidget(self.theme_btn)

    # -------------------- File ops --------------------
    def select_file(self):
        """Pick file without immediately loading it."""
        path, _ = QFileDialog.getOpenFileName(
            self, "Select File to Watch", "", "Text Files (*.txt);;All Files (*)"
        )
        if path:
            self.current_file = path
            self.load_file(path)

    def open_file(self):
        self.select_file()  # same behavior as select_file

    def load_file(self, path):
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                self.text_area.setPlainText(f.read())
            self.scroll_to_bottom()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open file:\n{e}")

    def save_file(self):
        if self.current_file:
            self._write_to_file(self.current_file)
        else:
            self.save_file_as()

    def save_file_as(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save File As", "", "Text Files (*.txt);;All Files (*)"
        )
        if path:
            self.current_file = path
            self._write_to_file(path)

    def _write_to_file(self, path):
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.text_area.toPlainText())
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save file:\n{e}")

    # -------------------- Watcher --------------------
    def toggle_watcher(self, state):
        self.watcher_enabled = bool(state)
        if self.watcher_enabled and self.current_file:
            self.timer.start(5000)  # refresh every 5 s
        else:
            self.timer.stop()

    def refresh_file(self):
        if self.watcher_enabled and self.current_file and os.path.exists(self.current_file):
            try:
                with open(self.current_file, "r", encoding="utf-8", errors="ignore") as f:
                    new_text = f.read()
                if new_text != self.text_area.toPlainText():
                    self.text_area.setPlainText(new_text)
                    self.scroll_to_bottom()
            except Exception as e:
                QMessageBox.warning(self, "Watcher Error", str(e))

    # -------------------- Font Size --------------------
    def increase_font(self):
        self.font_size += 1
        self.text_area.setFont(QFont(self.font_family, self.font_size))

    def decrease_font(self):
        if self.font_size > 6:
            self.font_size -= 1
            self.text_area.setFont(QFont(self.font_family, self.font_size))

    # -------------------- Misc --------------------
    def scroll_to_bottom(self):
        cursor = self.text_area.textCursor()
        cursor.movePosition(cursor.End)
        self.text_area.setTextCursor(cursor)
        self.text_area.ensureCursorVisible()

    def toggle_theme(self):
        if self.dark_mode:
            self.setStyleSheet("")
            self.text_area.setStyleSheet("background:white; color:black;")
            self.theme_btn.setText("🌞 Light")
            self.dark_mode = False
        else:
            self.text_area.setStyleSheet("background:#121212; color:#eeeeee;")
            self.theme_btn.setText("🌙 Dark")
            self.dark_mode = True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Notepad()
    window.show()
    sys.exit(app.exec_())
