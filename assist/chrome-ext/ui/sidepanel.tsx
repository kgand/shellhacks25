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
    const captureBtnText = document.getElementById('captureBtnText') as HTMLElement;
    const muteToggle = document.getElementById('muteToggle') as HTMLInputElement;
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
    this.elements.muteToggle.addEventListener('change', (e => {
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
    
    // Update connection indicator
    this.elements.connectionIndicator.className = 'w-2 h-2 rounded-full mr-2';
    if (status === 'Connected') {
      this.elements.connectionIndicator.classList.add('bg-success');
    } else {
      this.elements.connectionIndicator.classList.add('bg-error');
    }
  }

  private updateCaptureButton() {
    const canCapture = this.consentGiven && this.isConnected;
    this.elements.captureBtn.disabled = !canCapture;
    
    if (this.isRecording) {
      this.elements.captureBtnText.textContent = 'Stop Capture';
      this.elements.captureBtn.className = 'btn btn-error btn-lg w-full mb-4';
    } else {
      this.elements.captureBtnText.textContent = 'Start Capture';
      this.elements.captureBtn.className = 'btn btn-primary btn-lg w-full mb-4';
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
    this.elements.statusIndicator.className = 'w-2 h-2 rounded-full mr-2';
    if (type === 'success') {
      this.elements.statusIndicator.classList.add('bg-success');
    } else if (type === 'error') {
      this.elements.statusIndicator.classList.add('bg-error');
    } else if (this.isRecording) {
      this.elements.statusIndicator.classList.add('bg-warning');
    } else {
      this.elements.statusIndicator.classList.add('bg-error');
    }
  }

  private addActivity(message: string) {
    const activityList = document.getElementById('activityList');
    const timestamp = new Date().toLocaleTimeString();
    const activityItem = document.createElement('div');
    activityItem.className = 'text-xs text-base-content/60';
    activityItem.innerHTML = `<span class="text-base-content/40">${timestamp}</span> ${message}`;
    activityList.insertBefore(activityItem, activityList.firstChild);
    
    // Keep only last 5 activities
    while (activityList.children.length > 5) {
      activityList.removeChild(activityList.lastChild);
    }
  }

  private elements: {
    consentToggle: HTMLInputElement;
    captureBtn: HTMLButtonElement;
    captureBtnText: HTMLElement;
    muteToggle: HTMLInputElement;
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
