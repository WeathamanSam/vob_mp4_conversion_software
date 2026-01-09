import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTextEdit)

class HelpTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        # Remove margins so the dark background fills the whole tab
        layout.setContentsMargins(0, 0, 0, 0) 
        self.setLayout(layout)

        self.help_viewer = QTextEdit()
        self.help_viewer.setReadOnly(True)
        
        # FORCE the widget background to match the CSS body color (#1E1E1E)
        # This prevents white borders/flashing
        self.help_viewer.setStyleSheet("QTextEdit { background-color: #1E1E1E; border: none; }")
        
        layout.addWidget(self.help_viewer)

        self.load_content()

    def load_content(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        assets_dir = os.path.join(base_dir, "assets")
        
        html_path = os.path.join(assets_dir, "help.html")
        css_path = os.path.join(assets_dir, "style.css")

        html_content = "<h1>Error</h1><p>Help file missing.</p>"
        css_content = ""

        if os.path.exists(html_path):
            with open(html_path, "r", encoding="utf-8") as f:
                html_content = f.read()

        if os.path.exists(css_path):
            with open(css_path, "r", encoding="utf-8") as f:
                css_content = f.read()

        full_doc = f"""
        <html>
        <head>
            <style>{css_content}</style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """

        self.help_viewer.setHtml(full_doc)