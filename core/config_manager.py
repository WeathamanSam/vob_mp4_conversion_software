import json
import os
from pathlib import Path

class ConfigManager:
    def __init__(self):
        # Folder for the config file itself
        self.config_dir = os.path.join(Path.home(), ".config", "VobReel")
        self.config_file = os.path.join(self.config_dir, "config.json")
        
        # Defaults specific to VOB processing
        self.defaults = {
            # Default location for finished MP4s
            "default_export_path": os.path.join(Path.home(), "Desktop", "VobReel_Exports"),
            
            # FFmpeg Quality Settings (Lower CRF = Higher Quality)
            "ffmpeg_crf": "20",
            "ffmpeg_preset": "medium",
            
            # How to stitch VOBs: 'binary' (raw copy) or 'demuxer' (ffmpeg text list)
            # Binary is often safer for VOBs split purely by file size (1GB chunks)
            "concat_method": "binary" 
        }
        
        self.settings = self.defaults.copy()
        self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_dir):
            try:
                os.makedirs(self.config_dir)
            except OSError:
                print("Error creating config directory.")
                
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    self.settings.update(data)
            except json.JSONDecodeError:
                print("Config file corrupted. Using defaults.")
        else:
            self.save_config()

    def save_config(self):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
        except OSError as e:
            print(f"Failed to save config: {e}")

    def get(self, key):
        return self.settings.get(key, self.defaults.get(key))

    def set(self, key, value):
        self.settings[key] = value
        self.save_config()