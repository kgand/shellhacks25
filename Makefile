# Makefile for Messenger AI Assistant

.PHONY: help start dev gui install clean test setup

# Default target
help:
	@echo "Messenger AI Assistant - Available Commands:"
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
	@echo "🚀 Starting Messenger AI Assistant..."
	python start.py

# Development server only
dev:
	@echo "🚀 Starting backend server..."
	python assist/server/app.py

# Screen capture GUI only
gui:
	@echo "🖥️ Starting screen capture GUI..."
	python assist/screen_capture/gui.py

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

# Monitor system in real-time
monitor:
	@echo "📊 Starting system monitor..."
	python monitor_system.py

# Clean build artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf assist/__pycache__
	rm -rf assist/server/__pycache__
	rm -rf assist/screen_capture/__pycache__
	rm -rf assist/screen_capture/capture_output
	rm -rf assist/server/uploads
	rm -rf assist/server/processed
	@echo "✅ Cleanup complete"