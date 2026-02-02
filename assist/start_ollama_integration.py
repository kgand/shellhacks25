#!/usr/bin/env python3
"""
Start Ollama Integration System
Launches the complete Messenger AI Assistant with Ollama integration
"""

import subprocess
import sys
import os
import time
import threading
import webbrowser
from pathlib import Path
import logging
import requests

# Add utils to path for cross-platform support
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
from platform_utils import platform_detector

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OllamaIntegrationLauncher:
    """Launcher for the complete Ollama integration system"""
    
    def __init__(self):
        self.backend_process = None
        self.gui_process = None
        self.is_running = False
        
        # Log platform information
        logger.info(f"Initializing for {platform_detector.get_platform_name()}")
        
    def check_ollama_installation(self):
        """Check if Ollama is installed and running"""
        try:
            # Check if Ollama is running
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                logger.info("✅ Ollama is running")
                return True
        except:
            pass
        
        logger.warning("⚠️  Ollama is not running. Please start Ollama first:")
        logger.warning("   1. Install Ollama from https://ollama.ai")
        logger.warning("   2. Run: ollama serve")
        logger.warning("   3. Pull required models: ollama pull qwen2.5vl:7b && ollama pull llama3:8b")
        return False
    
    def check_dependencies(self):
        """Check if all dependencies are installed"""
        try:
            # Check backend dependencies
            import fastapi
            import uvicorn
            import opencv-python
            import numpy
            logger.info("✅ Backend dependencies found")
        except ImportError as e:
            logger.error(f"❌ Missing backend dependencies: {e}")
            logger.info("Installing dependencies...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "server/requirements.txt"])
            
        try:
            # Check screen capture dependencies
            import cv2
            import mss
            import sounddevice
            logger.info("✅ Screen capture dependencies found")
        except ImportError as e:
            logger.error(f"❌ Missing screen capture dependencies: {e}")
            logger.info("Installing dependencies...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "screen_capture/requirements.txt"])
    
    def start_backend(self):
        """Start the Ollama-integrated backend server"""
        try:
            logger.info("🚀 Starting Ollama-integrated backend server...")
            self.backend_process = subprocess.Popen([
                sys.executable, "app.py"
            ], cwd="server")
            
            # Wait for backend to start
            time.sleep(5)
            
            # Check if backend is running
            try:
                response = requests.get("http://127.0.0.1:8000/health", timeout=10)
                if response.status_code == 200:
                    logger.info("✅ Backend server started successfully")
                    
                    # Check Ollama integration
                    ollama_response = requests.get("http://127.0.0.1:8000/ollama-status", timeout=5)
                    if ollama_response.status_code == 200:
                        ollama_status = ollama_response.json()
                        if ollama_status.get("ollama_available"):
                            logger.info("✅ Ollama integration is working")
                        else:
                            logger.warning("⚠️  Ollama integration not available")
                    
                    return True
            except:
                pass
                
            logger.error("❌ Backend server failed to start")
            return False
            
        except Exception as e:
            logger.error(f"❌ Error starting backend: {e}")
            return False
    
    def start_gui(self):
        """Start the enhanced screen capture GUI"""
        try:
            logger.info("🖥️ Starting enhanced screen capture GUI...")
            self.gui_process = subprocess.Popen([
                sys.executable, "gui.py"
            ], cwd="screen_capture")
            
            logger.info("✅ Screen capture GUI started")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error starting GUI: {e}")
            return False
    
    def run_integration_test(self):
        """Run integration test to verify everything is working"""
        try:
            logger.info("🧪 Running integration test...")
            test_process = subprocess.Popen([
                sys.executable, "integration_test.py"
            ], cwd="server")
            
            # Wait for test to complete
            test_process.wait()
            
            if test_process.returncode == 0:
                logger.info("✅ Integration test passed")
                return True
            else:
                logger.warning("⚠️  Integration test had issues")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error running integration test: {e}")
            return False
    
    def run(self):
        """Run the complete Ollama integration system"""
        print("🚀 Messenger AI Assistant - Ollama Integration")
        print("=" * 60)
        
        # Check if we're in the right directory
        if not Path("assist").exists():
            print("❌ Error: Please run this script from the project root directory")
            sys.exit(1)
        
        # Change to assist directory
        os.chdir("assist")
        
        # Check Ollama installation
        ollama_available = self.check_ollama_installation()
        if not ollama_available:
            print("\n⚠️  Ollama is not running. Some features will not work.")
            print("   Please start Ollama and pull the required models:")
            print("   ollama pull qwen2.5vl:7b")
            print("   ollama pull llama3:8b")
            print("\n   Continuing without Ollama...")
        
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
        
        # Run integration test
        if ollama_available:
            self.run_integration_test()
        
        print("\n✅ Messenger AI Assistant with Ollama Integration is running!")
        print("   Backend: http://127.0.0.1:8000")
        print("   Health: http://127.0.0.1:8000/health")
        print("   GUI: Screen capture window should be open")
        print("\n🤖 Ollama Integration Features:")
        print("   • Real-time VLM analysis of Messenger conversations")
        print("   • Audio transcription and processing")
        print("   • AI-powered conversation summarization")
        print("   • Multi-modal analysis (visual + audio)")
        print("   • Automatic content analysis and insights")
        print("   • Files saved to 'capture_output' and 'processed' folders")
        print("\n📖 Usage:")
        print("   1. Open Messenger Web in your browser")
        print("   2. Select a Messenger window in the GUI")
        print("   3. Click 'Start Capture' to begin recording")
        print("   4. Click 'Start AI Analysis' for real-time analysis")
        print("   5. View AI insights and summaries in the GUI")
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
            print("\n🛑 Shutting down Ollama integration system...")
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
    launcher = OllamaIntegrationLauncher()
    launcher.run()

if __name__ == "__main__":
    main()
