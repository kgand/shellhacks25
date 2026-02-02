/**
 * UI Controller class
 * Handles all UI updates and user interactions
 */
export class UIController {
    constructor() {
      // Cache DOM elements
      this.elements = {
        systemPrompt: document.getElementById('systemPrompt'),
        startScreenBtn: document.getElementById('startScreenBtn'),
        stopButton: document.getElementById('stopButton'),
        messages: document.getElementById('messages'),
        videoContainer: document.getElementById('videoContainer')
      };
    }
    
    /**
     * Get user configuration from form inputs
     * @returns {Object} - Configuration object
     */
    getConfig() {
      return {
        systemPrompt: this.elements.systemPrompt.value,
        voice: 'Puck', // Default voice
        googleSearch: true, // Default to true
        allowInterruptions: true // Default to true
      };
    }
    
    /**
     * Update UI elements based on streaming state
     * @param {boolean} isStreaming - Whether streaming is active
     */
    updateUIForStreaming(isStreaming) {
      // Get all start buttons
      const startButtons = document.querySelectorAll('#startAudioBtn, #startCameraBtn, #startScreenBtn');
      startButtons.forEach(btn => btn.disabled = isStreaming);
      this.elements.stopButton.disabled = !isStreaming;
    }
    
    /**
     * Show video preview container
     */
    showVideoPreview() {
      this.elements.videoContainer.classList.remove('hidden');
    }
    
    /**
     * Hide video preview container
     */
    hideVideoPreview() {
      this.elements.videoContainer.classList.add('hidden');
    }
    
    /**
     * Append a message to the conversation area
     * @param {string} message - Message text to display
     */
    appendMessage(message) {
      const messageDiv = document.createElement('div');
      messageDiv.className = 'message';
      messageDiv.textContent = message;
      
      this.elements.messages.appendChild(messageDiv);
      this.elements.messages.scrollTop = this.elements.messages.scrollHeight;
    }
    
    /**
     * Append a context log entry to the tracking area
     * @param {string} contextData - Context analysis data
     * @param {string} timestamp - Timestamp of the analysis
     */
    appendContextLog(contextData, timestamp) {
      const logDiv = document.createElement('div');
      logDiv.className = 'context-log-entry';
      
      const timeDiv = document.createElement('div');
      timeDiv.className = 'context-timestamp';
      timeDiv.textContent = new Date(timestamp).toLocaleTimeString();
      
      const dataDiv = document.createElement('div');
      dataDiv.className = 'context-data';
      dataDiv.textContent = contextData;
      
      logDiv.appendChild(timeDiv);
      logDiv.appendChild(dataDiv);
      
      this.elements.messages.appendChild(logDiv);
      this.elements.messages.scrollTop = this.elements.messages.scrollHeight;
    }
    
    /**
     * Show an error message
     * @param {string} errorText - Error message to display
     */
    showError(errorText) {
      const errorDiv = document.createElement('div');
      errorDiv.className = 'message';
      errorDiv.style.borderLeftColor = 'var(--accent-danger)';
      errorDiv.textContent = `Error: ${errorText}`;
      
      this.elements.messages.appendChild(errorDiv);
      this.elements.messages.scrollTop = this.elements.messages.scrollHeight;
      
      console.error(errorText);
    }
  }
