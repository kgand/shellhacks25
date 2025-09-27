"""
Gemini Live API client for real-time audio transcription and processing
"""

import asyncio
import logging
import json
import base64
from typing import Optional, List, Dict, Any
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os

logger = logging.getLogger(__name__)

class GeminiLiveClient:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash-live-001")
        self.is_connected = False
        self.transcript_buffer = []
        
    async def initialize(self):
        """Initialize Gemini Live session"""
        try:
            # Configure safety settings
            safety_settings = {
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
            
            self.model = genai.GenerativeModel(
                "gemini-2.0-flash-live-001",
                safety_settings=safety_settings
            )
            
            self.is_connected = True
            logger.info("Gemini Live client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Gemini Live client: {e}")
            raise
    
    async def send_audio_frames(self, audio_frames: List[float]):
        """Send audio frames to Gemini Live for transcription"""
        try:
            if not self.is_connected:
                await self.initialize()
            
            # Convert audio frames to base64
            audio_bytes = self._float_array_to_bytes(audio_frames)
            audio_b64 = base64.b64encode(audio_bytes).decode('utf-8')
            
            # Send to Gemini Live
            response = await self._send_audio_to_gemini(audio_b64)
            
            if response and 'transcript' in response:
                transcript = response['transcript']
                timestamp = response.get('timestamp', asyncio.get_event_loop().time())
                
                # Store transcript
                self.transcript_buffer.append({
                    'text': transcript,
                    'timestamp': timestamp,
                    'confidence': response.get('confidence', 0.0)
                })
                
                logger.info(f"Transcript received: {transcript[:50]}...")
                
                return transcript
                
        except Exception as e:
            logger.error(f"Failed to send audio frames to Gemini: {e}")
            return None
    
    async def _send_audio_to_gemini(self, audio_b64: str) -> Optional[Dict[str, Any]]:
        """Send audio data to Gemini Live API"""
        try:
            # Create audio data structure
            audio_data = {
                "mimeType": "audio/webm",
                "data": audio_b64
            }
            
            # Send to Gemini Live
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.model.generate_content(
                    audio_data,
                    generation_config={
                        "response_modalities": ["TEXT"],
                        "response_mime_type": "text/plain"
                    }
                )
            )
            
            if response and response.text:
                return {
                    'transcript': response.text,
                    'timestamp': asyncio.get_event_loop().time(),
                    'confidence': 0.9  # Placeholder confidence
                }
            
        except Exception as e:
            logger.error(f"Gemini Live API error: {e}")
            return None
    
    def _float_array_to_bytes(self, audio_frames: List[float]) -> bytes:
        """Convert float array to bytes for transmission"""
        import struct
        return struct.pack('f' * len(audio_frames), *audio_frames)
    
    async def generate_recap(self, memories: List[Dict], cue: str) -> str:
        """Generate a stitched recap from memories using Gemini 2.5 Pro"""
        try:
            # Use Gemini 2.5 Pro for reasoning
            model = genai.GenerativeModel("gemini-2.5-pro")
            
            # Prepare context
            context = self._prepare_memory_context(memories)
            
            prompt = f"""
            Based on the following memories and the cue "{cue}", create a comprehensive recap:
            
            Memories:
            {context}
            
            Please provide a coherent summary that connects these memories and addresses the cue.
            """
            
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: model.generate_content(prompt)
            )
            
            return response.text if response else "Unable to generate recap"
            
        except Exception as e:
            logger.error(f"Failed to generate recap: {e}")
            return "Error generating recap"
    
    def _prepare_memory_context(self, memories: List[Dict]) -> str:
        """Prepare memory context for recap generation"""
        context_parts = []
        
        for memory in memories:
            context_parts.append(f"""
            - {memory.get('text', '')}
              Timestamp: {memory.get('timestamp', 'Unknown')}
              Type: {memory.get('type', 'Unknown')}
            """)
        
        return "\n".join(context_parts)
    
    async def get_recent_transcripts(self, limit: int = 10) -> List[Dict]:
        """Get recent transcripts from buffer"""
        return self.transcript_buffer[-limit:] if self.transcript_buffer else []
    
    async def clear_transcript_buffer(self):
        """Clear the transcript buffer"""
        self.transcript_buffer.clear()
        logger.info("Transcript buffer cleared")
