# Messenger AI Assistant

A professional screen capture and AI processing system for Messenger Web conversations. This system captures audio and video from Messenger Web using Python screen detection, processes it through a FastAPI backend, and uses Ollama AI models for real-time conversation analysis and summarization.

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** (all platforms)
- **Windows 10/11**, **macOS 10.15+**, or **Linux (Ubuntu/Debian)**
- **Ollama** installed and running
- **Audio drivers** (for audio capture)
- **Browser** (Chrome, Firefox, Safari, or Edge)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd shellhacks25
   ```

2. **Install Ollama**
   ```bash
   # Download from https://ollama.ai
   # Start Ollama service
   ollama serve
   
   # Pull required models
   ollama pull gemma3:4b
   ollama pull qwen3:8b
   ```

3. **Run cross-platform setup**
   ```bash
   cd assist
   python setup_cross_platform.py
   ```

4. **Start the application**
   ```bash
   python start.py
   ```

## 🏗️ Architecture

```
Cross-Platform Screen Capture → FastAPI Backend → Ollama AI Processing → File Storage
├── Windows: Native Windows API
├── macOS: Quartz/Cocoa Framework  
└── Linux: X11 Window System
```

### Components

1. **Cross-Platform Screen Capture System** (`assist/screen_capture/`)
   - Direct file-based audio/video capture
   - Cross-platform Messenger window detection
   - Professional GUI interface
   - Smart cropping and color correction
   - **Windows**: Native Windows API integration
   - **macOS**: Quartz and Cocoa framework integration
   - **Linux**: X11 window system integration

2. **Backend API Server** (`assist/server/`)
   - FastAPI REST API
   - File upload and processing
   - Session management
   - Auto-processing pipeline

3. **AI Processing** (`assist/server/`)
   - Ollama VLM integration (gemma3:4b)
   - Ollama LLM integration (qwen3:8b)
   - Real-time frame analysis
   - Audio transcription and processing
   - Conversation summarization

## 📁 Project Structure

```
assist/
├── screen_capture/          # Screen capture system
│   ├── screen_capture.py    # Core capture engine
│   ├── gui.py              # GUI interface
│   └── requirements.txt    # Dependencies
├── server/                  # Backend API
│   ├── app.py              # FastAPI server
│   ├── ollama_client.py    # Ollama AI integration
│   ├── realtime_analyzer.py # Real-time analysis
│   ├── audio_processor.py  # Audio processing
│   ├── summarization_service.py # AI summarization
│   ├── integration_test.py # Testing framework
│   └── requirements.txt    # Backend dependencies
├── start_ollama_integration.py # Main launcher
└── README.md               # Documentation
```

## 🎯 Features

### Cross-Platform Screen Capture
- **Direct File Output**: No websockets, saves directly to files
- **Audio/Video Capture**: Simultaneous recording with optimization
- **Cross-Platform Window Detection**: Automatic Messenger window detection
- **Smart Cropping**: Focuses on video content, removes browser UI
- **Color Correction**: Fixes blue tint issues in captured frames
- **Platform-Specific Optimizations**: Native performance on all platforms

### AI Processing
- **Real-time VLM Analysis**: Frame-by-frame visual understanding using gemma3:4b
- **Audio Transcription**: Multi-format audio processing and transcription
- **Conversation Summarization**: AI-powered conversation summaries using qwen3:8b
- **Multi-modal Integration**: Visual + audio content analysis
- **Comprehensive Summaries**: Multiple summary types (brief, detailed, key points, timeline)

### Backend API
- **RESTful Endpoints**: Complete API for file management and AI processing
- **Session Management**: Organized capture sessions
- **Auto-Processing**: Automatic file processing pipeline
- **Real-time Analysis**: Continuous AI analysis of captured content
- **Statistics**: Usage tracking and monitoring

## 🚀 Usage

### Screen Capture Application

1. **Start Ollama** (if not already running)
   ```bash
   ollama serve
   ```

2. **Open Messenger Web** in your browser (messenger.com)

3. **Run the launcher**: `python start.py`

4. **Select a Messenger window** from the GUI

5. **Click "Start Capture"** to begin recording

6. **Click "Start AI Analysis"** for real-time AI processing

7. **Files are saved** to `assist/screen_capture/capture_output/` and `assist/server/processed/`

### API Endpoints

- `GET /health` - System health check
- `GET /ollama-status` - Ollama service status
- `POST /analyze-frame` - Analyze single frame with VLM
- `POST /process-text` - Process text with LLM
- `POST /start-analysis/{session_id}` - Start real-time analysis
- `GET /analysis-status` - Get analysis results
- `POST /generate-summary/{session_id}` - Generate session summary

### Example API Usage

```bash
# Check health
curl http://localhost:8000/health

