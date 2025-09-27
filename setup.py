#!/usr/bin/env python3
"""
Setup script for Simple Screen Capture System
Automated installation and configuration
"""

import subprocess
import sys
import os
import platform
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required, found {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def install_dependencies():
    """Install all required dependencies"""
    print("\n📦 Installing dependencies...")
    
    # Install server dependencies
    if not run_command("cd assist/server && pip install -r requirements.txt", "Installing server dependencies"):
        return False
    
    # Install screen capture dependencies
    if not run_command("cd assist/screen_capture && pip install -r requirements.txt", "Installing screen capture dependencies"):
        return False
    
    return True

def test_imports():
    """Test if all modules can be imported"""
    print("\n🧪 Testing imports...")
    
    tests = [
        ("assist.server.app", "Backend server"),
        ("assist.screen_capture.screen_capture", "Screen capture"),
        ("assist.screen_capture.gui", "GUI"),
    ]
    
    for module, name in tests:
        try:
            __import__(module)
            print(f"✅ {name} imports successfully")
        except ImportError as e:
            print(f"❌ {name} import failed: {e}")
            return False
    
    return True

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = [
        "assist/capture_output",
        "assist/uploads", 
        "assist/processed",
        "assist/logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created {directory}")
    
    return True

def check_system_requirements():
    """Check system requirements"""
    print("\n🔍 Checking system requirements...")
    
    # Check OS
    system = platform.system()
    if system == "Windows":
        print("✅ Windows detected")
    elif system == "Darwin":
        print("✅ macOS detected")
    elif system == "Linux":
        print("✅ Linux detected")
    else:
        print(f"⚠️  Unknown system: {system}")
    
    # Check for required tools
    tools = ["pip", "python"]
    for tool in tools:
        try:
            subprocess.run([tool, "--version"], check=True, capture_output=True)
            print(f"✅ {tool} available")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"❌ {tool} not found")
            return False
    
    return True

def main():
    """Main setup function"""
    print("🚀 Simple Screen Capture System Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check system requirements
    if not check_system_requirements():
        print("❌ System requirements not met")
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        print("❌ Failed to create directories")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Test imports
    if not test_imports():
        print("❌ Import tests failed")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("  make start    - Start the complete system")
    print("  make dev      - Start backend only")
    print("  make gui      - Start GUI only")
    print("  make test     - Test system components")
    print("\nFor help: make help")

if __name__ == "__main__":
    main()
