"""
Simplified GUI for Screen Capture System
No websockets, no async/await complexity
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import logging
from datetime import datetime
import webbrowser
import os
from screen_capture import SimpleCaptureSystem, WindowInfo

class SimpleCaptureGUI:
    """Simplified GUI for the screen capture system"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simple Screen Capture - Messenger AI Assistant")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.root.configure(bg='#f8f9fa')
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Initialize capture system
        self.capture_system = SimpleCaptureSystem()
        self.is_capturing = False
        
        # Style configuration
        self._configure_styles()
        
        # Create GUI
        self._create_widgets()
        self._update_window_list()
        
        # Start window detection thread
        self._start_window_detection()
        
        # Center window on screen
        self._center_window()
    
    def _configure_styles(self):
        """Configure modern styling"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'), foreground='#2c3e50')
        style.configure('Subtitle.TLabel', font=('Segoe UI', 10), foreground='#7f8c8d')
        style.configure('Status.TLabel', font=('Segoe UI', 9), foreground='#27ae60')
        style.configure('Error.TLabel', font=('Segoe UI', 9), foreground='#e74c3c')
        style.configure('Info.TLabel', font=('Segoe UI', 9), foreground='#3498db')
        
        # Button styles
        style.configure('Start.TButton', font=('Segoe UI', 10, 'bold'))
        style.configure('Stop.TButton', font=('Segoe UI', 10, 'bold'))
        style.configure('Refresh.TButton', font=('Segoe UI', 9))
    
    def _center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def _create_widgets(self):
        """Create the main GUI widgets"""
        # Main container
        main_container = ttk.Frame(self.root, padding="20")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=1)
        main_container.rowconfigure(2, weight=1)
        
        # Header section
        self._create_header(main_container)
        
        # Status section
        self._create_status_section(main_container)
        
        # Window selection section
        self._create_window_section(main_container)
        
        # Control section
        self._create_control_section(main_container)
        
        # Log section
        self._create_log_section(main_container)
        
        # Footer
        self._create_footer(main_container)
    
    def _create_header(self, parent):
        """Create header section"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Title
        title_label = ttk.Label(header_frame, text="Simple Screen Capture", style='Title.TLabel')
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # Subtitle
        subtitle_label = ttk.Label(header_frame, text="Direct Audio & Video Capture - No Websockets", style='Subtitle.TLabel')
        subtitle_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        # Help button
        help_button = ttk.Button(header_frame, text="Help", command=self._show_help)
        help_button.grid(row=0, column=1, rowspan=2, sticky=tk.E)
    
    def _create_status_section(self, parent):
        """Create status section"""
        status_frame = ttk.LabelFrame(parent, text="System Status", padding="15")
        status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Status indicators
        self.status_label = ttk.Label(status_frame, text="● Ready", style='Status.TLabel')
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        self.audio_status = ttk.Label(status_frame, text="Audio: Checking...", style='Info.TLabel')
        self.audio_status.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        self.video_status = ttk.Label(status_frame, text="Video: Ready", style='Info.TLabel')
        self.video_status.grid(row=2, column=0, sticky=tk.W, pady=(2, 0))
        
        # Test button
        test_button = ttk.Button(status_frame, text="Test System", command=self._test_system)
        test_button.grid(row=0, column=1, rowspan=3, sticky=tk.E, padx=(20, 0))
    
    def _create_window_section(self, parent):
        """Create window selection section"""
        window_frame = ttk.LabelFrame(parent, text="Select Messenger Window", padding="15")
        window_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        window_frame.columnconfigure(0, weight=1)
        window_frame.rowconfigure(1, weight=1)
        
        # Window list
        list_frame = ttk.Frame(window_frame)
        list_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        
        self.window_listbox = tk.Listbox(list_frame, height=6, font=('Segoe UI', 9))
        self.window_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Scrollbar for listbox
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.window_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.window_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Window info
        self.window_info = ttk.Label(window_frame, text="No window selected", style='Info.TLabel')
        self.window_info.grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        
        # Buttons
        button_frame = ttk.Frame(window_frame)
        button_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        refresh_button = ttk.Button(button_frame, text="🔄 Refresh Windows", command=self._update_window_list, style='Refresh.TButton')
        refresh_button.grid(row=0, column=0, padx=(0, 10))
        
        open_messenger_button = ttk.Button(button_frame, text="🌐 Open Messenger", command=self._open_messenger)
        open_messenger_button.grid(row=0, column=1)
        
        # Bind selection event
        self.window_listbox.bind('<<ListboxSelect>>', self._on_window_select)
    
    def _create_control_section(self, parent):
        """Create control section"""
        control_frame = ttk.LabelFrame(parent, text="Capture Controls", padding="15")
        control_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Control buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)
        
        self.start_button = ttk.Button(button_frame, text="▶️ Start Capture", command=self._start_capture, style='Start.TButton')
        self.start_button.grid(row=0, column=0, padx=(0, 10), sticky=(tk.W, tk.E))
        
        self.stop_button = ttk.Button(button_frame, text="⏹️ Stop Capture", command=self._stop_capture, style='Stop.TButton', state='disabled')
        self.stop_button.grid(row=0, column=1, padx=(0, 10), sticky=(tk.W, tk.E))
        
        self.settings_button = ttk.Button(button_frame, text="⚙️ Settings", command=self._show_settings)
        self.settings_button.grid(row=0, column=2, sticky=(tk.W, tk.E))
        
        # Progress bar
        self.progress = ttk.Progressbar(control_frame, mode='indeterminate')
        self.progress.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(15, 0))
        
        # Status info
        self.capture_info = ttk.Label(control_frame, text="Ready to capture", style='Info.TLabel')
        self.capture_info.grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
    
    def _create_log_section(self, parent):
        """Create log section"""
        log_frame = ttk.LabelFrame(parent, text="Activity Log", padding="15")
        log_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Log text area
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, font=('Consolas', 9), wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Log controls
        log_controls = ttk.Frame(log_frame)
        log_controls.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        clear_log_button = ttk.Button(log_controls, text="Clear Log", command=self._clear_log)
        clear_log_button.grid(row=0, column=0, padx=(0, 10))
        
        save_log_button = ttk.Button(log_controls, text="Save Log", command=self._save_log)
        save_log_button.grid(row=0, column=1)
        
        open_output_button = ttk.Button(log_controls, text="📁 Open Output", command=self._open_output_folder)
        open_output_button.grid(row=0, column=2, padx=(10, 0))
    
    def _create_footer(self, parent):
        """Create footer section"""
        footer_frame = ttk.Frame(parent)
        footer_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Version info
        version_label = ttk.Label(footer_frame, text="v2.0.0 | Simplified Edition", style='Subtitle.TLabel')
        version_label.grid(row=0, column=0, sticky=tk.W)
        
        # Quick actions
        actions_frame = ttk.Frame(footer_frame)
        actions_frame.grid(row=0, column=1, sticky=tk.E)
        
        ttk.Button(actions_frame, text="📖 Documentation", command=self._open_docs).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(actions_frame, text="🐛 Report Issue", command=self._report_issue).grid(row=0, column=1)
    
    def _start_window_detection(self):
        """Start window detection in background thread"""
        def detect_windows():
            while True:
                try:
                    windows = self.capture_system.find_windows()
                    # Only update GUI if window count changed
                    if len(windows) != getattr(self, '_last_window_count', -1):
                        self.root.after(0, self._update_window_list)
                        self._last_window_count = len(windows)
                    threading.Event().wait(3)  # Check every 3 seconds
                except Exception as e:
                    self.logger.error(f"Window detection error: {e}")
                    threading.Event().wait(5)
        
        detection_thread = threading.Thread(target=detect_windows, daemon=True)
        detection_thread.start()
    
    def _update_window_list(self):
        """Update window list"""
        try:
            windows = self.capture_system.find_windows()
            
            # Only update if list actually changed
            current_items = [self.window_listbox.get(i) for i in range(self.window_listbox.size())]
            new_items = [f"{w.title} (PID: {w.pid})" for w in windows] if windows else ["No Messenger windows found"]
            
            if current_items != new_items:
                # Clear current list
                self.window_listbox.delete(0, tk.END)
                
                if not windows:
                    self.window_listbox.insert(tk.END, "No Messenger windows found")
                    self.window_listbox.itemconfig(0, {'fg': 'gray'})
                else:
                    for i, window in enumerate(windows):
                        display_text = f"{window.title} (PID: {window.pid})"
                        self.window_listbox.insert(tk.END, display_text)
                        
                        # Color code by type
                        if window.is_messenger:
                            self.window_listbox.itemconfig(i, {'fg': 'green'})
                        else:
                            self.window_listbox.itemconfig(i, {'fg': 'blue'})
                
                # Log if count changed
                if len(windows) != getattr(self, '_last_logged_count', 0):
                    self._log_message(f"Found {len(windows)} Messenger windows")
                    self._last_logged_count = len(windows)
            
        except Exception as e:
            self._log_message(f"Error updating window list: {e}", "ERROR")
    
    def _on_window_select(self, event):
        """Handle window selection"""
        selection = self.window_listbox.curselection()
        if selection:
            index = selection[0]
            windows = self.capture_system.find_windows()
            if index < len(windows):
                selected_window = windows[index]
                self.capture_system.select_window(selected_window)
                self.window_info.config(text=f"Selected: {selected_window.title}")
                self._log_message(f"Selected window: {selected_window.title}")
    
    def _start_capture(self):
        """Start screen capture"""
        if not self.capture_system.selected_window:
            messagebox.showwarning("No Window Selected", "Please select a Messenger window first.")
            return
        
        try:
            # Start capture in separate thread
            def start_capture_thread():
                if self.capture_system.start_capture(fps=15):
                    self.root.after(0, self._on_capture_started)
                else:
                    self.root.after(0, self._on_capture_failed)
            
            capture_thread = threading.Thread(target=start_capture_thread, daemon=True)
            capture_thread.start()
            
        except Exception as e:
            self._log_message(f"Failed to start capture: {e}", "ERROR")
            messagebox.showerror("Capture Error", f"Failed to start capture: {e}")
    
    def _on_capture_started(self):
        """Handle successful capture start"""
        self.is_capturing = True
        
        # Update UI
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.progress.start()
        self.status_label.config(text="● Capturing", style='Status.TLabel')
        self.capture_info.config(text="Capturing audio and video...")
        
        self._log_message("Screen capture started successfully")
    
    def _on_capture_failed(self):
        """Handle failed capture start"""
        self._log_message("Failed to start capture", "ERROR")
        messagebox.showerror("Capture Error", "Failed to start capture")
    
    def _stop_capture(self):
        """Stop screen capture"""
        try:
            self.capture_system.stop_capture()
            self.is_capturing = False
            
            # Update UI
            self.start_button.config(state='normal')
            self.stop_button.config(state='disabled')
            self.progress.stop()
            self.status_label.config(text="● Stopped", style='Status.TLabel')
            self.capture_info.config(text="Capture stopped")
            
            # Update status info
            status = self.capture_system.get_status()
            self._log_message(f"Screen capture stopped. Captured {status['frame_count']} frames")
            
        except Exception as e:
            self._log_message(f"Error stopping capture: {e}", "ERROR")
    
    def _test_system(self):
        """Test system capabilities"""
        try:
            # Test audio
            audio_available = self.capture_system.audio_capture.audio_available
            if audio_available:
                self.audio_status.config(text="Audio: Available ✓", style='Status.TLabel')
            else:
                self.audio_status.config(text="Audio: Not Available", style='Error.TLabel')
            
            # Test video
            self.video_status.config(text="Video: Ready ✓", style='Status.TLabel')
            
            # Test windows
            windows = self.capture_system.find_windows()
            self._log_message(f"System test: Audio={audio_available}, Video=Ready, Windows={len(windows)}")
            
        except Exception as e:
            self._log_message(f"System test failed: {e}", "ERROR")
    
    def _open_messenger(self):
        """Open Messenger in browser"""
        webbrowser.open("https://messenger.com")
        self._log_message("Opening Messenger in browser")
    
    def _open_output_folder(self):
        """Open output folder"""
        try:
            output_dir = os.path.abspath("capture_output")
            if os.path.exists(output_dir):
                os.startfile(output_dir)
                self._log_message(f"Opened output folder: {output_dir}")
            else:
                self._log_message("Output folder not found", "ERROR")
        except Exception as e:
            self._log_message(f"Error opening output folder: {e}", "ERROR")
    
    def _show_help(self):
        """Show help dialog"""
        help_text = """
Simple Screen Capture - Messenger AI Assistant

This application captures audio and video from Messenger Web conversations and saves them directly to files.

How to use:
1. Open Messenger Web in your browser
2. Select a Messenger window from the list
3. Click 'Start Capture' to begin recording
4. Files are saved to the 'capture_output' folder
5. Click 'Stop Capture' when finished

Features:
• Direct file-based capture (no websockets)
• Automatic Messenger window detection
• Real-time audio/video capture
• Simple, reliable operation

Output Files:
• Video frames: frame_XXXXXX_timestamp.jpg
• Audio: audio_timestamp.wav

For support, visit the documentation or report issues.
        """
        messagebox.showinfo("Help", help_text)
    
    def _show_settings(self):
        """Show settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.resizable(False, False)
        
        # Center the settings window
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Settings content
        ttk.Label(settings_window, text="Capture Settings", font=('Segoe UI', 12, 'bold')).pack(pady=20)
        
        # Frame rate setting
        frame_frame = ttk.Frame(settings_window)
        frame_frame.pack(fill=tk.X, padx=20, pady=10)
        ttk.Label(frame_frame, text="Frame Rate:").pack(side=tk.LEFT)
        frame_rate = ttk.Combobox(frame_frame, values=["10", "15", "20", "30"], state="readonly")
        frame_rate.set("15")
        frame_rate.pack(side=tk.RIGHT)
        
        # Quality setting
        quality_frame = ttk.Frame(settings_window)
        quality_frame.pack(fill=tk.X, padx=20, pady=10)
        ttk.Label(quality_frame, text="Quality:").pack(side=tk.LEFT)
        quality = ttk.Combobox(quality_frame, values=["Low", "Medium", "High"], state="readonly")
        quality.set("Medium")
        quality.pack(side=tk.RIGHT)
        
        # Audio setting
        audio_frame = ttk.Frame(settings_window)
        audio_frame.pack(fill=tk.X, padx=20, pady=10)
        audio_enabled = tk.BooleanVar(value=True)
        ttk.Checkbutton(audio_frame, text="Enable Audio Capture", variable=audio_enabled).pack(side=tk.LEFT)
        
        # Buttons
        button_frame = ttk.Frame(settings_window)
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        ttk.Button(button_frame, text="Save", command=settings_window.destroy).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Cancel", command=settings_window.destroy).pack(side=tk.RIGHT)
    
    def _clear_log(self):
        """Clear the log"""
        self.log_text.delete(1.0, tk.END)
    
    def _save_log(self):
        """Save log to file"""
        try:
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                with open(filename, 'w') as f:
                    f.write(self.log_text.get(1.0, tk.END))
                self._log_message(f"Log saved to {filename}")
        except Exception as e:
            self._log_message(f"Error saving log: {e}", "ERROR")
    
    def _open_docs(self):
        """Open documentation"""
        webbrowser.open("https://github.com/kgand/shellhacks25")
    
    def _report_issue(self):
        """Report an issue"""
        webbrowser.open("https://github.com/kgand/shellhacks25/issues")
    
    def _log_message(self, message, level="INFO"):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        
        # Color coding
        if level == "ERROR":
            self.log_text.tag_add("error", f"end-{len(log_entry)}c", tk.END)
            self.log_text.tag_config("error", foreground="red")
        elif level == "SUCCESS":
            self.log_text.tag_add("success", f"end-{len(log_entry)}c", tk.END)
            self.log_text.tag_config("success", foreground="green")
    
    def run(self):
        """Run the GUI"""
        self.root.mainloop()

def main():
    """Main function"""
    try:
        app = SimpleCaptureGUI()
        app.run()
    except Exception as e:
        print(f"Error starting GUI: {e}")

if __name__ == "__main__":
    main()
