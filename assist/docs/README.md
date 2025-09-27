# Messenger AI Assistant

A production-ready system that captures Messenger Web A/V using Python screen detection, streams it to a FastAPI backend, and uses Google Gemini + ADK + Vertex AI Memory Bank to conduct & summarize conversations, extract action items, learn relationships, and persist memories.

## Architecture

```
Python Screen Capture → FastAPI (Python) → Google (Gemini + ADK + Firestore)
```

## Features

- **Python Screen Capture**: Desktop application with GUI for capturing Messenger Web
- **FastAPI Backend**: WebSocket ingest, Gemini Live integration
- **ADK Agents**: Conversation processing with Memory Bank
- **Memory System**: Firestore storage with embedding-based retrieval
- **Revive API**: Intelligent memory recall and assembly

## Quick Start

### Prerequisites

- Python 3.11+
- Google Cloud CLI
- Google Cloud Project with Vertex AI and Firestore enabled

### Installation

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

4. **Start the application**
   ```bash
   python assist/launcher.py
   ```

## Usage

### Screen Capture Application

1. Open Messenger Web in your browser (messenger.com)
2. Run the launcher: `python assist/launcher.py`
3. The screen capture GUI will open automatically
4. Select a Messenger window from the list
5. Click "Start Capture" to begin recording
6. The application will capture both audio and video from the selected window

### Backend API

- **Health Check**: `GET /health`
- **WebSocket Ingest**: `WS /ingest`
- **Revive Memories**: `POST /revive`
- **Memory Statistics**: `GET /memories/{user_id}/statistics`
- **Search Memories**: `GET /memories/{user_id}/search`

### Example API Usage

```bash
# Check health
curl http://localhost:8000/health

# Revive memories
curl -X POST http://localhost:8000/revive \
  -H "Content-Type: application/json" \
  -d '{"cue": "What did we discuss about the project?", "limit": 10}'

# Get memory statistics
curl http://localhost:8000/memories/default/statistics
```

## Development

### Available Commands

```bash
python assist/launcher.py    # Start complete application
python assist/screen_capture/gui.py  # Start screen capture GUI only
python assist/server/app.py   # Start backend server only
```

### Project Structure

```
assist/
├── screen_capture/      # Python Screen Capture
│   ├── screen_detector.py
│   ├── gui.py
│   ├── requirements.txt
│   └── __init__.py
├── server/              # FastAPI Backend
│   ├── app.py
│   ├── adk_agents.py
│   ├── requirements.txt
│   └── legacy/
├── docs/                # Documentation
├── infra/               # Setup scripts
├── launcher.py          # Main launcher script
└── start.py            # Legacy startup script
```

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

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

### Google Cloud Setup

1. **Create a Google Cloud Project**
2. **Enable required APIs**:
   - Vertex AI API
   - Firestore API
   - Generative Language API
3. **Create a service account** with required permissions
4. **Download service account key** and set `GOOGLE_APPLICATION_CREDENTIALS`
5. **Initialize Firestore** in your project

## API Reference

### WebSocket Endpoint

**Endpoint**: `WS /ingest`

Receives audio/video data from Python screen capture application.

**Message Format**:
```json
{
  "type": "video_frame",
  "data": "hex_encoded_jpeg_data",
  "timestamp": "2024-01-01T00:00:00Z",
  "frame_count": 123
}
```

```json
{
  "type": "audio_chunk", 
  "data": "hex_encoded_audio_data",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Revive API

**Endpoint**: `POST /revive`

Retrieve and assemble memories based on a text cue.

**Request**:
```json
{
  "cue": "What did we discuss about the project?",
  "limit": 10,
  "user_id": "default"
}
```

**Response**:
```json
{
  "cue": "What did we discuss about the project?",
  "memories": [...],
  "recap": "Based on your conversations...",
  "count": 5
}
```

## Troubleshooting

### Common Issues

1. **"Backend not connected"**
   - Ensure the FastAPI server is running on port 8000
   - Check that WebSocket endpoint is accessible

2. **"No Messenger windows found"**
   - Ensure you have Messenger Web open in your browser
   - Try refreshing the window list in the GUI
   - Make sure the browser window title contains "Messenger"

3. **"Memory store not initialized"**
   - Check Google Cloud credentials
   - Verify Firestore is enabled
   - Check environment variables

4. **Screen capture not working**
   - Ensure you have the required dependencies installed
   - Check that you have proper permissions for screen capture
   - Try running as administrator (Windows) or with appropriate permissions

### Debug Mode

Enable debug logging by setting `LOG_LEVEL=DEBUG` in your `.env` file.

### Logs

Check logs in the `logs/` directory:
- `app.log` - Application logs
- `websocket.log` - WebSocket connection logs
- `memory.log` - Memory operations logs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linters
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs
3. Create an issue with detailed information
