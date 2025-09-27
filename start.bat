@echo off
echo 🚀 Simple Screen Capture System
echo ================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "assist" (
    echo ❌ Please run this script from the project root directory
    pause
    exit /b 1
)

REM Start the system
echo Starting system...
python assist/launcher.py

pause
