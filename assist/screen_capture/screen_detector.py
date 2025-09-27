"""
Screen detection and capture module for Messenger Web
Replaces Chrome extension with Python-based screen capture
"""

import cv2
import numpy as np
import pyautogui
import psutil
import time
import asyncio
import logging
from typing import Optional, Tuple, List, Dict, Any
from dataclasses import dataclass
from datetime import datetime
import json
import websockets
import threading
from PIL import Image
import mss
import pyaudio
import wave
import io

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

class ScreenDetector:
    """Detects and captures Messenger Web windows"""
    
    def __init__(self):
        self.messenger_keywords = [
            'messenger.com',
            'facebook.com/messages',
            'messenger',
            'facebook messenger'
        ]
        self.capture_region = None
        self.is_capturing = False
        self.screen_capture = mss.mss()
        
    def find_messenger_windows(self) -> List[WindowInfo]:
        """Find all Messenger-related windows"""
        messenger_windows = []
        
        try:
            # Get all processes
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    # Check if it's a browser process
                    if any(browser in proc.info['name'].lower() for browser in ['chrome', 'firefox', 'edge', 'safari']):
                        # Try to get window information (Windows-specific)
                        windows = self._get_windows_for_process(proc.info['pid'])
                        for window in windows:
                            if self._is_messenger_window(window):
                                messenger_windows.append(window)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
        except Exception as e:
            logger.error(f"Error finding messenger windows: {e}")
            
        return messenger_windows
    
    def _get_windows_for_process(self, pid: int) -> List[WindowInfo]:
        """Get window information for a process (Windows-specific)"""
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
                                height=rect[3] - rect[1]
                            )
                            windows_list.append(window_info)
                return True
            
            win32gui.EnumWindows(enum_windows_callback, windows)
            
        except ImportError:
            logger.warning("win32gui not available, using fallback method")
            # Fallback: use pyautogui to get screen info
            screen_width, screen_height = pyautogui.size()
            windows.append(WindowInfo(
                pid=pid,
                title="Screen",
                x=0,
                y=0,
                width=screen_width,
                height=screen_height
            ))
        except Exception as e:
            logger.error(f"Error getting windows for process {pid}: {e}")
            
        return windows
    
    def _is_messenger_window(self, window: WindowInfo) -> bool:
        """Check if a window is Messenger-related"""
        title_lower = window.title.lower()
        return any(keyword in title_lower for keyword in self.messenger_keywords)
    
    def select_capture_region(self, window: WindowInfo) -> Optional[Tuple[int, int, int, int]]:
        """Select capture region for a window"""
        try:
            # Return window coordinates
            return (window.x, window.y, window.width, window.height)
        except Exception as e:
            logger.error(f"Error selecting capture region: {e}")
            return None

class AudioCapture:
    """Captures system audio"""
    
    def __init__(self, sample_rate: int = 44100, channels: int = 2):
        self.sample_rate = sample_rate
        self.channels = channels
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.is_recording = False
        self.audio_buffer = []
        
    def start_recording(self):
        """Start audio recording"""
        try:
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=1024
            )
            self.is_recording = True
            logger.info("Audio recording started")
        except Exception as e:
            logger.error(f"Failed to start audio recording: {e}")
            
    def stop_recording(self):
        """Stop audio recording"""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        self.is_recording = False
        logger.info("Audio recording stopped")
        
    def get_audio_data(self) -> bytes:
        """Get audio data from stream"""
        if self.stream and self.is_recording:
            try:
                data = self.stream.read(1024, exception_on_overflow=False)
                return data
            except Exception as e:
                logger.error(f"Error reading audio data: {e}")
                return b''
        return b''

