#!/usr/bin/env python3
"""
Messenger AI Assistant Launcher
Cross-platform system startup and management
"""

import subprocess
import sys
import os
import time
import threading
import webbrowser
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MessengerAILauncher:
    """Launcher for the Messenger AI Assistant system"""
    
    def __init__(self):
        self.backend_process = None
        self.gui_process = None
        self.is_running = False
        
    def check_dependencies(self):
        """Check if all dependencies are installed"""
        try:
            # Check backend dependencies
            import fastapi
            import uvicorn
            logger.info("✅ Backend dependencies found")
        except ImportError:
            logger.error("❌ Backend dependencies missing. Installing...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "server/requirements.txt"])
            
        try:
            # Check screen capture dependencies
            import cv2
            import mss
            import sounddevice
            logger.info("✅ Screen capture dependencies found")
        except ImportError:
            logger.error("❌ Screen capture dependencies missing. Installing...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "screen_capture/requirements.txt"])
            
    def start_backend(self):
        """Start the simplified backend server"""
        try:
            logger.info("🚀 Starting simplified backend server...")
            self.backend_process = subprocess.Popen([
                sys.executable, "app.py"
            ], cwd="server")
            
            # Wait for backend to start
            time.sleep(3)
            
            # Check if backend is running
            import requests
            try:
                response = requests.get("http://127.0.0.1:8000/health", timeout=5)
                if response.status_code == 200:
                    logger.info("✅ Backend server started successfully")
                    return True
            except:
                pass
                
            logger.error("❌ Backend server failed to start")
            return False
            
        except Exception as e:
            logger.error(f"❌ Error starting backend: {e}")
            return False
    
    def start_gui(self):
        """Start the simplified screen capture GUI"""
        try:
            logger.info("🖥️ Starting simplified screen capture GUI...")
            self.gui_process = subprocess.Popen([
                sys.executable, "gui.py"
            ], cwd="screen_capture")
            
            logger.info("✅ Screen capture GUI started")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error starting GUI: {e}")
            return False
    
    def run(self):
        """Run the complete system"""
        print("🚀 Messenger AI Assistant Launcher")
        print("=" * 40)
        
        # Check if we're in the right directory
        if not Path("assist").exists():
            print("❌ Error: Please run this script from the project root directory")
            sys.exit(1)
        
        # Change to assist directory
        os.chdir("assist")
        
        # Check dependencies
        self.check_dependencies()
        
        # Start backend
        if not self.start_backend():
            print("❌ Failed to start backend server")
            sys.exit(1)
        
        # Start GUI
        if not self.start_gui():
            print("❌ Failed to start screen capture GUI")
            self.cleanup()
            sys.exit(1)
        
        print("\n✅ Messenger AI Assistant is running!")
        print("   Backend: http://127.0.0.1:8000")
        print("   Health: http://127.0.0.1:8000/health")
        print("   GUI: Screen capture window should be open")
        print("\nFeatures:")
        print("   • Direct file-based capture (no websockets)")
        print("   • AI-powered conversation analysis")
        print("   • Automatic Messenger window detection")
        print("   • Memory storage and retrieval")
        print("   • Files saved to 'capture_output' folder")
        print("\nPress Ctrl+C to stop all services")
        
        try:
            # Keep running until interrupted
            while True:
                time.sleep(1)
                
                # Check if processes are still running
                if self.backend_process and self.backend_process.poll() is not None:
                    logger.error("Backend process died")
                    break
                    
                if self.gui_process and self.gui_process.poll() is not None:
                    logger.error("GUI process died")
                    break
                    
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")
            self.cleanup()
    
    def cleanup(self):
        """Clean up running processes"""
        if self.backend_process:
            self.backend_process.terminate()
            self.backend_process.wait()
            logger.info("Backend process terminated")
            
        if self.gui_process:
            self.gui_process.terminate()
            self.gui_process.wait()
            logger.info("GUI process terminated")

def main():
    """Main function"""
    launcher = MessengerAILauncher()
    launcher.run()

if __name__ == "__main__":
    main()
