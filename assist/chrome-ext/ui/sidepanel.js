// Side Panel JavaScript Component
class MessengerAIAssistant {
    constructor() {
        this.isRecording = false;
        this.isConnected = false;
        this.consentGiven = false;
        this.bitrate = 128;
        this.isMuted = false;
        this.elements = {};

        this.initializeUI();
        this.setupEventListeners();
        this.checkBackendConnection();
    }

    initializeUI() {
        // Get DOM elements
        this.elements = {
            consentToggle: document.getElementById('consentToggle'),
            captureBtn: document.getElementById('captureBtn'),
            captureBtnText: document.getElementById('captureBtnText'),
            muteToggle: document.getElementById('muteToggle'),
            bitrateSlider: document.getElementById('bitrateSlider'),
            bitrateValue: document.getElementById('bitrateValue'),
            statusText: document.getElementById('statusText'),
            statusIndicator: document.getElementById('statusIndicator'),
            connectionStatus: document.getElementById('connectionStatus'),
            connectionIndicator: document.getElementById('connectionIndicator'),
            connectionDetails: document.getElementById('connectionDetails'),
            activityList: document.getElementById('activityList')
        };

        // Initialize UI state
        this.updateCaptureButton();
        this.updateStatus('info', 'Ready to capture');
    }

    setupEventListeners() {
        // Consent toggle
        if (this.elements.consentToggle) {
            console.log('Consent toggle found, adding event listener');
            this.elements.consentToggle.addEventListener('click', () => {
                console.log('Consent toggle clicked');
                this.consentGiven = !this.consentGiven;
                this.elements.consentToggle.classList.toggle('active', this.consentGiven);
                this.updateCaptureButton();
            });
        } else {
            console.error('Consent toggle element not found!');
        }

        // Capture button
        if (this.elements.captureBtn) {
            this.elements.captureBtn.addEventListener('click', () => {
                if (this.isRecording) {
                    this.stopCapture();
                } else {
                    this.startCapture();
                }
            });
        }

        // Mute toggle
        if (this.elements.muteToggle) {
            this.elements.muteToggle.addEventListener('click', () => {
                this.isMuted = !this.isMuted;
                this.elements.muteToggle.classList.toggle('active', this.isMuted);
            });
        }

        // Bitrate slider
        if (this.elements.bitrateSlider) {
            this.elements.bitrateSlider.addEventListener('input', (e) => {
                this.bitrate = parseInt(e.target.value);
                if (this.elements.bitrateValue) {
                    this.elements.bitrateValue.textContent = `${this.bitrate} kbps`;
                }
            });
        }
    }

