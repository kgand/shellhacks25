# Testing Guide - Messenger AI Assistant

This guide walks you through setting up and testing the complete system.

## Prerequisites

Before testing, ensure you have:
- Node.js 20+ installed
- Python 3.11+ installed
- Google Cloud CLI installed and authenticated
- A Google Cloud project with Vertex AI and Firestore enabled

## Quick Start

### 1. Environment Setup

```bash
# Clone and navigate to the project
cd shellhacks25

# Run the setup script
# On Windows:
powershell -ExecutionPolicy Bypass -File assist/infra/setup.ps1

# On Linux/macOS:
chmod +x assist/infra/setup.sh
./assist/infra/setup.sh
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Google Cloud Configuration
GOOGLE_PROJECT_ID=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account-key.json
VERTEX_LOCATION=us-central1

# Gemini API Configuration
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL_LIVE=gemini-2.0-flash-live-001
GEMINI_MODEL_REASONING=gemini-2.5-pro

# Firebase Configuration
FIREBASE_PROJECT_ID=your-firebase-project-id
```

## Testing Steps

### Step 1: Start the Backend Server

```bash
# Start the FastAPI server
make dev

# Or manually:
cd assist/server
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     All services initialized successfully
INFO:     Application startup complete.
```

### Step 2: Test Backend Health

Open a new terminal and test the backend:

```bash
# Test health endpoint
curl http://localhost:8000/health

# Expected response:
{
  "status": "healthy",
  "services": {
    "memory_store": true,
    "gemini_live": true,
    "adk_orchestrator": true,
    "websocket_ingest": true,
    "revive_api": true
  }
}
```

### Step 3: Build and Load Chrome Extension

```bash
# Build the extension
make chrome-build

# Or manually:
cd assist/chrome-ext
npm install
npm run build
```

**Load Extension in Chrome:**
1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select the `assist/chrome-ext/dist` folder
5. The extension should appear in your extensions list

### Step 4: Test Chrome Extension

1. **Navigate to Messenger Web:**
   - Go to `https://www.messenger.com`
   - Log in to your account

2. **Open Extension Side Panel:**
   - Click the extension icon in Chrome toolbar
   - The side panel should open with the clean UI

3. **Test Extension Functionality:**
   - Check that "Backend not connected" shows initially
   - Toggle "I consent to recording my conversations"
   - The "Start Capture" button should become enabled
   - Test the mute toggle and audio quality slider

### Step 5: Test Full Integration

1. **Start Recording:**
   - Click "Start Capture" button
   - You should see status change to "Recording started"
   - The button should change to "Stop Capture" (red)

2. **Test WebSocket Connection:**
   - Check browser console for WebSocket connection logs
   - Backend should show WebSocket connection established

3. **Test Audio Capture:**
   - Speak into your microphone
   - Check that audio is being captured (no errors in console)

4. **Stop Recording:**
   - Click "Stop Capture"
   - Status should return to "Ready to capture"

## Troubleshooting

### Common Issues

#### 1. "Backend not connected"
**Solution:**
- Ensure FastAPI server is running on port 8000
- Check firewall settings
- Verify no other service is using port 8000

#### 2. Chrome Extension not loading
**Solution:**
- Check that `assist/chrome-ext/dist` folder exists
- Verify `manifest.json` is valid
- Check Chrome console for errors

#### 3. "Please navigate to Messenger Web first"
**Solution:**
- Ensure you're on `messenger.com` domain
- Refresh the page and try again
- Check that the content script is injected

#### 4. WebSocket connection fails
**Solution:**
- Check that backend is running
- Verify WebSocket endpoint is accessible
- Check browser console for connection errors

#### 5. Google Cloud authentication errors
**Solution:**
- Verify `GOOGLE_APPLICATION_CREDENTIALS` path is correct
- Check that service account has required permissions
- Ensure APIs are enabled in Google Cloud Console

### Debug Mode

Enable debug logging:

```bash
# Set environment variable
export LOG_LEVEL=DEBUG

# Or add to .env file
LOG_LEVEL=DEBUG
```

### Log Files

Check these locations for logs:
- Backend logs: Console output from `make dev`
- Extension logs: Chrome DevTools Console
- WebSocket logs: Browser Network tab

## API Testing

### Test Revive API

```bash
# Test memory revival
curl -X POST http://localhost:8000/revive \
  -H "Content-Type: application/json" \
  -d '{"cue": "What did we discuss about the project?", "limit": 10}'
```

### Test Memory Statistics

```bash
# Get user memory statistics
curl http://localhost:8000/memories/default/statistics
```

### Test Memory Search

```bash
# Search memories
curl "http://localhost:8000/memories/default/search?query=project&limit=5"
```

## Performance Testing

### Load Testing

```bash
# Test with multiple connections
for i in {1..10}; do
  curl http://localhost:8000/health &
done
wait
```

### Memory Usage

```bash
# Monitor memory usage
ps aux | grep uvicorn
```

## Production Deployment

### Docker Deployment

```bash
# Build Docker image
make docker-build

# Run with Docker Compose
cd assist/server
docker-compose up
```

### Google Cloud Run

```bash
# Deploy to Cloud Run
gcloud run deploy messenger-ai-backend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## Success Criteria

✅ **Backend Health Check**: All services initialized  
✅ **Chrome Extension Loads**: No errors in extension console  
✅ **WebSocket Connection**: Stable connection to backend  
✅ **Audio Capture**: No errors during recording  
✅ **Memory Storage**: Data persists in Firestore  
✅ **Revive API**: Returns relevant memories  
✅ **UI Responsiveness**: All controls work smoothly  

## Next Steps

1. **Customize Settings**: Adjust audio quality and other preferences
2. **Test with Real Conversations**: Use with actual Messenger conversations
3. **Monitor Performance**: Check logs and system resources
4. **Scale Testing**: Test with multiple users and longer sessions

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review logs for error messages
3. Verify all prerequisites are met
4. Test individual components separately
