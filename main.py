import sys
import time
import threading
from PyQt5.QtWidgets import QApplication
import Files.overlay as overlay
import threaded_main

class MainApp:
    def __init__(self):
        self.terminate_event = threading.Event()
        self.overlay_app = None

    def run_overlay_app(self):
        print("\n\nRunning Overlay application...\n\n")
        self.overlay_app = overlay.OverlayApp(screen_scaling=1)
        threaded_main.set_overlay_app(self.overlay_app)
        self.overlay_app.run()
        sys.exit(self.overlay_app.app.exec_())

    def run(self):
        # Initialize and run the overlay application
        self.run_overlay_app()

if __name__ == "__main__":
    app = MainApp()
    app.run()
