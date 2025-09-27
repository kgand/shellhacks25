# Chrome Extension Testing Guide

This guide walks you through testing the Chrome extension with the full backend functionality.

## Prerequisites

1. **Backend Running**: The FastAPI server must be running
2. **Chrome Extension Built**: Extension must be built and loaded
3. **Messenger Web**: Access to messenger.com

## Step-by-Step Testing

### 1. Start the Backend

```bash
# Stop any existing server (Ctrl+C if running)
# Then start the full backend
make dev
```

**Expected Output:**
```
🚀 Starting development server...
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     🚀 Starting Messenger AI Assistant Backend...
INFO:     ✅ Memory store initialized
INFO:     ✅ Gemini Live client initialized
INFO:     ✅ ADK orchestrator initialized
INFO:     ✅ WebSocket ingest initialized
INFO:     ✅ Revive API initialized
INFO:     🎉 All services initialized successfully!
```

### 2. Test Backend Health

Open a new terminal and test:

```bash
curl http://127.0.0.1:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "services": {
    "memory_store": true,
    "gemini_live": true,
    "adk_orchestrator": true,
    "websocket_ingest": true,
    "revive_api": true
  },
  "message": "All services operational"
}
```

### 3. Build Chrome Extension

```bash
make chrome-build
```

**Expected Output:**
```
🔨 Building Chrome extension...
> npm install
> npm run build
✅ Chrome extension built successfully
```

### 4. Load Extension in Chrome

1. **Open Chrome** and go to `chrome://extensions/`
2. **Enable Developer mode** (toggle in top right)
3. **Click "Load unpacked"**
4. **Select the folder**: `assist/chrome-ext/dist`
5. **Verify extension appears** in the extensions list

### 5. Test Extension UI

1. **Go to Messenger Web**: `https://www.messenger.com`
2. **Log in** to your Messenger account
3. **Click the extension icon** in Chrome toolbar
4. **Verify side panel opens** with the clean UI

**Expected UI Elements:**
- ✅ Header with "Messenger AI Assistant"
- ✅ Status indicator (should show "Backend not connected" initially)
- ✅ Consent toggle
- ✅ Start Capture button (disabled until consent given)
- ✅ Settings (mute toggle, audio quality slider)
- ✅ Connection status
- ✅ Recent activity section

### 6. Test Backend Connection

1. **In the side panel**, check the connection status
2. **It should show**: "Connected" with green indicator
3. **If not connected**, refresh the page and try again

### 7. Test Recording Functionality

1. **Toggle "I consent to recording my conversations"**
2. **Start Capture button should become enabled**
3. **Click "Start Capture"**
4. **Verify status changes** to "Recording started"
5. **Button should change** to "Stop Capture" (red)
6. **Speak into microphone** for a few seconds
7. **Click "Stop Capture"**
8. **Verify status returns** to "Ready to capture"

### 8. Test WebSocket Connection

1. **Open Chrome DevTools** (F12)
2. **Go to Console tab**
3. **Start recording** in the extension
4. **Look for WebSocket connection logs**:
   ```
   WebSocket connected
   Received X bytes of data
   ```

### 9. Test API Endpoints

```bash
# Test revive API
curl -X POST http://127.0.0.1:8000/revive \
  -H "Content-Type: application/json" \
  -d '{"cue": "test query", "limit": 5}'

# Test memory statistics
curl http://127.0.0.1:8000/memories/default/statistics

# Test memory search
curl "http://127.0.0.1:8000/memories/default/search?query=test&limit=5"
```

### 10. Test Full Integration

1. **Start recording** in the extension
2. **Have a conversation** (speak into microphone)
3. **Stop recording**
4. **Check backend logs** for processing messages
5. **Test revive API** with a relevant query

## Troubleshooting

### Common Issues

#### 1. "Backend not connected"
**Solutions:**
- Ensure backend is running: `make dev`
- Check URL in extension: should be `http://127.0.0.1:8000`
- Refresh the page and try again

#### 2. Extension won't load
**Solutions:**
- Rebuild extension: `make chrome-build`
- Check `assist/chrome-ext/dist` folder exists
- Verify `manifest.json` is valid

#### 3. "Please navigate to Messenger Web first"
**Solutions:**
- Ensure you're on `messenger.com` domain
- Refresh the page
- Check content script injection

#### 4. WebSocket connection fails
**Solutions:**
- Check backend is running
- Verify WebSocket endpoint: `ws://127.0.0.1:8765/ingest`
- Check browser console for errors

#### 5. Recording doesn't work
**Solutions:**
- Check microphone permissions
- Ensure consent toggle is enabled
- Check browser console for errors
- Verify MediaRecorder API support

### Debug Mode

Enable detailed logging:

1. **Open Chrome DevTools** (F12)
2. **Go to Console tab**
3. **Look for extension logs**
4. **Check Network tab** for WebSocket connections
5. **Check Application tab** for extension storage

### Log Files

- **Backend logs**: Console output from `make dev`
- **Extension logs**: Chrome DevTools Console
- **WebSocket logs**: Browser Network tab

## Success Criteria

✅ **Backend Health**: All services show `true`  
✅ **Extension Loads**: No errors in extension console  
✅ **UI Responsive**: All controls work smoothly  
✅ **WebSocket Connection**: Stable connection to backend  
✅ **Audio Capture**: No errors during recording  
✅ **API Endpoints**: All endpoints respond correctly  
✅ **Full Integration**: End-to-end functionality works  

## Next Steps

1. **Test with Real Conversations**: Use with actual Messenger conversations
2. **Monitor Performance**: Check logs and system resources
3. **Customize Settings**: Adjust audio quality and other preferences
4. **Scale Testing**: Test with multiple users and longer sessions

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review logs for error messages
3. Verify all prerequisites are met
4. Test individual components separately
