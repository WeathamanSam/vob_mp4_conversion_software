import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTabWidget)

# --- IMPORT MODULES ---
# These will be created in the next steps
from core.config_manager import ConfigManager
from tabs.info_tab import WelcomeTab
from tabs.batch_convert_tab import BatchConvertTab
from tabs.diagnostics_tab import DiagnosticsTab
from tabs.help_tab import HelpTab

class VobReelApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VobReel: Batch DVD Processor")
        self.resize(900, 650)

        # Initialize Config Manager (matches RetroReel structure)
        self.cfg = ConfigManager()

        # Main Tab Widget Setup
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabBar::tab { height: 40px; padding: 10px; font-size: 10pt; }
            QTabBar::tab:selected { font-weight: bold; }
            QTabBar::tab:disabled { color: #888; background: #e0e0e0; }
        """)
        self.setCentralWidget(self.tabs)

        # Build Tabs
        self.welcome_tab = WelcomeTab()
        # Pass config to converter so it knows default paths
        self.convert_tab = BatchConvertTab(self.cfg) 
        self.diag_tab = DiagnosticsTab()

        # Add Tabs to Window
        self.tabs.addTab(self.welcome_tab, "🏠 Welcome")
        self.tabs.addTab(self.convert_tab, "💿 Batch Converter")
        self.tabs.addTab(self.diag_tab, "🔧 Diagnostics")

        # Auto-run diagnostics on startup to ensure FFmpeg is ready
        self.diag_tab.run_diagnostics()

        self.help_tab = HelpTab()
        self.tabs.addTab(self.help_tab, "❓ Help Guide")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion") # Standard clean look for PyQt6
    window = VobReelApp()
    window.show()
    sys.exit(app.exec())