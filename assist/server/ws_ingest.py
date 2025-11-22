"""
WebSocket ingest handler for receiving audio/video chunks from Chrome extension
"""

import asyncio
import logging
import base64
from typing import Optional
from fastapi import WebSocket
import numpy as np
from io import BytesIO

logger = logging.getLogger(__name__)

class WebSocketIngest:
    def __init__(self, gemini_live, adk_orchestrator):
        self.gemini_live = gemini_live
        self.adk_orchestrator = adk_orchestrator
        self.active_connections: Dict[str, WebSocket] = {}
        self.frame_counter = 0
        self.frame_interval = 30  # Capture frame every 30 chunks
        
    async def handle_connection(self, websocket: WebSocket):
        """Handle WebSocket connection from Chrome extension"""
        connection_id = f"conn_{id(websocket)}"
        self.active_connections[connection_id] = websocket
        
        try:
            logger.info(f"WebSocket connection established: {connection_id}")
            
            while True:
                # Receive binary data (WebM chunks)
                data = await websocket.receive_bytes()
                await self.process_chunk(data, connection_id)
                
        except Exception as e:
            logger.error(f"Error in WebSocket connection {connection_id}: {e}")
        finally:
            if connection_id in self.active_connections:
                del self.active_connections[connection_id]
            logger.info(f"WebSocket connection closed: {connection_id}")
    
    async def process_chunk(self, chunk_data: bytes, connection_id: str):
        """Process incoming WebM chunk"""
        try:
            # Extract audio frames from WebM chunk
            audio_frames = await self.extract_audio_frames(chunk_data)
            
            if audio_frames is not None and len(audio_frames) > 0:
                # Send to Gemini Live for transcription
                if self.gemini_live:
                    await self.gemini_live.send_audio_frames(audio_frames)
                
                # Process with ADK orchestrator
                if self.adk_orchestrator:
                    await self.adk_orchestrator.process_audio_chunk(audio_frames, connection_id)
            
            # Periodically capture video frames for embeddings
            self.frame_counter += 1
            if self.frame_counter % self.frame_interval == 0:
                await self.capture_video_frame(chunk_data, connection_id)
                
        except Exception as e:
            logger.error(f"Error processing chunk: {e}")
    
    async def extract_audio_frames(self, webm_data: bytes) -> Optional[np.ndarray]:
        """Extract audio frames from WebM chunk"""
        try:
            # This is a simplified extraction - in production, you'd use proper WebM parsing
            # For now, we'll simulate audio frame extraction
            # In a real implementation, you'd use libraries like ffmpeg-python or pymediainfo
            
            # Simulate audio frame extraction
            # In practice, you'd parse the WebM container and extract PCM audio
            audio_length = len(webm_data) // 4  # Rough estimate
            audio_frames = np.random.randn(audio_length).astype(np.float32)
            
            return audio_frames
            
        except Exception as e:
            logger.error(f"Failed to extract audio frames: {e}")
            return None
    
    async def capture_video_frame(self, webm_data: bytes, connection_id: str):
        """Capture video frame for embedding generation"""
        try:
            # Extract video frame from WebM chunk
            # In production, you'd use proper video frame extraction
            frame_data = await self.extract_video_frame(webm_data)
            
            if frame_data:
                # Generate embedding for the frame
                if self.adk_orchestrator:
                    await self.adk_orchestrator.process_video_frame(frame_data, connection_id)
                    
        except Exception as e:
            logger.error(f"Failed to capture video frame: {e}")
    
    async def extract_video_frame(self, webm_data: bytes) -> Optional[bytes]:
        """Extract video frame from WebM chunk"""
        try:
            # Simplified video frame extraction
            # In production, you'd use proper video parsing
            # For now, return a placeholder
            return webm_data[:1024]  # First 1KB as placeholder
            
        except Exception as e:
            logger.error(f"Failed to extract video frame: {e}")
            return None
    
    async def send_message(self, connection_id: str, message: dict):
        """Send message to specific WebSocket connection"""
        if connection_id in self.active_connections:
            try:
                websocket = self.active_connections[connection_id]
                await websocket.send_json(message)
            except Exception as e:
                logger.error(f"Failed to send message to {connection_id}: {e}")
    
    async def broadcast_message(self, message: dict):
        """Broadcast message to all active connections"""
        for connection_id in list(self.active_connections.keys()):
            await self.send_message(connection_id, message)
