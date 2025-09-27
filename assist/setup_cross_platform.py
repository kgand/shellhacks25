"""
Cross-platform setup script for Messenger AI Assistant
Handles Windows, macOS, and Linux installation
"""

import os
import sys
import subprocess
import platform
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CrossPlatformSetup:
    """Cross-platform setup for Messenger AI Assistant"""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.is_windows = self.system == 'windows'
        self.is_mac = self.system == 'darwin'
        self.is_linux = self.system == 'linux'
        
        # Get project root
        self.project_root = Path(__file__).parent
        self.screen_capture_dir = self.project_root / "screen_capture"
        self.server_dir = self.project_root / "server"
        
    def run_setup(self):
        """Run the complete setup process"""
        logger.info(f"Starting cross-platform setup for {self.system.title()}")
        
        try:
            # Check Python version
            self._check_python_version()
            
            # Install dependencies
            self._install_dependencies()
            
            # Setup platform-specific configurations
            self._setup_platform_config()
            
            # Verify installation
            self._verify_installation()
            
            logger.info("Setup completed successfully!")
            self._print_next_steps()
            
        except Exception as e:
            logger.error(f"Setup failed: {e}")
            sys.exit(1)
    
    def _check_python_version(self):
        """Check if Python version is compatible"""
        if sys.version_info < (3, 8):
            logger.error("Python 3.8 or higher is required")
            sys.exit(1)
        
        logger.info(f"Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    def _install_dependencies(self):
        """Install platform-specific dependencies"""
        logger.info("Installing dependencies...")
        
        # Install server dependencies
        self._install_requirements(self.server_dir / "requirements.txt")
        
        # Install screen capture dependencies
        self._install_requirements(self.screen_capture_dir / "requirements.txt")
        
        # Install platform-specific dependencies
        self._install_platform_dependencies()
    
    def _install_requirements(self, requirements_file):
        """Install requirements from a file"""
        if not requirements_file.exists():
            logger.warning(f"Requirements file not found: {requirements_file}")
            return
        
        try:
            logger.info(f"Installing requirements from {requirements_file}")
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
            ], check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install requirements: {e}")
            raise
    
    def _install_platform_dependencies(self):
        """Install platform-specific dependencies"""
        if self.is_windows:
            self._install_windows_dependencies()
        elif self.is_mac:
            self._install_mac_dependencies()
        elif self.is_linux:
            self._install_linux_dependencies()
    
    def _install_windows_dependencies(self):
        """Install Windows-specific dependencies"""
        logger.info("Installing Windows-specific dependencies...")
        
        try:
            # Install pywin32
            subprocess.run([sys.executable, "-m", "pip", "install", "pywin32"], check=True)
            
            # Install audio dependencies
            subprocess.run([sys.executable, "-m", "pip", "install", "sounddevice"], check=True)
            
        except subprocess.CalledProcessError as e:
            logger.warning(f"Some Windows dependencies failed to install: {e}")
    
    def _install_mac_dependencies(self):
        """Install macOS-specific dependencies"""
        logger.info("Installing macOS-specific dependencies...")
        
        try:
            # Install PyObjC frameworks
            subprocess.run([
                sys.executable, "-m", "pip", "install", 
                "pyobjc-framework-Quartz", "pyobjc-framework-Cocoa"
            ], check=True)
            
            # Install audio dependencies
            subprocess.run([sys.executable, "-m", "pip", "install", "sounddevice"], check=True)
            
        except subprocess.CalledProcessError as e:
            logger.warning(f"Some macOS dependencies failed to install: {e}")
    
    def _install_linux_dependencies(self):
        """Install Linux-specific dependencies"""
        logger.info("Installing Linux-specific dependencies...")
        
        try:
            # Install X11 dependencies
            subprocess.run([
                sys.executable, "-m", "pip", "install", "python3-xlib"
            ], check=True)
            
            # Install audio dependencies
            subprocess.run([sys.executable, "-m", "pip", "install", "sounddevice"], check=True)
            
        except subprocess.CalledProcessError as e:
            logger.warning(f"Some Linux dependencies failed to install: {e}")
    
    def _setup_platform_config(self):
        """Setup platform-specific configurations"""
        logger.info("Setting up platform-specific configurations...")
        
        # Create necessary directories
        os.makedirs("capture_output", exist_ok=True)
        os.makedirs("processed", exist_ok=True)
        os.makedirs("uploads", exist_ok=True)
        
        # Platform-specific setup
        if self.is_mac:
            self._setup_mac_config()
        elif self.is_linux:
            self._setup_linux_config()
    
    def _setup_mac_config(self):
        """Setup macOS-specific configurations"""
        logger.info("Setting up macOS configurations...")
        
        # Check for accessibility permissions
        logger.info("Note: You may need to grant accessibility permissions to the app")
        logger.info("Go to System Preferences > Security & Privacy > Privacy > Accessibility")
    
    def _setup_linux_config(self):
        """Setup Linux-specific configurations"""
        logger.info("Setting up Linux configurations...")
        
        # Check for X11
        if not os.environ.get('DISPLAY'):
            logger.warning("DISPLAY environment variable not set. X11 may not be available.")
    
    def _verify_installation(self):
        """Verify that the installation was successful"""
        logger.info("Verifying installation...")
        
        try:
            # Test imports
            import cv2
            import numpy as np
            import mss
            import sounddevice as sd
            
            logger.info("Core dependencies verified")
            
            # Test platform-specific imports
            if self.is_windows:
                try:
                    import win32gui
                    logger.info("Windows-specific dependencies verified")
                except ImportError:
                    logger.warning("Windows-specific dependencies not available")
            
            elif self.is_mac:
                try:
                    from AppKit import NSWorkspace
                    from Quartz import CGWindowListCopyWindowInfo
                    logger.info("macOS-specific dependencies verified")
                except ImportError:
                    logger.warning("macOS-specific dependencies not available")
            
            elif self.is_linux:
                try:
                    from Xlib import display
                    logger.info("Linux-specific dependencies verified")
                except ImportError:
                    logger.warning("Linux-specific dependencies not available")
            
        except ImportError as e:
            logger.error(f"Verification failed: {e}")
            raise
    
    def _print_next_steps(self):
        """Print next steps for the user"""
        print("\n" + "="*60)
        print("🎉 Setup Complete!")
        print("="*60)
        print(f"Platform: {self.system.title()}")
        print("\nNext steps:")
        print("1. Start Ollama (if not already running):")
        print("   ollama serve")
        print("\n2. Pull required models:")
        print("   ollama pull gemma3:4b")
        print("   ollama pull qwen3:8b")
        print("\n3. Start the application:")
        print("   python start.py")
        print("\n4. Or start components individually:")
        print("   # Terminal 1: Backend")
        print("   cd assist/server && python app.py")
        print("   # Terminal 2: GUI")
        print("   cd assist/screen_capture && python gui.py")
        print("\nFor help, see README.md or run with --help")
        print("="*60)

def main():
    """Main setup function"""
    setup = CrossPlatformSetup()
    setup.run_setup()

if __name__ == "__main__":
    main()
