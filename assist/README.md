# Messenger AI Assistant

A professional screen capture and AI processing system for Messenger Web conversations. This system captures audio and video from Messenger Web using Python screen detection, processes it through a FastAPI backend, and uses AI agents for conversation analysis, summarization, and memory storage.

## Features

- **Direct File-Based Capture**: No websockets, saves directly to files
- **AI-Powered Processing**: Conversation summarization and analysis
- **Memory Storage**: Persistent memory with Firestore integration
- **Professional GUI**: Clean, modern interface with real-time status
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Smart Capture**: Automatic window detection and smart cropping
- **Audio/Video Sync**: Simultaneous recording with optimization
- **Auto-Processing**: Automatic file processing pipeline
- **Color Correction**: Fixes blue tint issues in captured frames
- **Relationship Mining**: Discovers relationships between people

## Architecture

```
Python Screen Capture → FastAPI Backend → AI Processing → Memory Storage
```

### Components

1. **Screen Capture System** (`assist/screen_capture/`)
   - Direct file-based audio/video capture
   - Automatic Messenger window detection
   - Professional GUI interface
   - Smart cropping and color correction

2. **Backend API Server** (`assist/server/`)
   - FastAPI REST API
   - File upload and processing
   - Session management
   - Auto-processing pipeline

3. **AI Processing** (`assist/server/`)
   - Gemini Live API integration
   - ADK Agent Development Kit
   - Memory storage with Firestore
   - Conversation analysis and summarization

## Installation

### Prerequisites

- Python 3.8+
- Windows 10/11, macOS 10.15+, or Linux
- Audio drivers (for audio capture)

### Quick Setup

```bash
# Cross-platform setup
python setup.py

# Or use platform-specific scripts
# Windows
start.bat

# PowerShell
powershell -ExecutionPolicy Bypass -File start.ps1
```

### Key Dependencies

- `opencv-python`: Video processing
- `mss`: Fast screen capture
- `sounddevice`: Audio capture
- `fastapi`: Backend API
- `uvicorn`: ASGI server
- `pywin32`: Windows integration (Windows only)

## Usage

### Quick Start

1. **Launch the system**:
   ```bash
   python start.py
   ```

2. **Open Messenger Web** in your browser

3. **Select a Messenger window** from the GUI

4. **Click "Start Capture"** to begin recording

5. **Files are saved** to `assist/screen_capture/capture_output/` folder

### Manual Start

1. **Start backend**:
   ```bash
   python assist/server/app.py
   ```

2. **Start GUI**:
   ```bash
   python assist/screen_capture/gui.py
   ```

## Output Files

### Video Frames
- Format: `frame_XXXXXX_YYYYMMDD_HHMMSS_mmm.jpg`
- Location: `assist/screen_capture/capture_output/`
- Quality: 85% JPEG compression with optimization

### Audio
- Format: `audio_timestamp.wav`
- Location: `assist/screen_capture/capture_output/`
- Sample Rate: 44.1kHz, 16-bit, Stereo

## API Endpoints

### Root Endpoint
```
GET /                    # System information and available endpoints
```

### Health Check
```
GET /health              # System health status
```

### Session Management
```
POST /sessions            # Create session
GET /sessions            # List sessions
GET /sessions/{id}       # Get session
DELETE /sessions/{id}    # Delete session
```

### File Management
```
POST /upload/{session_id}           # Upload file
GET /files/{session_id}             # List session files
GET /download/{session_id}/{file}   # Download file
DELETE /files/{session_id}/{file}   # Delete file
```

### Processing
```
POST /process/{session_id}  # Process session
POST /auto-process         # Auto-process captured files
GET /stats                 # System statistics
POST /cleanup              # Cleanup old files
```

## Configuration

### GUI Settings

- **Frame Rate**: 10, 15, 20, 30 FPS
- **Quality**: Low, Medium, High
- **Audio**: Enable/Disable audio capture

### Backend Settings

- **Upload Directory**: `uploads/`
- **Output Directory**: `processed/`
- **Cleanup Threshold**: 24 hours

## Troubleshooting

### Common Issues

1. **No Messenger windows found**
   - Ensure Messenger Web is open
   - Check window title contains "messenger"
   - Try refreshing the window list

2. **Audio capture fails**
   - Install sounddevice: `pip install sounddevice`
   - Check audio drivers
   - Verify microphone permissions

3. **Screen capture fails**
   - Check window is visible
   - Ensure window is not minimized
   - Try selecting a different window

4. **Backend connection fails**
   - Check if backend is running on port 8000
   - Verify firewall settings
   - Check for port conflicts

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Performance Optimization

### Video Capture
- Lower frame rates for better performance
- Reduce JPEG quality for smaller files
- Limit capture region size

### Audio Capture
- Use lower sample rates for smaller files
- Enable audio compression
- Monitor disk space

### System Resources
- Monitor CPU usage during capture
- Check available disk space
- Close unnecessary applications

## Development

### Project Structure
```
assist/
├── screen_capture/
│   ├── simple_capture.py    # Core capture system
│   ├── simple_gui.py       # GUI interface
│   └── requirements.txt    # Dependencies
├── server/
│   ├── simple_app.py       # Backend API
│   └── requirements.txt    # Backend dependencies
├── simple_launcher.py      # System launcher
└── README.md              # This file
```

### Adding Features

1. **New Capture Formats**: Modify `SimpleScreenCapture` class
2. **GUI Enhancements**: Update `SimpleCaptureGUI` class
3. **API Extensions**: Add endpoints to `simple_app.py`
4. **Audio Processing**: Extend `SimpleAudioCapture` class

## Migration from Old System

### Removed Components
- ❌ WebSocket connections
- ❌ Async/await complexity
- ❌ Chrome extension integration
- ❌ Complex threading

### New Benefits
- ✅ Direct file output
- ✅ Simplified architecture
- ✅ Better error handling
- ✅ Easier debugging
- ✅ More reliable capture

## License

This project is part of the ShellHacks 2025 competition.

## Support

For issues and questions:
- GitHub Issues: [Repository Issues](https://github.com/kgand/shellhacks25/issues)
- Documentation: [Project Wiki](https://github.com/kgand/shellhacks25/wiki)

## Changelog

### v2.0.0 - Simplified Architecture
- Complete rewrite with file-based capture
- Removed websocket dependencies
- Added direct audio capture
- Simplified GUI and backend
- Better error handling and logging
- Professional code structure
