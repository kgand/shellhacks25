import json
import os
from websockets import connect
from typing import Dict, Optional, Any

class A2AADKConnection:
    """
    Client for connecting to the Google A2A ADK Multimodal API
    Handles WebSocket communication, audio/video streaming, and response processing
    """
    
    def __init__(self):
        """Initialize the Google A2A ADK connection with API key from environment"""
        self.api_key = os.environ.get("A2A_ADK_API_KEY")
        if not self.api_key:
            raise ValueError("A2A_ADK_API_KEY environment variable is not set")
            
        self.model = "gemini-2.0-flash-exp"
        self.uri = (
            "wss://generativelanguage.googleapis.com/ws/"
            "google.ai.generativelanguage.v1alpha.GenerativeService.BidiGenerateContent"
            f"?key={self.api_key}"
        )
        self.ws = None
        self.config = None

    def set_config(self, config_data: Dict[str, Any]) -> None:
        """
        Store systemPrompt, voice, and other configuration.
        
        Args:
            config_data: Dict containing configuration like:
                {
                  'systemPrompt': 'You are a friendly AI Assistant...',
                  'voice': 'Puck',
                  'googleSearch': True,
                  'allowInterruptions': True
                }
        """
        self.config = config_data

    async def connect(self) -> None:
        """
        Establish WebSocket connection and send initial setup message
        Configure Google A2A ADK for real-time conversation with audio responses
        
        Raises:
            ValueError: If configuration is not set
            ConnectionError: If connection fails
        """
        if not self.config:
            raise ValueError("Configuration must be set before connecting.")

        try:
            self.ws = await connect(self.uri)

            # Build 'setup' payload for real-time conversation
            setup_message = {
                "setup": {
                    "model": f"models/{self.model}",
                    "generation_config": {
                        "response_modalities": ["AUDIO"],
                        "speech_config": {
                            "voice_config": {
                                "prebuilt_voice_config": {
                                    "voice_name": self.config.get("voice", "Puck")
                                }
                            }
                        }
                    },
                    "system_instruction": {
                        "parts": [
                            {
                                "text": self.config.get(
                                    "systemPrompt",
                                    """You are a friendly AI Assistant that can see, hear, and respond in real-time. You can interrupt and be interrupted naturally in conversation. Use the visual and audio context provided to give helpful, contextual responses."""
                                )
                            }
                        ]
                    }
                }
            }

            # Send setup as the first message
            await self.ws.send(json.dumps(setup_message))

            # Read the initial response from Google A2A ADK (often just an ack)
            setup_response = await self.ws.recv()
            print("Google A2A ADK setup response:", setup_response)
            
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Google A2A ADK API: {str(e)}")

    async def send_audio(self, base64_pcm: str) -> None:
        """
        Send 16-bit PCM audio (base64) to Google A2A ADK under 'realtime_input'.
        
        Args:
            base64_pcm: Base64 encoded 16-bit PCM audio data
        """
        if not self.ws:
            return
            
        payload = {
            "realtime_input": {
                "media_chunks": [
                    {
                        "data": base64_pcm,
                        "mime_type": "audio/pcm"
                    }
                ]
            }
        }
        await self.ws.send(json.dumps(payload))

    async def send_text(self, text: str) -> None:
        """
        Send text message to Google A2A ADK.
        
        Args:
            text: Text content to send
        """
        if not self.ws:
            return
            
        text_msg = {
            "client_content": {
                "turns": [
                    {
                        "role": "user",
                        "parts": [{"text": text}]
                    }
                ],
                "turn_complete": True
            }
        }
        await self.ws.send(json.dumps(text_msg))

    async def send_image(self, base64_jpeg: str) -> None:
        """
        Send image data to Google A2A ADK for visual context.
        
        Args:
            base64_jpeg: Base64 encoded JPEG image data
        """
        if not self.ws:
            return
            
        payload = {
            "realtime_input": {
                "media_chunks": [
                    {
                        "data": base64_jpeg,
                        "mime_type": "image/jpeg"
                    }
                ]
            }
        }
        await self.ws.send(json.dumps(payload))

    async def send_interrupt(self) -> None:
        """
        Send interrupt signal to Google A2A ADK to stop current response
        """
        if not self.ws:
            return
            
        interrupt_msg = {
            "interrupt": {}
        }
        await self.ws.send(json.dumps(interrupt_msg))

    async def receive(self) -> Optional[str]:
        """
        Wait for next message from Google A2A ADK.
        
        Returns:
            JSON response string or None if connection is closed
        """
        if not self.ws:
            return None
        return await self.ws.recv()

    async def close(self) -> None:
        """Close the WebSocket connection."""
        if self.ws:
            await self.ws.close()
            self.ws = None
