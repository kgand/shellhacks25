# Screen Capture System

A professional, high-performance screen capture system for Messenger AI Assistant that replaces Chrome extension functionality with a native desktop application.

## Features

- **Real-time Screen Capture**: Efficient capture of Messenger Web windows
- **Audio Recording**: Optional system audio capture with PyAudio
- **Adaptive Performance**: Smart frame rate adjustment based on system performance
- **Professional GUI**: Modern Tkinter-based interface with real-time status
- **Robust Error Handling**: Comprehensive error recovery and logging
- **WebSocket Integration**: Real-time data streaming to FastAPI backend
- **Cross-platform Support**: Windows, macOS, and Linux compatibility

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   GUI (Tkinter) │    │  Screen Capture  │    │  FastAPI Backend│
│                 │    │                  │    │                 │
│ • Window Select │◄──►│ • Frame Capture  │◄──►│ • WebSocket     │
│ • Start/Stop    │    │ • Audio Capture  │    │ • Data Storage  │
│ • Status Display │    │ • Performance    │    │ • Memory Store  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Installation

### Prerequisites

- Python 3.8+
- Windows 10+ (for win32gui support)
- Chrome/Firefox/Edge browser

### Dependencies

```bash
pip install -r requirements.txt
```

**Core Dependencies:**
- `opencv-python` - Computer vision and image processing
- `mss` - Fast screen capture
- `numpy` - Numerical computing
- `websockets` - WebSocket communication
- `pyautogui` - GUI automation
- `psutil` - System process monitoring
- `pywin32` - Windows API access

**Optional Dependencies:**
- `pyaudio` - Audio capture (requires PortAudio)

## Usage

### Quick Start

1. **Start the complete system:**
   ```bash
   make start
   ```

2. **Start only the screen capture GUI:**
   ```bash
   make gui
   ```

3. **Start only the backend server:**
   ```bash
   make dev
   ```

### Manual Usage

1. **Start the backend server:**
   ```bash
   cd assist/server
   uvicorn app:app --host 127.0.0.1 --port 8000 --reload
   ```

2. **Start the screen capture GUI:**
   ```bash
   cd assist/screen_capture
   python gui.py
   ```

### GUI Interface

The screen capture GUI provides:

- **Window Selection**: Automatic detection of Messenger windows
- **Real-time Status**: Connection status and capture indicators
- **Performance Monitoring**: Frame rate and data transfer statistics
- **Error Logging**: Comprehensive activity log with color coding
- **Settings**: Configurable capture parameters

## API Reference

### ScreenCapture Class

Main class for coordinating video and audio capture.

```python
capture = ScreenCapture(backend_url="ws://127.0.0.1:8000/ingest")

# Initialize and start capture
await capture.initialize()
await capture.start_capture(selected_window)

# Stop capture
await capture.stop_capture()
```

### ScreenDetector Class

Detects and manages Messenger windows.

```python
detector = ScreenDetector()
windows = detector.find_messenger_windows()
detector.set_selected_window(windows[0])
```

### AudioCapture Class

Handles system audio recording.

```python
audio = AudioCapture()
audio.start_recording()
data = audio.get_audio_data()
audio.stop_recording()
```

## Performance Optimization

### Adaptive Frame Rate

The system automatically adjusts capture frequency based on:
- Frame processing time
- Network latency
- System performance

### Smart Compression

- **Adaptive JPEG Quality**: Adjusts based on frame size
- **Progressive JPEG**: Better compression for large frames
- **Dynamic Size Limits**: Allows larger frames periodically

### Memory Management

- **Contiguous Arrays**: Optimized memory access
- **Resource Cleanup**: Automatic cleanup on errors
- **Thread Management**: Proper thread lifecycle management

## Error Handling

### Connection Recovery

- **Exponential Backoff**: Smart retry logic for failed connections
- **Automatic Reconnection**: Handles temporary network issues
- **Graceful Degradation**: Continues operation with reduced functionality

### Error Monitoring

- **Error Counting**: Tracks consecutive errors
- **Performance Monitoring**: Logs frame rates and processing times
- **Resource Cleanup**: Ensures proper cleanup on failures

## Testing

Run the comprehensive test suite:

```bash
cd assist/screen_capture
python test_capture.py
```

**Test Coverage:**
- Window detection
- Audio capture functionality
- GUI component testing
- Frame capture validation
- Error handling scenarios

## Configuration

### Environment Variables

- `BACKEND_URL`: WebSocket backend URL (default: `ws://127.0.0.1:8000/ingest`)
- `LOG_LEVEL`: Logging level (default: `INFO`)

### GUI Settings

Accessible through the Settings button:
- **Frame Rate**: 10-30 FPS options
- **Quality**: Low/Medium/High compression
- **Audio**: Enable/disable audio capture

## Troubleshooting

### Common Issues

1. **"No Messenger windows found"**
   - Ensure Messenger Web is open in browser
   - Check browser process is running
   - Try refreshing the window list

2. **"Audio capture not available"**
   - Install PyAudio: `pip install pyaudio`
   - On Windows, install PortAudio first
   - Audio capture is optional - system works without it

3. **"Connection failed"**
   - Ensure backend server is running
   - Check firewall settings
   - Verify WebSocket URL is correct

4. **"High CPU usage"**
   - Reduce frame rate in settings
   - Lower quality setting
   - Close unnecessary applications

### Performance Tips

- **Optimal Settings**: Use Medium quality with 15 FPS for best balance
- **System Resources**: Close unnecessary applications during capture
- **Network**: Ensure stable connection to backend
- **Browser**: Use hardware acceleration in browser settings

## Development

### Code Structure

```
assist/screen_capture/
├── gui.py              # Main GUI application
├── screen_detector.py   # Core capture functionality
├── test_capture.py     # Comprehensive test suite
├── requirements.txt    # Dependencies
└── README.md          # This file
```

### Contributing

1. Follow existing code style and patterns
2. Add tests for new functionality
3. Update documentation for API changes
4. Ensure all tests pass before submitting

### Debugging

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## License

This project is part of the Messenger AI Assistant system.

## Support

For issues and support:
- Check the troubleshooting section above
- Run the test suite to identify issues
- Review logs for error details
- Create an issue with detailed information
