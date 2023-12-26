import sys
import os
import threading
from PyQt5.QtWidgets import QApplication
import Files.overlay as overlay
import threaded_main

class MainApp:
    def __init__(self):
        self.terminate_event = threading.Event()
        self.overlay_app = overlay.OverlayApp(screen_scaling=1)
        self.overlay_app.custom_window.closed.connect(self.on_overlay_closed)
        self.overlay_app.custom_window.finish_signal.connect(self.on_overlay_closed)

        self.threaded_main_app = threaded_main.ThreadedMain()
        self.threaded_main_app.set_overlay_app(self.overlay_app)
        

    def run(self):
        # Start the background task in a separate thread
        self.background_task_thread = threading.Thread(target=self.threaded_main_app.main, daemon=True, args=(self.terminate_event,))
        self.background_task_thread.start()

        # Run the overlay application directly on the main thread
        self.overlay_app.run()

    def on_overlay_closed(self):
        print("OverlayApp closed.")
        # Signal to stop the ThreadedMain thread when overlay is closed
        self.terminate_event.set()


if __name__ == "__main__":
    app = MainApp()
    app.run()
