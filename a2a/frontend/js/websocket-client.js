/**
 * WebSocket client for communicating with the Google A2A ADK backend
 * Handles connection setup, data transmission, and event handling
 */
export class WebSocketClient {
    constructor() {
      this.websocket = null;
      this.clientId = null;
      this.callbacks = {
        onMessage: null,
        onClose: null,
        onError: null
      };
    }
  
    /**
     * Establish WebSocket connection and configure event handlers
     * @param {Object} config - Configuration for Google A2A ADK
     * @param {Object} callbacks - Event callbacks
     * @returns {Promise} - Resolves when connection is established
     */
    connect(config, callbacks) {
      return new Promise((resolve, reject) => {
        // Generate a unique ID for this client session
        this.clientId = crypto.randomUUID();
        
        // Store callbacks
        this.callbacks = callbacks;
        
        // Create WebSocket connection
        this.websocket = new WebSocket(`ws://localhost:8000/ws/${this.clientId}`);
        
        this.websocket.onopen = () => {
          console.log("WebSocket connection established");
          
          // Send initial configuration
          this.websocket.send(JSON.stringify({
            type: 'config',
            config: config
          }));
          
          resolve();
        };
        
        this.websocket.onmessage = (event) => {
          const response = JSON.parse(event.data);
          if (this.callbacks.onMessage) {
            this.callbacks.onMessage(response);
          }
        };
        
        this.websocket.onclose = () => {
          console.log("WebSocket connection closed");
          if (this.callbacks.onClose) {
            this.callbacks.onClose();
          }
        };
        
        this.websocket.onerror = (error) => {
          console.error("WebSocket error:", error);
          if (this.callbacks.onError) {
            this.callbacks.onError(error);
          }
          reject(error);
        };
      });
    }
    
    /**
     * Check if websocket is connected
     * @returns {boolean} - True if connected
     */
    isConnected() {
      return this.websocket && this.websocket.readyState === WebSocket.OPEN;
    }
    
    /**
     * Send audio data to the server
     * @param {string} base64Audio - Base64 encoded audio data
     */
    sendAudio(base64Audio) {
      if (!this.isConnected()) return;
      
      this.websocket.send(JSON.stringify({
        type: 'audio',
        data: base64Audio
      }));
    }
    
    /**
     * Send image data to the server
     * @param {string} base64Image - Base64 encoded image data
     */
    sendImage(base64Image) {
      if (!this.isConnected()) return;
      
      this.websocket.send(JSON.stringify({
        type: 'image',
        data: base64Image
      }));
    }
    
    /**
     * Send text message to the server
     * @param {string} text - Text to send
     */
    sendText(text) {
      if (!this.isConnected()) return;
      
      this.websocket.send(JSON.stringify({
        type: 'text',
        data: text
      }));
    }
    
    /**
     * Send interrupt signal to the server
     */
    sendInterrupt() {
      if (!this.isConnected()) return;
      
      this.websocket.send(JSON.stringify({
        type: 'interrupt'
      }));
    }
    
    /**
     * Close the WebSocket connection
     */
    disconnect() {
      if (this.websocket) {
        this.websocket.close();
        this.websocket = null;
      }
    }
  }
