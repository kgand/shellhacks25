"""
Cross-Platform Screen Capture System
Direct audio and video capture without websockets
Supports Windows, macOS, and Linux
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

# Cross-platform imports
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from platform_utils import platform_detector
from window_detector import CrossPlatformWindowDetector, WindowInfo
from audio_capture import CrossPlatformAudioCapture
from screen_capture import CrossPlatformScreenCapture, CaptureRegion

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

class SimpleAudioCapture(CrossPlatformAudioCapture):
    """Cross-platform audio capture using system audio"""
    
    def __init__(self, sample_rate: int = 44100, channels: int = 2):
        super().__init__(sample_rate, channels)
        
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
                    wf.writeframes(b''.join(chunk.tobytes() for chunk in self.audio_data))
                logger.info(f"Audio saved to: {self.output_file}")
            except Exception as e:
                logger.error(f"Error saving audio: {e}")
    
    def _record_audio(self):
        """Optimized audio recording with performance monitoring"""
        try:
            audio_stats = {
                'chunks_recorded': 0,
                'total_bytes': 0,
                'last_log_time': time.time()
            }
            
            def audio_callback(indata, frames, callback_time, status):
                if status:
                    logger.warning(f"Audio callback status: {status}")
                
                if self.is_recording:
                    # Optimize audio data handling
                    audio_chunk = indata.copy()
                    self.audio_data.append(audio_chunk)
                    
                    # Update stats
                    audio_stats['chunks_recorded'] += 1
                    audio_stats['total_bytes'] += len(audio_chunk.tobytes())
                    
                    # Log performance every 10 seconds
                    import time as time_module
                    current_time = time_module.time()
                    if current_time - audio_stats['last_log_time'] > 10:
                        time_diff = current_time - audio_stats['last_log_time']
                        if time_diff > 0:  # Prevent division by zero
                            chunks_per_sec = audio_stats['chunks_recorded'] / time_diff
                            bytes_per_sec = audio_stats['total_bytes'] / time_diff
                            logger.info(f"Audio: {chunks_per_sec:.1f} chunks/sec, {bytes_per_sec/1024:.1f} KB/sec")
                        
                        # Reset stats
                        audio_stats['chunks_recorded'] = 0
                        audio_stats['total_bytes'] = 0
                        audio_stats['last_log_time'] = current_time
            
            with sd.InputStream(
                callback=audio_callback,
                channels=self.channels,
                samplerate=self.sample_rate,
                dtype='int16',
                blocksize=1024  # Optimize block size
            ):
                while self.is_recording:
                    time.sleep(0.1)
                    
        except Exception as e:
            logger.error(f"Audio recording error: {e}")

class SimpleScreenCapture(CrossPlatformScreenCapture):
    """Cross-platform screen capture using MSS and platform-specific optimizations"""
    
    def __init__(self):
        super().__init__()
        
    def start_capture(self, window: WindowInfo, fps: int = 15, crop_region=None):
        """Start screen capture for a specific window"""
        if self.is_capturing:
            logger.warning("Capture already in progress")
            return False
            
        try:
            self.is_capturing = True
            self.frame_count = 0
            self.fps = fps
            self.window = window
            self.crop_region = crop_region
            
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
            
        logger.info(f"Screen capture stopped. Captured {self.frame_count} frames")
    
    def _capture_loop(self):
        """Optimized capture loop with performance monitoring"""
        frame_interval = 1.0 / self.fps
        performance_stats = {
            'frame_times': [],
            'save_times': [],
            'total_frames': 0,
            'dropped_frames': 0
        }
        
        try:
            while self.is_capturing:
                loop_start = time.time()
                
                # Capture screen frame
                capture_start = time.time()
                frame = self._capture_frame()
                capture_time = time.time() - capture_start
                
                if frame is not None:
                    # Save frame to file
                    save_start = time.time()
                    self._save_frame(frame)
                    save_time = time.time() - save_start
                    
                    # Update performance stats
                    performance_stats['frame_times'].append(capture_time)
                    performance_stats['save_times'].append(save_time)
                    performance_stats['total_frames'] += 1
                    self.frame_count += 1
                    
                    # Keep only last 30 frame times for rolling average
                    if len(performance_stats['frame_times']) > 30:
                        performance_stats['frame_times'] = performance_stats['frame_times'][-30:]
                        performance_stats['save_times'] = performance_stats['save_times'][-30:]
                else:
                    performance_stats['dropped_frames'] += 1
                
                # Adaptive sleep based on performance
                elapsed = time.time() - loop_start
                sleep_time = max(0, frame_interval - elapsed)
                
                # If we're consistently behind, reduce frame rate
                if len(performance_stats['frame_times']) > 10:
                    avg_frame_time = sum(performance_stats['frame_times']) / len(performance_stats['frame_times'])
                    if avg_frame_time > frame_interval * 0.8:  # If taking >80% of frame time
                        sleep_time = max(0, sleep_time * 0.5)  # Reduce sleep time
                
                time.sleep(sleep_time)
                
                # Log performance every 100 frames
                if self.frame_count % 100 == 0:
                    frame_times = performance_stats['frame_times'][-10:]
                    save_times = performance_stats['save_times'][-10:]
                    
                    if frame_times and save_times:
                        avg_capture = sum(frame_times) / len(frame_times)
                        avg_save = sum(save_times) / len(save_times)
                        logger.info(f"Performance: {self.frame_count} frames, "
                                  f"avg capture: {avg_capture:.3f}s, "
                                  f"avg save: {avg_save:.3f}s, "
                                  f"dropped: {performance_stats['dropped_frames']}")
                    else:
                        logger.info(f"Performance: {self.frame_count} frames, "
                                  f"dropped: {performance_stats['dropped_frames']}")
                
        except Exception as e:
            logger.error(f"Error in capture loop: {e}")
    
    def _capture_frame(self) -> Optional[np.ndarray]:
        """Capture a single frame with smart video area detection"""
        try:
            # Define capture region - focus on video content area
            # More aggressive cropping to avoid browser UI and taskbar
            monitor = {
                "top": self.window.y + 80,  # Skip more browser UI
                "left": self.window.x + 30,  # Skip more left padding
                "width": self.window.width - 60,  # Remove more side padding
                "height": self.window.height - 150  # Remove more browser UI and taskbar
            }
            
            # Create a new MSS instance for each capture to avoid threading issues
            with mss.mss() as mss_instance:
                screenshot = mss_instance.grab(monitor)
                frame = np.array(screenshot)
            
            # Convert BGRA to BGR if needed
            if len(frame.shape) == 3 and frame.shape[2] == 4:
                frame = frame[:, :, :3]
            
            # Apply user-defined crop region if available
            if self.crop_region:
                x, y, width, height = self.crop_region
                # Ensure crop region is within frame bounds
                frame_height, frame_width = frame.shape[:2]
                x = max(0, min(x, frame_width - 1))
                y = max(0, min(y, frame_height - 1))
                width = min(width, frame_width - x)
                height = min(height, frame_height - y)
                
                if width > 0 and height > 0:
                    frame = frame[y:y+height, x:x+width]
            else:
                # Try to detect and crop to video content area
                frame = self._crop_to_video_content(frame)
            
            return frame
            
        except Exception as e:
            logger.error(f"Error capturing frame: {e}")
            return None
    
    def _crop_to_video_content(self, frame: np.ndarray) -> np.ndarray:
        """Smart cropping to focus on video content"""
        try:
            height, width = frame.shape[:2]
            
            # Convert to grayscale for edge detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect edges to find video boundaries
            edges = cv2.Canny(gray, 50, 150)
            
            # Find contours to detect video area
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                # Find the largest contour (likely the video area)
                largest_contour = max(contours, key=cv2.contourArea)
                x, y, w, h = cv2.boundingRect(largest_contour)
                
                # Only crop if we found a reasonable video area
                if w > width * 0.3 and h > height * 0.3:  # At least 30% of original size
                    # Add some padding around the detected area
                    padding = 20
                    x = max(0, x - padding)
                    y = max(0, y - padding)
                    w = min(width - x, w + 2 * padding)
                    h = min(height - y, h + 2 * padding)
                    
                    return frame[y:y+h, x:x+w]
            
            # If no good video area detected, try center cropping
            # Focus on center 70% of the frame to avoid UI elements
            center_x, center_y = width // 2, height // 2
            crop_width = int(width * 0.7)
            crop_height = int(height * 0.7)
            
            x = center_x - crop_width // 2
            y = center_y - crop_height // 2
            
            # Ensure coordinates are within bounds
            x = max(0, x)
            y = max(0, y)
            crop_width = min(crop_width, width - x)
            crop_height = min(crop_height, height - y)
            
            return frame[y:y+crop_height, x:x+crop_width]
            
        except Exception as e:
            logger.warning(f"Error in video content detection: {e}")
            return frame
    
    def _save_frame(self, frame: np.ndarray):
        """Optimized frame saving with compression and error handling"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = f"{self.output_dir}/frame_{self.frame_count:06d}_{timestamp}.jpg"
            
            # Optimize frame before encoding
            optimized_frame = self._optimize_frame(frame)
            
            # Encode with optimized settings
            encode_params = [
                cv2.IMWRITE_JPEG_QUALITY, 85,
                cv2.IMWRITE_JPEG_OPTIMIZE, 1,
                cv2.IMWRITE_JPEG_PROGRESSIVE, 1
            ]
            
            success, buffer = cv2.imencode('.jpg', optimized_frame, encode_params)
            if success:
                # Write to file with error handling
                try:
                    with open(filename, 'wb') as f:
                        f.write(buffer)
                    
                    # Log every 30 frames with file size
                    if self.frame_count % 30 == 0:
                        file_size = len(buffer)
                        logger.info(f"Saved frame {self.frame_count}: {filename} ({file_size} bytes)")
                        
                except IOError as e:
                    logger.error(f"IO Error saving frame {self.frame_count}: {e}")
                except Exception as e:
                    logger.error(f"Unexpected error saving frame {self.frame_count}: {e}")
            else:
                logger.warning(f"Failed to encode frame {self.frame_count}")
                    
        except Exception as e:
            logger.error(f"Error saving frame: {e}")
    
    def _optimize_frame(self, frame: np.ndarray) -> np.ndarray:
        """Optimize frame for better compression and performance"""
        try:
            # Resize if frame is too large
            height, width = frame.shape[:2]
            max_width = 1920  # Limit width for performance
            
            if width > max_width:
                scale = max_width / width
                new_width = int(width * scale)
                new_height = int(height * scale)
                frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)
            
            # Keep original color space - don't convert BGR to RGB
            # The frame is already in the correct BGR format for OpenCV
            # Converting to RGB would cause color channel swapping issues
            
            return frame
            
        except Exception as e:
            logger.error(f"Error optimizing frame: {e}")
            return frame
    
    def _fix_color_tint(self, frame: np.ndarray) -> np.ndarray:
        """Fix color tint issues in captured frames - DISABLED to preserve original colors"""
        # Return frame unchanged to preserve original colors
        # Color correction was causing blue/orange shifting issues
        return frame

