"""
Platform utilities for cross-platform compatibility
Handles Windows, macOS, and Linux differences
"""

import os
import sys
import platform
import subprocess
from typing import List, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class PlatformDetector:
    """Detects and provides platform-specific functionality"""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.is_windows = self.system == 'windows'
        self.is_mac = self.system == 'darwin'
        self.is_linux = self.system == 'linux'
        
    def get_platform_name(self) -> str:
        """Get human-readable platform name"""
        if self.is_windows:
            return "Windows"
        elif self.is_mac:
            return "macOS"
        elif self.is_linux:
            return "Linux"
        else:
            return "Unknown"
    
    def open_file_manager(self, path: str) -> bool:
        """Open file manager at specified path"""
        try:
            if self.is_windows:
                os.startfile(path)
            elif self.is_mac:
                subprocess.run(['open', path])
            elif self.is_linux:
                subprocess.run(['xdg-open', path])
            else:
                return False
            return True
        except Exception as e:
            logger.error(f"Error opening file manager: {e}")
            return False
    
    def get_browser_command(self) -> List[str]:
        """Get command to open browser"""
        if self.is_windows:
            return ['start', 'https://messenger.com']
        elif self.is_mac:
            return ['open', 'https://messenger.com']
        elif self.is_linux:
            return ['xdg-open', 'https://messenger.com']
        else:
            return ['python', '-m', 'webbrowser', 'https://messenger.com']
    
    def get_audio_dependencies(self) -> List[str]:
        """Get platform-specific audio dependencies"""
        if self.is_windows:
            return ['sounddevice', 'pyaudio']
        elif self.is_mac:
            return ['sounddevice', 'pyaudio']
        elif self.is_linux:
            return ['sounddevice', 'pyaudio']
        else:
            return ['sounddevice']
    
    def get_screen_capture_dependencies(self) -> List[str]:
        """Get platform-specific screen capture dependencies"""
        base_deps = ['opencv-python', 'mss', 'numpy', 'Pillow', 'pyautogui', 'psutil']
        
        if self.is_windows:
            return base_deps + ['pywin32']
        elif self.is_mac:
            return base_deps + ['pyobjc-framework-Quartz', 'pyobjc-framework-Cocoa']
        elif self.is_linux:
            return base_deps + ['python3-xlib']
        else:
            return base_deps

# Global platform detector instance
platform_detector = PlatformDetector()
