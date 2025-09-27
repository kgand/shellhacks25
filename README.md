# Messenger AI Assistant

A professional screen capture and AI processing system for Messenger Web conversations. This system captures audio and video from Messenger Web using Python screen detection, processes it through a FastAPI backend, and uses AI agents for conversation analysis, summarization, and memory storage.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Windows 10/11 or macOS 10.15+
- Audio drivers (for audio capture)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd shellhacks25
   ```

2. **Run setup**
   ```bash
   # Cross-platform setup
   python setup.py
   
   # Or use platform-specific scripts
   # Windows
   start.bat
   
   # PowerShell
   powershell -ExecutionPolicy Bypass -File start.ps1
   ```

3. **Start the application**
   ```bash
   python start.py
   ```

## 🏗️ Architecture

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

## 📁 Project Structure

```
assist/
├── screen_capture/          # Screen capture system
│   ├── screen_capture.py    # Core capture engine
│   ├── gui.py              # GUI interface
│   └── requirements.txt    # Dependencies
├── server/                  # Backend API
│   ├── app.py              # FastAPI server
│   ├── adk_agents.py       # AI agents
│   ├── gemini_live.py      # Gemini integration
│   ├── memory/             # Memory storage
│   ├── models/             # Data schemas
│   ├── prompts/            # AI prompts
│   └── requirements.txt    # Backend dependencies
├── launcher.py             # System launcher
└── README.md               # Documentation
```

## 🎯 Features

### Screen Capture
- **Direct File Output**: No websockets, saves directly to files
- **Audio/Video Capture**: Simultaneous recording with optimization
- **Window Detection**: Automatic Messenger window detection
- **Smart Cropping**: Focuses on video content, removes browser UI
- **Color Correction**: Fixes blue tint issues in captured frames

### AI Processing
- **Conversation Summarization**: AI-powered conversation summaries
- **Action Item Extraction**: Identifies and categorizes action items
- **Relationship Mining**: Discovers relationships between people
- **Memory Storage**: Persistent memory with Firestore integration
- **Revive API**: Intelligent memory recall and assembly

### Backend API
- **RESTful Endpoints**: Complete API for file management
- **Session Management**: Organized capture sessions
- **Auto-Processing**: Automatic file processing pipeline
- **Statistics**: Usage tracking and monitoring

## 🚀 Usage

### Screen Capture Application

1. **Open Messenger Web** in your browser (messenger.com)
2. **Run the launcher**: `python start.py`
3. **Select a Messenger window** from the GUI
4. **Click "Start Capture"** to begin recording
5. **Files are saved** to `assist/screen_capture/capture_output/`

### API Endpoints

- `GET /health` - System health check
- `POST /sessions` - Create capture session
- `POST /upload/{session_id}` - Upload files
- `POST /auto-process` - Process captured files
- `GET /stats` - System statistics

### Example API Usage

```bash
# Check health
curl http://localhost:8000/health

# Auto-process captured files
curl -X POST http://localhost:8000/auto-process

# Get statistics
curl http://localhost:8000/stats
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with:

```env
# Google Cloud Configuration
GOOGLE_PROJECT_ID=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account-key.json

# Gemini API Configuration
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL_LIVE=gemini-2.0-flash-live-001
```

### GUI Settings

- **Frame Rate**: 10, 15, 20, 30 FPS
- **Quality**: Low, Medium, High
- **Audio**: Enable/Disable audio capture

## 📊 Output Files

### Video Frames
- **Format**: `frame_XXXXXX_YYYYMMDD_HHMMSS_mmm.jpg`
- **Location**: `assist/screen_capture/capture_output/`
- **Quality**: 85% JPEG compression with optimization

### Audio
- **Format**: `audio_timestamp.wav`
- **Location**: `assist/screen_capture/capture_output/`
- **Specs**: 44.1kHz, 16-bit, Stereo

## 🛠️ Development

### Available Commands

```bash
python start.py                    # Start complete system
python assist/server/app.py       # Start backend only
python assist/screen_capture/gui.py # Start GUI only
python setup.py                   # Install dependencies
```

### Testing

```bash
# Test system components
python -c "import assist.server.app; print('Backend OK')"
python -c "import assist.screen_capture.screen_capture; print('Capture OK')"
python -c "import assist.screen_capture.gui; print('GUI OK')"
```

## 🐛 Troubleshooting

### Common Issues

1. **No Messenger windows found**
   - Ensure Messenger Web is open
   - Check window title contains "messenger"
   - Try refreshing the window list

2. **Audio capture fails**
   - Install sounddevice: `pip install sounddevice`
   - Check audio drivers and permissions

3. **Screen capture fails**
   - Ensure window is visible and not minimized
   - Try selecting a different window

4. **Backend connection fails**
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

### v2.0.0 - Professional Release
- Complete rewrite with file-based capture
- Removed websocket dependencies
- Added direct audio capture
- Professional GUI and backend
- Better error handling and logging
- Cross-platform support
- AI processing pipeline
- Memory storage integration
