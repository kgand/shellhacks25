"""
Gemini Live API integration for real-time conversation processing
"""

import asyncio
import logging
import json
import websockets
from typing import AsyncGenerator, Dict, Any, Optional
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class GeminiLiveClient:
    """Client for Gemini Live API WebSocket connection"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.websocket = None
        self.is_connected = False
        self.model = os.getenv('GEMINI_MODEL_LIVE', 'gemini-2.0-flash-live-001')
        
    async def connect(self) -> bool:
        """Connect to Gemini Live API"""
        try:
            if not self.api_key:
                logger.error("GEMINI_API_KEY not found in environment variables")
                return False
                
            # Gemini Live API WebSocket endpoint
            url = f"wss://generativelanguage.googleapis.com/v1beta/models/{self.model}:streamGenerateContent"
            
            # Add API key to headers
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            self.websocket = await websockets.connect(url, extra_headers=headers)
            self.is_connected = True
            logger.info("Connected to Gemini Live API")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to Gemini Live API: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect from Gemini Live API"""
        if self.websocket:
            await self.websocket.close()
            self.is_connected = False
            logger.info("Disconnected from Gemini Live API")
    
    async def send_audio_frame(self, audio_data: bytes) -> bool:
        """Send audio frame to Gemini Live API"""
        try:
            if not self.is_connected or not self.websocket:
                logger.error("Not connected to Gemini Live API")
                return False
            
            # Create message for audio frame
            message = {
                "contents": [{
                    "role": "user",
                    "parts": [{
                        "inline_data": {
                            "mime_type": "audio/webm",
                            "data": audio_data.hex()
                        }
                    }]
                }]
            }
            
            await self.websocket.send(json.dumps(message))
            return True
            
        except Exception as e:
            logger.error(f"Failed to send audio frame: {e}")
            return False
    
    async def receive_transcript(self) -> AsyncGenerator[Dict[str, Any], None]:
        """Receive transcript chunks from Gemini Live API"""
        try:
            if not self.is_connected or not self.websocket:
                logger.error("Not connected to Gemini Live API")
                return
            
            async for message in self.websocket:
                try:
                    data = json.loads(message)
                    
                    # Extract transcript from response
                    if 'candidates' in data and data['candidates']:
                        candidate = data['candidates'][0]
                        if 'content' in candidate and 'parts' in candidate['content']:
                            for part in candidate['content']['parts']:
                                if 'text' in part:
                                    yield {
                                        'text': part['text'],
                                        'timestamp': datetime.utcnow().isoformat(),
                                        'confidence': candidate.get('finishReason', 'STOP')
                                    }
                    
                except json.JSONDecodeError:
                    logger.error("Failed to parse Gemini Live response")
                except Exception as e:
                    logger.error(f"Error processing Gemini Live response: {e}")
                    
        except Exception as e:
            logger.error(f"Error receiving transcript: {e}")
    
    async def send_text_message(self, text: str) -> bool:
        """Send text message to Gemini Live API"""
        try:
            if not self.is_connected or not self.websocket:
                logger.error("Not connected to Gemini Live API")
                return False
            
            message = {
                "contents": [{
                    "role": "user",
                    "parts": [{"text": text}]
                }]
            }
            
            await self.websocket.send(json.dumps(message))
            return True
            
        except Exception as e:
            logger.error(f"Failed to send text message: {e}")
            return False

class GeminiLiveProcessor:
    """Processor for handling Gemini Live API interactions"""
    
    def __init__(self):
        self.client = GeminiLiveClient()
        self.is_processing = False
        
    async def start_processing(self):
        """Start processing with Gemini Live API"""
        try:
            if not await self.client.connect():
                return False
                
            self.is_processing = True
            logger.info("Started Gemini Live processing")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start Gemini Live processing: {e}")
            return False
    
    async def stop_processing(self):
        """Stop processing"""
        self.is_processing = False
        await self.client.disconnect()
        logger.info("Stopped Gemini Live processing")
    
    async def process_audio_chunk(self, audio_data: bytes) -> Optional[Dict[str, Any]]:
        """Process audio chunk and return transcript"""
        try:
            if not self.is_processing:
                return None
                
            # Send audio frame
            if not await self.client.send_audio_frame(audio_data):
                return None
            
            # Wait for transcript (with timeout)
            try:
                async for transcript in self.client.receive_transcript():
                    return transcript
            except asyncio.TimeoutError:
                logger.warning("Timeout waiting for transcript")
                return None
                
        except Exception as e:
            logger.error(f"Error processing audio chunk: {e}")
            return None
    
    async def get_transcript_stream(self) -> AsyncGenerator[Dict[str, Any], None]:
        """Get stream of transcripts"""
        try:
            async for transcript in self.client.receive_transcript():
                yield transcript
        except Exception as e:
            logger.error(f"Error in transcript stream: {e}")

# Global processor instance
gemini_processor = GeminiLiveProcessor()

async def initialize_gemini_live():
    """Initialize Gemini Live processing"""
    return await gemini_processor.start_processing()

async def shutdown_gemini_live():
    """Shutdown Gemini Live processing"""
    await gemini_processor.stop_processing()

async def process_audio_with_gemini(audio_data: bytes) -> Optional[Dict[str, Any]]:
    """Process audio data with Gemini Live API"""
    return await gemini_processor.process_audio_chunk(audio_data)
