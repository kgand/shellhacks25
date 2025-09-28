#!/usr/bin/env python3
"""
Startup script for the Cognitive Assistance System
Alzheimer's Support with Google A2A ADK Integration
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_environment():
    """Check if environment is properly configured"""
    print("🔍 Checking environment configuration...")
    
    # Check if .env file exists
    env_file = Path(__file__).parent / "backend" / ".env"
    if not env_file.exists():
        print("❌ Environment file not found")
        print("   Please run: python setup.py")
        return False
    
    # Check if API key is configured
    with open(env_file, 'r') as f:
        content = f.read()
        if "your_google_a2a_adk_api_key_here" in content:
            print("⚠️  A2A ADK API key not configured")
            print("   Please edit backend/.env and add your API key")
            return False
    
    print("✅ Environment configuration looks good")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    print("📦 Checking dependencies...")
    
    try:
        import fastapi
        import uvicorn
        import websockets
        print("✅ Core dependencies available")
        return True
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("   Please run: python setup.py")
        return False

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting Cognitive Assistance System...")
    print("=" * 60)
    
    # Change to backend directory
    backend_dir = Path(__file__).parent / "backend"
    os.chdir(backend_dir)
    
    # Start the server
    try:
        print("🌐 Starting server on http://localhost:8000")
        print("📱 Open your browser to access the interface")
        print("🎤 Grant microphone/camera permissions when prompted")
        print("💬 Start chatting with the cognitive assistant!")
        print("\n" + "=" * 60)
        print("Press Ctrl+C to stop the server")
        print("=" * 60)
        
        # Start the server
        subprocess.run([
            sys.executable, "-m", "uvicorn", "app:app", 
            "--host", "127.0.0.1", "--port", "8000", "--reload"
        ])
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False
    
    return True

def open_browser():
    """Open browser to the application"""
    print("🌐 Opening browser...")
    time.sleep(2)  # Give server time to start
    webbrowser.open("http://localhost:8000")

def main():
    """Main startup function"""
    print("🧠 Cognitive Assistance System for Alzheimer's Support")
    print("🤖 Powered by Google A2A ADK Multimodal AI")
    print("=" * 60)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Start server
    print("\n🚀 Starting the system...")
    start_server()

if __name__ == "__main__":
    main()