class ScreenCapture:
    """Main screen capture class that coordinates video and audio capture"""
    
    def __init__(self, backend_url: str = "ws://127.0.0.1:8000/ingest"):
        self.detector = ScreenDetector()
        self.audio_capture = AudioCapture()
        self.backend_url = backend_url
        self.websocket = None
        self.is_capturing = False
        self.capture_thread = None
        self.selected_window = None
        
    async def initialize(self):
        """Initialize the capture system"""
        logger.info("Initializing screen capture system...")
        
        # Find Messenger windows
        messenger_windows = self.detector.find_messenger_windows()
        if not messenger_windows:
            logger.warning("No Messenger windows found")
            return False
            
        # Select the first Messenger window
        self.selected_window = messenger_windows[0]
        logger.info(f"Selected window: {self.selected_window.title}")
        
        return True
    
    async def start_capture(self):
        """Start capturing screen and audio"""
        if self.is_capturing:
            logger.warning("Capture already in progress")
            return False
            
        try:
            # Connect to backend
            await self._connect_to_backend()
            
            # Start audio capture
            self.audio_capture.start_recording()
            
            # Start capture thread
            self.is_capturing = True
            self.capture_thread = threading.Thread(target=self._capture_loop)
            self.capture_thread.start()
            
            logger.info("Screen capture started")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start capture: {e}")
            return False
    
    async def stop_capture(self):
        """Stop capturing"""
        if not self.is_capturing:
            return
            
        self.is_capturing = False
        
        # Stop audio capture
        self.audio_capture.stop_recording()
        
        # Wait for capture thread to finish
        if self.capture_thread:
            self.capture_thread.join()
            
        # Close WebSocket connection
        if self.websocket:
            await self.websocket.close()
            
        logger.info("Screen capture stopped")
    
    async def _connect_to_backend(self):
        """Connect to the FastAPI backend"""
        try:
            self.websocket = await websockets.connect(self.backend_url)
            logger.info("Connected to backend")
        except Exception as e:
            logger.error(f"Failed to connect to backend: {e}")
            raise
    
    def _capture_loop(self):
        """Main capture loop (runs in separate thread)"""
        frame_count = 0
        
        while self.is_capturing:
            try:
                # Capture screen frame
                if self.selected_window:
                    frame = self._capture_screen_frame()
                    if frame is not None:
                        # Send frame to backend
                        asyncio.run(self._send_frame(frame, frame_count))
                        frame_count += 1
                
                # Capture audio data
                audio_data = self.audio_capture.get_audio_data()
                if audio_data:
                    asyncio.run(self._send_audio(audio_data))
                
                # Small delay to prevent overwhelming the system
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error in capture loop: {e}")
                time.sleep(1)
    
    def _capture_screen_frame(self) -> Optional[np.ndarray]:
        """Capture a single screen frame"""
        try:
            if not self.selected_window:
                return None
                
            # Capture screen region
            monitor = {
                "top": self.selected_window.y,
                "left": self.selected_window.x,
                "width": self.selected_window.width,
                "height": self.selected_window.height
            }
            
            screenshot = self.detector.screen_capture.grab(monitor)
            frame = np.array(screenshot)
            
            # Convert BGRA to BGR
            if len(frame.shape) == 3 and frame.shape[2] == 4:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            
            return frame
            
        except Exception as e:
            logger.error(f"Error capturing screen frame: {e}")
            return None
    
    async def _send_frame(self, frame: np.ndarray, frame_count: int):
        """Send frame to backend"""
        try:
            if self.websocket and not self.websocket.closed:
                # Encode frame as JPEG
                _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                frame_data = buffer.tobytes()
                
                # Create message
                message = {
                    "type": "video_frame",
                    "frame_count": frame_count,
                    "timestamp": datetime.now().isoformat(),
                    "data": frame_data.hex()  # Convert to hex string for JSON
                }
                
                await self.websocket.send(json.dumps(message))
                
        except Exception as e:
            logger.error(f"Error sending frame: {e}")
    
    async def _send_audio(self, audio_data: bytes):
        """Send audio data to backend"""
        try:
            if self.websocket and not self.websocket.closed:
                # Create message
                message = {
                    "type": "audio_chunk",
                    "timestamp": datetime.now().isoformat(),
                    "data": audio_data.hex()  # Convert to hex string for JSON
                }
                
                await self.websocket.send(json.dumps(message))
                
        except Exception as e:
            logger.error(f"Error sending audio: {e}")

# CLI interface for testing
async def main():
    """Main function for testing the screen capture"""
    logging.basicConfig(level=logging.INFO)
    
    capture = ScreenCapture()
    
    # Initialize
    if not await capture.initialize():
        print("Failed to initialize capture system")
        return
    
    print("Screen capture system initialized")
    print("Press Enter to start capture, Enter again to stop...")
    
    input()  # Wait for user input
    
    # Start capture
    if await capture.start_capture():
        print("Capture started! Press Enter to stop...")
        input()  # Wait for user input
        
        # Stop capture
        await capture.stop_capture()
        print("Capture stopped")
    else:
        print("Failed to start capture")

if __name__ == "__main__":
    asyncio.run(main())
