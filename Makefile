# Makefile for Simple Screen Capture System

.PHONY: help start dev gui install clean test setup

# Default target
help:
	@echo "Simple Screen Capture System - Available Commands:"
	@echo ""
	@echo "  make start    - Start the complete system (backend + GUI)"
	@echo "  make dev      - Start backend server only"
	@echo "  make gui      - Start screen capture GUI only"
	@echo "  make install  - Install all dependencies"
	@echo "  make setup    - Complete setup (install + test)"
	@echo "  make test     - Test system components"
	@echo "  make clean    - Clean build artifacts"
	@echo ""

# Start complete system
start:
	@echo "🚀 Starting Simple Screen Capture System..."
	python assist/launcher.py

# Development server only
dev:
	@echo "🚀 Starting backend server..."
	cd assist/server && python app.py

# Screen capture GUI only
gui:
	@echo "🖥️ Starting screen capture GUI..."
	cd assist/screen_capture && python gui.py

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	cd assist/server && pip install -r requirements.txt
	cd assist/screen_capture && pip install -r requirements.txt
	@echo "✅ Dependencies installed successfully"

# Complete setup
setup: install test
	@echo "✅ Setup complete! Run 'make start' to begin"

# Test system components
test:
	@echo "🧪 Testing system components..."
	@echo "Testing backend..."
	@cd assist/server && python -c "import app; print('✅ Backend imports successful')"
	@echo "Testing screen capture..."
	@cd assist/screen_capture && python -c "import screen_capture; print('✅ Screen capture imports successful')"
	@echo "Testing GUI..."
	@cd assist/screen_capture && python -c "import gui; print('✅ GUI imports successful')"
	@echo "✅ All tests passed"

# Clean build artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf assist/__pycache__
	rm -rf assist/server/__pycache__
	rm -rf assist/screen_capture/__pycache__
	rm -rf assist/capture_output
	rm -rf assist/uploads
	rm -rf assist/processed
	@echo "✅ Cleanup complete"