"""
Cross-platform audio capture system
Supports Windows, macOS, and Linux
"""

import os
import time
import threading
import logging
import wave
import numpy as np
from typing import Optional, Dict, Any
from platform_utils import platform_detector

logger = logging.getLogger(__name__)

class CrossPlatformAudioCapture:
    """Cross-platform audio capture using system audio"""
    
    def __init__(self, sample_rate: int = 44100, channels: int = 2):
        self.sample_rate = sample_rate
        self.channels = channels
        self.is_recording = False
        self.audio_data = []
        self.recording_thread = None
        self.audio_available = self._check_audio_availability()
        
    def _check_audio_availability(self) -> bool:
        """Check if audio capture is available on this platform"""
        try:
            if platform_detector.is_windows:
                return self._check_audio_windows()
            elif platform_detector.is_mac:
                return self._check_audio_mac()
            elif platform_detector.is_linux:
                return self._check_audio_linux()
            else:
                return False
        except Exception as e:
            logger.error(f"Error checking audio availability: {e}")
            return False
    
    def _check_audio_windows(self) -> bool:
        """Check audio availability on Windows"""
        try:
            import sounddevice as sd
            import pyaudio
            
            # Test if we can get device info
            devices = sd.query_devices()
            return len(devices) > 0
        except ImportError:
            logger.warning("Audio dependencies not available on Windows")
            return False
        except Exception as e:
            logger.error(f"Error checking Windows audio: {e}")
            return False
    
    def _check_audio_mac(self) -> bool:
        """Check audio availability on macOS"""
        try:
            import sounddevice as sd
            
            # Test if we can get device info
            devices = sd.query_devices()
            return len(devices) > 0
        except ImportError:
            logger.warning("Audio dependencies not available on macOS")
            return False
        except Exception as e:
            logger.error(f"Error checking macOS audio: {e}")
            return False
    
    def _check_audio_linux(self) -> bool:
        """Check audio availability on Linux"""
        try:
            import sounddevice as sd
            
            # Test if we can get device info
            devices = sd.query_devices()
            return len(devices) > 0
        except ImportError:
            logger.warning("Audio dependencies not available on Linux")
            return False
        except Exception as e:
            logger.error(f"Error checking Linux audio: {e}")
            return False
    
    def start_recording(self, output_file: str = None) -> bool:
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
            import sounddevice as sd
            
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
                    current_time = time.time()
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
    
    def get_audio_devices(self) -> Dict[str, Any]:
        """Get available audio devices"""
        try:
            import sounddevice as sd
            
            devices = sd.query_devices()
            input_devices = []
            output_devices = []
            
            for i, device in enumerate(devices):
                device_info = {
                    'index': i,
                    'name': device['name'],
                    'channels': device['max_input_channels'] if device['max_input_channels'] > 0 else device['max_output_channels'],
                    'sample_rate': device['default_samplerate']
                }
                
                if device['max_input_channels'] > 0:
                    input_devices.append(device_info)
                if device['max_output_channels'] > 0:
                    output_devices.append(device_info)
            
            return {
                'input_devices': input_devices,
                'output_devices': output_devices,
                'default_input': sd.default.device[0],
                'default_output': sd.default.device[1]
            }
            
        except Exception as e:
            logger.error(f"Error getting audio devices: {e}")
            return {'input_devices': [], 'output_devices': []}
    
    def test_audio_capture(self) -> bool:
        """Test audio capture functionality"""
        try:
            if not self.audio_available:
                return False
            
            # Try to start and immediately stop recording
            if self.start_recording("test_audio.wav"):
                time.sleep(0.1)  # Record for 100ms
                self.stop_recording()
                
                # Check if file was created
                if os.path.exists("test_audio.wav"):
                    os.remove("test_audio.wav")  # Clean up
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Audio test failed: {e}")
            return False
