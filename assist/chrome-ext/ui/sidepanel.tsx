// Side Panel TypeScript Component
class MessengerAIAssistant {
  private isRecording = false;
  private isConnected = false;
  private consentGiven = false;
  private bitrate = 128;
  private isMuted = false;

  constructor() {
    this.initializeUI();
    this.setupEventListeners();
    this.checkBackendConnection();
  }

  private initializeUI() {
    // Get DOM elements
    const consentToggle = document.getElementById('consentToggle') as HTMLElement;
    const captureBtn = document.getElementById('captureBtn') as HTMLButtonElement;
    const captureBtnText = document.getElementById('captureBtnText') as HTMLElement;
    const muteToggle = document.getElementById('muteToggle') as HTMLElement;
    const bitrateSlider = document.getElementById('bitrateSlider') as HTMLInputElement;
    const bitrateValue = document.getElementById('bitrateValue') as HTMLElement;
    const statusText = document.getElementById('statusText') as HTMLElement;
    const statusIndicator = document.getElementById('statusIndicator') as HTMLElement;
    const connectionStatus = document.getElementById('connectionStatus') as HTMLElement;
    const connectionIndicator = document.getElementById('connectionIndicator') as HTMLElement;
    const connectionDetails = document.getElementById('connectionDetails') as HTMLElement;

    // Store references
    this.elements = {
      consentToggle,
      captureBtn,
      captureBtnText,
      muteToggle,
      bitrateSlider,
      bitrateValue,
      statusText,
      statusIndicator,
      connectionStatus,
      connectionIndicator,
      connectionDetails
    };
  }

  private setupEventListeners() {
    // Consent toggle
    this.elements.consentToggle.addEventListener('click', () => {
      this.consentGiven = !this.consentGiven;
      this.elements.consentToggle.classList.toggle('active', this.consentGiven);
      this.updateCaptureButton();
    });

    // Capture button
    this.elements.captureBtn.addEventListener('click', () => {
      if (this.isRecording) {
        this.stopCapture();
      } else {
        this.startCapture();
      }
    });

    // Mute toggle
    this.elements.muteToggle.addEventListener('click', () => {
      this.isMuted = !this.isMuted;
      this.elements.muteToggle.classList.toggle('active', this.isMuted);
    });

    // Bitrate slider
    this.elements.bitrateSlider.addEventListener('input', (e) => {
      this.bitrate = parseInt((e.target as HTMLInputElement).value);
      this.elements.bitrateValue.textContent = `${this.bitrate} kbps`;
    });
  }

  private async checkBackendConnection() {
    try {
      const response = await fetch('http://localhost:8000/health');
      if (response.ok) {
        this.isConnected = true;
        this.updateConnectionStatus('Connected', 'Backend ready');
      } else {
        throw new Error('Backend not responding');
      }
    } catch (error) {
      this.isConnected = false;
      this.updateConnectionStatus('Disconnected', 'Backend not available');
    }
  }

  private updateConnectionStatus(status: string, details: string) {
    this.elements.connectionStatus.textContent = status;
    this.elements.connectionDetails.textContent = details;
    
    // Update connection indicator
    this.elements.connectionIndicator.className = 'status-indicator';
    if (status === 'Connected') {
      this.elements.connectionIndicator.classList.add('status-connected');
    } else {
      this.elements.connectionIndicator.classList.add('status-disconnected');
    }
  }

  private updateCaptureButton() {
    const canCapture = this.consentGiven && this.isConnected;
    this.elements.captureBtn.disabled = !canCapture;
    
    if (this.isRecording) {
      this.elements.captureBtnText.textContent = 'Stop Capture';
      this.elements.captureBtn.className = 'modern-button w-full py-4 px-6 rounded-xl text-white font-semibold text-lg mb-6 flex items-center justify-center space-x-3';
      this.elements.captureBtn.style.background = 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)';
    } else {
      this.elements.captureBtnText.textContent = 'Start Capture';
      this.elements.captureBtn.className = 'modern-button w-full py-4 px-6 rounded-xl text-white font-semibold text-lg mb-6 flex items-center justify-center space-x-3';
      this.elements.captureBtn.style.background = canCapture 
        ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
        : '#9ca3af';
    }
  }

  private async startCapture() {
    try {
      // Validate we're on Messenger
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      if (!tab.url?.includes('messenger.com')) {
        this.updateStatus('error', 'Please navigate to Messenger Web first');
        return;
      }

      // Create offscreen document if needed
      await chrome.runtime.sendMessage({ type: 'CREATE_OFFSCREEN' });

      // Request tab capture (requires user gesture)
      const stream = await chrome.tabCapture.capture({
        audio: !this.isMuted,
        video: true,
        audioConstraints: {
          mandatory: {
            chromeMediaSource: 'tab',
            chromeMediaSourceId: tab.id
          }
        }
      });

      if (!stream) {
        throw new Error('Failed to capture tab');
      }

      // Send stream to offscreen document
      await chrome.runtime.sendMessage({
        type: 'START_CAPTURE',
        mediaStream: stream
      });

      this.isRecording = true;
      this.updateStatus('success', 'Recording started');
      this.updateCaptureButton();
      this.addActivity('Recording started');

    } catch (error) {
      console.error('Failed to start capture:', error);
      this.updateStatus('error', `Failed to start: ${error.message}`);
    }
  }

  private async stopCapture() {
    try {
      await chrome.runtime.sendMessage({ type: 'STOP_CAPTURE' });
      
      this.isRecording = false;
      this.updateStatus('info', 'Recording stopped');
      this.updateCaptureButton();
      this.addActivity('Recording stopped');

    } catch (error) {
      console.error('Failed to stop capture:', error);
      this.updateStatus('error', `Failed to stop: ${error.message}`);
    }
  }

  private updateStatus(type: 'info' | 'success' | 'error', message: string) {
    this.elements.statusText.textContent = message;
    
    // Update status indicator
    this.elements.statusIndicator.className = 'status-indicator';
    if (type === 'success') {
      this.elements.statusIndicator.classList.add('status-connected');
    } else if (type === 'error') {
      this.elements.statusIndicator.classList.add('status-disconnected');
    } else if (this.isRecording) {
      this.elements.statusIndicator.classList.add('status-recording');
    } else {
      this.elements.statusIndicator.classList.add('status-disconnected');
    }
  }

  private addActivity(message: string) {
    const activityList = document.getElementById('activityList');
    const timestamp = new Date().toLocaleTimeString();
    const activityItem = document.createElement('div');
    activityItem.className = 'activity-item';
    activityItem.innerHTML = `<span class="text-gray-500 text-xs">${timestamp}</span> ${message}`;
    activityList.insertBefore(activityItem, activityList.firstChild);
    
    // Keep only last 5 activities
    while (activityList.children.length > 5) {
      activityList.removeChild(activityList.lastChild);
    }
  }

  private elements: {
    consentToggle: HTMLElement;
    captureBtn: HTMLButtonElement;
    captureBtnText: HTMLElement;
    muteToggle: HTMLElement;
    bitrateSlider: HTMLInputElement;
    bitrateValue: HTMLElement;
    statusText: HTMLElement;
    statusIndicator: HTMLElement;
    connectionStatus: HTMLElement;
    connectionIndicator: HTMLElement;
    connectionDetails: HTMLElement;
  };
}

// Initialize the assistant when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new MessengerAIAssistant();
});
