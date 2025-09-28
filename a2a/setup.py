#!/usr/bin/env python3
"""
Setup script for the Cognitive Assistance System
Alzheimer's Support with Google A2A ADK Integration
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version}")

def install_requirements():
    """Install required packages"""
    print("📦 Installing Python dependencies...")
    
    requirements_file = Path(__file__).parent / "backend" / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ requirements.txt not found")
        sys.exit(1)
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ], check=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)

def setup_environment():
    """Set up environment variables"""
    print("🔧 Setting up environment...")
    
    env_file = Path(__file__).parent / "backend" / ".env"
    env_template = Path(__file__).parent / "backend" / "env_template.txt"
    
    if not env_file.exists() and env_template.exists():
        print("📝 Creating .env file from template...")
        with open(env_template, 'r') as template:
            content = template.read()
        
        with open(env_file, 'w') as env:
            env.write(content)
        
        print("✅ Environment file created")
        print("⚠️  Please edit .env file and add your Google A2A ADK API key")
    else:
        print("✅ Environment file already exists")

def check_a2a_adk_key():
    """Check if A2A ADK API key is configured"""
    env_file = Path(__file__).parent / "backend" / ".env"
    
    if env_file.exists():
        with open(env_file, 'r') as f:
            content = f.read()
            if "your_google_a2a_adk_api_key_here" in content:
                print("⚠️  Please configure your Google A2A ADK API key in .env file")
                return False
            elif "A2A_ADK_API_KEY=" in content:
                print("✅ A2A ADK API key appears to be configured")
                return True
    
    print("⚠️  A2A ADK API key not found in environment")
    return False

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    
    directories = [
        "backend/logs",
        "backend/data",
        "backend/sessions"
    ]
    
    for directory in directories:
        dir_path = Path(__file__).parent / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def run_tests():
    """Run basic tests to verify installation"""
    print("🧪 Running basic tests...")
    
    try:
        # Test imports
        sys.path.insert(0, str(Path(__file__).parent / "backend"))
        
        # Test cognitive assistance system
        from cognitive_assistance_system import CognitiveAssistant
        print("✅ Cognitive assistance system imports successfully")
        
        # Test A2A integration
        from cognitive_assistance_system.a2a_integration import A2ACognitiveIntegration
        print("✅ A2A integration imports successfully")
        
        print("✅ All tests passed")
        return True
        
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Cognitive Assistance System for Alzheimer's Support")
    print("=" * 70)
    
    # Check Python version
    check_python_version()
    
    # Install requirements
    install_requirements()
    
    # Create directories
    create_directories()
    
    # Setup environment
    setup_environment()
    
    # Check A2A ADK key
    a2a_configured = check_a2a_adk_key()
    
    # Run tests
    tests_passed = run_tests()
    
    print("\n" + "=" * 70)
    print("📋 Setup Summary:")
    print("=" * 70)
    
    if tests_passed:
        print("✅ Installation completed successfully")
    else:
        print("❌ Installation completed with errors")
        sys.exit(1)
    
    if not a2a_configured:
        print("⚠️  Please configure your Google A2A ADK API key")
        print("   1. Get your API key from Google Cloud Console")
        print("   2. Edit backend/.env file")
        print("   3. Replace 'your_google_a2a_adk_api_key_here' with your actual key")
    
    print("\n🎯 Next Steps:")
    print("   1. Configure your A2A ADK API key (if not done)")
    print("   2. Run: python backend/app.py")
    print("   3. Open: http://localhost:8000")
    print("   4. Start chatting with the cognitive assistance system!")
    
    print("\n📚 Documentation:")
    print("   - README.md: General overview")
    print("   - DEPLOYMENT_GUIDE.md: Deployment instructions")
    print("   - backend/README.md: Backend API documentation")

if __name__ == "__main__":
    main()
