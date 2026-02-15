
import os
import time
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QFileDialog, 
    QRadioButton, QButtonGroup, QCheckBox, QSpinBox, 
    QTextEdit, QProgressBar, QGroupBox, QMessageBox,
    QFrame
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QIcon, QColor, QPalette
from core.worker import CrackerWorker
from core.jtr_worker import JTRWorker
from utils.helpers import find_john_path

# ──────────────────────────────────────────────────────────────
# HACKER DARK THEME STYLESHEET
# ──────────────────────────────────────────────────────────────
HACKER_STYLESHEET = """
/* ── Global ───────────────────────────────────────────────── */
QMainWindow {
    background-color: #0a0a0f;
}

QWidget {
    background-color: transparent;
    color: #c0c0c0;
    font-family: 'Consolas', 'Fira Code', 'Courier New', monospace;
    font-size: 13px;
}

/* ── Group Boxes ──────────────────────────────────────────── */
QGroupBox {
    background-color: rgba(10, 15, 10, 0.85);
    border: 1px solid #00ff41;
    border-radius: 8px;
    margin-top: 18px;
    padding: 14px 10px 10px 10px;
    font-size: 13px;
    font-weight: bold;
    color: #00ff41;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 2px 12px;
    background-color: #0a0a0f;
    border: 1px solid #00ff41;
    border-radius: 4px;
    color: #00ff41;
    font-size: 12px;
    letter-spacing: 1px;
}

/* ── Line Edits ───────────────────────────────────────────── */
QLineEdit {
    background-color: #0d0d14;
    border: 1px solid #1a3a1a;
    border-radius: 5px;
    padding: 8px 12px;
    color: #00ff41;
    selection-background-color: #00ff41;
    selection-color: #0a0a0f;
    font-size: 13px;
}
QLineEdit:focus {
    border: 1px solid #00ff41;
    background-color: #0f0f18;
}
QLineEdit::placeholder {
    color: #3a5a3a;
}

/* ── Buttons ──────────────────────────────────────────────── */
QPushButton {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #0d2818, stop:1 #1a4a28);
    border: 1px solid #00ff41;
    border-radius: 6px;
    padding: 9px 22px;
    color: #00ff41;
    font-weight: bold;
    font-size: 13px;
    letter-spacing: 0.5px;
    min-width: 80px;
}
QPushButton:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #1a4a28, stop:1 #2a6a3a);
    border: 1px solid #33ff66;
    color: #33ff66;
}
QPushButton:pressed {
    background-color: #00ff41;
    color: #0a0a0f;
    border: 1px solid #00ff41;
}
QPushButton:disabled {
    background-color: #0d0d14;
    border: 1px solid #1a2a1a;
    color: #2a3a2a;
}

/* ── Start Button (special) ───────────────────────────────── */
QPushButton#startBtn {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #004d1a, stop:1 #00802b);
    border: 2px solid #00ff41;
    font-size: 14px;
    padding: 10px 30px;
    letter-spacing: 1px;
}
QPushButton#startBtn:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #00802b, stop:1 #00b33c);
    border: 2px solid #66ff8c;
}
QPushButton#startBtn:pressed {
    background-color: #00ff41;
    color: #0a0a0f;
}

/* ── Stop Button (special) ────────────────────────────────── */
QPushButton#stopBtn {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #3d0d0d, stop:1 #5a1a1a);
    border: 1px solid #ff3333;
    color: #ff3333;
}
QPushButton#stopBtn:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #5a1a1a, stop:1 #7a2a2a);
    border: 1px solid #ff5555;
    color: #ff5555;
}
QPushButton#stopBtn:pressed {
    background-color: #ff3333;
    color: #0a0a0f;
}
QPushButton#stopBtn:disabled {
    background-color: #0d0d14;
    border: 1px solid #2a1a1a;
    color: #3a2222;
}

/* ── Radio Buttons ────────────────────────────────────────── */
QRadioButton {
    color: #a0d0a0;
    font-size: 13px;
    spacing: 8px;
    padding: 4px 0;
}
QRadioButton::indicator {
    width: 16px;
    height: 16px;
    border: 2px solid #00ff41;
    border-radius: 9px;
    background-color: #0d0d14;
}
QRadioButton::indicator:checked {
    background-color: #00ff41;
    border: 2px solid #00ff41;
}
QRadioButton::indicator:hover {
    border: 2px solid #33ff66;
}

/* ── Checkboxes ───────────────────────────────────────────── */
QCheckBox {
    color: #a0d0a0;
    font-size: 13px;
    spacing: 8px;
    padding: 3px 0;
}
QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border: 2px solid #00ff41;
    border-radius: 3px;
    background-color: #0d0d14;
}
QCheckBox::indicator:checked {
    background-color: #00ff41;
    border: 2px solid #00ff41;
}
QCheckBox::indicator:hover {
    border: 2px solid #33ff66;
}

/* ── Spin Boxes ───────────────────────────────────────────── */
QSpinBox {
    background-color: #0d0d14;
    border: 1px solid #1a3a1a;
    border-radius: 5px;
    padding: 5px 8px;
    color: #00ff41;
    font-size: 13px;
    min-width: 60px;
}
QSpinBox:focus {
    border: 1px solid #00ff41;
}
QSpinBox::up-button, QSpinBox::down-button {
    background-color: #0d2818;
    border: none;
    width: 20px;
}
QSpinBox::up-button:hover, QSpinBox::down-button:hover {
    background-color: #1a4a28;
}
QSpinBox::up-arrow {
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-bottom: 5px solid #00ff41;
    width: 0; height: 0;
}
QSpinBox::down-arrow {
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #00ff41;
    width: 0; height: 0;
}

/* ── Progress Bar ─────────────────────────────────────────── */
QProgressBar {
    background-color: #0d0d14;
    border: 1px solid #1a3a1a;
    border-radius: 6px;
    text-align: center;
    color: #00ff41;
    font-size: 12px;
    font-weight: bold;
    height: 22px;
}
QProgressBar::chunk {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #003d10, stop:0.5 #00ff41, stop:1 #003d10);
    border-radius: 5px;
}

/* ── Log / Text Area ─────────────────────────────────────── */
QTextEdit {
    background-color: #050508;
    border: 1px solid #1a3a1a;
    border-radius: 6px;
    padding: 8px;
    color: #00ff41;
    font-family: 'Consolas', 'Fira Code', monospace;
    font-size: 12px;
    selection-background-color: #00ff41;
    selection-color: #050508;
}

/* ── Labels ───────────────────────────────────────────────── */
QLabel {
    color: #a0d0a0;
    font-size: 13px;
}
QLabel#titleLabel {
    color: #00ff41;
    font-size: 24px;
    font-weight: bold;
    letter-spacing: 2px;
}
QLabel#subtitleLabel {
    color: #3a8a4a;
    font-size: 12px;
    letter-spacing: 1px;
}
QLabel#statusLabel {
    color: #00ff41;
    font-size: 12px;
    padding: 4px 0;
}

/* ── Separator Line ───────────────────────────────────────── */
QFrame#separator {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 transparent, stop:0.2 #00ff41, stop:0.5 #00ff41,
        stop:0.8 #00ff41, stop:1 transparent);
    max-height: 1px;
    min-height: 1px;
}

/* ── Scrollbar ────────────────────────────────────────────── */
QScrollBar:vertical {
    background-color: #0a0a0f;
    width: 10px;
    border: none;
    border-radius: 5px;
}
QScrollBar::handle:vertical {
    background-color: #1a3a1a;
    border-radius: 5px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background-color: #00ff41;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

/* ── Message Box ──────────────────────────────────────────── */
QMessageBox {
    background-color: #0a0a0f;
}
QMessageBox QLabel {
    color: #00ff41;
    font-size: 14px;
}
QMessageBox QPushButton {
    min-width: 80px;
}
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("⚡ ZIP CRACKER ⚡")
        self.setGeometry(100, 60, 820, 680)
        self.setMinimumSize(700, 550)
        
        self.worker = None
        self._start_time = None
        self.setStyleSheet(HACKER_STYLESHEET)
        self.init_ui()

        # Blinking cursor effect on status label
        self._cursor_visible = True
        self._blink_timer = QTimer(self)
        self._blink_timer.timeout.connect(self._blink_cursor)
        self._blink_timer.start(600)

    def _blink_cursor(self):
        """Blinking terminal cursor on the status label."""
        self._cursor_visible = not self._cursor_visible
        cursor = "█" if self._cursor_visible else " "
        if hasattr(self, '_base_status'):
            self.status_label.setText(self._base_status + cursor)

    def _format_elapsed(self):
        """Return formatted elapsed time string."""
        if self._start_time is None:
            return "0.00s"
        elapsed = time.time() - self._start_time
        if elapsed < 60:
            return f"{elapsed:.2f}s"
        elif elapsed < 3600:
            mins = int(elapsed // 60)
            secs = elapsed % 60
            return f"{mins}m {secs:.1f}s"
        else:
            hrs = int(elapsed // 3600)
            mins = int((elapsed % 3600) // 60)
            secs = elapsed % 60
            return f"{hrs}h {mins}m {secs:.0f}s"

    def _set_status(self, text):
        self._base_status = text
        self.status_label.setText(text + "█")

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(24, 18, 24, 18)
        main_layout.setSpacing(12)

        # ── Header ────────────────────────────────────────────
        header_layout = QVBoxLayout()
        header_layout.setSpacing(2)

        title_label = QLabel("🔓  ZIP CRACKER")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title_label)

        subtitle_label = QLabel("[ ADVANCED PASSWORD RECOVERY TOOL ]")
        subtitle_label.setObjectName("subtitleLabel")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(subtitle_label)

        main_layout.addLayout(header_layout)

        # ── Separator ────────────────────────────────────────
        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine)
        main_layout.addWidget(sep)

        # ── Target File ──────────────────────────────────────
        file_group = QGroupBox("⬡  TARGET FILE")
        file_layout = QHBoxLayout()
        file_layout.setSpacing(8)
        self.zip_path_edit = QLineEdit()
        self.zip_path_edit.setPlaceholderText("Select encrypted .zip archive...")
        browse_btn = QPushButton("📂  Browse")
        browse_btn.clicked.connect(self.browse_zip)
        browse_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        file_layout.addWidget(self.zip_path_edit, stretch=1)
        file_layout.addWidget(browse_btn)
        file_group.setLayout(file_layout)
        main_layout.addWidget(file_group)

        # ── Attack Mode ──────────────────────────────────────
        mode_group = QGroupBox("⚔  ATTACK MODE")
        mode_layout = QVBoxLayout()
        mode_layout.setSpacing(8)

        # Radio buttons row
        radio_row = QHBoxLayout()
        self.dictionary_radio = QRadioButton("📖  Dictionary Attack")
        self.bruteforce_radio = QRadioButton("🔨  Brute Force Attack")
        self.jtr_radio = QRadioButton("🔑  John the Ripper")
        self.dictionary_radio.setChecked(True)
        self.dictionary_radio.toggled.connect(self.toggle_mode_ui)
        self.bruteforce_radio.toggled.connect(self.toggle_mode_ui)
        self.jtr_radio.toggled.connect(self.toggle_mode_ui)
        radio_row.addWidget(self.dictionary_radio)
        radio_row.addWidget(self.bruteforce_radio)
        radio_row.addWidget(self.jtr_radio)
        radio_row.addStretch()
        mode_layout.addLayout(radio_row)

        # Dictionary Options
        self.dict_options_widget = QWidget()
        dict_layout = QHBoxLayout(self.dict_options_widget)
        dict_layout.setContentsMargins(0, 4, 0, 0)
        dict_layout.setSpacing(8)
        self.wordlist_path_edit = QLineEdit()
        self.wordlist_path_edit.setPlaceholderText("Select wordlist file...")
        wordlist_browse_btn = QPushButton("📂  Browse")
        wordlist_browse_btn.clicked.connect(self.browse_wordlist)
        wordlist_browse_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        dict_layout.addWidget(self.wordlist_path_edit, stretch=1)
        dict_layout.addWidget(wordlist_browse_btn)
        mode_layout.addWidget(self.dict_options_widget)

        # Brute Force Options
        self.brute_options_widget = QWidget()
        brute_layout = QVBoxLayout(self.brute_options_widget)
        brute_layout.setContentsMargins(0, 4, 0, 0)
        brute_layout.setSpacing(8)
        self.brute_options_widget.setVisible(False)

        # Charset row
        charset_label = QLabel("CHARACTER SET:")
        charset_label.setStyleSheet("color: #00ff41; font-size: 11px; font-weight: bold; letter-spacing: 1px;")
        brute_layout.addWidget(charset_label)

        charset_layout = QHBoxLayout()
        charset_layout.setSpacing(16)
        self.check_lower = QCheckBox("a-z")
        self.check_upper = QCheckBox("A-Z")
        self.check_digits = QCheckBox("0-9")
        self.check_symbols = QCheckBox("!@#$")
        self.check_lower.setChecked(True)
        self.check_digits.setChecked(True)
        charset_layout.addWidget(self.check_lower)
        charset_layout.addWidget(self.check_upper)
        charset_layout.addWidget(self.check_digits)
        charset_layout.addWidget(self.check_symbols)
        charset_layout.addStretch()
        brute_layout.addLayout(charset_layout)

        # Length row
        len_layout = QHBoxLayout()
        len_layout.setSpacing(10)
        min_label = QLabel("MIN LENGTH:")
        min_label.setStyleSheet("color: #00ff41; font-size: 11px; font-weight: bold;")
        len_layout.addWidget(min_label)
        self.spin_min = QSpinBox()
        self.spin_min.setRange(1, 20)
        self.spin_min.setValue(3)
        len_layout.addWidget(self.spin_min)

        len_layout.addSpacing(20)

        max_label = QLabel("MAX LENGTH:")
        max_label.setStyleSheet("color: #00ff41; font-size: 11px; font-weight: bold;")
        len_layout.addWidget(max_label)
        self.spin_max = QSpinBox()
        self.spin_max.setRange(1, 20)
        self.spin_max.setValue(6)
        len_layout.addWidget(self.spin_max)
        len_layout.addStretch()
        brute_layout.addLayout(len_layout)

        mode_layout.addWidget(self.brute_options_widget)

        # John the Ripper Options
        self.jtr_options_widget = QWidget()
        jtr_layout = QVBoxLayout(self.jtr_options_widget)
        jtr_layout.setContentsMargins(0, 4, 0, 0)
        jtr_layout.setSpacing(8)
        self.jtr_options_widget.setVisible(False)

        # JtR path row
        jtr_path_label = QLabel("JOHN THE RIPPER PATH:")
        jtr_path_label.setStyleSheet("color: #00ff41; font-size: 11px; font-weight: bold; letter-spacing: 1px;")
        jtr_layout.addWidget(jtr_path_label)

        jtr_path_row = QHBoxLayout()
        jtr_path_row.setSpacing(8)
        self.jtr_path_edit = QLineEdit()
        self.jtr_path_edit.setPlaceholderText("Path to JtR run/ directory (containing john.exe)...")

        # Auto-detect JtR path
        detected_path = find_john_path()
        if detected_path:
            self.jtr_path_edit.setText(detected_path)

        jtr_browse_btn = QPushButton("📂  Browse")
        jtr_browse_btn.clicked.connect(self.browse_jtr_path)
        jtr_browse_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        jtr_path_row.addWidget(self.jtr_path_edit, stretch=1)
        jtr_path_row.addWidget(jtr_browse_btn)
        jtr_layout.addLayout(jtr_path_row)

        # JtR sub-mode row
        jtr_mode_label = QLabel("JTR CRACKING MODE:")
        jtr_mode_label.setStyleSheet("color: #00ff41; font-size: 11px; font-weight: bold; letter-spacing: 1px;")
        jtr_layout.addWidget(jtr_mode_label)

        jtr_mode_row = QHBoxLayout()
        jtr_mode_row.setSpacing(16)
        self.jtr_wordlist_radio = QRadioButton("📖  Wordlist")
        self.jtr_incremental_radio = QRadioButton("🔄  Incremental (Auto)")
        self.jtr_wordlist_radio.setChecked(True)
        self.jtr_wordlist_radio.toggled.connect(self._toggle_jtr_wordlist)
        jtr_mode_row.addWidget(self.jtr_wordlist_radio)
        jtr_mode_row.addWidget(self.jtr_incremental_radio)
        jtr_mode_row.addStretch()
        jtr_layout.addLayout(jtr_mode_row)

        # JtR wordlist path row
        self.jtr_wordlist_widget = QWidget()
        jtr_wl_layout = QHBoxLayout(self.jtr_wordlist_widget)
        jtr_wl_layout.setContentsMargins(0, 0, 0, 0)
        jtr_wl_layout.setSpacing(8)
        self.jtr_wordlist_path_edit = QLineEdit()
        self.jtr_wordlist_path_edit.setPlaceholderText("Select wordlist for JtR...")
        jtr_wl_browse_btn = QPushButton("📂  Browse")
        jtr_wl_browse_btn.clicked.connect(self.browse_jtr_wordlist)
        jtr_wl_browse_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        jtr_wl_layout.addWidget(self.jtr_wordlist_path_edit, stretch=1)
        jtr_wl_layout.addWidget(jtr_wl_browse_btn)
        jtr_layout.addWidget(self.jtr_wordlist_widget)

        mode_layout.addWidget(self.jtr_options_widget)

        mode_group.setLayout(mode_layout)
        main_layout.addWidget(mode_group)

        # ── Controls ─────────────────────────────────────────
        control_layout = QHBoxLayout()
        control_layout.setSpacing(12)

        self.start_btn = QPushButton("▶  START CRACKING")
        self.start_btn.setObjectName("startBtn")
        self.start_btn.clicked.connect(self.start_cracking)
        self.start_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        self.stop_btn = QPushButton("■  STOP")
        self.stop_btn.setObjectName("stopBtn")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_cracking)
        self.stop_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        control_layout.addWidget(self.start_btn, stretch=2)
        control_layout.addWidget(self.stop_btn, stretch=1)
        main_layout.addLayout(control_layout)

        # ── Progress ─────────────────────────────────────────
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setRange(0, 0)  # Indeterminate by default
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)

        self.status_label = QLabel("")
        self.status_label.setObjectName("statusLabel")
        self._base_status = "root@zipcracker:~$ ready"
        self.status_label.setText(self._base_status + "█")
        main_layout.addWidget(self.status_label)

        # ── Log Area ─────────────────────────────────────────
        log_group = QGroupBox("⌥  TERMINAL OUTPUT")
        log_layout = QVBoxLayout()
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setMinimumHeight(140)
        self.log_area.setPlaceholderText("Waiting for commands...")
        log_layout.addWidget(self.log_area)
        log_group.setLayout(log_layout)
        main_layout.addWidget(log_group, stretch=1)

    # ── File Browse ───────────────────────────────────────────
    def browse_zip(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Select Zip File", "", "Zip Files (*.zip)")
        if filename:
            self.zip_path_edit.setText(filename)
            self.log(f"[+] Target loaded: {os.path.basename(filename)}")

    def browse_wordlist(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Select Wordlist", "", "Text Files (*.txt);;All Files (*)")
        if filename:
            self.wordlist_path_edit.setText(filename)
            self.log(f"[+] Wordlist loaded: {os.path.basename(filename)}")

    def browse_jtr_path(self):
        directory = QFileDialog.getExistingDirectory(
            self, "Select John the Ripper 'run' Directory")
        if directory:
            self.jtr_path_edit.setText(directory)
            self.log(f"[+] JtR path set: {directory}")

    def browse_jtr_wordlist(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Select Wordlist for JtR", "", "Text Files (*.txt);;All Files (*)")
        if filename:
            self.jtr_wordlist_path_edit.setText(filename)
            self.log(f"[+] JtR wordlist loaded: {os.path.basename(filename)}")

    def _toggle_jtr_wordlist(self):
        self.jtr_wordlist_widget.setVisible(self.jtr_wordlist_radio.isChecked())

    # ── Mode Toggle ───────────────────────────────────────────
    def toggle_mode_ui(self):
        is_dict = self.dictionary_radio.isChecked()
        is_brute = self.bruteforce_radio.isChecked()
        is_jtr = self.jtr_radio.isChecked()
        self.dict_options_widget.setVisible(is_dict)
        self.brute_options_widget.setVisible(is_brute)
        self.jtr_options_widget.setVisible(is_jtr)

    # ── Logging ───────────────────────────────────────────────
    def log(self, message):
        self.log_area.append(message)

    # ── Cracking ──────────────────────────────────────────────
    def start_cracking(self):
        zip_path = self.zip_path_edit.text()
        if not zip_path or not os.path.exists(zip_path):
            QMessageBox.warning(self, "⚠ Error", "Please select a valid zip file.")
            return

        if self.dictionary_radio.isChecked():
            attack_mode = 'dictionary'
        elif self.bruteforce_radio.isChecked():
            attack_mode = 'brute_force'
        else:
            attack_mode = 'jtr'

        kwargs = {}
        if attack_mode == 'dictionary':
            wordlist = self.wordlist_path_edit.text()
            if not wordlist or not os.path.exists(wordlist):
                QMessageBox.warning(self, "⚠ Error", "Please select a valid wordlist.")
                return
            kwargs['wordlist_path'] = wordlist
        elif attack_mode == 'brute_force':
            kwargs['use_lower'] = self.check_lower.isChecked()
            kwargs['use_upper'] = self.check_upper.isChecked()
            kwargs['use_digits'] = self.check_digits.isChecked()
            kwargs['use_symbols'] = self.check_symbols.isChecked()
            kwargs['min_length'] = self.spin_min.value()
            kwargs['max_length'] = self.spin_max.value()
        elif attack_mode == 'jtr':
            john_dir = self.jtr_path_edit.text()
            if not john_dir or not os.path.isdir(john_dir):
                QMessageBox.warning(self, "⚠ Error",
                    "Please provide a valid path to John the Ripper's run/ directory.")
                return
            jtr_mode = 'wordlist' if self.jtr_wordlist_radio.isChecked() else 'incremental'
            if jtr_mode == 'wordlist':
                wl = self.jtr_wordlist_path_edit.text()
                if not wl or not os.path.exists(wl):
                    QMessageBox.warning(self, "⚠ Error", "Please select a valid wordlist for JtR.")
                    return
                kwargs['wordlist_path'] = wl

        self._start_time = time.time()

        if attack_mode == 'jtr':
            self.worker = JTRWorker(zip_path, john_dir, jtr_mode, **kwargs)
        else:
            self.worker = CrackerWorker(zip_path, attack_mode, **kwargs)

        self.worker.progress_updated.connect(self.update_progress_text)
        self.worker.stats_updated.connect(self._on_stats_updated)
        self.worker.password_found.connect(self.on_success)
        self.worker.task_finished.connect(self.on_finished)
        self.worker.error_occurred.connect(self.on_error)

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate spinner
        self.log_area.clear()

        mode_map = {'dictionary': 'DICTIONARY', 'brute_force': 'BRUTE FORCE', 'jtr': 'JOHN THE RIPPER'}
        mode_str = mode_map[attack_mode]
        self.log(f"{'='*50}")
        self.log(f"  ⚡  ZIP CRACKER — {mode_str} MODE")
        self.log(f"{'='*50}")
        self.log(f"[*] Target : {os.path.basename(zip_path)}")
        if attack_mode == 'dictionary':
            self.log(f"[*] Wordlist: {os.path.basename(kwargs['wordlist_path'])}")
        elif attack_mode == 'brute_force':
            chars = []
            if kwargs.get('use_lower'): chars.append('a-z')
            if kwargs.get('use_upper'): chars.append('A-Z')
            if kwargs.get('use_digits'): chars.append('0-9')
            if kwargs.get('use_symbols'): chars.append('symbols')
            self.log(f"[*] Charset : {', '.join(chars)}")
            self.log(f"[*] Length  : {kwargs['min_length']} - {kwargs['max_length']}")
        elif attack_mode == 'jtr':
            self.log(f"[*] JtR Path: {john_dir}")
            self.log(f"[*] JtR Mode: {jtr_mode.title()}")
            if jtr_mode == 'wordlist':
                self.log(f"[*] Wordlist: {os.path.basename(kwargs['wordlist_path'])}")
        self.log(f"[*] Started : {time.strftime('%H:%M:%S')}")
        self.log(f"[*] Status  : Initializing attack...\n")
        self._set_status("root@zipcracker:~$ cracking in progress... ")
        self.worker.start()

    def stop_cracking(self):
        if self.worker:
            self.worker.stop()
            self.log("[!] User requested stop...")
            self._set_status("root@zipcracker:~$ aborting... ")

    def _on_stats_updated(self, attempts):
        elapsed = self._format_elapsed()
        speed = attempts / max(time.time() - self._start_time, 0.001)
        self.log(f"[~] Attempts: {attempts}  |  Elapsed: {elapsed}  |  Speed: {speed:.0f} pwd/s")
        self._set_status(
            f"root@zipcracker:~$ attempts: {attempts} | time: {elapsed} ")

    def update_progress(self, current_pass):
        pass  # Indeterminate bar handles visual feedback

    def update_progress_text(self, text):
        """Handle progress text from both CrackerWorker and JTRWorker."""
        self.log(text)

    def on_success(self, password):
        elapsed = self._format_elapsed()
        total_attempts = self.worker.attempts if self.worker else 0
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(100)
        self.log(f"\n{'='*50}")
        self.log(f"  🔓  PASSWORD FOUND!")
        self.log(f"{'='*50}")
        self.log(f"  ➤  Password : {password}")
        self.log(f"  ⏱  Time     : {elapsed}")
        self.log(f"  🔢  Attempts : {total_attempts}")
        self.log(f"{'='*50}\n")
        self._set_status(f"root@zipcracker:~$ CRACKED in {elapsed}: {password} ")
        QMessageBox.information(
            self, "🔓 Password Found!",
            f"Successfully cracked!\n\nPassword: {password}\nTime: {elapsed}\nAttempts: {total_attempts}")

    def on_finished(self):
        elapsed = self._format_elapsed()
        total_attempts = self.worker.attempts if self.worker else 0
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setVisible(False)
        self.log(f"[*] Process finished.  Total time: {elapsed}  |  Total attempts: {total_attempts}")
        self._set_status("root@zipcracker:~$ ready ")
        self._start_time = None

    def on_error(self, msg):
        self.log(f"[ERROR] {msg}")
        self._set_status("root@zipcracker:~$ error encountered ")
