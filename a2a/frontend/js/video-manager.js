/**
 * Video Manager class
 * Handles video/screen capture and frame extraction
 */
export class VideoManager {
    constructor() {
      this.videoStream = null;
      this.audioStream = null;
      this.videoElement = document.getElementById('videoElem');
      this.canvasElement = document.getElementById('canvasElem');
      this.videoInterval = null;
      this.onImageData = null;
      this.onAudioData = null;
      
      // Audio processing
      this.audioContext = null;
      this.scriptProcessor = null;
      this.mediaSource = null;
    }
    
    /**
     * Start screen capture with audio for context tracking
     * @param {string} mode - Capture mode: 'screen' (only screen supported)
     * @param {Function} onImageData - Callback for captured frames
     * @param {Function} onAudioData - Callback for captured audio
     * @returns {Promise} - Resolves when capture is initialized
     */
    async startCapture(mode, onImageData, onAudioData) {
      if (mode !== 'screen' && mode !== 'camera') {
        throw new Error('Only screen and camera capture modes are supported');
      }
      
      this.onImageData = onImageData;
      this.onAudioData = onAudioData;
      
      try {
        // Acquire video capture based on mode
        if (mode === 'screen') {
          this.videoStream = await navigator.mediaDevices.getDisplayMedia({
            video: { width: { ideal: 1920 }, height: { ideal: 1080 } },
            audio: true // Include system audio
          });
        } else if (mode === 'camera') {
          this.videoStream = await navigator.mediaDevices.getUserMedia({
            video: { width: { ideal: 1280 }, height: { ideal: 720 } },
            audio: true
          });
        }
        
        // Set video source
        this.videoElement.srcObject = this.videoStream;
        
        // Set up audio processing if audio is available
        const audioTracks = this.videoStream.getAudioTracks();
        if (audioTracks.length > 0 && this.onAudioData) {
          this.setupAudioProcessing();
        }
        
        // Periodically capture and send frames
        this.videoInterval = setInterval(() => {
          this.captureAndSendFrame();
        }, 1000); // Send a frame every second
        
      } catch (error) {
        console.error('Error initializing video capture:', error);
        throw new Error(`Video capture failed: ${error.message}`);
      }
    }
    
    /**
     * Stop video capture and release resources
     */
    stopCapture() {
      // Clear capture interval
      if (this.videoInterval) {
        clearInterval(this.videoInterval);
        this.videoInterval = null;
      }
      
      // Stop audio processing
      if (this.scriptProcessor) {
        this.scriptProcessor.disconnect();
        this.scriptProcessor = null;
      }
      
      if (this.mediaSource) {
        this.mediaSource.disconnect();
        this.mediaSource = null;
      }
      
      if (this.audioContext) {
        this.audioContext.close();
        this.audioContext = null;
      }
      
      // Stop all video tracks
      if (this.videoStream) {
        this.videoStream.getTracks().forEach(track => track.stop());
        this.videoStream = null;
      }
      
      // Clear video source
      if (this.videoElement) {
        this.videoElement.srcObject = null;
      }
    }
    
    /**
     * Capture current video frame and send through callback
     * @private
     */
    captureAndSendFrame() {
      if (!this.videoStream || !this.onImageData) return;
      
      const ctx = this.canvasElement.getContext('2d');
      
      // Set canvas size to match video dimensions
      this.canvasElement.width = this.videoElement.videoWidth;
      this.canvasElement.height = this.videoElement.videoHeight;
      
      // Draw video frame to canvas
      ctx.drawImage(this.videoElement, 0, 0, this.videoElement.videoWidth, this.videoElement.videoHeight);
      
      // Get JPEG image as base64
      const base64Image = this.canvasElement.toDataURL('image/jpeg').split(',')[1];
      
      // Send through callback
      this.onImageData(base64Image);
    }
    
    /**
     * Set up audio processing for screen capture audio
     * @private
     */
    setupAudioProcessing() {
      try {
        // Create audio context for capture at 16kHz (Google A2A ADK's input requirement)
        this.audioContext = new AudioContext({ sampleRate: 16000 });
        
        // Create media source from screen audio stream
        this.mediaSource = this.audioContext.createMediaStreamSource(this.videoStream);
        
        // Create script processor for audio processing (buffer size 512, mono)
        this.scriptProcessor = this.audioContext.createScriptProcessor(512, 1, 1);
        
        // Set up audio processing callback
        this.scriptProcessor.onaudioprocess = (event) => {
          // Get audio samples as Float32Array (-1.0 to 1.0)
          const floatSamples = event.inputBuffer.getChannelData(0);
          
          // Convert to PCM 16-bit and send base64 encoded data
          const pcm16 = this.float32ToPcm16(floatSamples);
          const base64Audio = this.pcm16ToBase64(pcm16);
          
          // Send data through callback
          if (this.onAudioData) {
            this.onAudioData(base64Audio);
          }
        };
        
        // Connect the audio processing chain
        this.mediaSource.connect(this.scriptProcessor);
        this.scriptProcessor.connect(this.audioContext.destination);
        
      } catch (error) {
        console.error('Error setting up audio processing:', error);
      }
    }
    
    /**
     * Convert Float32Array samples (-1.0 to 1.0) to 16-bit PCM
     * @param {Float32Array} float32Array - Audio samples
     * @returns {Int16Array} - 16-bit PCM data
     * @private
     */
    float32ToPcm16(float32Array) {
      const pcm16 = new Int16Array(float32Array.length);
      
      for (let i = 0; i < float32Array.length; i++) {
        // Clamp values to -1.0...1.0 range
        const sample = Math.max(-1, Math.min(1, float32Array[i]));
        
        // Convert to 16-bit range: negative values to -32768..0, positive to 0..32767
        pcm16[i] = sample < 0 ? sample * 0x8000 : sample * 0x7FFF;
      }
      
      return pcm16;
    }
    
    /**
     * Convert PCM 16-bit data to base64 string
     * @param {Int16Array} pcm16 - 16-bit PCM data
     * @returns {string} - Base64 encoded data
     * @private
     */
    pcm16ToBase64(pcm16) {
      const bytes = new Uint8Array(pcm16.buffer);
      let binary = "";
      
      for (let i = 0; i < bytes.length; i++) {
        binary += String.fromCharCode(bytes[i]);
      }
      
      return btoa(binary);
    }
  }
