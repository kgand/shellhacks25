# Makefile for Messenger AI Assistant

.PHONY: help start dev build clean

# Default target
help:
	@echo "Messenger AI Assistant - Available Commands:"
	@echo ""
	@echo "  make start    - Start the complete system"
	@echo "  make dev      - Start backend server only"
	@echo "  make build    - Build Chrome extension"
	@echo "  make clean    - Clean build artifacts"
	@echo ""

# Start complete system
start:
	@echo "🚀 Starting Messenger AI Assistant..."
	python assist/start.py

# Development server only
dev:
	@echo "🚀 Starting backend server..."
	cd assist/server && uvicorn app:app --host 127.0.0.1 --port 8000 --reload

# Build Chrome extension
build:
	@echo "🔨 Building Chrome extension..."
	cd assist/chrome-ext && npm install && npm run build

# Clean build artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf assist/chrome-ext/dist
	rm -rf assist/chrome-ext/node_modules
	rm -rf __pycache__
	rm -rf .pytest_cache