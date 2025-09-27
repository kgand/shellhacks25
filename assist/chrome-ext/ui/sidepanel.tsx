// Side Panel TypeScript Component
class MessengerAIAssistant {
    private isRecording = false;
    private isConnected = false;
    private consentGiven = false;
    private bitrate = 128;
    private isMuted = false;
    private elements: any = {};

    constructor() {
        this.initializeUI();
        this.setupEventListeners();
        this.checkBackendConnection();
    }

    private initializeUI() {
        // Get DOM elements
        this.elements = {
            consentToggle: document.getElementById('consentToggle') as HTMLInputElement,
            captureBtn: document.getElementById('captureBtn') as HTMLButtonElement,
            captureBtnText: document.getElementById('captureBtnText') as HTMLElement,
            muteToggle: document.getElementById('muteToggle') as HTMLInputElement,
            bitrateSlider: document.getElementById('bitrateSlider') as HTMLInputElement,
            bitrateValue: document.getElementById('bitrateValue') as HTMLElement,
            statusText: document.getElementById('statusText') as HTMLElement,
            statusIndicator: document.getElementById('statusIndicator') as HTMLElement,
            connectionStatus: document.getElementById('connectionStatus') as HTMLElement,
            connectionIndicator: document.getElementById('connectionIndicator') as HTMLElement,
            connectionDetails: document.getElementById('connectionDetails') as HTMLElement,
            activityList: document.getElementById('activityList') as HTMLElement
        };

        // Initialize UI state
        this.updateCaptureButton();
        this.updateStatus('info', 'Ready to capture');
    }

    private setupEventListeners() {
        // Consent toggle
        this.elements.consentToggle?.addEventListener('click', () => {
            this.consentGiven = !this.consentGiven;
            this.elements.consentToggle.classList.toggle('active', this.consentGiven);
            this.updateCaptureButton();
        });

        // Capture button
        this.elements.captureBtn?.addEventListener('click', () => {
            if (this.isRecording) {
                this.stopCapture();
            } else {
                this.startCapture();
            }
        });

        // Mute toggle
        this.elements.muteToggle?.addEventListener('click', () => {
            this.isMuted = !this.isMuted;
            this.elements.muteToggle.classList.toggle('active', this.isMuted);
        });

        // Bitrate slider
        this.elements.bitrateSlider?.addEventListener('input', (e: Event) => {
            this.bitrate = parseInt((e.target as HTMLInputElement).value);
            if (this.elements.bitrateValue) {
                this.elements.bitrateValue.textContent = `${this.bitrate} kbps`;
            }
        });
    }

    private async checkBackendConnection() {
        try {
            // Use Chrome extension API to make the request
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

    private updateConnectionStatus(status: string, details: string) {
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

    private updateCaptureButton() {
        const canCapture = this.consentGiven && this.isConnected;
        if (this.elements.captureBtn) {
            this.elements.captureBtn.disabled = !canCapture;
        }
        
        if (this.isRecording) {
            if (this.elements.captureBtnText) {
                this.elements.captureBtnText.textContent = 'Stop Capture';
            }
            if (this.elements.captureBtn) {
                this.elements.captureBtn.className = 'btn btn-error btn-lg w-full mb-4';
            }
        } else {
            if (this.elements.captureBtnText) {
                this.elements.captureBtnText.textContent = 'Start Capture';
            }
            if (this.elements.captureBtn) {
                this.elements.captureBtn.className = 'btn btn-primary btn-lg w-full mb-4';
            }
        }
    }

    private async startCapture() {
        try {
            // Validate we're on Messenger
            const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
            if (!tab || !tab.url || !tab.url.includes('messenger.com')) {
                this.updateStatus('error', 'Please open Messenger Web to start capture.');
                return;
            }

            // Request media stream
            const stream = await new Promise<MediaStream>((resolve, reject) => {
                chrome.tabCapture.capture({ audio: true, video: true }, (stream) => {
                    if (stream) {
                        resolve(stream);
                    } else {
                        reject(new Error('Failed to capture media stream'));
                    }
                });
            });
            
            // Create offscreen document if it doesn't exist
            await chrome.offscreen.createDocument({
                url: 'offscreen.html',
                reasons: ['USER_MEDIA' as chrome.offscreen.Reason],
                justification: 'A/V capture & encoding'
            });

            // Send stream to offscreen document
            chrome.runtime.sendMessage({
                type: 'start-recording',
                target: 'offscreen',
                streamId: stream.id,
                bitrate: this.bitrate,
                muteMic: this.isMuted
            });

            this.isRecording = true;
            this.updateCaptureButton();
            this.updateStatus('info', 'Recording started...');
            this.addActivity('Recording started');

        } catch (error) {
            console.error('Failed to start capture:', error);
            this.updateStatus('error', `Failed to start: ${error instanceof Error ? error.message : 'Unknown error'}`);
        }
    }

    private async stopCapture() {
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
            this.updateStatus('error', `Failed to stop: ${error instanceof Error ? error.message : 'Unknown error'}`);
        }
    }

    private updateStatus(type: 'info' | 'success' | 'error', message: string) {
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

    private addActivity(message: string) {
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