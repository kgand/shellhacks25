# Cross-Platform Messenger AI Assistant

A professional screen capture and AI processing system for Messenger Web conversations that works seamlessly across **Windows**, **macOS**, and **Linux**.

## 🌍 Platform Support

| Platform | Status | Notes |
|----------|--------|-------|
| **Windows 10/11** | ✅ Full Support | Native Windows API integration |
| **macOS 10.15+** | ✅ Full Support | Quartz and Cocoa framework integration |
| **Linux (Ubuntu/Debian)** | ✅ Full Support | X11 window system integration |

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (all platforms)
- **Ollama** installed and running
- **Audio drivers** (for audio capture)
- **Browser** (Chrome, Firefox, Safari, or Edge)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd shellhacks25
   ```

2. **Run cross-platform setup**
   ```bash
   cd assist
   python setup_cross_platform.py
   ```

3. **Install Ollama** (if not already installed)
   ```bash
   # Download from https://ollama.ai
   # Start Ollama service
   ollama serve
   
   # Pull required models
   ollama pull gemma3:4b
   ollama pull qwen3:8b
   ```

4. **Start the application**
   ```bash
   python start.py
   ```

## 🏗️ Architecture

```
Cross-Platform Messenger AI Assistant
├── Platform Detection Layer
│   ├── Windows API (win32gui, win32process)
│   ├── macOS APIs (Quartz, Cocoa)
│   └── Linux X11 (python3-xlib)
├── Cross-Platform Components
│   ├── Window Detection
│   ├── Audio Capture
│   ├── Screen Capture
│   └── File Management
├── AI Processing Layer
│   ├── Ollama VLM Integration
│   ├── Real-time Analysis
│   └── Summarization
└── User Interface
    ├── Professional GUI
    ├── Platform-specific Optimizations
    └── Error Handling
```

## 📋 Platform-Specific Features

### Windows
- **Window Detection**: Native Windows API using `win32gui` and `win32process`
- **Audio Capture**: DirectSound integration via `sounddevice`
- **Screen Capture**: MSS with Windows-specific optimizations
- **File Management**: Native Windows file operations

### macOS
- **Window Detection**: Quartz framework using `CGWindowListCopyWindowInfo`
- **Audio Capture**: Core Audio integration via `sounddevice`
- **Screen Capture**: MSS with macOS-specific optimizations
- **File Management**: Native macOS file operations
- **Accessibility**: Automatic permission detection and guidance

### Linux
- **Window Detection**: X11 window system using `python3-xlib`
- **Audio Capture**: ALSA/PulseAudio integration via `sounddevice`
- **Screen Capture**: MSS with Linux-specific optimizations
- **File Management**: Native Linux file operations
- **Display**: X11 display detection and configuration

## 🔧 Platform-Specific Setup

### Windows Setup
```bash
# Install Windows-specific dependencies
pip install pywin32 sounddevice

# Run setup
python setup_cross_platform.py
```

### macOS Setup
```bash
# Install macOS-specific dependencies
pip install pyobjc-framework-Quartz pyobjc-framework-Cocoa sounddevice

# Grant accessibility permissions (if needed)
# System Preferences > Security & Privacy > Privacy > Accessibility

# Run setup
python setup_cross_platform.py
```

### Linux Setup
```bash
# Install Linux-specific dependencies
pip install python3-xlib sounddevice

# Ensure X11 is running
echo $DISPLAY

