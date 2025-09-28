"""
A2A ADK Integration for Cognitive Assistance System

This module provides integration between the cognitive assistance system
and the Google A2A ADK multimodal API for real-time Alzheimer's support.
"""

import json
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid

from .core_assistant import CognitiveAssistant
from .agents.memory_agent import MemoryAssistanceAgent
from .agents.routine_agent import RoutineManagementAgent
from .agents.safety_agent import SafetyMonitoringAgent
from .agents.communication_agent import FamilyCommunicationAgent

class A2ACognitiveIntegration:
    """
    Integration class that connects the cognitive assistance system
    with the Google A2A ADK multimodal API.
    """
    
    def __init__(self, user_id: str = None):
        """
        Initialize the A2A cognitive integration.
        
        Args:
            user_id: Unique identifier for the user
        """
        self.user_id = user_id or str(uuid.uuid4())
        self.cognitive_assistant = CognitiveAssistant(self.user_id)
        
        # A2A ADK configuration for Alzheimer's assistance
        self.a2a_config = {
            "systemPrompt": self._get_alzheimer_system_prompt(),
            "voice": "Puck",  # Gentle, calm voice
            "googleSearch": True,
            "allowInterruptions": True,
            "response_modalities": ["AUDIO", "TEXT"],
            "safety_features": {
                "emergency_detection": True,
                "fall_detection": True,
                "wandering_alert": True
            }
        }
        
        # Session management
        self.session_id = str(uuid.uuid4())
        self.session_start = datetime.now()
        self.interaction_count = 0
        
        # Performance metrics
        self.metrics = {
            "total_interactions": 0,
            "successful_responses": 0,
            "emergency_triggers": 0,
            "family_notifications": 0,
            "average_response_time": 0.0
        }
    
    def get_a2a_config(self) -> Dict[str, Any]:
        """
        Get the A2A ADK configuration for Alzheimer's assistance.
        
        Returns:
            Configuration dictionary for A2A ADK
        """
        return self.a2a_config.copy()
    
    async def process_multimodal_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process multimodal input from A2A ADK and return appropriate response.
        
        Args:
            input_data: Multimodal input from A2A ADK
            
        Returns:
            Response for A2A ADK
        """
        try:
            start_time = datetime.now()
            self.interaction_count += 1
            
            # Process input through cognitive assistant
            response = await self.cognitive_assistant.process_user_input(input_data)
            
            # Calculate response time
            response_time = (datetime.now() - start_time).total_seconds()
            self.metrics["average_response_time"] = (
                (self.metrics["average_response_time"] * (self.interaction_count - 1) + response_time) 
                / self.interaction_count
            )
            
            # Update metrics
            self.metrics["total_interactions"] += 1
            if not response.get("error"):
                self.metrics["successful_responses"] += 1
            
            # Check for emergency triggers
            if self._is_emergency_response(response):
                self.metrics["emergency_triggers"] += 1
                await self._handle_emergency_escalation(response)
            
            # Format response for A2A ADK
            a2a_response = self._format_a2a_response(response)
            
            return a2a_response
            
        except Exception as e:
            return {
                "error": True,
                "message": f"Error processing input: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "session_id": self.session_id
            }
    
    def _get_alzheimer_system_prompt(self) -> str:
        """Get the system prompt optimized for Alzheimer's assistance."""
        return """
You are a compassionate AI assistant specifically designed to help individuals with Alzheimer's disease and their families. Your role is to provide gentle, patient, and supportive assistance.

Key Guidelines:
1. Always speak in a calm, reassuring tone
2. Be patient and never rush the user
3. Use simple, clear language
4. Repeat important information when needed
5. Provide gentle reminders and encouragement
6. Be understanding of memory challenges
7. Offer emotional support and comfort
8. Help with daily routines and safety
9. Facilitate family communication
10. Respond to emergencies with appropriate urgency

Specialized Capabilities:
- Memory assistance and reminiscence therapy
- Daily routine management and medication reminders
- Safety monitoring and emergency response
- Family communication and caregiver coordination
- Cognitive exercises and mental stimulation
- Emotional support and companionship

Remember: You are not just an AI assistant - you are a caring companion who understands the unique challenges of Alzheimer's disease and is here to provide meaningful support and assistance.
        """.strip()
    
    def _is_emergency_response(self, response: Dict[str, Any]) -> bool:
        """Check if the response indicates an emergency situation."""
        if response.get("agent") == "safety_monitoring":
            return response.get("type") in ["emergency", "fall_incident"]
        return False
    
    async def _handle_emergency_escalation(self, response: Dict[str, Any]):
        """Handle emergency escalation procedures."""
        # Log emergency
        print(f"🚨 EMERGENCY DETECTED: {response.get('type', 'Unknown')}")
        
        # In a real system, this would:
        # 1. Send alerts to family members
        # 2. Contact emergency services if needed
        # 3. Update caregiver dashboards
        # 4. Log the incident for medical records
        
        self.metrics["emergency_triggers"] += 1
    
    def _format_a2a_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Format response for A2A ADK compatibility."""
        # Extract the main content
        content = response.get("content", "I'm here to help you.")
        
        # Add emotional context for Alzheimer's assistance
        if response.get("agent") == "memory_assistance":
            content = self._add_memory_support_context(content)
        elif response.get("agent") == "safety_monitoring":
            content = self._add_safety_context(content)
        elif response.get("agent") == "routine_management":
            content = self._add_routine_context(content)
        elif response.get("agent") == "family_communication":
            content = self._add_communication_context(content)
        
        return {
            "text": content,
            "agent": response.get("agent", "cognitive_assistant"),
            "timestamp": response.get("timestamp", datetime.now().isoformat()),
            "session_id": self.session_id,
            "user_id": self.user_id,
            "metrics": self.metrics
        }
    
    def _add_memory_support_context(self, content: str) -> str:
        """Add memory support context to response."""
        return f"💭 {content}\n\nTake your time remembering. I'm here to help you with your memories."
    
    def _add_safety_context(self, content: str) -> str:
        """Add safety context to response."""
        return f"🛡️ {content}\n\nYour safety is my priority. I'm monitoring your wellbeing."
    
    def _add_routine_context(self, content: str) -> str:
        """Add routine context to response."""
        return f"📅 {content}\n\nI'm here to help you stay on track with your daily routine."
    
    def _add_communication_context(self, content: str) -> str:
        """Add communication context to response."""
        return f"📞 {content}\n\nI'm helping you stay connected with your family and caregivers."
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get a summary of the current session."""
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "start_time": self.session_start.isoformat(),
            "duration_minutes": (datetime.now() - self.session_start).total_seconds() / 60,
            "interaction_count": self.interaction_count,
            "metrics": self.metrics,
            "cognitive_assistant_summary": self.cognitive_assistant.get_session_summary()
        }
    
    def update_user_profile(self, profile_data: Dict[str, Any]):
        """Update user profile information."""
        self.cognitive_assistant.update_user_profile(profile_data)
    
    def get_user_profile(self) -> Dict[str, Any]:
        """Get current user profile."""
        return self.cognitive_assistant.get_user_profile()
    
    def reset_session(self):
        """Reset the current session."""
        self.session_id = str(uuid.uuid4())
        self.session_start = datetime.now()
        self.interaction_count = 0
        self.metrics = {
            "total_interactions": 0,
            "successful_responses": 0,
            "emergency_triggers": 0,
            "family_notifications": 0,
            "average_response_time": 0.0
        }
