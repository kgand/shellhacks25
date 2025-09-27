# Makefile for Messenger AI Assistant

.PHONY: help start dev gui install clean test setup kill kill-safe

# Default target
help:
	@echo "Messenger AI Assistant - Available Commands:"
	@echo ""
	@echo "  make start    - Start the complete system (backend + GUI)"
	@echo "  make dev      - Start backend server only"
	@echo "  make gui      - Start screen capture GUI only"
	@echo "  make install  - Install all dependencies"
	@echo "  make setup     - Complete setup (install + test)"
	@echo "  make test     - Test system components"
	@echo "  make kill     - Kill all Python server processes"
	@echo "  make kill-safe - Kill server processes (excludes current)"
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

# Kill all Python server processes
kill:
	@echo "🔪 Killing all Python server processes..."
	@python kill_python_servers.py --yes --force
	@echo "✅ Kill operation complete"

# Kill all Python server processes (safer - excludes current process)
kill-safe:
	@echo "🔪 Killing Python server processes (safe mode)..."
	@python -c "import psutil, os; killed=0; current_pid=os.getpid(); [killed := killed + 1 for p in psutil.process_iter(['pid', 'name', 'cmdline']) if p.info['pid'] != current_pid and 'python' in p.info['name'].lower() and any(k in ' '.join(p.info['cmdline']).lower() for k in ['app.py', 'server', 'fastapi', 'flask', 'django', 'uvicorn', 'screen_capture', 'gui.py', 'launcher.py', 'http.server']) and p.terminate()]; print(f'✅ Killed {killed} server processes')"
	@echo "✅ Safe kill operation complete"

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