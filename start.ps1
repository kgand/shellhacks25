# Simple Screen Capture System - PowerShell Launcher
# Run with: powershell -ExecutionPolicy Bypass -File start.ps1

Write-Host "🚀 Simple Screen Capture System" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8+ and try again." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if we're in the right directory
if (-not (Test-Path "assist")) {
    Write-Host "❌ Please run this script from the project root directory" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check dependencies
Write-Host "🔍 Checking dependencies..." -ForegroundColor Yellow
try {
    python -c "import fastapi, uvicorn, cv2, mss, sounddevice" 2>$null
    Write-Host "✅ Dependencies found" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Some dependencies missing. Installing..." -ForegroundColor Yellow
    python setup.py
}

# Start the system
Write-Host "🚀 Starting system..." -ForegroundColor Green
python assist/launcher.py

Read-Host "Press Enter to exit"
