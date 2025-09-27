#!/bin/bash
# Setup script for Messenger AI Assistant (Linux/macOS)

set -e

echo "🚀 Setting up Messenger AI Assistant..."

# Check if running on supported OS
if [[ "$OSTYPE" != "linux-gnu"* && "$OSTYPE" != "darwin"* ]]; then
    echo "❌ This script is for Linux/macOS only. Use setup.ps1 for Windows."
    exit 1
fi

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+ from https://python.org/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
if [[ "$PYTHON_VERSION" < "3.11" ]]; then
    echo "❌ Python 3.11+ is required. Current version: $(python3 --version)"
    exit 1
fi

echo "✅ Python version: $(python3 --version)"

# Check gcloud CLI
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud CLI is not installed. Please install from https://cloud.google.com/sdk/docs/install"
    exit 1
fi

echo "✅ Google Cloud CLI installed"

# Check gcloud authentication
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ Not authenticated with Google Cloud. Please run: gcloud auth login"
    exit 1
fi

echo "✅ Google Cloud authenticated"

# Set up environment variables
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your Google Cloud project details"
fi

# Enable required Google Cloud APIs
echo "🔧 Enabling Google Cloud APIs..."
gcloud services enable aiplatform.googleapis.com
gcloud services enable firestore.googleapis.com
gcloud services enable generativelanguage.googleapis.com

echo "✅ Google Cloud APIs enabled"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
cd assist/server
pip install -r requirements.txt

echo "✅ Backend dependencies installed"

# Install screen capture dependencies
echo "📦 Installing screen capture dependencies..."
cd ../screen_capture
pip install -r requirements.txt

echo "✅ Screen capture dependencies installed"

# Create directories
echo "📁 Creating necessary directories..."
mkdir -p logs
mkdir -p data

echo "✅ Directories created"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Google Cloud project details"
echo "2. Run 'python assist/launcher.py' to start the application"
echo "3. Open Messenger Web in your browser"
echo "4. Use the screen capture GUI to start recording"
echo ""
echo "For more information, see docs/README.md"
