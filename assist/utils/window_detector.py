"""
Cross-platform window detection system
Supports Windows, macOS, and Linux
"""

import os
import sys
import logging
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from .platform_utils import platform_detector

logger = logging.getLogger(__name__)

@dataclass
class WindowInfo:
    """Information about a detected window"""
    pid: int
    title: str
    x: int
    y: int
    width: int
    height: int
    is_messenger: bool = False

class CrossPlatformWindowDetector:
    """Cross-platform window detection"""
    
    def __init__(self):
        self.messenger_keywords = [
            'messenger.com',
            'facebook.com/messages',
            'messenger',
            'facebook messenger',
            'messenger call'
        ]
    
    def find_messenger_windows(self) -> List[WindowInfo]:
        """Find Messenger windows across all platforms"""
        if platform_detector.is_windows:
            return self._find_windows_windows()
        elif platform_detector.is_mac:
            return self._find_windows_mac()
        elif platform_detector.is_linux:
            return self._find_windows_linux()
        else:
            logger.warning(f"Unsupported platform: {platform_detector.get_platform_name()}")
            return []
    
    def _find_windows_windows(self) -> List[WindowInfo]:
        """Find windows on Windows"""
        windows = []
        try:
            import psutil
            import win32gui
            import win32process
            
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    # Check if it's a browser process
                    if any(browser in proc.info['name'].lower() for browser in ['chrome', 'firefox', 'edge', 'safari']):
                        # Get windows for this process
                        process_windows = self._get_windows_for_process_windows(proc.info['pid'])
                        for window in process_windows:
                            if self._is_messenger_window(window):
                                windows.append(window)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
        except ImportError:
            logger.warning("Windows-specific dependencies not available")
            # Fallback to basic detection
            windows = self._fallback_window_detection()
        except Exception as e:
            logger.error(f"Error finding windows on Windows: {e}")
            
        return windows
    
    def _find_windows_mac(self) -> List[WindowInfo]:
        """Find windows on macOS"""
        windows = []
        try:
            import psutil
            from AppKit import NSWorkspace, NSRunningApplication
            from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly, kCGNullWindowID
            
            # Get all running applications
            running_apps = NSWorkspace.sharedWorkspace().runningApplications()
            
            for app in running_apps:
                try:
                    if app.isActive() and app.localizedName():
                        app_name = app.localizedName().lower()
                        
                        # Check if it's a browser
                        if any(browser in app_name for browser in ['chrome', 'firefox', 'safari', 'edge']):
                            # Get window information
                            window_list = CGWindowListCopyWindowInfo(
                                kCGWindowListOptionOnScreenOnly, 
                                kCGNullWindowID
                            )
                            
                            for window in window_list:
                                if window.get('kCGWindowOwnerPID') == app.processIdentifier():
                                    title = window.get('kCGWindowName', '')
                                    bounds = window.get('kCGWindowBounds', {})
                                    
                                    if title and self._is_messenger_title(title):
                                        window_info = WindowInfo(
                                            pid=app.processIdentifier(),
                                            title=title,
                                            x=int(bounds.get('X', 0)),
                                            y=int(bounds.get('Y', 0)),
                                            width=int(bounds.get('Width', 0)),
                                            height=int(bounds.get('Height', 0)),
                                            is_messenger=True
                                        )
                                        windows.append(window_info)
                                        
                except Exception as e:
                    logger.debug(f"Error processing app {app.localizedName()}: {e}")
                    continue
                    
        except ImportError:
            logger.warning("macOS-specific dependencies not available")
            # Fallback to basic detection
            windows = self._fallback_window_detection()
        except Exception as e:
            logger.error(f"Error finding windows on macOS: {e}")
            
        return windows
    
    def _find_windows_linux(self) -> List[WindowInfo]:
        """Find windows on Linux"""
        windows = []
        try:
            import psutil
            from Xlib import display, X
            from Xlib.xobject.drawable import Window as XWindow
            
            # Connect to X server
            d = display.Display()
            root = d.screen().root
            
            # Get all windows
            window_list = root.query_tree().children
            
            for window in window_list:
                try:
                    # Get window attributes
                    attrs = window.get_attributes()
                    geometry = window.get_geometry()
                    
                    if attrs.map_state == X.IsViewable:
                        # Get window name
                        name = window.get_wm_name()
                        if name:
                            # Check if it's a browser window
                            if any(browser in name.lower() for browser in ['chrome', 'firefox', 'safari', 'edge']):
                                if self._is_messenger_title(name):
                                    # Get process ID (this is complex on Linux)
                                    pid = self._get_pid_for_window_linux(window)
                                    
                                    window_info = WindowInfo(
                                        pid=pid,
                                        title=name,
                                        x=geometry.x,
                                        y=geometry.y,
                                        width=geometry.width,
                                        height=geometry.height,
                                        is_messenger=True
                                    )
                                    windows.append(window_info)
                                    
                except Exception as e:
                    logger.debug(f"Error processing window: {e}")
                    continue
                    
        except ImportError:
            logger.warning("Linux-specific dependencies not available")
            # Fallback to basic detection
            windows = self._fallback_window_detection()
        except Exception as e:
            logger.error(f"Error finding windows on Linux: {e}")
            
        return windows
    
    def _get_windows_for_process_windows(self, pid: int) -> List[WindowInfo]:
        """Get windows for a process on Windows"""
        windows = []
        try:
            import win32gui
            import win32process
            
            def enum_windows_callback(hwnd, windows_list):
                if win32gui.IsWindowVisible(hwnd):
                    _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                    if found_pid == pid:
                        title = win32gui.GetWindowText(hwnd)
                        if title:
                            rect = win32gui.GetWindowRect(hwnd)
                            window_info = WindowInfo(
                                pid=pid,
                                title=title,
                                x=rect[0],
                                y=rect[1],
                                width=rect[2] - rect[0],
                                height=rect[3] - rect[1],
                                is_messenger=self._is_messenger_title(title)
                            )
                            windows_list.append(window_info)
                return True
            
            win32gui.EnumWindows(enum_windows_callback, windows)
            
        except Exception as e:
            logger.error(f"Error getting windows for process {pid}: {e}")
            
        return windows
    
    def _get_pid_for_window_linux(self, window) -> int:
        """Get process ID for a window on Linux (simplified)"""
        try:
            # This is a simplified approach - in practice, you'd need more complex logic
            return 0  # Placeholder
        except Exception:
            return 0
    
    def _fallback_window_detection(self) -> List[WindowInfo]:
        """Fallback window detection when platform-specific methods fail"""
        try:
            import pyautogui
            screen_width, screen_height = pyautogui.size()
            
            # Return a generic screen window
            return [WindowInfo(
                pid=0,
                title="Screen",
                x=0,
                y=0,
                width=screen_width,
                height=screen_height,
                is_messenger=False
            )]
        except Exception as e:
            logger.error(f"Fallback window detection failed: {e}")
            return []
    
    def _is_messenger_window(self, window: WindowInfo) -> bool:
        """Check if window is Messenger-related"""
        return self._is_messenger_title(window.title)
    
    def _is_messenger_title(self, title: str) -> bool:
        """Check if title contains Messenger keywords"""
        title_lower = title.lower()
        return any(keyword in title_lower for keyword in self.messenger_keywords)
