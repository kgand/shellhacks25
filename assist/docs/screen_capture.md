# Screen Capture System Documentation

## Overview

The Messenger AI Assistant now uses a Python-based screen capture system instead of a Chrome extension. This approach provides better reliability, easier setup, and more control over the capture process.

## Architecture

```
Python Screen Capture GUI → FastAPI Backend → Google (Gemini + ADK + Firestore)
```

## Components

### 1. Screen Detector (`screen_detector.py`)

**Purpose**: Detects and captures Messenger Web windows

**Key Features**:
- Automatic window detection for Messenger Web
- Cross-platform screen capture using MSS
- Audio capture using PyAudio
- WebSocket streaming to backend

**Classes**:
- `ScreenDetector`: Finds Messenger windows
- `AudioCapture`: Captures system audio
- `ScreenCapture`: Main coordinator class

### 2. GUI Interface (`gui.py`)

**Purpose**: User-friendly desktop application

**Features**:
- Window selection interface
- Real-time status monitoring
- Connection status to backend
- Logging display
- Start/Stop controls

### 3. Launcher (`launcher.py`)

**Purpose**: Starts both backend and GUI automatically

**Features**:
- Dependency checking
- Process management
- Error handling
- Clean shutdown

## Installation

### Prerequisites

- Python 3.11+
- Windows 10+ (for win32gui support)
- Google Cloud credentials

### Dependencies

**Backend Dependencies** (`server/requirements.txt`):
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
websockets==12.0
python-dotenv==1.0.0
pydantic==2.5.0
requests==2.31.0
```

**Screen Capture Dependencies** (`screen_capture/requirements.txt`):
```
opencv-python==4.8.1.78
pyautogui==0.9.54
psutil==5.9.6
Pillow==10.1.0
mss==9.0.1
pyaudio==0.2.11
websockets==12.0
numpy==1.24.3
pywin32==306
```

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd shellhacks25
   ```

2. **Run setup script**
   ```bash
   # Linux/macOS
   chmod +x assist/infra/setup.sh
   ./assist/infra/setup.sh
   
   # Windows
   powershell -ExecutionPolicy Bypass -File assist/infra/setup.ps1
   ```

3. **Configure environment**
   ```bash
   cp assist/.env.example .env
   # Edit .env with your Google Cloud project details
   ```

## Usage

### Quick Start

1. **Start the application**
   ```bash
   python assist/launcher.py
   ```

2. **Open Messenger Web**
   - Navigate to messenger.com in your browser
   - Make sure the window title contains "Messenger"

3. **Use the GUI**
   - The screen capture GUI will open automatically
   - Select a Messenger window from the list
   - Click "Start Capture" to begin recording

### Manual Usage

**Start backend only**:
```bash
python assist/server/app.py
```

**Start GUI only**:
```bash
python assist/screen_capture/gui.py
```

## Technical Details

### Window Detection

The system uses multiple methods to detect Messenger windows:

1. **Process enumeration**: Scans running processes for browsers
2. **Window title matching**: Looks for "messenger" keywords
3. **URL detection**: Checks for messenger.com domains

### Screen Capture

**Video Capture**:
- Uses MSS (Multi-Screen Shot) for efficient screen capture
- Captures specific window regions
- Converts to JPEG format for transmission
- Configurable quality settings

**Audio Capture**:
- Uses PyAudio for system audio capture
- 44.1kHz sample rate, stereo
- Real-time streaming to backend

### Data Transmission

**WebSocket Protocol**:
- Connects to `ws://127.0.0.1:8000/ingest`
- Sends JSON messages with hex-encoded data
- Automatic reconnection with exponential backoff

**Message Formats**:

Video frame:
```json
{
  "type": "video_frame",
  "data": "hex_encoded_jpeg_data",
  "timestamp": "2024-01-01T00:00:00Z",
  "frame_count": 123
}
```

Audio chunk:
```json
{
  "type": "audio_chunk",
  "data": "hex_encoded_audio_data",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## Configuration

### Environment Variables

Create a `.env` file with:

```env
# Google Cloud Configuration
GOOGLE_PROJECT_ID=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account-key.json
VERTEX_LOCATION=us-central1

# Gemini API Configuration
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL_LIVE=gemini-2.0-flash-live-001
GEMINI_MODEL_REASONING=gemini-2.5-pro

# Firebase Configuration
FIREBASE_PROJECT_ID=your-firebase-project-id
```

### GUI Settings

The GUI provides several configuration options:

- **Bitrate**: Audio quality (64, 128, 256, 512 kbps)
- **Window Selection**: Choose specific Messenger window
- **Connection Status**: Monitor backend connectivity

## Troubleshooting

### Common Issues

1. **"No Messenger windows found"**
   - Ensure Messenger Web is open in your browser
   - Check that the window title contains "Messenger"
   - Try refreshing the window list

2. **"Backend not connected"**
   - Ensure the FastAPI server is running on port 8000
   - Check firewall settings
   - Verify WebSocket endpoint accessibility

3. **Screen capture not working**
   - Check permissions for screen capture
   - Ensure required dependencies are installed
   - Try running as administrator (Windows)

4. **Audio not captured**
   - Check system audio settings
   - Ensure PyAudio is properly installed
   - Verify audio device permissions

### Debug Mode

Enable debug logging by setting `LOG_LEVEL=DEBUG` in your `.env` file.

### Logs

Check the GUI log panel for real-time information about:
- Window detection
- Capture status
- Connection status
- Error messages

## Development

### Project Structure

```
assist/screen_capture/
├── __init__.py
├── screen_detector.py    # Core capture logic
├── gui.py               # GUI interface
├── requirements.txt     # Dependencies
└── README.md           # This file
```

### Adding Features

1. **New capture methods**: Extend `ScreenCapture` class
2. **GUI improvements**: Modify `ScreenCaptureGUI` class
3. **Window detection**: Update `ScreenDetector` class

### Testing

```bash
# Test screen detection
python assist/screen_capture/screen_detector.py

# Test GUI
python assist/screen_capture/gui.py

# Test backend
python assist/server/app.py
```

## Performance Considerations

### Optimization Tips

1. **Frame rate**: Adjust capture frequency based on needs
2. **Quality**: Balance between quality and bandwidth
3. **Window size**: Capture only necessary regions
4. **Audio**: Use appropriate sample rates

### Resource Usage

- **CPU**: Moderate usage for screen capture
- **Memory**: Low memory footprint
- **Network**: Efficient WebSocket streaming
- **Storage**: Minimal local storage requirements

## Security

### Privacy Considerations

- No data is stored locally
- All data is streamed to backend
- User consent required before capture
- Secure WebSocket connections

### Permissions

- Screen capture permissions
- Audio capture permissions
- Network access for backend communication

## Migration from Chrome Extension

### Key Differences

1. **No browser extension required**
2. **Desktop application instead of browser UI**
3. **Better cross-platform support**
4. **More reliable capture**

### Migration Steps

1. Remove old Chrome extension
2. Install new Python dependencies
3. Update configuration files
4. Use new launcher script

## Support

For issues and questions:

1. Check the troubleshooting section
2. Review the GUI logs
3. Verify dependencies are installed
4. Create an issue with detailed information

## License

This project is licensed under the MIT License.
