#!/usr/bin/env python3
"""
Resume File Watcher

Watches for changes to resume_data.yaml and automatically regenerates
the PDF resume with timestamped backups.
"""

import sys
import time
import subprocess
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ResumeHandler(FileSystemEventHandler):
    """Handler for resume file changes."""

    def __init__(self, yaml_file: str = "resume_data.yaml"):
        self.yaml_file = Path(yaml_file).resolve()
        self.last_modified = 0

    def on_modified(self, event):
        """Handle file modification events."""
        if event.is_directory:
            return

        file_path = Path(event.src_path).resolve()

        # Check if it's our YAML file and avoid duplicate events
        if file_path == self.yaml_file:
            current_time = time.time()
            if current_time - self.last_modified < 1:  # Debounce for 1 second
                return
            self.last_modified = current_time

            print(f"\nDetected change in {self.yaml_file.name}")
            self.regenerate_resume()

    def regenerate_resume(self):
        """Regenerate the resume PDF."""
        try:
            print("Regenerating resume...")
            result = subprocess.run([
                sys.executable, "generate_resume.py"
            ], capture_output=True, text=True)

            if result.returncode == 0:
                print("Resume updated successfully!")
                print(result.stdout.strip())
            else:
                print("Error generating resume:")
                print(result.stderr.strip())

        except Exception as e:
            print(f"Error running generator: {e}")

def main():
    """Main function to start file watching."""
    yaml_file = "resume_data.yaml"
    yaml_path = Path(yaml_file)

    if not yaml_path.exists():
        print(f"Error: {yaml_file} not found in current directory")
        return 1

    print(f"Watching {yaml_file} for changes...")
    print("Backups will be saved to 'backups/' directory")
    print("Press Ctrl+C to stop watching\n")

    # Initial generation
    handler = ResumeHandler(yaml_file)
    handler.regenerate_resume()

    # Set up file watcher
    observer = Observer()
    observer.schedule(handler, path=yaml_path.parent, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping file watcher...")
        observer.stop()

    observer.join()
    print("File watcher stopped")
    return 0

if __name__ == "__main__":
    exit(main())