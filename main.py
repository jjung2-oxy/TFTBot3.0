import sys
import time
import threading
import tkinter as tk
from PyQt5.QtWidgets import QApplication
import threaded_main
import Files.interface as interface
import Files.overlayNEW as overlayNEW

# Flag to signal the background thread to terminate
terminate_event = threading.Event()

# Global variables for overlay and Tkinter applications
global overlay_app
global root

def background_task():
    while not terminate_event.is_set():
        time.sleep(1)  # Wait before performing the task
        threaded_main.main()
        time.sleep(1)  # Wait after performing the task

    print("Background task is stopped")

def run_overlay_app():
    global overlay_app
    print("\n\nRunning Overlay application...\n\n")
    overlay_app = overlayNEW.OverlayApp(screen_scaling=1)
    threaded_main.set_overlay_app(overlay_app)
    overlay_app.run()
    sys.exit(overlay_app.app.exec_())

def run_tkinter_app():
    global root
    print("\n\nRunning Tkinter application...\n\n")
    root = interface.interface()
    root.protocol("WM_DELETE_WINDOW", quit_application)
    root.mainloop()

def quit_application():
    # Signal the background thread to terminate
    terminate_event.set()

    # Close the overlay window
    if overlay_app is not None:
        overlay_app.close_window()

    # Close Tkinter window
    if root is not None:
        root.quit()
        root.destroy()

    sys.exit(0)
    
def main():
    try:
        # Thread for the background task
        background_thread = threading.Thread(target=background_task)
        background_thread.start()
    
        # Thread for the OverlayApp
        overlay_thread = threading.Thread(target=run_overlay_app)
        overlay_thread.start()
        
        # Run Tkinter app in the main thread
        run_tkinter_app()

        # Wait for threads to complete
        background_thread.join()
        overlay_thread.join()
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
