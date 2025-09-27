"""
Ollama Client for VLM and LLM Processing
Real-time video and audio analysis with Ollama models
"""

import requests
import json
import base64
import time
import logging
from typing import Optional, Dict, Any
from datetime import datetime
import cv2
import numpy as np

logger = logging.getLogger(__name__)

class OllamaClient:
    """Client for interacting with Ollama VLM and LLM models"""
    
    def __init__(self, host: str = "http://localhost:11434"):
        self.host = host
        self.vlm_model = "gemma3:4b"     # Vision Language Model
        self.llm_model = "qwen3:8b"      # Text Language Model
        self.timeout = 300  # 5 minutes timeout
        
    def _call_ollama_api(self, model: str, prompt: str, image_base64: str = None) -> Dict[str, Any]:
        """
        Call Ollama API with optional image input
        
        Args:
            model: Ollama model name
            prompt: Text prompt
            image_base64: Base64 encoded image (optional)
            
        Returns:
            Dict containing Ollama response
        """
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
        }
        
        if image_base64:
            payload["images"] = [image_base64]
        
        try:
            response = requests.post(
                f"{self.host}/api/generate",
                headers=headers,
                data=json.dumps(payload),
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.Timeout:
            raise Exception("Ollama request timed out. Model might be loading or busy.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error calling Ollama: {e}")
        except json.JSONDecodeError:
            raise Exception(f"Error decoding Ollama response: {response.text}")
        except Exception as e:
            raise Exception(f"Unexpected error during Ollama call: {e}")
    
    def analyze_frame(self, frame: np.ndarray, system_prompt: str = None, user_query: str = None) -> str:
        """
        Analyze a video frame using VLM
        
        Args:
            frame: OpenCV frame (numpy array)
            system_prompt: Optional system prompt
            user_query: User query for analysis
            
        Returns:
            Analysis result as string
        """
        try:
            # Encode frame to base64
            _, buffer = cv2.imencode('.png', frame)
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            
            # Build prompt
            full_prompt = ""
            if system_prompt:
                full_prompt += f"{system_prompt}\n\n"
            if user_query:
                full_prompt += user_query
            else:
                full_prompt += "Describe what is happening in this image in detail. Focus on objects, actions, and the overall scene."
            
            # Call Ollama VLM
            response = self._call_ollama_api(self.vlm_model, full_prompt, img_base64)
            return response.get("response", "No response from VLM")
            
        except Exception as e:
            logger.error(f"Error analyzing frame: {e}")
            return f"VLM analysis failed: {e}"
    
    def process_text(self, prompt: str, system_prompt: str = None) -> str:
        """
        Process text using LLM
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            
        Returns:
            LLM response as string
        """
        try:
            # Build full prompt
            full_prompt = ""
            if system_prompt:
                full_prompt += f"{system_prompt}\n\n"
            full_prompt += prompt
            
            # Call Ollama LLM
            response = self._call_ollama_api(self.llm_model, full_prompt)
            return response.get("response", "No response from LLM")
            
        except Exception as e:
            logger.error(f"Error processing text: {e}")
            return f"LLM processing failed: {e}"
    
    def summarize_content(self, content: str, system_prompt: str = None) -> str:
        """
        Summarize content using LLM
        
        Args:
            content: Content to summarize
            system_prompt: Optional system prompt for summarization
            
        Returns:
            Summary as string
        """
        try:
            # Default summarization prompt
            default_system_prompt = """You are an AI assistant tasked with summarizing content from a Messenger conversation.
            Provide a concise, coherent summary focusing on key points, important information, and main topics discussed.
            Keep the summary under 400 characters and make it easy to understand."""
            
            system_prompt = system_prompt or default_system_prompt
            
            # Build full prompt
            full_prompt = f"{system_prompt}\n\nContent to summarize:\n{content}"
            
            # Call Ollama LLM
            response = self._call_ollama_api(self.llm_model, full_prompt)
            return response.get("response", "No summary generated")
            
        except Exception as e:
            logger.error(f"Error summarizing content: {e}")
            return f"Summarization failed: {e}"
    
    def transcribe_audio(self, audio_file_path: str) -> str:
        """
        Transcribe audio file using Ollama (if supported) or return placeholder
        
        Args:
            audio_file_path: Path to audio file
            
        Returns:
            Transcription as string
        """
        try:
            # For now, return a placeholder since Ollama doesn't directly support audio transcription
            # In a real implementation, you would use a speech-to-text service
            logger.info(f"Audio transcription requested for: {audio_file_path}")
            return f"[Audio transcription placeholder for {audio_file_path}]"
            
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            return f"Audio transcription failed: {e}"
    
    def get_models(self) -> Dict[str, Any]:
        """
        Get available Ollama models
        
        Returns:
            Dict containing model information
        """
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=30)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            logger.error(f"Error getting models: {e}")
            return {"error": str(e)}
    
    def is_available(self) -> bool:
        """
        Check if Ollama is available and running
        
        Returns:
            True if Ollama is available, False otherwise
        """
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