# Run setup
python setup_cross_platform.py
```

## 🎯 Features by Platform

### Universal Features
- ✅ **Cross-Platform Screen Capture**: Works on all platforms
- ✅ **Audio Recording**: Multi-format audio support
- ✅ **AI Analysis**: Ollama VLM/LLM integration
- ✅ **Real-time Processing**: Continuous analysis
- ✅ **Professional GUI**: Modern interface
- ✅ **File Management**: Organized output

### Platform-Specific Optimizations

#### Windows
- **High Performance**: Optimized for Windows 10/11
- **Native Integration**: Windows API for best performance
- **Audio Quality**: DirectSound for high-quality audio
- **Window Detection**: Advanced browser window detection

#### macOS
- **Retina Support**: High-DPI display support
- **Accessibility**: Automatic permission handling
- **Audio Quality**: Core Audio for professional audio
- **Window Detection**: Quartz framework integration

#### Linux
- **X11 Integration**: Native Linux window system
- **Audio Support**: ALSA/PulseAudio compatibility
- **Performance**: Optimized for Linux systems
- **Window Detection**: X11 window management

## 🚀 Usage

### Starting the Application

1. **Complete System** (Recommended)
   ```bash
   python start.py
   ```

2. **Individual Components**
   ```bash
   # Terminal 1: Backend
   cd assist/server
   python app.py
   
   # Terminal 2: GUI
   cd assist/screen_capture
   python gui.py
   ```

### Platform-Specific Usage

#### Windows
- **Window Selection**: Automatic detection of browser windows
- **Audio Capture**: System audio recording
- **File Output**: Native Windows file paths

#### macOS
- **Accessibility**: May require permission grants
- **Window Selection**: Quartz-based window detection
- **Audio Capture**: Core Audio integration

#### Linux
- **X11 Display**: Requires X11 session
- **Window Selection**: X11 window system integration
- **Audio Capture**: ALSA/PulseAudio support

## 🔍 Troubleshooting

### Common Issues

#### Windows
1. **No Messenger windows found**
   - Ensure Messenger Web is open
   - Check Windows Defender settings
   - Try running as administrator

2. **Audio capture fails**
   - Check audio drivers
   - Verify microphone permissions
   - Test with `python -c "import sounddevice; print(sounddevice.query_devices())"`

#### macOS
1. **Accessibility permissions required**
   - Go to System Preferences > Security & Privacy > Privacy > Accessibility
   - Add your terminal or Python to allowed apps

2. **Window detection fails**
   - Ensure app has screen recording permissions
   - Check System Preferences > Security & Privacy > Privacy > Screen Recording

3. **Audio capture fails**
   - Check microphone permissions
   - Verify audio input devices

#### Linux
1. **X11 display not found**
   - Ensure X11 is running: `echo $DISPLAY`
   - Check if running in WSL (may need X11 forwarding)

2. **Audio capture fails**
   - Check ALSA/PulseAudio configuration
   - Verify audio device permissions

3. **Window detection fails**
   - Ensure X11 session is active
   - Check window manager compatibility

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Platform Detection

Check your platform:
```python
from assist.utils.platform_utils import platform_detector
print(f"Platform: {platform_detector.get_platform_name()}")
print(f"Windows: {platform_detector.is_windows}")
print(f"macOS: {platform_detector.is_mac}")
print(f"Linux: {platform_detector.is_linux}")
```

## 📊 Performance

### Platform-Specific Performance

| Platform | Screen Capture | Audio Capture | AI Processing |
|----------|----------------|---------------|---------------|
| **Windows** | Excellent | Excellent | Excellent |
| **macOS** | Excellent | Excellent | Excellent |
| **Linux** | Good | Good | Excellent |

### Optimization Tips

1. **Windows**: Use hardware acceleration when available
2. **macOS**: Grant all required permissions
3. **Linux**: Ensure X11 is properly configured

## 🤝 Contributing

### Platform-Specific Contributions

1. **Windows**: Test with different Windows versions
2. **macOS**: Test with different macOS versions
3. **Linux**: Test with different distributions

### Testing

```bash
# Test platform detection
python -c "from assist.utils.platform_utils import platform_detector; print(platform_detector.get_platform_name())"

# Test window detection
python -c "from assist.utils.window_detector import CrossPlatformWindowDetector; wd = CrossPlatformWindowDetector(); print(len(wd.find_messenger_windows()))"

# Test audio capture
python -c "from assist.utils.audio_capture import CrossPlatformAudioCapture; ac = CrossPlatformAudioCapture(); print(ac.audio_available)"
```

## 📄 License

This project is part of the ShellHacks 2025 competition.

## 🆘 Support

For platform-specific issues:
- **Windows**: Check Windows Defender and permissions
- **macOS**: Check System Preferences permissions
- **Linux**: Check X11 and audio configuration

For general support:
- Check the troubleshooting section
- Review the logs in `assist/server/logs/`
- Create an issue with platform information

## 📝 Changelog

### v2.1.0 - Cross-Platform Release
- ✅ **Full Windows Support**: Native Windows API integration
- ✅ **Full macOS Support**: Quartz and Cocoa framework integration
- ✅ **Full Linux Support**: X11 window system integration
- ✅ **Cross-Platform Audio**: Universal audio capture
- ✅ **Cross-Platform Screen Capture**: MSS with platform optimizations
- ✅ **Platform Detection**: Automatic platform detection and configuration
- ✅ **Professional Setup**: Cross-platform installation script
- ✅ **Comprehensive Testing**: Platform-specific testing framework
