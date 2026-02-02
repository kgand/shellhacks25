/**
 * Audio Manager class
 * Handles audio capture from microphone and playback of received audio
 */
export class AudioManager {
    constructor() {
      // Audio capture
      this.captureAudioContext = null;
      this.playbackAudioContext = null;
      this.scriptProcessor = null;
      this.mediaStream = null;
      this.mediaSource = null;
      this.onAudioData = null;
      
      // Audio playback
      this.audioBufferQueue = [];
      this.isPlaying = false;
      
      // Voice activity detection for interruption
      this.speechDetectionHistory = [];
      this.speechDetectionWindowSize = 5; // Number of recent samples to consider
      this.lastInterruptTime = 0;
    }
    
    /**
     * Start audio capture from microphone
     * @param {Function} onAudioData - Callback for captured audio data
     * @returns {Promise} - Resolves when audio capture is initialized
     */
    async startCapture(onAudioData) {
      this.onAudioData = onAudioData;
      
      try {
        // Get microphone access at system rate, resampled to 16 kHz by AudioContext
        this.mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        
        // Create audio context for capture at 16kHz (Google A2A ADK's input requirement)
        this.captureAudioContext = new AudioContext({ sampleRate: 16000 });
        
        // Create audio context for playback at 24kHz (Google A2A ADK's output format)
        this.playbackAudioContext = new AudioContext({ sampleRate: 24000 });
        
        // Create media source from mic stream
        this.mediaSource = this.captureAudioContext.createMediaStreamSource(this.mediaStream);
        
        // Create script processor for audio processing (buffer size 512, mono)
        this.scriptProcessor = this.captureAudioContext.createScriptProcessor(512, 1, 1);
        
        // Set up audio processing callback
        this.scriptProcessor.onaudioprocess = (event) => {
          // Get audio samples as Float32Array (-1.0 to 1.0)
          const floatSamples = event.inputBuffer.getChannelData(0);
          
          // Calculate audio level (RMS) for voice activity detection
          const audioLevel = this.calculateAudioLevel(floatSamples);
          const speechThreshold = 0.01; // Adjust based on testing
          const currentTimestamp = Date.now() / 1000;
          
          // Add to speech detection history
          this.speechDetectionHistory.push({
            level: audioLevel,
            timestamp: currentTimestamp,
            isSpeaking: audioLevel > speechThreshold
          });
          
          // Keep only recent samples
          if (this.speechDetectionHistory.length > this.speechDetectionWindowSize) {
            this.speechDetectionHistory.shift();
          }
          
          // Determine if user is actively speaking (based on recent history)
          const recentSpeechCount = this.speechDetectionHistory.filter(sample => sample.isSpeaking).length;
          const isActivelySpeaking = recentSpeechCount >= 2; // At least 2 of last 5 samples
          
          // Prevent interrupt spam (debounce interrupts)
          const timeSinceLastInterrupt = currentTimestamp - this.lastInterruptTime;
          const canInterrupt = timeSinceLastInterrupt > 0.5; // 500ms debounce
          
          // Convert to PCM 16-bit and send base64 encoded data
          const pcm16 = this.float32ToPcm16(floatSamples);
          const base64Audio = this.pcm16ToBase64(pcm16);
          
          // Send data through callback with enhanced speech detection info
          if (this.onAudioData) {
            this.onAudioData(base64Audio, { 
              audioLevel: audioLevel, 
              isSpeaking: isActivelySpeaking,
              canInterrupt: canInterrupt,
              timestamp: currentTimestamp
            });
            
            // Update last interrupt time if we're signaling an interrupt
            if (isActivelySpeaking && canInterrupt) {
              this.lastInterruptTime = currentTimestamp;
            }
          }
        };
        
        // Connect the audio processing chain
        this.mediaSource.connect(this.scriptProcessor);
        this.scriptProcessor.connect(this.captureAudioContext.destination);
        
      } catch (error) {
        console.error('Error initializing audio capture:', error);
        throw new Error(`Microphone access denied: ${error.message}`);
      }
    }
    
