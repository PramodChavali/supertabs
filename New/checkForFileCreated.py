from watchdog import *
import time
import subprocess

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define the folder to monitor
FOLDER_TO_WATCH = "D:/vsCode/python/New/PDFInputs"  # Replace with the path to your folder

# Custom event handler
class FileCreatedHandler(FileSystemEventHandler):
    def on_created(self, event):
        """
        Called when a file or directory is created.
        """
        subprocess.run(["python", "midiToTabs.py"])
        print("directory updated")


        if not event.is_directory:  # Ignore directory creation events
            print(f"New file created: {event.src_path}")

# Set up the observer
event_handler = FileCreatedHandler()
observer = Observer()
observer.schedule(event_handler, path=FOLDER_TO_WATCH, recursive=False)

# Start monitoring
print(f"Monitoring folder: {FOLDER_TO_WATCH}")
observer.start()

try:
    while True:
        time.sleep(1)  # Keep the script running
except KeyboardInterrupt:
    observer.stop()  # Stop monitoring on keyboard interrupt

observer.join()  # Wait for the observer thread to finish