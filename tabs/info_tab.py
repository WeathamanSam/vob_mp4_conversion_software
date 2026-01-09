from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class WelcomeTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # --- TITLE SECTION ---
        title = QLabel("Welcome to VobReel")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("The Automated VOB-to-MP4 Batch Processor")
        subtitle.setStyleSheet("color: #888; font-size: 14pt;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        # --- DIVIDER ---
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addSpacing(20)
        layout.addWidget(line)
        layout.addSpacing(20)
        
        # --- INSTRUCTIONS ---
        instructions = QLabel(
            "<h3>How to use VobReel:</h3>"
            "<ol style='font-size: 12pt; line-height: 1.5;'>"
            "<li><b>Prepare your files:</b> Ensure your DVD rips are in folders (e.g. <code>/Movies/Wedding_DVD/VIDEO_TS/</code>).</li>"
            "<li><b>Select Source:</b> Go to the <b>Batch Converter</b> tab and select the parent folder containing your rips.</li>"
            "<li><b>Select Output:</b> Choose where you want the finished MP4s to be saved.</li>"
            "<li><b>Convert:</b> Click Start. VobReel will automatically stitch the VOB chunks into single MP4 files.</li>"
            "</ol>"
            "<p style='color: #666;'><i>Note: This tool uses FFmpeg to stitch files without re-encoding quality loss where possible.</i></p>"
        )
        instructions.setWordWrap(True)
        instructions.setAlignment(Qt.AlignmentFlag.AlignLeft)
        # Indent the instructions slightly
        instructions.setContentsMargins(50, 0, 50, 0)
        
        layout.addWidget(instructions)
        layout.addStretch()