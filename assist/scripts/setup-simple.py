#!/usr/bin/env python3
"""
Simple setup script for Messenger AI Assistant
This script sets up the system with minimal dependencies
"""

import subprocess
import sys
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

def main():
    print("🚀 Setting up Messenger AI Assistant (Simplified Mode)")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("assist").exists():
        print("❌ Error: Please run this script from the project root directory")
        print("   Expected to find 'assist' folder in current directory")
        sys.exit(1)
    
    # Install Python dependencies
    print("📦 Installing Python dependencies...")
    success, stdout, stderr = run_command(
        "pip install -r assist/server/requirements_simple.txt"
    )
    
    if not success:
        print(f"❌ Failed to install Python dependencies: {stderr}")
        sys.exit(1)
    
    print("✅ Python dependencies installed")
    
    # Install Node.js dependencies
    print("📦 Installing Node.js dependencies...")
    success, stdout, stderr = run_command(
        "cd assist/chrome-ext && npm install"
    )
    
    if not success:
        print(f"❌ Failed to install Node.js dependencies: {stderr}")
        sys.exit(1)
    
    print("✅ Node.js dependencies installed")
    
    # Build Chrome extension
    print("🔨 Building Chrome extension...")
    success, stdout, stderr = run_command(
        "cd assist/chrome-ext && npm run build"
    )
    
    if not success:
        print(f"❌ Failed to build Chrome extension: {stderr}")
        sys.exit(1)
    
    print("✅ Chrome extension built")
    
    # Create .env file if it doesn't exist
    env_file = Path("assist/.env")
    if not env_file.exists():
        print("📝 Creating .env file...")
        env_content = """# Messenger AI Assistant Environment Variables
# These are optional for simplified mode

# Google Cloud Configuration (optional)
GOOGLE_PROJECT_ID=
GOOGLE_APPLICATION_CREDENTIALS=

# Gemini API Configuration (optional)
GEMINI_API_KEY=

# Firebase Configuration (optional)
FIREBASE_PROJECT_ID=

# Backend Configuration
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000
WEBSOCKET_PORT=8765
"""
        env_file.write_text(env_content)
        print("✅ .env file created in assist folder")
    else:
        print("✅ .env file already exists in assist folder")
    
    print("\n🎉 Setup complete!")
    print("\n📋 Next steps:")
    print("1. Start the backend: make dev")
    print("2. Test the system: make test-system")
    print("3. Load the Chrome extension from assist/chrome-ext/dist")
    print("4. Go to messenger.com and test the extension")
    
    print("\n🔧 Available commands:")
    print("  make dev          - Start backend server")
    print("  make test-system  - Test all components")
    print("  make chrome-build - Build Chrome extension")
    print("  make start        - Start with helper script")

if __name__ == "__main__":
    main()
