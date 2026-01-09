import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                             QProgressBar, QTextEdit, QFileDialog, QHBoxLayout,
                             QLineEdit, QMessageBox, QComboBox, QGroupBox, 
                             QCheckBox)
from PyQt6.QtCore import Qt
from core.vob_worker import VobWorker

class BatchConvertTab(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.worker = None

        layout = QVBoxLayout()
        self.setLayout(layout)

        # --- HEADER ---
        lbl_title = QLabel("DVD VOB Batch Processor")
        lbl_title.setStyleSheet("font-size: 14pt; font-weight: bold; color: #888;")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_title)

        # --- 1. SOURCE & DESTINATION ---
        src_group = QGroupBox("1. File Locations")
        src_layout = QVBoxLayout()
        
        # Source
        src_row = QHBoxLayout()
        self.input_path_display = QLineEdit()
        self.input_path_display.setPlaceholderText("Select folder with VIDEO_TS subfolders...")
        self.btn_browse_src = QPushButton("📂 Browse Source")
        self.btn_browse_src.clicked.connect(self.select_source_folder)
        src_row.addWidget(self.input_path_display)
        src_row.addWidget(self.btn_browse_src)
        src_layout.addLayout(src_row)

        # Destination
        dest_row = QHBoxLayout()
        self.output_path_display = QLineEdit()
        self.output_path_display.setText(self.config.get("default_export_path"))
        self.btn_browse_dest = QPushButton("📂 Browse Output")
        self.btn_browse_dest.clicked.connect(self.select_output_folder)
        dest_row.addWidget(self.output_path_display)
        dest_row.addWidget(self.btn_browse_dest)
        src_layout.addLayout(dest_row)
        
        src_group.setLayout(src_layout)
        layout.addWidget(src_group)

        # --- 2. SETTINGS (UPDATED) ---
        settings_group = QGroupBox("2. Quality & format")
        settings_layout = QHBoxLayout()

        # Quality Dropdown (Plain English)
        self.combo_quality = QComboBox()
        self.combo_quality.addItem("🌟 Best Quality (Preserve Grain)", 18)
        self.combo_quality.addItem("✅ Standard (Balanced)", 20)
        self.combo_quality.addItem("💾 Compact (Shareable)", 23)
        self.combo_quality.setToolTip(
            "Controls the visual clarity.\n"
            "• Best Quality: Larger files, keeps VHS grain intact.\n"
            "• Standard: Good balance for most DVDs.\n"
            "• Compact: Smoother image, smaller file size."
        )
        self.combo_quality.setCurrentIndex(0) 

        # Speed Dropdown
        self.combo_speed = QComboBox()
        self.combo_speed.addItem("🐢 High Efficiency (Slow)", "slow")
        self.combo_speed.addItem("🐇 Balanced Speed (Medium)", "medium")
        self.combo_speed.addItem("🚀 Fast Preview", "fast")
        self.combo_speed.setToolTip(
            "Controls how hard the computer works to compress the file.\n"
            "• Slow: Takes longer, but produces better looking files for the same size.\n"
            "• Fast: Finishes quickly, but file might be larger or blockier."
        )
        self.combo_speed.setCurrentIndex(1)

        # Audio Checkbox (NEW)
        self.chk_audio_copy = QCheckBox("Keep Original Audio")
        self.chk_audio_copy.setChecked(False)
        self.chk_audio_copy.setToolTip(
            "If checked, the original DVD audio (AC3/PCM) is copied exactly.\n"
            "If unchecked, audio is converted to AAC (widely compatible but slight quality loss)."
        )

        settings_layout.addWidget(QLabel("Video Quality:"))
        settings_layout.addWidget(self.combo_quality)
        settings_layout.addSpacing(15)
        settings_layout.addWidget(QLabel("Speed:"))
        settings_layout.addWidget(self.combo_speed)
        settings_layout.addSpacing(15)
        settings_layout.addWidget(self.chk_audio_copy)
        
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)

        layout.addSpacing(10)

        # --- 3. ACTION ---
        self.btn_start = QPushButton("🚀 Start Batch Conversion")
        self.btn_start.setMinimumHeight(50)
        self.btn_start.setStyleSheet("font-size: 12pt; font-weight: bold; background-color: #2196F3; color: white;")
        self.btn_start.clicked.connect(self.start_conversion)
        layout.addWidget(self.btn_start)

        # --- PROGRESS & LOGS ---
        self.progress = QProgressBar()
        self.progress.setValue(0)
        layout.addWidget(self.progress)

        self.log_window = QTextEdit()
        self.log_window.setReadOnly(True)
        self.log_window.setStyleSheet("background-color: #111; color: #0f0; font-family: Monospace;")
        layout.addWidget(self.log_window)

    def select_source_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Source Folder")
        if folder: self.input_path_display.setText(folder)

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder: self.output_path_display.setText(folder)

    def log(self, message):
        self.log_window.append(message)
        sb = self.log_window.verticalScrollBar()
        sb.setValue(sb.maximum())

    def start_conversion(self):
        source = self.input_path_display.text().strip()
        output = self.output_path_display.text().strip()

        if not source or not os.path.exists(source):
            QMessageBox.warning(self, "Input Error", "Please select a valid Source directory.")
            return
        if not output:
            QMessageBox.warning(self, "Input Error", "Please select a valid Output directory.")
            return

        # Get User Selections
        selected_crf = str(self.combo_quality.currentData())
        selected_preset = self.combo_speed.currentData()
        keep_audio = self.chk_audio_copy.isChecked()

        # UI Lock
        self.btn_start.setEnabled(False)
        self.log_window.clear()
        self.progress.setValue(0)

        self.log(f"Starting batch process...")
        self.log(f"Settings: CRF {selected_crf} | Preset: {selected_preset} | Audio Copy: {keep_audio}")

        # Pass specific settings to worker
        # Note: We haven't updated the worker yet to accept 'keep_audio'
        self.worker = VobWorker(source, output, selected_crf, selected_preset, keep_audio)
        self.worker.log_message.connect(self.log)
        self.worker.progress_update.connect(self.progress.setValue)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    def on_finished(self, success):
        self.btn_start.setEnabled(True)
        status = "COMPLETE" if success else "FAILED / STOPPED"
        self.log(f"\n--- JOB {status} ---")
        if success:
            QMessageBox.information(self, "Success", "Batch conversion finished successfully!")