"""
Cross-platform screen capture system
Supports Windows, macOS, and Linux
"""

import os
import time
import threading
import logging
import cv2
import numpy as np
from typing import Optional, Tuple, List, Dict, Any
from dataclasses import dataclass
from platform_utils import platform_detector
from window_detector import WindowInfo

logger = logging.getLogger(__name__)

@dataclass
class CaptureRegion:
    """Defines a capture region"""
    x: int
    y: int
    width: int
    height: int

class CrossPlatformScreenCapture:
    """Cross-platform screen capture using MSS and platform-specific optimizations"""
    
    def __init__(self):
        self.is_capturing = False
        self.capture_thread = None
        self.frame_count = 0
        self.output_dir = "capture_output"
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Platform-specific optimizations
        self._setup_platform_optimizations()
    
    def _setup_platform_optimizations(self):
        """Setup platform-specific optimizations"""
        if platform_detector.is_mac:
            self._setup_mac_optimizations()
        elif platform_detector.is_linux:
            self._setup_linux_optimizations()
        elif platform_detector.is_windows:
            self._setup_windows_optimizations()
    
    def _setup_mac_optimizations(self):
        """Setup macOS-specific optimizations"""
        try:
            # macOS-specific optimizations for better performance
            import os
            # Set environment variables for better performance
            os.environ['PYTHONUNBUFFERED'] = '1'
            logger.info("macOS optimizations applied")
        except Exception as e:
            logger.warning(f"Could not apply macOS optimizations: {e}")
    
    def _setup_linux_optimizations(self):
        """Setup Linux-specific optimizations"""
        try:
            # Linux-specific optimizations
            import os
            os.environ['PYTHONUNBUFFERED'] = '1'
            logger.info("Linux optimizations applied")
        except Exception as e:
            logger.warning(f"Could not apply Linux optimizations: {e}")
    
    def _setup_windows_optimizations(self):
        """Setup Windows-specific optimizations"""
        try:
            # Windows-specific optimizations
            import os
            os.environ['PYTHONUNBUFFERED'] = '1'
            logger.info("Windows optimizations applied")
        except Exception as e:
            logger.warning(f"Could not apply Windows optimizations: {e}")
    
    def start_capture(self, window: WindowInfo, fps: int = 15, crop_region: Optional[CaptureRegion] = None) -> bool:
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
            import mss
            
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
                x, y, width, height = self.crop_region.x, self.crop_region.y, self.crop_region.width, self.crop_region.height
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
            timestamp = time.strftime("%Y%m%d_%H%M%S_%f")[:-3]
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
    
    def get_capture_info(self) -> Dict[str, Any]:
        """Get current capture information"""
        return {
            "is_capturing": self.is_capturing,
            "frame_count": self.frame_count,
            "output_dir": self.output_dir,
            "platform": platform_detector.get_platform_name()
        }
