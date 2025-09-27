# Makefile for Messenger AI Assistant

.PHONY: help dev chrome-build install clean test test-system start lint format

# Default target
help:
	@echo "Messenger AI Assistant - Available Commands:"
	@echo ""
	@echo "  make dev          - Start development server"
	@echo "  make chrome-build - Build Chrome extension"
	@echo "  make install      - Install all dependencies"
	@echo "  make clean        - Clean build artifacts"
	@echo "  make test         - Run tests"
	@echo "  make test-system  - Test entire system"
	@echo "  make start        - Start system with helper script"
	@echo "  make lint         - Run linters"
	@echo "  make format       - Format code"
	@echo ""

# Development server
dev:
	@echo "🚀 Starting development server..."
	cd assist/server && uvicorn app_simple:app --host 0.0.0.0 --port 8000 --reload

# Build Chrome extension
chrome-build:
	@echo "🔨 Building Chrome extension..."
	cd assist/chrome-ext && npm install && npm run build

# Install all dependencies
install:
	@echo "📦 Installing dependencies..."
	cd assist/server && pip install -r requirements_simple.txt
	cd assist/chrome-ext && npm install

# Simple setup
setup-simple:
	@echo "🚀 Setting up system (simplified mode)..."
	python assist/scripts/setup-simple.py

# Clean build artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf assist/chrome-ext/dist
	rm -rf assist/chrome-ext/node_modules
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf logs/*.log

# Run tests
test:
	@echo "🧪 Running tests..."
	cd assist/server && python -m pytest tests/ -v

# Test entire system
test-system:
	@echo "🧪 Testing entire system..."
	python assist/scripts/test-system.py

# Start system with helper
start:
	@echo "🚀 Starting system..."
	python assist/scripts/start-system.py

# Run linters
lint:
	@echo "🔍 Running linters..."
	cd assist/server && python -m flake8 . --max-line-length=100
	cd assist/chrome-ext && npm run lint

# Format code
format:
	@echo "✨ Formatting code..."
	cd assist/server && python -m black . --line-length=100
	cd assist/chrome-ext && npm run format

# Setup development environment
setup:
	@echo "🔧 Setting up development environment..."
	@if [ -f "assist/infra/setup.sh" ]; then \
		chmod +x assist/infra/setup.sh && \
		./assist/infra/setup.sh; \
	elif [ -f "assist/infra/setup.ps1" ]; then \
		powershell -ExecutionPolicy Bypass -File assist/infra/setup.ps1; \
	else \
		echo "❌ Setup script not found"; \
	fi

# Production build
build: chrome-build
	@echo "🏗️  Building for production..."
	cd assist/server && pip install -r requirements.txt

# Docker build
docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t messenger-ai-assistant .

# Docker run
docker-run:
	@echo "🐳 Running Docker container..."
	docker run -p 8000:8000 -p 8765:8765 messenger-ai-assistant

# Check system requirements
check:
	@echo "🔍 Checking system requirements..."
	@echo "Node.js version: $$(node --version 2>/dev/null || echo 'Not installed')"
	@echo "Python version: $$(python3 --version 2>/dev/null || echo 'Not installed')"
	@echo "Google Cloud CLI: $$(gcloud --version 2>/dev/null | head -1 || echo 'Not installed')"

# Generate documentation
docs:
	@echo "📚 Generating documentation..."
	cd assist/server && python -m pydoc -w app
	cd assist/server && python -m pydoc -w gemini_live
	cd assist/server && python -m pydoc -w revive_api

# Backup data
backup:
	@echo "💾 Backing up data..."
	mkdir -p backups
	tar -czf backups/backup-$$(date +%Y%m%d-%H%M%S).tar.gz data/ logs/

# Restore data
restore:
	@echo "📥 Restoring data..."
	@if [ -z "$(BACKUP_FILE)" ]; then \
		echo "❌ Please specify BACKUP_FILE=path/to/backup.tar.gz"; \
		exit 1; \
	fi
	tar -xzf $(BACKUP_FILE) -C .

# Monitor logs
logs:
	@echo "📊 Monitoring logs..."
	tail -f logs/*.log

# Health check
health:
	@echo "🏥 Checking system health..."
	curl -f http://localhost:8000/health || echo "❌ Server not responding"

# Deploy to production
deploy:
	@echo "🚀 Deploying to production..."
	@echo "⚠️  This is a placeholder - implement your deployment strategy"
	@echo "Consider using:"
	@echo "  - Google Cloud Run for the backend"
	@echo "  - Chrome Web Store for the extension"
	@echo "  - Cloud Firestore for data storage"
