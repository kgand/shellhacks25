"""
Simplified Screen Capture System
Direct audio and video capture without websockets
"""

import cv2
import numpy as np
import mss
import time
import threading
import logging
import os
import wave
from typing import Optional, Tuple, List
from dataclasses import dataclass
from datetime import datetime
import json
import psutil
import pyautogui

# Audio capture imports
try:
    import pyaudio
    import sounddevice as sd
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    pyaudio = None
    sd = None

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

class SimpleAudioCapture:
    """Simplified audio capture using system audio"""
    
    def __init__(self, sample_rate: int = 44100, channels: int = 2):
        self.sample_rate = sample_rate
        self.channels = channels
        self.is_recording = False
        self.audio_data = []
        self.recording_thread = None
        self.audio_available = AUDIO_AVAILABLE
        
    def start_recording(self, output_file: str = None):
        """Start audio recording to file"""
        if not self.audio_available:
            logger.warning("Audio recording not available")
            return False
            
        try:
            self.output_file = output_file or f"capture_audio_{int(time.time())}.wav"
            self.is_recording = True
            self.audio_data = []
            
            # Start recording thread
            self.recording_thread = threading.Thread(target=self._record_audio, daemon=True)
            self.recording_thread.start()
            
            logger.info(f"Audio recording started: {self.output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start audio recording: {e}")
            return False
    
    def stop_recording(self):
        """Stop audio recording and save to file"""
        if not self.is_recording:
            return
            
        self.is_recording = False
        
        if self.recording_thread:
            self.recording_thread.join()
        
        # Save audio data to file
        if self.audio_data and hasattr(self, 'output_file'):
            try:
                with wave.open(self.output_file, 'wb') as wf:
                    wf.setnchannels(self.channels)
                    wf.setsampwidth(2)  # 16-bit
                    wf.setframerate(self.sample_rate)
                    wf.writeframes(b''.join(self.audio_data))
                logger.info(f"Audio saved to: {self.output_file}")
            except Exception as e:
                logger.error(f"Error saving audio: {e}")
    
    def _record_audio(self):
        """Record audio in separate thread"""
        try:
            def audio_callback(indata, frames, time, status):
                if status:
                    logger.warning(f"Audio callback status: {status}")
                if self.is_recording:
                    self.audio_data.append(indata.copy())
            
            with sd.InputStream(
                callback=audio_callback,
                channels=self.channels,
                samplerate=self.sample_rate,
                dtype='int16'
            ):
                while self.is_recording:
                    time.sleep(0.1)
                    
        except Exception as e:
            logger.error(f"Audio recording error: {e}")

