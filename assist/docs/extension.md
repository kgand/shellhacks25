# Messenger AI Assistant - Chrome Extension

## Overview
A Chrome Extension (MV3) that captures audio/video from Messenger Web conversations and streams them to a Python backend for AI analysis.

## Installation

### Development Setup
1. Clone the repository
2. Navigate to `chrome-ext/` directory
3. Install dependencies: `npm install`
4. Build the extension: `npm run build`
5. Open Chrome and go to `chrome://extensions/`
6. Enable "Developer mode"
7. Click "Load unpacked" and select the `chrome-ext/dist` directory

## Usage

### Prerequisites
- Must be on Messenger Web (messenger.com)
- Backend server must be running (see server documentation)
- User consent must be given in the side panel

### Starting Capture
1. Navigate to Messenger Web
2. Click the extension icon to open the side panel
3. Toggle "I consent to recording my conversations"
4. Click "Start Capture" (this requires user gesture for tabCapture API)
5. The extension will begin recording audio/video from the current tab

### Features
- **User Gesture Enforcement**: Capture only starts after explicit user click
- **Offscreen Document**: Uses offscreen document for stable MediaRecorder
- **WebSocket Streaming**: Streams WebM/Opus chunks to backend
- **Quality Controls**: Adjustable audio bitrate (64-256 kbps)
- **Mute Option**: Option to exclude microphone input
- **Real-time Status**: Connection and recording status indicators

## Technical Details

### Architecture
- **Service Worker**: Handles extension lifecycle and message routing
- **Side Panel**: User interface with controls and status
- **Offscreen Document**: Owns MediaRecorder for stable capture
- **Content Script**: Detects Messenger Web pages

### Permissions
- `tabCapture`: Required for capturing tab audio/video
- `offscreen`: Required for offscreen document
- `sidePanel`: Required for side panel UI
- `storage`: For user preferences
- `activeTab`: For tab interaction
- `scripting`: For content script injection

### WebSocket Protocol
- Connects to `ws://localhost:8765/ingest`
- Sends WebM chunks as binary data
- Handles reconnection with exponential backoff
- Queues chunks when disconnected

## Troubleshooting

### Common Issues
1. **"Please navigate to Messenger Web first"**
   - Ensure you're on messenger.com
   - Refresh the page and try again

2. **"Backend not connected"**
   - Start the Python backend server
   - Check that it's running on localhost:8000

3. **Capture fails to start**
   - Ensure user consent is given
   - Try refreshing the page and clicking Start Capture again
   - Check browser console for errors

### Debug Mode
- Open Chrome DevTools
- Go to Extensions page
- Click "Inspect views: service worker" for service worker logs
- Check "offscreen.html" for MediaRecorder logs
