#!/usr/bin/env python3
"""
Test script for the overhauled screen capture functionality
Tests all major components and error scenarios
"""

import asyncio
import logging
import time
import sys
import os
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from screen_detector import ScreenDetector, ScreenCapture, AudioCapture
import tkinter as tk
from tkinter import messagebox

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ScreenCaptureTester:
    """Comprehensive test suite for screen capture functionality"""
    
    def __init__(self):
        self.detector = ScreenDetector()
        self.capture = None
        self.test_results = {}
        
    def test_window_detection(self):
        """Test window detection functionality"""
        logger.info("Testing window detection...")
        try:
            windows = self.detector.find_messenger_windows()
            logger.info(f"Found {len(windows)} windows")
            
            for i, window in enumerate(windows):
                logger.info(f"Window {i+1}: {window.title} (PID: {window.pid})")
            
            self.test_results['window_detection'] = {
                'success': True,
                'window_count': len(windows),
                'windows': [{'title': w.title, 'pid': w.pid} for w in windows]
            }
            return True
            
        except Exception as e:
            logger.error(f"Window detection test failed: {e}")
            self.test_results['window_detection'] = {
                'success': False,
                'error': str(e)
            }
            return False
    
    def test_audio_capture(self):
        """Test audio capture functionality"""
        logger.info("Testing audio capture...")
        try:
            audio_capture = AudioCapture()
            
            if not audio_capture.audio_available:
                logger.warning("Audio capture not available (PyAudio not installed)")
                self.test_results['audio_capture'] = {
                    'success': True,
                    'available': False,
                    'message': 'Audio capture not available - PyAudio not installed'
                }
                return True
            
            # Test audio capture
            audio_capture.start_recording()
            time.sleep(1)  # Record for 1 second
            
            audio_data = audio_capture.get_audio_data()
            audio_capture.stop_recording()
            
            self.test_results['audio_capture'] = {
                'success': True,
                'available': True,
                'data_size': len(audio_data) if audio_data else 0
            }
            return True
            
        except Exception as e:
            logger.error(f"Audio capture test failed: {e}")
            self.test_results['audio_capture'] = {
                'success': False,
                'error': str(e)
            }
            return False
    
    async def test_screen_capture_initialization(self):
        """Test screen capture initialization"""
        logger.info("Testing screen capture initialization...")
        try:
            capture = ScreenCapture()
            
            # Test initialization
            result = await capture.initialize()
            
            self.test_results['capture_initialization'] = {
                'success': result,
                'message': 'Initialization successful' if result else 'No Messenger windows found'
            }
            return result
            
        except Exception as e:
            logger.error(f"Screen capture initialization test failed: {e}")
            self.test_results['capture_initialization'] = {
                'success': False,
                'error': str(e)
            }
            return False
    
    async def test_capture_without_backend(self):
        """Test capture functionality without backend connection"""
        logger.info("Testing capture without backend...")
        try:
            capture = ScreenCapture()
            
            # Find a window to test with
            windows = self.detector.find_messenger_windows()
            if not windows:
                logger.warning("No windows found for capture test")
                self.test_results['capture_test'] = {
                    'success': False,
                    'message': 'No windows available for testing'
                }
                return False
            
            # Test frame capture
            capture.selected_window = windows[0]
            frame = capture._capture_screen_frame()
            
            if frame is not None:
                logger.info(f"Successfully captured frame: {frame.shape}")
                self.test_results['capture_test'] = {
                    'success': True,
                    'frame_shape': frame.shape,
                    'frame_size': frame.nbytes
                }
                return True
            else:
                self.test_results['capture_test'] = {
                    'success': False,
                    'message': 'Frame capture returned None'
                }
                return False
                
        except Exception as e:
            logger.error(f"Capture test failed: {e}")
            self.test_results['capture_test'] = {
                'success': False,
                'error': str(e)
            }
            return False
    
    def test_gui_components(self):
        """Test GUI components"""
        logger.info("Testing GUI components...")
        try:
            # Test if GUI can be imported and basic components work
            from gui import ScreenCaptureGUI
            
            # Create a test window (don't show it)
            root = tk.Tk()
            root.withdraw()  # Hide the window
            
            # Test basic GUI creation
            gui = ScreenCaptureGUI()
            
            # Test window detection in GUI
            gui._update_window_list()
            
            # Test window selection
            windows = gui.detector.find_messenger_windows()
            if windows:
                gui.detector.set_selected_window(windows[0])
                logger.info(f"Selected window: {windows[0].title}")
            
            root.destroy()
            
            self.test_results['gui_test'] = {
                'success': True,
                'message': 'GUI components working correctly'
            }
            return True
            
        except Exception as e:
            logger.error(f"GUI test failed: {e}")
            self.test_results['gui_test'] = {
                'success': False,
                'error': str(e)
            }
            return False
    
    def run_all_tests(self):
        """Run all tests and return results"""
        logger.info("Starting comprehensive screen capture tests...")
        
        # Test 1: Window detection
        self.test_window_detection()
        
        # Test 2: Audio capture
        self.test_audio_capture()
        
        # Test 3: GUI components
        self.test_gui_components()
        
        # Test 4: Screen capture initialization (async)
        async def run_async_tests():
            await self.test_screen_capture_initialization()
            await self.test_capture_without_backend()
        
        asyncio.run(run_async_tests())
        
        # Print results
        self.print_test_results()
        
        return self.test_results
    
    def print_test_results(self):
        """Print comprehensive test results"""
        logger.info("\n" + "="*60)
        logger.info("SCREEN CAPTURE TEST RESULTS")
        logger.info("="*60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result.get('success', False))
        
        for test_name, result in self.test_results.items():
            status = "✅ PASS" if result.get('success', False) else "❌ FAIL"
            logger.info(f"{test_name}: {status}")
            
            if not result.get('success', False):
                if 'error' in result:
                    logger.error(f"  Error: {result['error']}")
                if 'message' in result:
                    logger.warning(f"  Message: {result['message']}")
            else:
                if 'message' in result:
                    logger.info(f"  {result['message']}")
        
        logger.info("="*60)
        logger.info(f"Tests passed: {passed_tests}/{total_tests}")
        logger.info("="*60)
        
        if passed_tests == total_tests:
            logger.info("🎉 All tests passed! Screen capture system is working correctly.")
        else:
            logger.warning(f"⚠️  {total_tests - passed_tests} test(s) failed. Check the logs above for details.")

def main():
    """Main test function"""
    print("🧪 Screen Capture Test Suite")
    print("=" * 40)
    
    tester = ScreenCaptureTester()
    results = tester.run_all_tests()
    
    # Return exit code based on results
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result.get('success', False))
    
    if passed_tests == total_tests:
        print("\n✅ All tests passed!")
        return 0
    else:
        print(f"\n❌ {total_tests - passed_tests} test(s) failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
