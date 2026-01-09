import shutil
import subprocess
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                             QProgressBar, QTextEdit, QMessageBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont

# --- WORKER THREAD FOR CHECKS ---
class DiagnosticWorker(QThread):
    finished = pyqtSignal(bool, list)

    def run(self):
        missing = []
        # We only strictly need ffmpeg. 
        # (ffprobe is usually included with ffmpeg, but good to check).
        required_tools = ['ffmpeg', 'ffprobe']

        for tool in required_tools:
            if shutil.which(tool) is None:
                missing.append(tool)
        
        # Success if list is empty
        self.finished.emit(len(missing) == 0, missing)

# --- MAIN TAB UI ---
class DiagnosticsTab(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Title
        self.title = QLabel("System Diagnostics")
        self.title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title)

        # Status Window
        self.log_window = QTextEdit()
        self.log_window.setReadOnly(True)
        self.log_window.setStyleSheet("""
            background-color: #1e1e1e; 
            color: #00ff00; 
            font-family: Monospace; 
            font-size: 10pt;
        """)
        layout.addWidget(self.log_window)

        # Progress Bar
        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        layout.addWidget(self.progress)

        # Run Button
        self.btn_run = QPushButton("🔄 Run System Check")
        self.btn_run.setMinimumHeight(40)
        self.btn_run.clicked.connect(self.run_diagnostics)
        layout.addWidget(self.btn_run)

    def log(self, message):
        self.log_window.append(message)

    def run_diagnostics(self):
        self.log_window.clear()
        self.log("Checking system requirements...")
        self.progress.setRange(0, 0) # Indeterminate mode

        self.worker = DiagnosticWorker()
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    def on_finished(self, success, missing_items):
        self.progress.setRange(0, 100)
        self.progress.setValue(100)

        if success:
            self.log("\n✅ SUCCESS: FFmpeg is installed and ready.")
        else:
            self.log("\n❌ ERROR: Missing components!")
            for item in missing_items:
                self.log(f"   - {item} not found in PATH")
            
            QMessageBox.critical(self, "Missing Software", 
                "FFmpeg was not found.\n\nPlease install FFmpeg to use this software.")