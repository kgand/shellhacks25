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
import cv2
import numpy as np
from PIL import Image, ImageTk
from screen_capture import SimpleCaptureSystem, WindowInfo

class CropDialog:
    """Interactive cropping dialog for selecting crop region"""
    
    def __init__(self, parent, frame_image, window_title="Select Crop Region"):
        self.parent = parent
        self.frame_image = frame_image
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(window_title)
        self.dialog.geometry("900x700")
        self.dialog.resizable(True, True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Configure window properties for better layering
        self.dialog.attributes('-topmost', True)
        self.dialog.attributes('-toolwindow', False)
        
        # Center the dialog properly
        self.dialog.update_idletasks()
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        # Calculate center position relative to parent
        x = parent_x + (parent_width // 2) - (900 // 2)
        y = parent_y + (parent_height // 2) - (700 // 2)
        
        # Ensure dialog is within screen bounds
        screen_width = self.dialog.winfo_screenwidth()
        screen_height = self.dialog.winfo_screenheight()
        x = max(0, min(x, screen_width - 900))
        y = max(0, min(y, screen_height - 700))
        
        self.dialog.geometry(f"900x700+{x}+{y}")
        
        # Ensure dialog stays on top and gets focus
        self.dialog.lift()
        self.dialog.focus_force()
        self.dialog.attributes('-topmost', False)  # Remove topmost after positioning
        
        # Crop region variables
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0
        self.drawing = False
        self.rect_id = None
        
        # Convert frame to display format
        self._prepare_display_image()
        
        # Create UI
        self._create_widgets()
        
        # Bind mouse events
        self.canvas.bind("<Button-1>", self._on_mouse_press)
        self.canvas.bind("<B1-Motion>", self._on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_mouse_release)
    
    def _prepare_display_image(self):
        """Prepare the frame image for display"""
        try:
            # Convert BGR to RGB if needed
            if len(self.frame_image.shape) == 3 and self.frame_image.shape[2] == 3:
                display_image = cv2.cvtColor(self.frame_image, cv2.COLOR_BGR2RGB)
            else:
                display_image = self.frame_image.copy()
            
            # Resize image to fit dialog if too large
            height, width = display_image.shape[:2]
            max_width, max_height = 700, 500
            
            if width > max_width or height > max_height:
                scale = min(max_width / width, max_height / height)
                new_width = int(width * scale)
                new_height = int(height * scale)
                display_image = cv2.resize(display_image, (new_width, new_height))
                self.scale_factor = scale
            else:
                self.scale_factor = 1.0
            
            # Convert to PIL Image for tkinter
            self.pil_image = Image.fromarray(display_image)
            self.tk_image = ImageTk.PhotoImage(self.pil_image)
            
        except Exception as e:
            print(f"Error preparing display image: {e}")
            # Create a placeholder image
            self.pil_image = Image.new('RGB', (400, 300), color='gray')
            self.tk_image = ImageTk.PhotoImage(self.pil_image)
            self.scale_factor = 1.0
    
    def _create_widgets(self):
        """Create the dialog widgets"""
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.rowconfigure(1, weight=1)  # Make canvas expandable
        main_frame.columnconfigure(0, weight=1)
        
        # Instructions
        instructions = ttk.Label(main_frame, text="Click and drag to select the area you want to capture:", 
                                font=('Segoe UI', 11, 'bold'))
        instructions.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Canvas for image display with scrollbars
        canvas_container = ttk.Frame(main_frame)
        canvas_container.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        canvas_container.rowconfigure(0, weight=1)
        canvas_container.columnconfigure(0, weight=1)
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(canvas_container, orient=tk.VERTICAL)
        h_scrollbar = ttk.Scrollbar(canvas_container, orient=tk.HORIZONTAL)
        
        self.canvas = tk.Canvas(canvas_container, bg='white', 
                              yscrollcommand=v_scrollbar.set, 
                              xscrollcommand=h_scrollbar.set)
        
        self.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        v_scrollbar.config(command=self.canvas.yview)
        h_scrollbar.config(command=self.canvas.xview)
        
        # Display the image
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        
        # Buttons frame - fixed at bottom with better layout
        button_frame = ttk.LabelFrame(main_frame, text="Actions", padding="10")
        button_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        button_frame.columnconfigure(0, weight=1)
        
        # Top row with crop info
        info_frame = ttk.Frame(button_frame)
        info_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        info_frame.columnconfigure(0, weight=1)
        
        self.crop_info = ttk.Label(info_frame, text="No selection made - click and drag to select area", 
                                  font=('Segoe UI', 10))
        self.crop_info.grid(row=0, column=0, sticky=tk.W)
        
        # Bottom row with buttons
        button_row = ttk.Frame(button_frame)
        button_row.grid(row=1, column=0, sticky=(tk.W, tk.E))
        button_row.columnconfigure(0, weight=1)
        
        # Buttons on the right
        button_container = ttk.Frame(button_row)
        button_container.grid(row=0, column=1, sticky=tk.E)
        
        apply_btn = ttk.Button(button_container, text="✓ Apply Crop", command=self._apply_crop, 
                              style='Start.TButton')
        apply_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        cancel_btn = ttk.Button(button_container, text="✗ Cancel", command=self._cancel)
        cancel_btn.pack(side=tk.RIGHT)
    
    def _on_mouse_press(self, event):
        """Handle mouse press"""
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.drawing = True
        
        # Remove previous rectangle
        if self.rect_id:
            self.canvas.delete(self.rect_id)
    
    def _on_mouse_drag(self, event):
        """Handle mouse drag"""
        if not self.drawing:
            return
        
        self.end_x = self.canvas.canvasx(event.x)
        self.end_y = self.canvas.canvasy(event.y)
        
        # Remove previous rectangle
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        
        # Draw new rectangle
        self.rect_id = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.end_x, self.end_y,
            outline='red', width=2
        )
        
        # Update crop info
        width = abs(self.end_x - self.start_x)
        height = abs(self.end_y - self.start_y)
        self.crop_info.config(text=f"Selection: {int(width)}x{int(height)} pixels - Release to confirm")
    
    def _on_mouse_release(self, event):
        """Handle mouse release"""
        if not self.drawing:
            return
        
        self.drawing = False
        self.end_x = self.canvas.canvasx(event.x)
        self.end_y = self.canvas.canvasy(event.y)
        
        # Update crop info to show final selection
        width = abs(self.end_x - self.start_x)
        height = abs(self.end_y - self.start_y)
        if width > 0 and height > 0:
            self.crop_info.config(text=f"Selected: {int(width)}x{int(height)} pixels - Click 'Apply Crop' to confirm")
        else:
            self.crop_info.config(text="No selection made - click and drag to select area")
    
    def _apply_crop(self):
        """Apply the crop selection"""
        if not self.rect_id:
            messagebox.showwarning("No Selection", "Please select an area to crop.")
            return
        
        # Calculate crop region in original image coordinates
        x1 = min(self.start_x, self.end_x)
        y1 = min(self.start_y, self.end_y)
        x2 = max(self.start_x, self.end_x)
        y2 = max(self.start_y, self.end_y)
        
        # Convert to original image coordinates
        x1 = int(x1 / self.scale_factor)
        y1 = int(y1 / self.scale_factor)
        x2 = int(x2 / self.scale_factor)
        y2 = int(y2 / self.scale_factor)
        
        width = x2 - x1
        height = y2 - y1
        
        if width <= 0 or height <= 0:
            messagebox.showwarning("Invalid Selection", "Please select a valid area.")
            return
        
        self.result = (x1, y1, width, height)
        self.dialog.destroy()
    
    def _cancel(self):
        """Cancel cropping"""
        self.result = None
        self.dialog.destroy()

class SimpleCaptureGUI:
    """Simplified GUI for the screen capture system"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Messenger AI Assistant - Screen Capture")
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
        title_label = ttk.Label(header_frame, text="Messenger AI Assistant", style='Title.TLabel')
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # Subtitle
        subtitle_label = ttk.Label(header_frame, text="Screen Capture & AI Analysis", style='Subtitle.TLabel')
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
        
        self.realtime_status = ttk.Label(status_frame, text="Real-time: Ready", style='Info.TLabel')
        self.realtime_status.grid(row=3, column=0, sticky=tk.W, pady=(2, 0))
        
        # Test button
        test_button = ttk.Button(status_frame, text="Test System", command=self._test_system)
        test_button.grid(row=0, column=1, rowspan=4, sticky=tk.E, padx=(20, 0))
    
    def _create_window_section(self, parent):
        """Create window selection section"""
        window_frame = ttk.LabelFrame(parent, text="Select Messenger Window & Tab", padding="15")
        window_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        window_frame.columnconfigure(0, weight=1)
        window_frame.rowconfigure(3, weight=1)
        
        # Window list
        list_frame = ttk.Frame(window_frame)
        list_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        
        self.window_listbox = tk.Listbox(list_frame, height=4, font=('Segoe UI', 9))
        self.window_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.window_listbox.bind('<<ListboxSelect>>', self._on_window_select)
        
        # Scrollbar for listbox
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.window_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.window_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Tab selection
        tab_frame = ttk.Frame(window_frame)
        tab_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        tab_frame.columnconfigure(1, weight=1)
        
        ttk.Label(tab_frame, text="Select Tab:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.tab_combobox = ttk.Combobox(tab_frame, state="readonly", width=40)
        self.tab_combobox.grid(row=0, column=1, sticky=(tk.W, tk.E))
        self.tab_combobox.bind('<<ComboboxSelected>>', self._on_tab_select)
        
        # Add default tab options
        self.tab_combobox['values'] = ('Select a tab...', 'Video Call', 'Chat', 'Group Chat', 'Other')
        self.tab_combobox.set('Select a tab...')
        
        # Refresh button
        refresh_button = ttk.Button(tab_frame, text="🔄 Refresh", command=self._refresh_windows)
        refresh_button.grid(row=0, column=2, padx=(10, 0))
        
        # Window info
        self.window_info = ttk.Label(window_frame, text="No window selected", style='Info.TLabel')
        self.window_info.grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
        
        # Crop status
        self.crop_status = ttk.Label(window_frame, text="No crop region set", style='Info.TLabel')
        self.crop_status.grid(row=3, column=0, sticky=tk.W, pady=(5, 0))
        
        # Buttons
        button_frame = ttk.Frame(window_frame)
        button_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
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
        
        # Add real-time output button (manual control)
        self.realtime_output_button = ttk.Button(button_frame, text="📊 View Real-time Output", command=self._show_realtime_output)
        self.realtime_output_button.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Progress bar
        self.progress = ttk.Progressbar(control_frame, mode='indeterminate')
        self.progress.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(15, 0))
        
        # Status info
        self.capture_info = ttk.Label(control_frame, text="Ready to capture", style='Info.TLabel')
        self.capture_info.grid(row=3, column=0, sticky=tk.W, pady=(10, 0))
    
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
    
    def _on_tab_select(self, event):
        """Handle tab selection"""
        selected_tab = self.tab_combobox.get()
        if selected_tab and selected_tab != 'Select a tab...':
            self._log_message(f"Selected tab: {selected_tab}")
            # Update window info to show selected tab
            if self.capture_system.selected_window:
                self.window_info.config(text=f"Selected: {self.capture_system.selected_window.title} - {selected_tab}")
                # Trigger cropping dialog after tab selection
                self._show_crop_dialog()
    
    def _refresh_windows(self):
        """Refresh the window list"""
        self._log_message("Refreshing window list...")
        self._update_window_list()
    
    def _capture_preview_frame(self):
        """Capture a preview frame for cropping"""
        try:
            if not self.capture_system.selected_window:
                return None
            
            import mss
            import numpy as np
            
            # Define capture region - same as in screen capture
            monitor = {
                "top": self.capture_system.selected_window.y + 80,
                "left": self.capture_system.selected_window.x + 30,
                "width": self.capture_system.selected_window.width - 60,
                "height": self.capture_system.selected_window.height - 150
            }
            
            # Capture frame
            with mss.mss() as mss_instance:
                screenshot = mss_instance.grab(monitor)
                frame = np.array(screenshot)
            
            # Convert BGRA to BGR if needed
            if len(frame.shape) == 3 and frame.shape[2] == 4:
                frame = frame[:, :, :3]
            
            return frame
            
        except Exception as e:
            self._log_message(f"Error capturing preview frame: {e}", "ERROR")
            return None
    
    def _show_crop_dialog(self):
        """Show the cropping dialog"""
        try:
            # Capture a preview frame
            preview_frame = self._capture_preview_frame()
            if preview_frame is None:
                messagebox.showerror("Error", "Could not capture preview frame. Please try again.")
                return
            
            # Show cropping dialog
            crop_dialog = CropDialog(self.root, preview_frame, "Select Crop Region for Messenger Tab")
            
            # Wait for dialog to close
            self.root.wait_window(crop_dialog.dialog)
            
            # Get crop result
            if crop_dialog.result:
                x, y, width, height = crop_dialog.result
                self.capture_system.set_crop_region(x, y, width, height)
                self._log_message(f"Crop region set: {width}x{height} at ({x}, {y})")
                self.crop_status.config(text=f"Crop region set: {width}x{height} pixels", style='Status.TLabel')
                messagebox.showinfo("Crop Set", f"Crop region set to {width}x{height} pixels.\nYou can now start capture.")
            else:
                self._log_message("Crop selection cancelled")
                self.crop_status.config(text="No crop region set", style='Info.TLabel')
                
        except Exception as e:
            self._log_message(f"Error showing crop dialog: {e}", "ERROR")
            messagebox.showerror("Error", f"Error showing crop dialog: {e}")
    
    def _start_capture(self):
        """Start screen capture"""
        if not self.capture_system.selected_window:
            messagebox.showwarning("No Window Selected", "Please select a Messenger window first.")
            return
        
        # Check if crop region is set
        if not self.capture_system.get_crop_region():
            messagebox.showwarning("No Crop Region Set", "Please select a tab and set up the crop region first.")
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
        
        # Automatically start AI analysis when capture starts
        self._start_ai_analysis_auto()
    
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
            
            # Automatically stop AI analysis when capture stops
            self._stop_ai_analysis_auto()
            
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
            
            # Test real-time analysis
            try:
                import requests
                response = requests.get("http://127.0.0.1:8000/health", timeout=5)
                if response.status_code == 200:
                    self.realtime_status.config(text="Real-time: Server Ready ✓", style='Status.TLabel')
                else:
                    self.realtime_status.config(text="Real-time: Server Error", style='Error.TLabel')
            except:
                self.realtime_status.config(text="Real-time: Server Offline", style='Error.TLabel')
            
            # Test windows
            windows = self.capture_system.find_windows()
            self._log_message(f"System test: Audio={audio_available}, Video=Ready, Real-time=Server, Windows={len(windows)}")
            
        except Exception as e:
            self._log_message(f"System test failed: {e}", "ERROR")
    
    def _process_captured_files(self):
        """Manually trigger processing of captured files"""
        try:
            self._log_message("Triggering manual processing of captured files...")
            
            # Call the auto-process method
            self.capture_system._auto_process_captured_files()
            
            self._log_message("Manual processing completed", "SUCCESS")
            
        except Exception as e:
            self._log_message(f"Error in manual processing: {e}", "ERROR")
    
    def _start_ai_analysis_auto(self):
        """Automatically start AI analysis when capture starts"""
        try:
            self._log_message("Auto-starting AI analysis...")
            
            # Check if server is running
            import requests
            try:
                response = requests.get("http://127.0.0.1:8000/health", timeout=5)
                if response.status_code != 200:
                    self._log_message("Server is not running. Please start the server first.", "ERROR")
                    return
            except:
                self._log_message("Cannot connect to server. Please start the server first.", "ERROR")
                return
            
            # Create a session for AI analysis
            session_data = {"ai_analysis": True, "timestamp": datetime.now().isoformat()}
            session_response = requests.post("http://127.0.0.1:8000/sessions", json=session_data)
            
            if session_response.status_code == 200:
                session_id = session_response.json()["session_id"]
                self._log_message(f"Created AI analysis session: {session_id}")
                
                # Start real-time analysis
                analysis_response = requests.post(f"http://127.0.0.1:8000/start-analysis/{session_id}")
                
                if analysis_response.status_code == 200:
                    self._log_message("AI analysis started automatically", "SUCCESS")
                    self.capture_info.config(text="AI analysis in progress...")
                    self.realtime_status.config(text="Real-time: Analysis Active ✓", style='Status.TLabel')
                    
                    # Start monitoring analysis in background
                    self._monitor_ai_analysis(session_id)
                    
                    # Auto-open real-time output window
                    self._show_realtime_output_auto()
                else:
                    self._log_message(f"Failed to start AI analysis: {analysis_response.status_code}", "ERROR")
            else:
                self._log_message(f"Failed to create session: {session_response.status_code}", "ERROR")
                
        except Exception as e:
            self._log_message(f"Error starting AI analysis: {e}", "ERROR")
    
    def _stop_ai_analysis_auto(self):
        """Automatically stop AI analysis when capture stops"""
        try:
            import requests
            
            # Stop real-time analysis
            response = requests.post("http://127.0.0.1:8000/stop-analysis", timeout=5)
            
            if response.status_code == 200:
                self._log_message("AI analysis stopped automatically", "SUCCESS")
                self.capture_info.config(text="AI analysis stopped")
                self.realtime_status.config(text="Real-time: Ready", style='Info.TLabel')
                
                # Auto-close real-time output window
                self._close_realtime_output_auto()
            else:
                self._log_message(f"Failed to stop AI analysis: {response.status_code}", "ERROR")
                
        except Exception as e:
            self._log_message(f"Error stopping AI analysis: {e}", "ERROR")
    
    def _start_ai_analysis(self):
        """Start AI analysis of captured content (manual)"""
        try:
            self._log_message("Starting AI analysis...")
            
            # Check if server is running
            import requests
            try:
                response = requests.get("http://127.0.0.1:8000/health", timeout=5)
                if response.status_code != 200:
                    self._log_message("Server is not running. Please start the server first.", "ERROR")
                    return
            except:
                self._log_message("Cannot connect to server. Please start the server first.", "ERROR")
                return
            
            # Create a session for AI analysis
            session_data = {"ai_analysis": True, "timestamp": datetime.now().isoformat()}
            session_response = requests.post("http://127.0.0.1:8000/sessions", json=session_data)
            
            if session_response.status_code == 200:
                session_id = session_response.json()["session_id"]
                self._log_message(f"Created AI analysis session: {session_id}")
                
                # Start real-time analysis
                analysis_response = requests.post(f"http://127.0.0.1:8000/start-analysis/{session_id}")
                
                if analysis_response.status_code == 200:
                    self._log_message("AI analysis started successfully", "SUCCESS")
                    self.capture_info.config(text="AI analysis in progress...")
                    self.realtime_status.config(text="Real-time: Analysis Active ✓", style='Status.TLabel')
                    
                    # Start monitoring analysis in background
                    self._monitor_ai_analysis(session_id)
                else:
                    self._log_message(f"Failed to start AI analysis: {analysis_response.status_code}", "ERROR")
            else:
                self._log_message(f"Failed to create session: {session_response.status_code}", "ERROR")
                
        except Exception as e:
            self._log_message(f"Error starting AI analysis: {e}", "ERROR")
    
    def _monitor_ai_analysis(self, session_id):
        """Monitor AI analysis progress"""
        def monitor_thread():
            try:
                import requests
                import time
                
                while True:
                    # Check analysis status
                    status_response = requests.get("http://127.0.0.1:8000/analysis-status")
                    if status_response.status_code == 200:
                        status = status_response.json()
                        analysis = status.get("analysis", {})
                        
                        # Update GUI with analysis results
                        frame_count = analysis.get("frame_analyses", 0)
                        audio_count = analysis.get("audio_analyses", 0)
                        summary = analysis.get("summary", "")
                        realtime_outputs_count = analysis.get("realtime_outputs_count", 0)
                        
                        self.root.after(0, lambda: self._update_analysis_display(
                            frame_count, audio_count, summary, realtime_outputs_count
                        ))
                        
                        # Check for latest real-time output
                        latest_output = analysis.get("latest_realtime_output")
                        if latest_output:
                            self.root.after(0, lambda: self._display_latest_realtime_output(latest_output))
                        
                        # Check if we have a comprehensive summary
                        comprehensive = analysis.get("comprehensive_summary")
                        if comprehensive:
                            self.root.after(0, lambda: self._display_comprehensive_summary(comprehensive))
                            break
                    
                    time.sleep(2)  # Check every 2 seconds for more responsive updates
                    
            except Exception as e:
                self.root.after(0, lambda: self._log_message(f"Error monitoring AI analysis: {e}", "ERROR"))
        
        # Start monitoring in background thread
        import threading
        monitor_thread_obj = threading.Thread(target=monitor_thread, daemon=True)
        monitor_thread_obj.start()
    
    def _update_analysis_display(self, frame_count, audio_count, summary, realtime_outputs_count=0):
        """Update the analysis display"""
        self.capture_info.config(text=f"AI Analysis: {frame_count} frames, {audio_count} audio files, {realtime_outputs_count} real-time outputs")
        
        if summary:
            self._log_message(f"Analysis Summary: {summary[:100]}...")
    
    def _display_latest_realtime_output(self, latest_output):
        """Display the latest real-time output in the log"""
        try:
            output_type = latest_output.get("type", "unknown")
            content = latest_output.get("content", "No content")
            timestamp = latest_output.get("timestamp", "Unknown")
            
            # Truncate content for log display
            display_content = content[:150] + "..." if len(content) > 150 else content
            
            self._log_message(f"🤖 Real-time {output_type}: {display_content}")
            
        except Exception as e:
            self._log_message(f"Error displaying latest real-time output: {e}", "ERROR")
    
    def _display_comprehensive_summary(self, comprehensive_summary):
        """Display comprehensive summary"""
        try:
            if isinstance(comprehensive_summary, dict):
                overall = comprehensive_summary.get("overall_summary", "No summary available")
                summaries = comprehensive_summary.get("summaries", {})
                
                self._log_message("🎉 AI Analysis Complete!", "SUCCESS")
                self._log_message(f"Overall Summary: {overall}")
                
                if summaries.get("brief"):
                    self._log_message(f"Brief: {summaries['brief']}")
                if summaries.get("key_points"):
                    self._log_message(f"Key Points: {summaries['key_points']}")
                
                self.capture_info.config(text="AI analysis completed successfully")
            else:
                self._log_message("AI analysis completed", "SUCCESS")
                self.capture_info.config(text="AI analysis completed")
                
        except Exception as e:
            self._log_message(f"Error displaying summary: {e}", "ERROR")
    
    def _show_realtime_output(self):
        """Show real-time output window"""
        try:
            # Create real-time output window
            self.realtime_window = tk.Toplevel(self.root)
            self.realtime_window.title("Real-time AI Analysis Output")
            self.realtime_window.geometry("800x600")
            self.realtime_window.resizable(True, True)
            self.realtime_window.transient(self.root)
            
            # Center the window
            self.realtime_window.update_idletasks()
            x = (self.realtime_window.winfo_screenwidth() // 2) - (800 // 2)
            y = (self.realtime_window.winfo_screenheight() // 2) - (600 // 2)
            self.realtime_window.geometry(f"800x600+{x}+{y}")
            
            # Create main frame
            main_frame = ttk.Frame(self.realtime_window, padding="15")
            main_frame.pack(fill=tk.BOTH, expand=True)
            main_frame.rowconfigure(1, weight=1)
            main_frame.columnconfigure(0, weight=1)
            
            # Header
            header_frame = ttk.Frame(main_frame)
            header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
            header_frame.columnconfigure(1, weight=1)
            
            title_label = ttk.Label(header_frame, text="Real-time AI Analysis Output", 
                                 font=('Segoe UI', 14, 'bold'))
            title_label.grid(row=0, column=0, sticky=tk.W)
            
            # Control buttons
            button_frame = ttk.Frame(header_frame)
            button_frame.grid(row=0, column=1, sticky=tk.E)
            
            refresh_button = ttk.Button(button_frame, text="🔄 Refresh", command=self._refresh_realtime_output)
            refresh_button.grid(row=0, column=0, padx=(0, 10))
            
            clear_button = ttk.Button(button_frame, text="🗑️ Clear", command=self._clear_realtime_output)
            clear_button.grid(row=0, column=1)
            
            # Output display area
            output_frame = ttk.LabelFrame(main_frame, text="Live Analysis Output", padding="10")
            output_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
            output_frame.rowconfigure(0, weight=1)
            output_frame.columnconfigure(0, weight=1)
            
            # Text area with scrollbar
            text_frame = ttk.Frame(output_frame)
            text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            text_frame.rowconfigure(0, weight=1)
            text_frame.columnconfigure(0, weight=1)
            
            self.realtime_text = scrolledtext.ScrolledText(text_frame, height=20, font=('Consolas', 10), 
                                                         wrap=tk.WORD, state=tk.DISABLED)
            self.realtime_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            # Status bar
            status_frame = ttk.Frame(main_frame)
            status_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
            status_frame.columnconfigure(0, weight=1)
            
            self.realtime_status = ttk.Label(status_frame, text="Ready to display real-time output", 
                                           font=('Segoe UI', 9))
            self.realtime_status.grid(row=0, column=0, sticky=tk.W)
            
            # Auto-refresh checkbox
            self.auto_refresh_var = tk.BooleanVar(value=True)
            auto_refresh_check = ttk.Checkbutton(status_frame, text="Auto-refresh", 
                                               variable=self.auto_refresh_var)
            auto_refresh_check.grid(row=0, column=1, sticky=tk.E)
            
            # Load initial data
            self._refresh_realtime_output()
            
            # Start auto-refresh if enabled
            if self.auto_refresh_var.get():
                self._start_auto_refresh()
                
        except Exception as e:
            self._log_message(f"Error showing real-time output: {e}", "ERROR")
            messagebox.showerror("Error", f"Error showing real-time output: {e}")
    
    def _refresh_realtime_output(self):
        """Refresh real-time output display"""
        try:
            import requests
            
            # Get real-time outputs from server
            response = requests.get("http://127.0.0.1:8000/realtime-outputs?limit=100", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                outputs = data.get("outputs", [])
                
                # Clear and update text
                self.realtime_text.config(state=tk.NORMAL)
                self.realtime_text.delete(1.0, tk.END)
                
                if outputs:
                    for output in outputs:
                        timestamp = output.get("timestamp", "Unknown")
                        output_type = output.get("type", "unknown")
                        content = output.get("content", "No content")
                        
                        # Format output
                        formatted_output = f"[{timestamp}] {output_type.upper()}: {content}\n\n"
                        self.realtime_text.insert(tk.END, formatted_output)
                    
                    self.realtime_text.see(tk.END)
                    self.realtime_status.config(text=f"Displaying {len(outputs)} real-time outputs")
                else:
                    self.realtime_text.insert(tk.END, "No real-time outputs available yet.\nStart AI analysis to see live output.")
                    self.realtime_status.config(text="No real-time outputs available")
                
                self.realtime_text.config(state=tk.DISABLED)
                
            else:
                self.realtime_status.config(text=f"Error fetching outputs: {response.status_code}")
                
        except Exception as e:
            self.realtime_status.config(text=f"Error: {e}")
    
    def _clear_realtime_output(self):
        """Clear real-time outputs"""
        try:
            import requests
            
            response = requests.post("http://127.0.0.1:8000/clear-realtime-outputs", timeout=5)
            
            if response.status_code == 200:
                self._refresh_realtime_output()
                self._log_message("Real-time outputs cleared", "SUCCESS")
            else:
                self._log_message(f"Error clearing outputs: {response.status_code}", "ERROR")
                
        except Exception as e:
            self._log_message(f"Error clearing real-time outputs: {e}", "ERROR")
    
    def _start_auto_refresh(self):
        """Start auto-refresh for real-time output"""
        if hasattr(self, 'realtime_window') and self.realtime_window.winfo_exists():
            if self.auto_refresh_var.get():
                self._refresh_realtime_output()
                # Schedule next refresh
                self.realtime_window.after(2000, self._start_auto_refresh)  # Refresh every 2 seconds
    
    def _show_realtime_output_auto(self):
        """Automatically show real-time output window when capture starts"""
        try:
            # Only show if not already open
            if not hasattr(self, 'realtime_window') or not self.realtime_window.winfo_exists():
                self._show_realtime_output()
                self._log_message("Real-time output window opened automatically")
        except Exception as e:
            self._log_message(f"Error auto-opening real-time window: {e}", "ERROR")
    
    def _close_realtime_output_auto(self):
        """Automatically close real-time output window when capture stops"""
        try:
            if hasattr(self, 'realtime_window') and self.realtime_window.winfo_exists():
                self.realtime_window.destroy()
                self._log_message("Real-time output window closed automatically")
        except Exception as e:
            self._log_message(f"Error auto-closing real-time window: {e}", "ERROR")
    
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
Messenger AI Assistant - Screen Capture

This application captures audio and video from Messenger Web conversations and processes them with AI for analysis, summarization, and memory storage.

How to use:
1. Open Messenger Web in your browser
2. Select a Messenger window from the list
3. Click 'Start Capture' to begin recording
4. Files are saved to the 'capture_output' folder
5. Click 'Stop Capture' when finished

Features:
• AI-powered conversation analysis
• Automatic Messenger window detection
• Real-time audio/video capture
• Memory storage and retrieval
• Clean interface

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
