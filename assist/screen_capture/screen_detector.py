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

# Optional audio imports - will be handled gracefully if not available
try:
    import pyaudio
    import wave
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    pyaudio = None
    wave = None

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
        self.screen_capture = None
        self.selected_window = None  # Add missing selected_window attribute
        self._init_screen_capture()
    
    def _init_screen_capture(self):
        """Initialize screen capture with proper threading"""
        try:
            self.screen_capture = mss.mss()
        except Exception as e:
            logger.error(f"Failed to initialize screen capture: {e}")
            self.screen_capture = None
    
    def set_selected_window(self, window: WindowInfo):
        """Set the selected window for capture"""
        self.selected_window = window
        logger.info(f"Selected window: {window.title}")
        
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
        self.audio = None
        self.stream = None
        self.is_recording = False
        self.audio_buffer = []
        self.audio_available = AUDIO_AVAILABLE
        
        if self.audio_available:
            try:
                self.audio = pyaudio.PyAudio()
            except Exception as e:
                logger.warning(f"PyAudio not available: {e}")
                self.audio_available = False
        
    def start_recording(self):
        """Start audio recording"""
        if not self.audio_available:
            logger.warning("Audio recording not available - PyAudio not installed")
            return
            
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
        if not self.audio_available:
            return b''
            
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
        
        # Error handling and recovery
        self.error_count = 0
        self.max_errors = 10
        self.last_error_time = 0
        self.connection_retries = 0
        self.max_retries = 3
        
        # Performance monitoring
        self.frame_count = 0
        self.audio_chunk_count = 0
        self.start_time = None
        
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
    
    async def start_capture(self, selected_window=None):
        """Start capturing screen and audio with robust error handling"""
        if self.is_capturing:
            logger.warning("Capture already in progress")
            return False
        
        # Use provided window or detector's selected window
        if selected_window:
            self.selected_window = selected_window
        elif self.detector.selected_window:
            self.selected_window = self.detector.selected_window
        else:
            logger.error("No window selected for capture")
            return False
        
        # Reset error tracking
        self.error_count = 0
        self.connection_retries = 0
        self.start_time = time.time()
        self.frame_count = 0
        self.audio_chunk_count = 0
            
        try:
            # Start audio capture with error handling
            try:
                self.audio_capture.start_recording()
                logger.info("Audio capture started")
            except Exception as e:
                logger.warning(f"Audio capture failed to start: {e}")
                # Continue without audio if it fails
            
            # Start capture thread (WebSocket connection will be established in the thread)
            self.is_capturing = True
            self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
            self.capture_thread.start()
            
            logger.info(f"Screen capture started for window: {self.selected_window.title}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start capture: {e}")
            await self._cleanup_resources()
            return False
    
    async def stop_capture(self):
        """Stop capturing with proper cleanup"""
        if not self.is_capturing:
            logger.info("Capture not running")
            return
            
        logger.info("Stopping screen capture...")
        self.is_capturing = False
        
        try:
            # Stop audio capture
            try:
                self.audio_capture.stop_recording()
                logger.info("Audio capture stopped")
            except Exception as e:
                logger.warning(f"Error stopping audio capture: {e}")
            
            # Wait for capture thread to finish with timeout
            if self.capture_thread and self.capture_thread.is_alive():
                self.capture_thread.join(timeout=5.0)
                if self.capture_thread.is_alive():
                    logger.warning("Capture thread did not stop gracefully")
            
            # Close WebSocket connection
            if self.websocket and not self.websocket.closed:
                try:
                    await self.websocket.close()
                    logger.info("WebSocket connection closed")
                except Exception as e:
                    logger.warning(f"Error closing WebSocket: {e}")
            
            # Log performance statistics
            if self.start_time:
                duration = time.time() - self.start_time
                fps = self.frame_count / duration if duration > 0 else 0
                logger.info(f"Capture session ended - Duration: {duration:.1f}s, Frames: {self.frame_count}, FPS: {fps:.1f}")
            
        except Exception as e:
            logger.error(f"Error during capture stop: {e}")
        finally:
            await self._cleanup_resources()
            logger.info("Screen capture stopped")
    
    async def _cleanup_resources(self):
        """Clean up all resources"""
        try:
            # Reset state
            self.is_capturing = False
            self.websocket = None
            self.capture_thread = None
            self.error_count = 0
            self.connection_retries = 0
            
            # Clean up audio
            if hasattr(self.audio_capture, 'stream') and self.audio_capture.stream:
                try:
                    self.audio_capture.stop_recording()
                except:
                    pass
            
        except Exception as e:
            logger.error(f"Error during resource cleanup: {e}")
    
    async def _connect_to_backend(self):
        """Connect to the FastAPI backend"""
        try:
            self.websocket = await websockets.connect(self.backend_url)
            logger.info("Connected to backend")
        except Exception as e:
            logger.error(f"Failed to connect to backend: {e}")
            raise
    
    def _capture_loop(self):
        """Optimized capture loop (runs in separate thread)"""
        frame_count = 0
        audio_chunk_count = 0
        
        # Create a new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Performance optimization: adaptive capture frequency
        frame_interval = 0.33  # Capture every 333ms (3 FPS) - reduced for better performance
        audio_interval = 0.2   # Audio every 200ms - reduced frequency
        last_frame_time = 0
        last_audio_time = 0
        
        # Performance monitoring
        frame_times = []
        max_frame_times = 10  # Keep last 10 frame times for adaptive timing
        
        # Establish WebSocket connection in this thread
        try:
            connection_success = False
            for attempt in range(self.max_retries):
                try:
                    self.websocket = loop.run_until_complete(websockets.connect(self.backend_url))
                    connection_success = True
                    logger.info("Connected to backend from capture thread")
                    break
                except Exception as e:
                    self.connection_retries += 1
                    logger.warning(f"Connection attempt {attempt + 1} failed: {e}")
                    if attempt < self.max_retries - 1:
                        loop.run_until_complete(asyncio.sleep(2 ** attempt))  # Exponential backoff
            
            if not connection_success:
                logger.error("Failed to connect to backend after all retries")
                self.is_capturing = False
                return
                
        except Exception as e:
            logger.error(f"Failed to establish WebSocket connection: {e}")
            self.is_capturing = False
            return
        
        try:
            while self.is_capturing:
                current_time = time.time()
                loop_start = time.time()
                
                try:
                    # Capture screen frame (optimized frequency with adaptive timing)
                    if self.selected_window and (current_time - last_frame_time) >= frame_interval:
                        frame_start = time.time()
                        frame = self._capture_screen_frame()
                        frame_capture_time = time.time() - frame_start
                        
                        if frame is not None:
                            # Send frame to backend asynchronously
                            send_start = time.time()
                            try:
                                loop.run_until_complete(self._send_frame(frame, frame_count))
                                send_time = time.time() - send_start
                                
                                frame_count += 1
                                last_frame_time = current_time
                                
                                # Track performance for adaptive timing
                                total_frame_time = frame_capture_time + send_time
                                frame_times.append(total_frame_time)
                                if len(frame_times) > max_frame_times:
                                    frame_times.pop(0)
                                
                                # Adaptive frame interval based on performance
                                if len(frame_times) >= 3:
                                    avg_frame_time = sum(frame_times) / len(frame_times)
                                    if avg_frame_time > 0.5:  # If frames take too long
                                        frame_interval = min(0.5, frame_interval * 1.1)  # Slow down
                                    elif avg_frame_time < 0.2:  # If frames are fast
                                        frame_interval = max(0.2, frame_interval * 0.95)  # Speed up
                                        
                            except Exception as e:
                                logger.error(f"Error sending frame {frame_count}: {e}")
                                # Check if we should stop due to too many errors
                                if self.error_count >= self.max_errors:
                                    logger.error("Too many errors, stopping capture")
                                    self.is_capturing = False
                                    break
                    
                    # Capture audio data (optimized frequency)
                    if (current_time - last_audio_time) >= audio_interval:
                        try:
                            audio_data = self.audio_capture.get_audio_data()
                            if audio_data:
                                loop.run_until_complete(self._send_audio(audio_data))
                                audio_chunk_count += 1
                                last_audio_time = current_time
                        except Exception as e:
                            logger.warning(f"Error capturing audio: {e}")
                    
                    # Adaptive sleep based on loop performance
                    loop_time = time.time() - loop_start
                    if loop_time < 0.1:  # If loop is fast, sleep longer
                        time.sleep(0.05)
                    else:  # If loop is slow, sleep less
                        time.sleep(0.02)
                    
                except Exception as e:
                    self.error_count += 1
                    self.last_error_time = current_time
                    logger.error(f"Error in capture loop (error #{self.error_count}): {e}")
                    
                    # If too many errors in a short time, stop
                    if self.error_count >= self.max_errors:
                        logger.error("Too many consecutive errors, stopping capture")
                        self.is_capturing = False
                        break
                    
                    time.sleep(0.5)  # Longer sleep on error
                    
        except Exception as e:
            logger.error(f"Fatal error in capture loop: {e}")
        finally:
            loop.close()
            logger.info("Capture loop ended")
    
    def _capture_screen_frame(self) -> Optional[np.ndarray]:
        """Optimized screen frame capture with better performance"""
        try:
            if not self.selected_window:
                return None
                
            # Capture screen region with bounds checking
            monitor = {
                "top": max(0, self.selected_window.y),
                "left": max(0, self.selected_window.x),
                "width": max(100, min(self.selected_window.width, 1920)),  # Reasonable limits
                "height": max(100, min(self.selected_window.height, 1080))
            }
            
            # Use a new MSS instance for each capture to avoid threading issues
            with mss.mss() as mss_instance:
                screenshot = mss_instance.grab(monitor)
                frame = np.array(screenshot)
            
            # Optimize frame processing with better memory management
            if len(frame.shape) == 3 and frame.shape[2] == 4:
                # Convert BGRA to BGR more efficiently - remove alpha channel
                frame = frame[:, :, :3]
            elif len(frame.shape) == 3 and frame.shape[2] == 3:
                # Already BGR, no conversion needed
                pass
            else:
                # Handle other formats
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            
            # Smart resizing for better performance
            height, width = frame.shape[:2]
            max_width = 1280
            max_height = 720
            
            if width > max_width or height > max_height:
                # Calculate scale to fit within limits while maintaining aspect ratio
                scale_w = max_width / width
                scale_h = max_height / height
                scale = min(scale_w, scale_h)
                
                new_width = int(width * scale)
                new_height = int(height * scale)
                
                # Use INTER_AREA for downscaling (better quality and performance)
                frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)
            
            # Additional optimization: convert to contiguous array for better memory access
            if not frame.flags['C_CONTIGUOUS']:
                frame = np.ascontiguousarray(frame)
            
            return frame
            
        except Exception as e:
            logger.error(f"Error capturing screen frame: {e}")
            return None
    
    async def _send_frame(self, frame: np.ndarray, frame_count: int):
        """Optimized frame sending to backend with better compression"""
        try:
            # Validate WebSocket connection
            if not self.websocket:
                logger.error("WebSocket connection is None")
                return
                
            if self.websocket.closed:
                logger.error("WebSocket connection is closed")
                return
            
            # Adaptive JPEG quality based on frame size
            height, width = frame.shape[:2]
            total_pixels = height * width
            
            # Adjust quality based on frame size
            if total_pixels > 800000:  # Large frames
                quality = 60
            elif total_pixels > 400000:  # Medium frames
                quality = 70
            else:  # Small frames
                quality = 80
            
            # Optimize JPEG encoding for better performance
            encode_params = [
                cv2.IMWRITE_JPEG_QUALITY, quality,
                cv2.IMWRITE_JPEG_OPTIMIZE, 1,  # Enable optimization
                cv2.IMWRITE_JPEG_PROGRESSIVE, 1  # Progressive JPEG for better compression
            ]
            
            _, buffer = cv2.imencode('.jpg', frame, encode_params)
            frame_data = buffer.tobytes()
            
            # Dynamic size limit based on frame count (allow larger frames occasionally)
            max_size = 300000 if frame_count % 5 == 0 else 200000  # 300KB every 5th frame, 200KB otherwise
            
            if len(frame_data) < max_size:
                message = {
                    "type": "video_frame",
                    "frame_count": frame_count,
                    "timestamp": datetime.now().isoformat(),
                    "data": frame_data.hex(),
                    "size": len(frame_data),
                    "quality": quality,
                    "dimensions": f"{width}x{height}"
                }
                
                await self.websocket.send(json.dumps(message))
                
                # Reduced logging frequency with more useful info
                if frame_count % 20 == 0:
                    logger.info(f"Sent frame {frame_count} ({len(frame_data)} bytes, {width}x{height}, quality={quality})")
            else:
                # Try with lower quality if frame is too large
                if quality > 40:
                    encode_params[1] = max(40, quality - 20)  # Reduce quality
                    _, buffer = cv2.imencode('.jpg', frame, encode_params)
                    frame_data = buffer.tobytes()
                    
                    if len(frame_data) < max_size:
                        message = {
                            "type": "video_frame",
                            "frame_count": frame_count,
                            "timestamp": datetime.now().isoformat(),
                            "data": frame_data.hex(),
                            "size": len(frame_data),
                            "quality": encode_params[1],
                            "dimensions": f"{width}x{height}"
                        }
                        await self.websocket.send(json.dumps(message))
                    else:
                        logger.warning(f"Frame {frame_count} still too large after quality reduction ({len(frame_data)} bytes), skipping")
                else:
                    logger.warning(f"Frame {frame_count} too large ({len(frame_data)} bytes), skipping")
                
        except Exception as e:
            logger.error(f"Error sending frame: {e}")
    
    async def _send_audio(self, audio_data: bytes):
        """Send audio data to backend"""
        try:
            # Validate WebSocket connection
            if not self.websocket:
                logger.error("WebSocket connection is None for audio")
                return
                
            if self.websocket.closed:
                logger.error("WebSocket connection is closed for audio")
                return
            
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
