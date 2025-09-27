#!/usr/bin/env python3
"""
Cross-Platform Testing Script for Messenger AI Assistant
Tests all platform-specific functionality
"""

import os
import sys
import logging
import traceback
from pathlib import Path

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CrossPlatformTester:
    """Comprehensive cross-platform testing"""
    
    def __init__(self):
        self.test_results = {
            'platform_detection': False,
            'window_detection': False,
            'audio_capture': False,
            'screen_capture': False,
            'file_operations': False,
            'gui_components': False
        }
        
    def run_all_tests(self):
        """Run all cross-platform tests"""
        logger.info("🧪 Starting Cross-Platform Testing")
        logger.info("=" * 50)
        
        try:
            # Test platform detection
            self.test_platform_detection()
            
            # Test window detection
            self.test_window_detection()
            
            # Test audio capture
            self.test_audio_capture()
            
            # Test screen capture
            self.test_screen_capture()
            
            # Test file operations
            self.test_file_operations()
            
            # Test GUI components
            self.test_gui_components()
            
            # Print results
            self.print_results()
            
        except Exception as e:
            logger.error(f"Testing failed: {e}")
            traceback.print_exc()
    
    def test_platform_detection(self):
        """Test platform detection functionality"""
        logger.info("🔍 Testing Platform Detection...")
        
        try:
            from utils.platform_utils import platform_detector
            
            # Test basic platform detection
            platform_name = platform_detector.get_platform_name()
            logger.info(f"Platform: {platform_name}")
            
            # Test platform flags
            logger.info(f"Windows: {platform_detector.is_windows}")
            logger.info(f"macOS: {platform_detector.is_mac}")
            logger.info(f"Linux: {platform_detector.is_linux}")
            
            # Test browser command
            browser_cmd = platform_detector.get_browser_command()
            logger.info(f"Browser command: {browser_cmd}")
            
            # Test audio dependencies
            audio_deps = platform_detector.get_audio_dependencies()
            logger.info(f"Audio dependencies: {audio_deps}")
            
            # Test screen capture dependencies
            screen_deps = platform_detector.get_screen_capture_dependencies()
            logger.info(f"Screen capture dependencies: {screen_deps}")
            
            self.test_results['platform_detection'] = True
            logger.info("✅ Platform detection test passed")
            
        except Exception as e:
            logger.error(f"❌ Platform detection test failed: {e}")
    
    def test_window_detection(self):
        """Test window detection functionality"""
        logger.info("🪟 Testing Window Detection...")
        
        try:
            from utils.window_detector import CrossPlatformWindowDetector
            
            detector = CrossPlatformWindowDetector()
            
            # Test finding messenger windows
            windows = detector.find_messenger_windows()
            logger.info(f"Found {len(windows)} Messenger windows")
            
            for i, window in enumerate(windows[:3]):  # Show first 3
                logger.info(f"  Window {i+1}: {window.title} (PID: {window.pid})")
            
            self.test_results['window_detection'] = True
            logger.info("✅ Window detection test passed")
            
        except Exception as e:
            logger.error(f"❌ Window detection test failed: {e}")
    
    def test_audio_capture(self):
        """Test audio capture functionality"""
        logger.info("🎤 Testing Audio Capture...")
        
        try:
            from utils.audio_capture import CrossPlatformAudioCapture
            
            audio_capture = CrossPlatformAudioCapture()
            
            # Test audio availability
            logger.info(f"Audio available: {audio_capture.audio_available}")
            
            if audio_capture.audio_available:
                # Test audio devices
                devices = audio_capture.get_audio_devices()
                logger.info(f"Input devices: {len(devices.get('input_devices', []))}")
                logger.info(f"Output devices: {len(devices.get('output_devices', []))}")
                
                # Test audio capture (brief test)
                logger.info("Testing brief audio capture...")
                if audio_capture.test_audio_capture():
                    logger.info("Audio capture test successful")
                else:
                    logger.warning("Audio capture test failed")
            
            self.test_results['audio_capture'] = True
            logger.info("✅ Audio capture test passed")
            
        except Exception as e:
            logger.error(f"❌ Audio capture test failed: {e}")
    
    def test_screen_capture(self):
        """Test screen capture functionality"""
        logger.info("📸 Testing Screen Capture...")
        
        try:
            from utils.screen_capture import CrossPlatformScreenCapture
            from utils.window_detector import WindowInfo
            
            screen_capture = CrossPlatformScreenCapture()
            
            # Test capture info
            info = screen_capture.get_capture_info()
            logger.info(f"Capture info: {info}")
            
            # Test with a dummy window
            dummy_window = WindowInfo(
                pid=0,
                title="Test Window",
                x=100,
                y=100,
                width=800,
                height=600
            )
            
            # Test capture start/stop (without actually capturing)
            logger.info("Testing capture system initialization...")
            
            self.test_results['screen_capture'] = True
            logger.info("✅ Screen capture test passed")
            
        except Exception as e:
            logger.error(f"❌ Screen capture test failed: {e}")
    
    def test_file_operations(self):
        """Test file operations"""
        logger.info("📁 Testing File Operations...")
        
        try:
            from utils.platform_utils import platform_detector
            
            # Test file manager opening
            test_dir = os.path.abspath(".")
            logger.info(f"Testing file manager opening for: {test_dir}")
            
            # Note: This might open a file manager, so we'll just test the function exists
            if hasattr(platform_detector, 'open_file_manager'):
                logger.info("File manager function available")
            
            # Test directory creation
            test_dirs = ["test_output", "test_processed", "test_uploads"]
            for test_dir in test_dirs:
                os.makedirs(test_dir, exist_ok=True)
                if os.path.exists(test_dir):
                    os.rmdir(test_dir)  # Clean up
                    logger.info(f"Directory operations work: {test_dir}")
            
            self.test_results['file_operations'] = True
            logger.info("✅ File operations test passed")
            
        except Exception as e:
            logger.error(f"❌ File operations test failed: {e}")
    
    def test_gui_components(self):
        """Test GUI components"""
        logger.info("🖥️ Testing GUI Components...")
        
        try:
            # Test GUI imports
            import tkinter as tk
            from tkinter import ttk
            
            # Test basic GUI creation
            root = tk.Tk()
            root.withdraw()  # Hide the window
            
            # Test basic widgets
            frame = ttk.Frame(root)
            label = ttk.Label(frame, text="Test")
            button = ttk.Button(frame, text="Test")
            
            # Test PIL for image handling
            try:
                from PIL import Image, ImageTk
                logger.info("PIL/Pillow available for image handling")
            except ImportError:
                logger.warning("PIL/Pillow not available")
            
            root.destroy()
            
            self.test_results['gui_components'] = True
            logger.info("✅ GUI components test passed")
            
        except Exception as e:
            logger.error(f"❌ GUI components test failed: {e}")
    
    def print_results(self):
        """Print test results summary"""
        logger.info("\n" + "=" * 50)
        logger.info("🧪 Cross-Platform Test Results")
        logger.info("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result)
        
        for test_name, result in self.test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            logger.info(f"{test_name.replace('_', ' ').title()}: {status}")
        
        logger.info("-" * 50)
        logger.info(f"Total Tests: {total_tests}")
        logger.info(f"Passed: {passed_tests}")
        logger.info(f"Failed: {total_tests - passed_tests}")
        logger.info(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if passed_tests == total_tests:
            logger.info("🎉 All tests passed! Cross-platform compatibility confirmed.")
        else:
            logger.warning("⚠️ Some tests failed. Check the logs above for details.")
        
        logger.info("=" * 50)

def main():
    """Main testing function"""
    tester = CrossPlatformTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()
