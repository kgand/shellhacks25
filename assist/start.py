#!/usr/bin/env python3
"""
Simple startup script for Messenger AI Assistant
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    print("🚀 Starting Messenger AI Assistant")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("assist").exists():
        print("❌ Error: Please run this script from the project root directory")
        sys.exit(1)
    
    # Load environment variables
    env_file = Path("assist/.env")
    if env_file.exists():
        from dotenv import load_dotenv
        load_dotenv(env_file)
        print("✅ Environment loaded")
    else:
        print("⚠️  No .env file found (optional)")
    
    # Install dependencies if needed
    print("📦 Checking dependencies...")
    try:
        import fastapi
        import uvicorn
        print("✅ Dependencies already installed")
    except ImportError:
        print("🔄 Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "assist/server/requirements.txt"])
        print("✅ Dependencies installed")
    
    # Build Chrome extension if needed
    extension_path = Path("assist/chrome-ext/dist")
    if not extension_path.exists():
        print("🔨 Building Chrome extension...")
        os.chdir("assist/chrome-ext")
        subprocess.run(["npm", "install"])
        subprocess.run(["npm", "run", "build"])
        os.chdir("../..")
        print("✅ Chrome extension built")
    else:
        print("✅ Chrome extension already built")
    
    # Start the backend
    print("🚀 Starting backend server...")
    print("   Backend will run at: http://127.0.0.1:8000")
    print("   Health check: http://127.0.0.1:8000/health")
    print("   Press Ctrl+C to stop")
    print()
    
    os.chdir("assist/server")
    subprocess.run([
        sys.executable, "-m", "uvicorn", 
        "app:app", 
        "--host", "127.0.0.1", 
        "--port", "8000", 
        "--reload"
    ])

if __name__ == "__main__":
    main()
