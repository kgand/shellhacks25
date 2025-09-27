#!/usr/bin/env python3
"""
Startup script for Messenger AI Assistant
This script helps you start all components in the correct order
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def run_command(command, cwd=None, shell=True):
    """Run a command and return success status"""
    try:
        result = subprocess.run(
            command,
            shell=shell,
            cwd=cwd,
            capture_output=True,
            text=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_backend_running():
    """Check if backend is already running"""
    try:
        import requests
        response = requests.get("http://localhost:8000/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def main():
    print("🚀 Starting Messenger AI Assistant System")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("assist").exists():
        print("❌ Error: Please run this script from the project root directory")
        print("   Expected to find 'assist' folder in current directory")
        sys.exit(1)
    
    # Check environment variables
    print("🔍 Checking environment...")
    required_vars = ['GOOGLE_PROJECT_ID', 'GEMINI_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("   Please create a .env file with the required variables")
        print("   See assist/.env.example for reference")
        sys.exit(1)
    
    print("✅ Environment variables found")
    
    # Check if backend is already running
    if check_backend_running():
        print("✅ Backend is already running")
    else:
        print("🔄 Starting backend server...")
        
        # Start the backend
        backend_cmd = "cd assist/server && uvicorn app:app --host 0.0.0.0 --port 8000 --reload"
        success, stdout, stderr = run_command(backend_cmd)
        
        if not success:
            print(f"❌ Failed to start backend: {stderr}")
            sys.exit(1)
        
        print("✅ Backend started successfully")
    
    # Check Chrome extension
    print("🔍 Checking Chrome extension...")
    extension_path = Path("assist/chrome-ext/dist")
    
    if not extension_path.exists():
        print("🔄 Building Chrome extension...")
        build_cmd = "cd assist/chrome-ext && npm install && npm run build"
        success, stdout, stderr = run_command(build_cmd)
        
        if not success:
            print(f"❌ Failed to build extension: {stderr}")
            sys.exit(1)
        
        print("✅ Chrome extension built successfully")
    else:
        print("✅ Chrome extension already built")
    
    print("\n🎉 System is ready!")
    print("\n📋 Next steps:")
    print("1. Open Chrome and go to chrome://extensions/")
    print("2. Enable 'Developer mode'")
    print("3. Click 'Load unpacked' and select: assist/chrome-ext/dist")
    print("4. Go to messenger.com")
    print("5. Click the extension icon to open the side panel")
    print("6. Test the recording functionality")
    
    print("\n🔧 Testing the system:")
    print("Run: python assist/scripts/test-system.py")
    
    print("\n📚 For detailed instructions, see: assist/docs/TESTING.md")

if __name__ == "__main__":
    main()
