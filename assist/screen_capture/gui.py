"""
Simple GUI interface for the screen capture system
Replaces Chrome extension with a desktop application
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import asyncio
import threading
import logging
from datetime import datetime
from screen_detector import ScreenCapture, ScreenDetector

class ScreenCaptureGUI:
    """GUI for the screen capture system"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Messenger AI Assistant - Screen Capture")
        self.root.geometry("600x500")
        
        # Initialize capture system
        self.capture = ScreenCapture()
        self.is_capturing = False
        
        # Setup logging to GUI
        self.setup_logging()
        
        # Create GUI elements
        self.create_widgets()
        
        # Initialize detector
        self.detector = ScreenDetector()
        self.refresh_windows()
        
    def setup_logging(self):
        """Setup logging to display in GUI"""
        self.log_handler = GUIHandler(self)
        logger = logging.getLogger()
        logger.addHandler(self.log_handler)
        logger.setLevel(logging.INFO)
        
    def create_widgets(self):
        """Create GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Messenger AI Assistant", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Status section
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.status_label = ttk.Label(status_frame, text="Ready", foreground="green")
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        self.connection_label = ttk.Label(status_frame, text="Backend: Disconnected", foreground="red")
        self.connection_label.grid(row=1, column=0, sticky=tk.W)
        
        # Window selection section
        window_frame = ttk.LabelFrame(main_frame, text="Messenger Windows", padding="10")
        window_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Window list
        self.window_listbox = tk.Listbox(window_frame, height=4)
        self.window_listbox.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Refresh button
        refresh_btn = ttk.Button(window_frame, text="Refresh Windows", 
                                command=self.refresh_windows)
        refresh_btn.grid(row=1, column=0, pady=(5, 0))
        
        # Control section
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        control_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Start/Stop button
        self.capture_btn = ttk.Button(control_frame, text="Start Capture", 
                                     command=self.toggle_capture, state="disabled")
        self.capture_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Settings
        settings_frame = ttk.Frame(control_frame)
        settings_frame.grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(settings_frame, text="Bitrate:").grid(row=0, column=0, sticky=tk.W)
        self.bitrate_var = tk.StringVar(value="128")
        bitrate_combo = ttk.Combobox(settings_frame, textvariable=self.bitrate_var, 
                                    values=["64", "128", "256", "512"], width=10)
        bitrate_combo.grid(row=0, column=1, padx=(5, 0))
        
        # Log section
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="10")
        log_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, width=70)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Check backend connection
        self.check_backend_connection()
        
    def refresh_windows(self):
        """Refresh the list of Messenger windows"""
        self.window_listbox.delete(0, tk.END)
        
        try:
            windows = self.detector.find_messenger_windows()
            if windows:
                for i, window in enumerate(windows):
                    self.window_listbox.insert(tk.END, f"{window.title} ({window.width}x{window.height})")
                self.capture_btn.config(state="normal")
                self.log_message("Found Messenger windows")
            else:
                self.window_listbox.insert(tk.END, "No Messenger windows found")
                self.capture_btn.config(state="disabled")
                self.log_message("No Messenger windows found")
        except Exception as e:
            self.log_message(f"Error refreshing windows: {e}")
            
    def check_backend_connection(self):
        """Check connection to backend"""
        try:
            import requests
            response = requests.get("http://127.0.0.1:8000/health", timeout=2)
            if response.status_code == 200:
                self.connection_label.config(text="Backend: Connected", foreground="green")
                return True
            else:
                self.connection_label.config(text="Backend: Error", foreground="red")
                return False
        except Exception as e:
            self.connection_label.config(text="Backend: Disconnected", foreground="red")
            return False
            
    def toggle_capture(self):
        """Toggle capture on/off"""
        if not self.is_capturing:
            self.start_capture()
        else:
            self.stop_capture()
            
    def start_capture(self):
        """Start screen capture"""
        try:
            # Check backend connection
            if not self.check_backend_connection():
                messagebox.showerror("Error", "Backend not connected. Please start the backend server.")
                return
                
            # Get selected window
            selection = self.window_listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a Messenger window")
                return
                
            # Initialize capture
            asyncio.run(self.capture.initialize())
            
            # Start capture in separate thread
            self.capture_thread = threading.Thread(target=self._run_capture)
            self.capture_thread.daemon = True
            self.capture_thread.start()
            
            self.is_capturing = True
            self.capture_btn.config(text="Stop Capture")
            self.status_label.config(text="Capturing...", foreground="blue")
            self.log_message("Capture started")
            
        except Exception as e:
            self.log_message(f"Error starting capture: {e}")
            messagebox.showerror("Error", f"Failed to start capture: {e}")
            
    def stop_capture(self):
        """Stop screen capture"""
        try:
            self.is_capturing = False
            asyncio.run(self.capture.stop_capture())
            
            self.capture_btn.config(text="Start Capture")
            self.status_label.config(text="Ready", foreground="green")
            self.log_message("Capture stopped")
            
        except Exception as e:
            self.log_message(f"Error stopping capture: {e}")
            
    def _run_capture(self):
        """Run capture in separate thread"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.capture.start_capture())
        except Exception as e:
            self.log_message(f"Capture error: {e}")
            
    def log_message(self, message: str):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        
    def run(self):
        """Run the GUI"""
        self.root.mainloop()

class GUIHandler(logging.Handler):
    """Custom logging handler for GUI"""
    
    def __init__(self, gui):
        super().__init__()
        self.gui = gui
        
    def emit(self, record):
        """Emit log record to GUI"""
        try:
            msg = self.format(record)
            self.gui.log_message(msg)
        except Exception:
            pass

def main():
    """Main function"""
    app = ScreenCaptureGUI()
    app.run()

if __name__ == "__main__":
    main()
