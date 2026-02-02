/**
 * Main application entry point
 * Initializes all components and sets up event listeners
 */

import { AudioManager } from './audio-manager.js';
import { VideoManager } from './video-manager.js';
import { WebSocketClient } from './websocket-client.js';
import { UIController } from './ui-controller.js';

class A2AADKApp {
  constructor() {
    // Initialize managers
    this.audioManager = new AudioManager();
    this.videoManager = new VideoManager();
    this.webSocketClient = new WebSocketClient();
    this.uiController = new UIController();
    
    // App state
    this.isStreaming = false;
    this.currentMode = null; // 'audio', 'camera', or 'screen'
    this.isA2AADKSpeaking = false;
    
    // Initialize
    this.initEventListeners();
  }
  
  /**
   * Set up event listeners for UI buttons
   */
  initEventListeners() {
    // Button references
    this.startAudioBtn = document.getElementById('startAudioBtn');
    this.startCameraBtn = document.getElementById('startCameraBtn');
    this.startScreenBtn = document.getElementById('startScreenBtn');
    this.stopButton = document.getElementById('stopButton');
    
    // Add click handlers
    if (this.startAudioBtn) {
      this.startAudioBtn.addEventListener('click', () => this.startStream('audio'));
    }
    if (this.startCameraBtn) {
      this.startCameraBtn.addEventListener('click', () => this.startStream('camera'));
    }
    if (this.startScreenBtn) {
      this.startScreenBtn.addEventListener('click', () => this.startStream('screen'));
    }
    if (this.stopButton) {
      this.stopButton.addEventListener('click', () => this.stopStream());
    }
    
    // Add keyboard interrupt handler
    document.addEventListener('keydown', (event) => {
      if (this.isStreaming && event.key === ' ' && event.ctrlKey) {
        event.preventDefault();
        this.sendInterrupt();
      }
    });
  }
  
  /**
   * Start streaming with the selected mode (audio, camera, screen)
   */
  async startStream(mode) {
    if (this.isStreaming) return;
    
    this.currentMode = mode;
    
    try {
      // Get configuration from UI
      const config = this.uiController.getConfig();
      
      // Initialize WebSocket connection
      await this.webSocketClient.connect(config, {
        onMessage: this.handleWebSocketMessage.bind(this),
        onClose: this.handleWebSocketClose.bind(this),
        onError: this.handleWebSocketError.bind(this)
      });
      
      // Initialize audio capture with interruption handling
      await this.audioManager.startCapture((audioData, audioInfo) => {
        // Always send audio data for processing (ensures transcription continues)
        this.webSocketClient.sendAudio(audioData);
        
        // Handle interruption when user speaks during A2A ADK's turn
        if (audioInfo && audioInfo.isSpeaking && audioInfo.canInterrupt && this.isA2AADKSpeaking) {
          console.log(`🎤 User interruption detected (level: ${audioInfo.audioLevel.toFixed(3)})`);
          this.sendInterrupt();
          this.uiController.appendMessage('[User interrupted - prioritizing your speech]');
        }
      });
      
      // Initialize video if needed
      if (mode !== 'audio') {
        await this.videoManager.startCapture(mode, (imageData) => {
          this.webSocketClient.sendImage(imageData);
        });
        this.uiController.showVideoPreview();
      }
      
      // Update UI state
      this.isStreaming = true;
      this.uiController.updateUIForStreaming(true);
      this.uiController.appendMessage(`Started ${mode} conversation with Google A2A ADK`);
      
    } catch (error) {
      this.uiController.showError(`Failed to start: ${error.message}`);
    }
  }
  
  /**
   * Stop all streaming and clean up resources
   */
  stopStream() {
    if (!this.isStreaming) return;
    
    // Clean up resources
    this.webSocketClient.disconnect();
    this.audioManager.stopCapture();
    this.videoManager.stopCapture();
    
    // Reset state
    this.isStreaming = false;
    this.currentMode = null;
    this.isA2AADKSpeaking = false;
    
    // Update UI
    this.uiController.updateUIForStreaming(false);
    this.uiController.hideVideoPreview();
    this.uiController.appendMessage('Conversation ended');
  }
  
  /**
   * Send interrupt signal to A2A ADK
   */
  sendInterrupt() {
    if (this.isStreaming && this.webSocketClient.isConnected()) {
      this.webSocketClient.sendInterrupt();
      this.isA2AADKSpeaking = false;
      this.uiController.appendMessage('[Interrupted A2A ADK]');
    }
  }
  
  /**
   * Handle incoming WebSocket messages
   */
  handleWebSocketMessage(response) {
    switch (response.type) {
      case 'audio':
        if (!this.isA2AADKSpeaking) {
          this.uiController.appendMessage('[Google A2A ADK speaking - you can interrupt anytime]');
        }
        this.isA2AADKSpeaking = true;
        this.audioManager.playAudio(response.data);
        break;
        
      case 'text':
        this.uiController.appendMessage(`[Google A2A ADK] ${response.text}`);
        break;
        
      case 'turn_complete':
        this.isA2AADKSpeaking = false;
        this.uiController.appendMessage('[Google A2A ADK finished - listening for your speech]');
        break;
        
      case 'error':
        this.uiController.showError(response.message);
        break;
        
      default:
        this.uiController.appendMessage(`[System] ${JSON.stringify(response)}`);
    }
  }
  
  /**
   * Handle WebSocket connection close
   */
  handleWebSocketClose() {
    this.uiController.appendMessage('WebSocket closed');
    this.stopStream();
  }
  
  /**
   * Handle WebSocket errors
   */
  handleWebSocketError(error) {
    this.uiController.showError(`WebSocket error: ${error.message}`);
  }
}

// Initialize the app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  window.app = new A2AADKApp();
});