class SimpleScreenCapture:
    """Simplified screen capture using MSS only"""
    
    def __init__(self):
        self.mss_instance = None
        self.is_capturing = False
        self.capture_thread = None
        self.frame_count = 0
        self.output_dir = "capture_output"
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
    def start_capture(self, window: WindowInfo, fps: int = 15):
        """Start screen capture for a specific window"""
        if self.is_capturing:
            logger.warning("Capture already in progress")
            return False
            
        try:
            self.mss_instance = mss.mss()
            self.is_capturing = True
            self.frame_count = 0
            self.fps = fps
            self.window = window
            
            # Start capture thread
            self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
            self.capture_thread.start()
            
            logger.info(f"Screen capture started for window: {window.title}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start screen capture: {e}")
            return False
    
    def stop_capture(self):
        """Stop screen capture"""
        if not self.is_capturing:
            return
            
        self.is_capturing = False
        
        if self.capture_thread:
            self.capture_thread.join()
            
        if self.mss_instance:
            self.mss_instance.close()
            
        logger.info(f"Screen capture stopped. Captured {self.frame_count} frames")
    
    def _capture_loop(self):
        """Main capture loop"""
        frame_interval = 1.0 / self.fps
        
        try:
            while self.is_capturing:
                start_time = time.time()
                
                # Capture screen frame
                frame = self._capture_frame()
                if frame is not None:
                    # Save frame to file
                    self._save_frame(frame)
                    self.frame_count += 1
                
                # Maintain frame rate
                elapsed = time.time() - start_time
                sleep_time = max(0, frame_interval - elapsed)
                time.sleep(sleep_time)
                
        except Exception as e:
            logger.error(f"Error in capture loop: {e}")
    
    def _capture_frame(self) -> Optional[np.ndarray]:
        """Capture a single frame"""
        try:
            # Define capture region
            monitor = {
                "top": self.window.y,
                "left": self.window.x,
                "width": self.window.width,
                "height": self.window.height
            }
            
            # Capture screenshot
            screenshot = self.mss_instance.grab(monitor)
            frame = np.array(screenshot)
            
            # Convert BGRA to BGR if needed
            if len(frame.shape) == 3 and frame.shape[2] == 4:
                frame = frame[:, :, :3]
            
            return frame
            
        except Exception as e:
            logger.error(f"Error capturing frame: {e}")
            return None
    
    def _save_frame(self, frame: np.ndarray):
        """Save frame to file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = f"{self.output_dir}/frame_{self.frame_count:06d}_{timestamp}.jpg"
            
            # Encode and save frame
            success, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            if success:
                with open(filename, 'wb') as f:
                    f.write(buffer)
                
                # Log every 30 frames
                if self.frame_count % 30 == 0:
                    logger.info(f"Saved frame {self.frame_count}: {filename}")
                    
        except Exception as e:
            logger.error(f"Error saving frame: {e}")

class SimpleWindowDetector:
    """Simplified window detection"""
    
    def __init__(self):
        self.messenger_keywords = [
            'messenger.com',
            'facebook.com/messages',
            'messenger',
            'facebook messenger',
            'messenger call'
        ]
    
    def find_messenger_windows(self) -> List[WindowInfo]:
        """Find Messenger windows"""
        windows = []
        
        try:
            # Get all processes
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    # Check if it's a browser process
                    if any(browser in proc.info['name'].lower() for browser in ['chrome', 'firefox', 'edge', 'safari']):
                        # Get windows for this process
                        process_windows = self._get_windows_for_process(proc.info['pid'])
                        for window in process_windows:
                            if self._is_messenger_window(window):
                                windows.append(window)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
        except Exception as e:
            logger.error(f"Error finding messenger windows: {e}")
            
        return windows
    
    def _get_windows_for_process(self, pid: int) -> List[WindowInfo]:
        """Get windows for a process (Windows-specific)"""
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
                                is_messenger=self._is_messenger_window_by_title(title)
                            )
                            windows_list.append(window_info)
                return True
            
            win32gui.EnumWindows(enum_windows_callback, windows)
            
        except ImportError:
            logger.warning("win32gui not available, using fallback")
            # Fallback: return screen info
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
        """Check if window is Messenger-related"""
        return self._is_messenger_window_by_title(window.title)
    
    def _is_messenger_window_by_title(self, title: str) -> bool:
        """Check if title contains Messenger keywords"""
        title_lower = title.lower()
        return any(keyword in title_lower for keyword in self.messenger_keywords)

class SimpleCaptureSystem:
    """Main capture system that coordinates audio and video"""
    
    def __init__(self):
        self.window_detector = SimpleWindowDetector()
        self.screen_capture = SimpleScreenCapture()
        self.audio_capture = SimpleAudioCapture()
        self.is_capturing = False
        self.selected_window = None
        
    def find_windows(self) -> List[WindowInfo]:
        """Find available Messenger windows"""
        return self.window_detector.find_messenger_windows()
    
    def select_window(self, window: WindowInfo):
        """Select a window for capture"""
        self.selected_window = window
        logger.info(f"Selected window: {window.title}")
    
    def start_capture(self, fps: int = 15) -> bool:
        """Start capturing audio and video"""
        if self.is_capturing:
            logger.warning("Capture already in progress")
            return False
            
        if not self.selected_window:
            logger.error("No window selected")
            return False
        
        try:
            # Start screen capture
            if not self.screen_capture.start_capture(self.selected_window, fps):
                return False
            
            # Start audio capture
            audio_file = f"capture_output/audio_{int(time.time())}.wav"
            if not self.audio_capture.start_recording(audio_file):
                logger.warning("Audio capture failed, continuing with video only")
            
            self.is_capturing = True
            logger.info("Capture system started successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start capture: {e}")
            return False
    
    def stop_capture(self):
        """Stop capturing"""
        if not self.is_capturing:
            return
            
        # Stop screen capture
        self.screen_capture.stop_capture()
        
        # Stop audio capture
        self.audio_capture.stop_recording()
        
        self.is_capturing = False
        logger.info("Capture system stopped")
    
    def get_status(self) -> dict:
        """Get current capture status"""
        return {
            "is_capturing": self.is_capturing,
            "selected_window": self.selected_window.title if self.selected_window else None,
            "frame_count": self.screen_capture.frame_count if self.screen_capture else 0,
            "audio_available": self.audio_capture.audio_available
        }

# CLI interface for testing
def main():
    """Main function for testing"""
    logging.basicConfig(level=logging.INFO)
    
    capture_system = SimpleCaptureSystem()
    
    print("Simple Screen Capture System")
    print("=" * 40)
    
    # Find windows
    windows = capture_system.find_windows()
    if not windows:
        print("No Messenger windows found")
        return
    
    print(f"Found {len(windows)} Messenger windows:")
    for i, window in enumerate(windows):
        print(f"{i+1}. {window.title} (PID: {window.pid})")
    
    # Select first window
    if windows:
        capture_system.select_window(windows[0])
        print(f"Selected: {windows[0].title}")
    
    # Start capture
    print("\nStarting capture...")
    if capture_system.start_capture():
        print("Capture started! Press Enter to stop...")
        input()
        
        capture_system.stop_capture()
        print("Capture stopped")
    else:
        print("Failed to start capture")

if __name__ == "__main__":
    main()
