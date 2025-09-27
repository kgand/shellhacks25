# Messenger AI Assistant

A production-ready system that captures Messenger Web A/V from a Chrome Extension, streams it to a Python backend, and uses Google Gemini + ADK + Vertex AI Memory Bank to conduct & summarize conversations, extract action items, learn relationships, and persist memories.

## Architecture

```
Chrome Extension (MV3) → FastAPI (Python) → Google (Gemini + ADK + Firestore)
```

## Features

- **Chrome Extension (MV3)**: Side Panel UI, Offscreen document, tabCapture for A/V
- **FastAPI Backend**: WebSocket ingest, Gemini Live integration
- **ADK Agents**: Conversation processing with Memory Bank
- **Memory System**: Firestore storage with embedding-based retrieval
- **Revive API**: Intelligent memory recall and assembly

## Quick Start

### Prerequisites

- Node.js 20+
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

4. **Start development server**
   ```bash
   make dev
   ```

5. **Load Chrome extension**
   - Open Chrome and go to `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked" and select `assist/chrome-ext/dist`

## Usage

### Chrome Extension

1. Navigate to Messenger Web (messenger.com)
2. Click the extension icon to open the side panel
3. Toggle "I consent to recording my conversations"
4. Click "Start Capture" (requires user gesture)
5. The extension will begin recording and streaming to the backend

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
make dev          # Start development server
make chrome-build # Build Chrome extension
make install      # Install all dependencies
make clean        # Clean build artifacts
make test         # Run tests
make lint         # Run linters
make format       # Format code
```

### Project Structure

```
assist/
├── chrome-ext/          # Chrome Extension (MV3)
│   ├── manifest.json
│   ├── sw.js
│   ├── ui/
│   ├── offscreen.html
│   └── package.json
├── server/              # FastAPI Backend
│   ├── app.py
│   ├── ws_ingest.py
│   ├── gemini_live.py
│   ├── adk_agents.py
│   ├── revive_api.py
│   ├── memory/
│   └── requirements.txt
├── docs/                # Documentation
├── infra/               # Setup scripts
└── Makefile
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

Receives WebM audio/video chunks from Chrome extension.

**Message Format**:
```json
{
  "type": "audio_chunk",
  "data": "base64_encoded_webm_data",
  "timestamp": "2024-01-01T00:00:00Z",
  "connection_id": "conn_123"
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

2. **"Please navigate to Messenger Web first"**
   - Ensure you're on messenger.com
   - Refresh the page and try again

3. **"Memory store not initialized"**
   - Check Google Cloud credentials
   - Verify Firestore is enabled
   - Check environment variables

4. **Chrome extension not loading**
   - Ensure you're using Chrome (not other browsers)
   - Check that the extension is built (`make chrome-build`)
   - Verify manifest.json is valid

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
