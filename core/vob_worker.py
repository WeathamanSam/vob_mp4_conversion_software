import os
import subprocess
import re
from PyQt6.QtCore import QThread, pyqtSignal

class VobWorker(QThread):
    log_message = pyqtSignal(str)
    progress_update = pyqtSignal(int)
    finished = pyqtSignal(bool)

    # CHANGED: Added crf and preset arguments
    def __init__(self, source_dir, output_dir, crf, preset):
        super().__init__()
        self.source_dir = source_dir
        self.output_dir = output_dir
        self.crf = crf      # User selected value
        self.preset = preset # User selected value
        self.is_running = True

    def scan_for_title_sets(self):
        """Scans source_dir for VOB sequences."""
        title_sets = {}
        vob_pattern = re.compile(r"VTS_(\d+)_(\d+)\.VOB", re.IGNORECASE)

        for root, dirs, files in os.walk(self.source_dir):
            local_groups = {}
            for f in files:
                match = vob_pattern.match(f)
                if match:
                    title_id = match.group(1) 
                    part_id = int(match.group(2)) 
                    if part_id == 0: continue # Skip menus

                    if title_id not in local_groups: local_groups[title_id] = []
                    local_groups[title_id].append(os.path.join(root, f))

            folder_name = os.path.basename(root)
            for title_id, file_paths in local_groups.items():
                sorted_paths = sorted(file_paths)
                unique_key = f"{folder_name}_Title_{title_id}"
                title_sets[unique_key] = sorted_paths

        return title_sets

    def run(self):
        self.log_message.emit(f"Scanning {self.source_dir}...")
        title_sets = self.scan_for_title_sets()
        
        if not title_sets:
            self.log_message.emit("❌ No valid VOB Title Sets found.")
            self.finished.emit(False)
            return

        self.log_message.emit(f"Found {len(title_sets)} titles to process.")
        if not os.path.exists(self.output_dir): os.makedirs(self.output_dir)

        total = len(title_sets)
        current = 0

        for output_name, vob_list in title_sets.items():
            if not self.is_running: break

            current += 1
            output_file = os.path.join(self.output_dir, f"{output_name}.mp4")
            
            if os.path.exists(output_file):
                self.log_message.emit(f"⚠️ Skipping existing: {output_name}.mp4")
                self.progress_update.emit(int((current / total) * 100))
                continue

            self.log_message.emit(f"🎥 Converting ({current}/{total}): {output_name}")
            
            concat_string = "concat:" + "|".join(vob_list)
            
            # CHANGED: Use self.crf and self.preset directly
            cmd = [
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-stats",
                "-analyzeduration", "100M", "-probesize", "100M",
                "-i", concat_string,
                "-c:v", "libx264", "-crf", self.crf, "-preset", self.preset,
                "-vf", "yadif,format=yuv420p",
                "-c:a", "aac", "-b:a", "192k",
                "-movflags", "+faststart",
                output_file
            ]

            try:
                subprocess.run(cmd, check=True)
                self.log_message.emit(f"✅ Finished: {output_name}.mp4")
            except subprocess.CalledProcessError as e:
                self.log_message.emit(f"❌ Error: {str(e)}")
            
            self.progress_update.emit(int((current / total) * 100))

        self.log_message.emit("--- BATCH COMPLETE ---")
        self.finished.emit(True)

    def stop(self):
        self.is_running = False