    async checkBackendConnection() {
        try {
            const response = await fetch('http://127.0.0.1:8000/health', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
                mode: 'cors'
            });
            
            if (response.ok) {
                const data = await response.json();
                this.isConnected = true;
                this.updateConnectionStatus('Connected', `Backend ready - ${data.connections} connections`);
            } else {
                this.isConnected = false;
                this.updateConnectionStatus('Disconnected', 'Backend not responding');
            }
        } catch (error) {
            console.log('Backend connection error:', error);
            this.isConnected = false;
            this.updateConnectionStatus('Disconnected', 'Backend not available');
        }
    }

    updateConnectionStatus(status, details) {
        if (this.elements.connectionStatus) {
            this.elements.connectionStatus.textContent = status;
        }
        if (this.elements.connectionDetails) {
            this.elements.connectionDetails.textContent = details;
        }
        
        // Update connection indicator
        if (this.elements.connectionIndicator) {
            this.elements.connectionIndicator.className = 'status-indicator';
            if (status === 'Connected') {
                this.elements.connectionIndicator.classList.add('connected');
                this.elements.connectionIndicator.classList.remove('disconnected');
            } else {
                this.elements.connectionIndicator.classList.add('disconnected');
                this.elements.connectionIndicator.classList.remove('connected');
            }
        }
    }

    updateCaptureButton() {
        const canCapture = this.consentGiven && this.isConnected;
        if (this.elements.captureBtn) {
            this.elements.captureBtn.disabled = !canCapture;
        }
        
        if (this.isRecording) {
            if (this.elements.captureBtnText) {
                this.elements.captureBtnText.textContent = 'Stop Capture';
            }
            if (this.elements.captureBtn) {
                this.elements.captureBtn.className = 'btn btn-error';
            }
        } else {
            if (this.elements.captureBtnText) {
                this.elements.captureBtnText.textContent = 'Start Capture';
            }
            if (this.elements.captureBtn) {
                this.elements.captureBtn.className = 'btn btn-primary';
            }
        }
    }

    async startCapture() {
        try {
            // Validate we're on Messenger
            const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
            if (!tab || !tab.url || !tab.url.includes('messenger.com')) {
                this.updateStatus('error', 'Please open Messenger Web to start capture.');
                return;
            }

            console.log('Creating offscreen document...');
            // Create offscreen document if it doesn't exist
            await chrome.offscreen.createDocument({
                url: 'offscreen.html',
                reasons: ['USER_MEDIA'],
                justification: 'A/V capture & encoding'
            });
            console.log('Offscreen document created');

            // Send recording options to offscreen document
            console.log('Sending message to offscreen document...');
            chrome.runtime.sendMessage({
                type: 'start-recording',
                target: 'offscreen',
                bitrate: this.bitrate,
                muteMic: this.isMuted
            });
            console.log('Message sent to offscreen document');

            this.isRecording = true;
            this.updateCaptureButton();
            this.updateStatus('info', 'Recording started...');
            this.addActivity('Recording started');

        } catch (error) {
            console.error('Failed to start capture:', error);
            this.updateStatus('error', `Failed to start: ${error.message || 'Unknown error'}`);
        }
    }

    async stopCapture() {
        try {
            chrome.runtime.sendMessage({
                type: 'stop-recording',
                target: 'offscreen'
            });

            this.isRecording = false;
            this.updateCaptureButton();
            this.updateStatus('info', 'Recording stopped.');
            this.addActivity('Recording stopped');

            // Close offscreen document
            await chrome.offscreen.closeDocument();

        } catch (error) {
            console.error('Failed to stop capture:', error);
            this.updateStatus('error', `Failed to stop: ${error.message || 'Unknown error'}`);
        }
    }

    updateStatus(type, message) {
        if (this.elements.statusText) {
            this.elements.statusText.textContent = message;
        }
        
        // Update status indicator
        if (this.elements.statusIndicator) {
            this.elements.statusIndicator.className = 'status-indicator';
            if (type === 'success') {
                this.elements.statusIndicator.classList.add('connected');
                this.elements.statusIndicator.classList.remove('disconnected', 'recording');
            } else if (type === 'error') {
                this.elements.statusIndicator.classList.add('disconnected');
                this.elements.statusIndicator.classList.remove('connected', 'recording');
            } else if (this.isRecording) {
                this.elements.statusIndicator.classList.add('recording');
                this.elements.statusIndicator.classList.remove('connected', 'disconnected');
            } else {
                this.elements.statusIndicator.classList.add('disconnected');
                this.elements.statusIndicator.classList.remove('connected', 'recording');
            }
        }
    }

    addActivity(message) {
        if (!this.elements.activityList) return;
        
        const timestamp = new Date().toLocaleTimeString();
        const activityItem = document.createElement('div');
        activityItem.className = 'activity-item';
        activityItem.innerHTML = `<span class="activity-time">${timestamp}</span> ${message}`;
        this.elements.activityList.insertBefore(activityItem, this.elements.activityList.firstChild);
        
        // Keep only last 5 activities
        while (this.elements.activityList.children.length > 5) {
            this.elements.activityList.removeChild(this.elements.activityList.lastChild);
        }
    }
}

// Initialize the assistant when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new MessengerAIAssistant();
});