class SimpleWindowDetector(CrossPlatformWindowDetector):
    """Cross-platform window detection"""
    
    def __init__(self):
        super().__init__()
    
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
    """Cross-platform capture system that coordinates audio and video"""
    
    def __init__(self):
        self.window_detector = SimpleWindowDetector()
        self.screen_capture = SimpleScreenCapture()
        self.audio_capture = SimpleAudioCapture()
        self.is_capturing = False
        self.selected_window = None
        self.server_url = "http://127.0.0.1:8000"
        self.crop_region = None  # Store crop region (x, y, width, height)
        
        # Log platform information
        logger.info(f"Initialized capture system for {platform_detector.get_platform_name()}")
        
    def find_windows(self) -> List[WindowInfo]:
        """Find available Messenger windows"""
        return self.window_detector.find_messenger_windows()
    
    def select_window(self, window: WindowInfo):
        """Select a window for capture"""
        self.selected_window = window
        logger.info(f"Selected window: {window.title}")
    
    def set_crop_region(self, x: int, y: int, width: int, height: int):
        """Set the crop region for frame capture"""
        self.crop_region = CaptureRegion(x, y, width, height)
        logger.info(f"Crop region set: x={x}, y={y}, width={width}, height={height}")
    
    def get_crop_region(self):
        """Get the current crop region"""
        return self.crop_region
    
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
            if not self.screen_capture.start_capture(self.selected_window, fps, self.crop_region):
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
        
        # Auto-process captured files
        self._auto_process_captured_files()
    
    def _auto_process_captured_files(self):
        """Automatically process captured files with the server"""
        try:
            import requests
            import os
            
            # Check if server is running
            try:
                health_response = requests.get(f"{self.server_url}/health", timeout=5)
                if health_response.status_code != 200:
                    logger.warning("Server is not running, skipping auto-processing")
                    return
            except:
                logger.warning("Server is not accessible, skipping auto-processing")
                return
            
            # Check if there are captured files to process
            capture_output_dir = "capture_output"
            if not os.path.exists(capture_output_dir):
                logger.info("No capture output directory found")
                return
                
            captured_files = [f for f in os.listdir(capture_output_dir) if f.endswith(('.jpg', '.wav'))]
            if not captured_files:
                logger.info("No captured files to process")
                return
            
            logger.info(f"Found {len(captured_files)} captured files, processing...")
            
            # Call the auto-process endpoint
            response = requests.post(f"{self.server_url}/auto-process", timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Auto-processed {result['processed_files']} files successfully")
            else:
                logger.warning(f"Auto-processing failed: {response.status_code} - {response.text}")
                
        except Exception as e:
            logger.error(f"Error auto-processing files: {e}")
    
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
