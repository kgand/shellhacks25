#!/usr/bin/env python3
"""
Cross-platform startup script for Messenger AI Assistant
Automatically detects OS and starts the appropriate components
"""

import sys
import os
import platform
import subprocess
import time
import threading
from pathlib import Path

def check_dependencies():
    """Check if all dependencies are installed"""
    try:
        # Check backend dependencies
        import fastapi
        import uvicorn
        print("✅ Backend dependencies found")
    except ImportError:
        print("❌ Backend dependencies missing. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "assist/server/requirements.txt"])
        
    try:
        # Check screen capture dependencies
        import cv2
        import mss
        import sounddevice
        print("✅ Screen capture dependencies found")
    except ImportError:
        print("❌ Screen capture dependencies missing. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "assist/screen_capture/requirements.txt"])

def start_backend():
    """Start the backend server"""
    try:
        print("🚀 Starting backend server...")
        process = subprocess.Popen([
            sys.executable, "assist/server/app.py"
        ])
        
        # Wait for backend to start
        time.sleep(3)
        
        # Check if backend is running
        import requests
        try:
            response = requests.get("http://127.0.0.1:8000/health", timeout=5)
            if response.status_code == 200:
                print("✅ Backend server started successfully")
                return process
        except:
            pass
            
        print("❌ Backend server failed to start")
        return None
        
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return None

def start_gui():
    """Start the screen capture GUI"""
    try:
        print("🖥️ Starting screen capture GUI...")
        process = subprocess.Popen([
            sys.executable, "assist/screen_capture/gui.py"
        ])
        
        print("✅ Screen capture GUI started")
        return process
        
    except Exception as e:
        print(f"❌ Error starting GUI: {e}")
        return None

def main():
    """Main function"""
    print("🚀 Messenger AI Assistant")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("assist").exists():
        print("❌ Error: Please run this script from the project root directory")
        sys.exit(1)
    
    # Check dependencies
    check_dependencies()
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ Failed to start backend server")
        sys.exit(1)
    
    # Start GUI
    gui_process = start_gui()
    if not gui_process:
        print("❌ Failed to start screen capture GUI")
        if backend_process:
            backend_process.terminate()
        sys.exit(1)
    
    print("\n✅ Messenger AI Assistant is running!")
    print("   Backend: http://127.0.0.1:8000")
    print("   Health: http://127.0.0.1:8000/health")
    print("   GUI: Screen capture window should be open")
    print("\nFeatures:")
    print("   • Direct file-based capture (no websockets)")
    print("   • Simplified audio/video capture")
    print("   • Automatic Messenger window detection")
    print("   • Files saved to 'capture_output' folder")
    print("\nPress Ctrl+C to stop all services")
    
    try:
        # Keep running until interrupted
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if backend_process and backend_process.poll() is not None:
                print("❌ Backend process died")
                break
                
            if gui_process and gui_process.poll() is not None:
                print("❌ GUI process died")
                break
                
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        if backend_process:
            backend_process.terminate()
            backend_process.wait()
            print("Backend process terminated")
            
        if gui_process:
            gui_process.terminate()
            gui_process.wait()
            print("GUI process terminated")

if __name__ == "__main__":
    main()
