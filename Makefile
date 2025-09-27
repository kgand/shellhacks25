# Makefile for Messenger AI Assistant

.PHONY: help start dev gui clean install

# Default target
help:
	@echo "Messenger AI Assistant - Available Commands:"
	@echo ""
	@echo "  make start    - Start the complete system (backend + GUI)"
	@echo "  make dev      - Start backend server only"
	@echo "  make gui      - Start screen capture GUI only"
	@echo "  make install  - Install all dependencies"
	@echo "  make clean    - Clean build artifacts"
	@echo ""

# Start complete system
start:
	@echo "🚀 Starting Messenger AI Assistant..."
	python assist/launcher.py

# Development server only
dev:
	@echo "🚀 Starting backend server..."
	cd assist/server && uvicorn app:app --host 127.0.0.1 --port 8000 --reload

# Screen capture GUI only
gui:
	@echo "🖥️ Starting screen capture GUI..."
	cd assist/screen_capture && python gui.py

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	cd assist/server && pip install -r requirements.txt
	cd assist/screen_capture && pip install -r requirements.txt

# Clean build artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf assist/__pycache__
	rm -rf assist/server/__pycache__
	rm -rf assist/screen_capture/__pycache__