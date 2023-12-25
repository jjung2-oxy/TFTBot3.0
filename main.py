import sys
import os
import threading
from PyQt5.QtWidgets import QApplication
import Files.overlay as overlay
import threaded_main  # Import the module

class MainApp:
    def __init__(self):
        self.terminate_event = threading.Event()
        self.overlay_app = None
        self.threaded_main_app = threaded_main.ThreadedMain()  # Create an instance of ThreadedMain

    def run_overlay_app(self):
        print("\n\nRunning Overlay application...\n\n")
        self.overlay_app = overlay.OverlayApp(screen_scaling=1)
        self.threaded_main_app.set_overlay_app(self.overlay_app)  # Set the overlay app in ThreadedMain
        self.overlay_app.run()

    def run_threaded_main(self):
        # Run the threaded_main logic in a separate thread
        threaded_main_thread = threading.Thread(target=self.threaded_main_app.main, args=(self.terminate_event,))
        threaded_main_thread.start()

    def run(self):
        # Start the threaded_main logic in a separate thread
        ''' PAUSED FOR OVERLAY TESTING'''
        self.run_threaded_main()

        # Initialize and run the overlay application
        self.run_overlay_app()

        # Wait for the PyQt5 event loop to finish before exiting
        sys.exit(self.overlay_app.app.exec_())

if __name__ == "__main__":
    app = MainApp()
    app.run()