    /**
     * Stop audio capture and release resources
     */
    stopCapture() {
      // Disconnect and release audio processing
      if (this.scriptProcessor) {
        this.scriptProcessor.disconnect();
        this.scriptProcessor = null;
      }
      
      if (this.mediaSource) {
        this.mediaSource.disconnect();
        this.mediaSource = null;
      }
      
      // Close audio contexts
      if (this.captureAudioContext) {
        this.captureAudioContext.close();
        this.captureAudioContext = null;
      }
      
      if (this.playbackAudioContext) {
        this.playbackAudioContext.close();
        this.playbackAudioContext = null;
      }
      
      // Stop all audio tracks
      if (this.mediaStream) {
        this.mediaStream.getTracks().forEach(track => track.stop());
        this.mediaStream = null;
      }
      
      // Clear queues
      this.audioBufferQueue = [];
      this.isPlaying = false;
    }
    
    /**
     * Play received audio data (queues chunks for continuous playback)
     * @param {string} base64Audio - Base64 encoded audio data from Google A2A ADK
     */
    playAudio(base64Audio) {
      // Convert base64 to float32 audio data
      const audioData = this.base64ToFloat32Array(base64Audio);
      
      // Add to playback queue
      this.audioBufferQueue.push(audioData);
      
      // Start playback if not already playing
      if (!this.isPlaying) {
        this.playNextChunk();
      }
    }
    
    /**
     * Play the next chunk from the audio queue
     * @private
     */
    playNextChunk() {
      if (!this.playbackAudioContext || this.audioBufferQueue.length === 0) {
        this.isPlaying = false;
        return;
      }
      
      this.isPlaying = true;
      
      // Get next chunk of audio data
      const chunk = this.audioBufferQueue.shift();
      
      // Create audio buffer with Google A2A ADK's 24kHz sample rate
      const a2aAdkSampleRate = 24000;
      const audioBuf = this.playbackAudioContext.createBuffer(1, chunk.length, a2aAdkSampleRate);
      audioBuf.copyToChannel(chunk, 0);
      
      // Create and play audio source
      const source = this.playbackAudioContext.createBufferSource();
      source.buffer = audioBuf;
      source.connect(this.playbackAudioContext.destination);
      
      // Continue to next chunk when this one finishes
      source.onended = () => {
        this.playNextChunk();
      };
      
      source.start();
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
     * Calculate audio level (RMS) for voice activity detection
     * @param {Float32Array} samples - Audio samples
     * @returns {number} - RMS level (0.0 to 1.0)
     * @private
     */
    calculateAudioLevel(samples) {
      let sum = 0;
      for (let i = 0; i < samples.length; i++) {
        sum += samples[i] * samples[i];
      }
      return Math.sqrt(sum / samples.length);
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
    
    /**
     * Convert base64 string to Float32Array (assumes 16-bit PCM input)
     * Enhanced to properly handle little-endian PCM data
     * @param {string} base64 - Base64 encoded audio data
     * @returns {Float32Array} - Audio samples (-1.0 to 1.0)
     * @private
     */
    base64ToFloat32Array(base64) {
      // Decode base64 to binary
      const binary = atob(base64);
      const bytes = new Uint8Array(binary.length);
      
      for (let i = 0; i < binary.length; i++) {
        bytes[i] = binary.charCodeAt(i);
      }
      
      // Create DataView to handle endianness properly
      const dataView = new DataView(bytes.buffer);
      const float32 = new Float32Array(dataView.byteLength / 2);
      
      for (let i = 0; i < float32.length; i++) {
        // Get 16-bit PCM value as little-endian (true for second parameter)
        const pcm16Value = dataView.getInt16(i * 2, true);
        
        // Normalize to -1.0...1.0 range
        float32[i] = pcm16Value / 32768.0;
      }
      
      return float32;
    }
  }
