// Offscreen document for MediaRecorder
class MediaCapture {
  constructor() {
    this.mediaRecorder = null;
    this.mediaStream = null;
    this.websocket = null;
    this.isRecording = false;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 1000;
    this.chunkQueue = [];
  }

  async connectWebSocket() {
    return new Promise((resolve, reject) => {
      try {
        this.websocket = new WebSocket('ws://127.0.0.1:8000/ingest');
        
        this.websocket.onopen = () => {
          console.log('WebSocket connected');
          this.reconnectAttempts = 0;
          this.processChunkQueue();
          resolve();
        };
        
        this.websocket.onclose = () => {
          console.log('WebSocket disconnected');
          this.handleReconnect();
        };
        
        this.websocket.onerror = (error) => {
          console.error('WebSocket error:', error);
          reject(error);
        };
        
      } catch (error) {
        reject(error);
      }
    });
  }

  async handleReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
      
      console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`);
      
      setTimeout(async () => {
        try {
          await this.connectWebSocket();
        } catch (error) {
          console.error('Reconnection failed:', error);
        }
      }, delay);
    } else {
      console.error('Max reconnection attempts reached');
    }
  }

  queueChunk(chunk) {
    this.chunkQueue.push(chunk);
    this.processChunkQueue();
  }

  processChunkQueue() {
    if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
      while (this.chunkQueue.length > 0) {
        const chunk = this.chunkQueue.shift();
        this.websocket.send(chunk);
      }
    }
  }

  async startCapture(mediaStream) {
    try {
      await this.connectWebSocket();
      
      this.mediaStream = mediaStream;
      this.mediaRecorder = new MediaRecorder(mediaStream, {
        mimeType: 'video/webm;codecs=opus',
        audioBitsPerSecond: 128000,
        videoBitsPerSecond: 1000000
      });

      this.mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          this.queueChunk(event.data);
        }
      };

      this.mediaRecorder.onstop = () => {
        console.log('MediaRecorder stopped');
        this.isRecording = false;
      };

      // Start recording with small chunks (800-1200ms)
      this.mediaRecorder.start(1000);
      this.isRecording = true;
      
      console.log('MediaRecorder started');
      
    } catch (error) {
      console.error('Failed to start capture:', error);
      throw error;
    }
  }

  stopCapture() {
    if (this.mediaRecorder && this.isRecording) {
      this.mediaRecorder.stop();
      this.isRecording = false;
    }
    
    if (this.mediaStream) {
      this.mediaStream.getTracks().forEach(track => track.stop());
      this.mediaStream = null;
    }
    
    if (this.websocket) {
      this.websocket.close();
      this.websocket = null;
    }
  }
}

// Global capture instance
const mediaCapture = new MediaCapture();

// Handle messages from service worker
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'START_CAPTURE') {
    mediaCapture.startCapture(message.mediaStream)
      .then(() => sendResponse({ success: true }))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true; // Keep message channel open for async response
  } else if (message.type === 'STOP_CAPTURE') {
    mediaCapture.stopCapture();
    sendResponse({ success: true });
  }
});
