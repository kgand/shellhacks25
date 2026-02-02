"""
Screen capture module for Messenger AI Assistant
Replaces Chrome extension with Python-based screen capture
"""

from .screen_detector import ScreenCapture, ScreenDetector, AudioCapture
from .gui import ScreenCaptureGUI

__all__ = ['ScreenCapture', 'ScreenDetector', 'AudioCapture', 'ScreenCaptureGUI']