# Check Ollama status
curl http://localhost:8000/ollama-status

# Start real-time analysis
curl -X POST http://localhost:8000/start-analysis/session_123

# Get analysis results
curl http://localhost:8000/analysis-status
```

## 🔧 Configuration

### Platform-Specific Setup

#### Windows
```bash
# Install Windows-specific dependencies
pip install pywin32 sounddevice

# Run setup
python setup_cross_platform.py
```

#### macOS
```bash
# Install macOS-specific dependencies
pip install pyobjc-framework-Quartz pyobjc-framework-Cocoa sounddevice

# Grant accessibility permissions (if needed)
# System Preferences > Security & Privacy > Privacy > Accessibility

# Run setup
python setup_cross_platform.py
```

#### Linux
```bash
# Install Linux-specific dependencies
pip install python3-xlib sounddevice

# Ensure X11 is running
echo $DISPLAY

# Run setup
python setup_cross_platform.py
```

### Ollama Setup

1. **Install Ollama**
   ```bash
   # Download from https://ollama.ai
   # Start Ollama service
   ollama serve
   ```

2. **Pull Required Models**
   ```bash
   # Vision model for frame analysis
   ollama pull gemma3:4b
   
   # Text model for summarization
   ollama pull qwen3:8b
   ```

3. **Verify Installation**
   ```bash
   # Check if models are available
   ollama list
   
   # Test Ollama API
   curl http://localhost:11434/api/tags
   ```

### GUI Settings

- **Frame Rate**: 10, 15, 20, 30 FPS
- **Quality**: Low, Medium, High
- **Audio**: Enable/Disable audio capture
- **AI Analysis**: Enable/Disable real-time AI processing

## 📊 Output Files

### Video Frames
- **Format**: `frame_XXXXXX_YYYYMMDD_HHMMSS_mmm.jpg`
- **Location**: `assist/screen_capture/capture_output/`
- **Quality**: 85% JPEG compression with optimization

### Audio
- **Format**: `audio_timestamp.wav`
- **Location**: `assist/screen_capture/capture_output/`
- **Specs**: 44.1kHz, 16-bit, Stereo

### AI Analysis Results
- **Analysis Results**: `assist/server/processed/{session_id}/analysis_results.json`
- **Conversation Summary**: `assist/server/processed/{session_id}/conversation_summary.json`
- **Processed Files**: `assist/server/processed/{session_id}/`

## 🛠️ Development

### Available Commands

```bash
python start.py                                    # Start complete system
python assist/start_ollama_integration.py         # Start with Ollama integration
python assist/server/app.py                       # Start backend only
python assist/screen_capture/gui.py               # Start GUI only
python setup.py                                   # Install dependencies
```

### Testing

```bash
# Test system components
python -c "import assist.server.app; print('Backend OK')"
python -c "import assist.screen_capture.screen_capture; print('Capture OK')"
python -c "import assist.screen_capture.gui; print('GUI OK')"

# Test Ollama integration
python assist/server/integration_test.py
python assist/server/test_ollama_client.py
```

## 🐛 Troubleshooting

### Platform-Specific Issues

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

### Common Issues

1. **No Messenger windows found**
   - Ensure Messenger Web is open
   - Check window title contains "messenger"
   - Try refreshing the window list

2. **Ollama not available**
   - Ensure Ollama is running: `ollama serve`
   - Check models are pulled: `ollama list`
   - Verify connection: `curl http://localhost:11434/api/tags`

3. **AI analysis not working**
   - Check Ollama status: `curl http://localhost:8000/ollama-status`
   - Ensure required models are installed: `ollama pull gemma3:4b && ollama pull qwen3:8b`
   - Check server logs for errors

4. **Audio capture fails**
   - Install sounddevice: `pip install sounddevice`
   - Check audio drivers and permissions

5. **Screen capture fails**
   - Ensure window is visible and not minimized
   - Try selecting a different window

6. **Backend connection fails**
   - Check if backend is running on port 8000
   - Verify firewall settings

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Performance

### Optimization Tips

- **Lower frame rates** for better performance
- **Reduce JPEG quality** for smaller files
- **Monitor disk space** during long captures
- **Close unnecessary applications** during capture

### System Requirements

- **CPU**: Multi-core processor recommended
- **RAM**: 4GB+ available memory
- **Storage**: 1GB+ free space for captures
- **Network**: Internet connection for AI processing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of the ShellHacks 2025 competition.

## 🆘 Support

For issues and questions:
- Check the troubleshooting section
- Review the logs in `assist/server/logs/`
- Create an issue with detailed information

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

### v2.0.0 - Professional Release
- Complete rewrite with file-based capture
- Removed websocket dependencies
- Added direct audio capture
- Professional GUI and backend
- Better error handling and logging
- AI processing pipeline
- Memory storage integration
