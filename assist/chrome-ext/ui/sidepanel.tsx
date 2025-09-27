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
    const consentToggle = document.getElementById('consentToggle') as HTMLInputElement;
    const captureBtn = document.getElementById('captureBtn') as HTMLButtonElement;
    const muteToggle = document.getElementById('muteToggle') as HTMLInputElement;
    const bitrateSlider = document.getElementById('bitrateSlider') as HTMLInputElement;
    const bitrateValue = document.getElementById('bitrateValue') as HTMLElement;
    const statusText = document.getElementById('statusText') as HTMLElement;
    const statusAlert = document.getElementById('statusAlert') as HTMLElement;
    const connectionStatus = document.getElementById('connectionStatus') as HTMLElement;
    const connectionDetails = document.getElementById('connectionDetails') as HTMLElement;

    // Store references
    this.elements = {
      consentToggle,
      captureBtn,
      muteToggle,
      bitrateSlider,
      bitrateValue,
      statusText,
      statusAlert,
      connectionStatus,
      connectionDetails
    };
  }

  private setupEventListeners() {
    // Consent toggle
    this.elements.consentToggle.addEventListener('change', (e) => {
      this.consentGiven = (e.target as HTMLInputElement).checked;
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
    this.elements.muteToggle.addEventListener('change', (e) => {
      this.isMuted = (e.target as HTMLInputElement).checked;
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
    this.elements.connectionStatus.className = status === 'Connected' 
      ? 'badge badge-success' 
      : 'badge badge-error';
  }

  private updateCaptureButton() {
    const canCapture = this.consentGiven && this.isConnected;
    this.elements.captureBtn.disabled = !canCapture;
    
    if (this.isRecording) {
      this.elements.captureBtn.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 10a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z" />
        </svg>
        Stop Capture
      `;
      this.elements.captureBtn.className = 'btn btn-error btn-lg w-full';
    } else {
      this.elements.captureBtn.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
        </svg>
        Start Capture
      `;
      this.elements.captureBtn.className = 'btn btn-primary btn-lg w-full';
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
    this.elements.statusAlert.className = `alert alert-${type}`;
  }

  private addActivity(message: string) {
    const activityList = document.getElementById('activityList');
    const timestamp = new Date().toLocaleTimeString();
    const activityItem = document.createElement('div');
    activityItem.className = 'text-sm';
    activityItem.innerHTML = `<span class="opacity-50">${timestamp}</span> ${message}`;
    activityList.insertBefore(activityItem, activityList.firstChild);
    
    // Keep only last 5 activities
    while (activityList.children.length > 5) {
      activityList.removeChild(activityList.lastChild);
    }
  }

  private elements: {
    consentToggle: HTMLInputElement;
    captureBtn: HTMLButtonElement;
    muteToggle: HTMLInputElement;
    bitrateSlider: HTMLInputElement;
    bitrateValue: HTMLElement;
    statusText: HTMLElement;
    statusAlert: HTMLElement;
    connectionStatus: HTMLElement;
    connectionDetails: HTMLElement;
  };
}

// Initialize the assistant when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new MessengerAIAssistant();
});
