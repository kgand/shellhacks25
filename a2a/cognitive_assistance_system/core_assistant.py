"""
Core Cognitive Assistant

This module provides the main cognitive assistance system that orchestrates
all specialized agents for comprehensive Alzheimer's support.
"""

import asyncio
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import uuid

class CognitiveAssistant:
    """
    Main cognitive assistance system that coordinates all specialized agents
    to provide comprehensive support for individuals with Alzheimer's disease.
    """
    
    def __init__(self, user_id: str = None):
        """
        Initialize the cognitive assistant system.
        
        Args:
            user_id: Unique identifier for the user
        """
        self.user_id = user_id or str(uuid.uuid4())
        self.session_id = str(uuid.uuid4())
        self.created_at = datetime.now()
        
        # Initialize specialized agents
        self.memory_agent = None
        self.routine_agent = None
        self.safety_agent = None
        self.communication_agent = None
        
        # User profile and preferences
        self.user_profile = {
            "name": "",
            "age": None,
            "stage": "early",  # early, moderate, advanced
            "preferences": {
                "voice_speed": "slow",
                "reminder_frequency": "frequent",
                "family_contacts": [],
                "medical_contacts": []
            },
            "daily_routines": [],
            "important_memories": [],
            "safety_contacts": []
        }
        
        # Session state
        self.current_context = {
            "time_of_day": None,
            "location": None,
            "mood": None,
            "recent_interactions": [],
            "active_reminders": []
        }
        
        # Initialize agents
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize all specialized agents."""
        from .agents.memory_agent import MemoryAssistanceAgent
        from .agents.routine_agent import RoutineManagementAgent
        from .agents.safety_agent import SafetyMonitoringAgent
        from .agents.communication_agent import FamilyCommunicationAgent
        
        self.memory_agent = MemoryAssistanceAgent(self.user_id)
        self.routine_agent = RoutineManagementAgent(self.user_id)
        self.safety_agent = SafetyMonitoringAgent(self.user_id)
        self.communication_agent = FamilyCommunicationAgent(self.user_id)
    
    async def process_user_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process user input and coordinate appropriate agent responses.
        
        Args:
            input_data: User input containing text, audio, or other data
            
        Returns:
            Response from the most appropriate agent
        """
        try:
            # Update current context
            self._update_context(input_data)
            
            # Determine which agent should handle the request
            primary_agent = self._determine_primary_agent(input_data)
            
            # Get response from primary agent
            response = await primary_agent.process_request(input_data, self.current_context)
            
            # Add contextual information
            response["timestamp"] = datetime.now().isoformat()
            response["session_id"] = self.session_id
            response["user_id"] = self.user_id
            
            # Update interaction history
            self._update_interaction_history(input_data, response)
            
            return response
            
        except Exception as e:
            return {
                "error": True,
                "message": f"Error processing request: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "session_id": self.session_id
            }
    
    def _update_context(self, input_data: Dict[str, Any]):
        """Update the current context with new information."""
        current_time = datetime.now()
        self.current_context["time_of_day"] = current_time.strftime("%H:%M")
        
        # Update recent interactions
        self.current_context["recent_interactions"].append({
            "timestamp": current_time.isoformat(),
            "type": input_data.get("type", "unknown"),
            "content": input_data.get("content", "")
        })
        
        # Keep only last 10 interactions
        if len(self.current_context["recent_interactions"]) > 10:
            self.current_context["recent_interactions"] = self.current_context["recent_interactions"][-10:]
    
    def _determine_primary_agent(self, input_data: Dict[str, Any]) -> Any:
        """
        Determine which agent should primarily handle the request.
        
        Args:
            input_data: User input data
            
        Returns:
            The most appropriate agent
        """
        content = input_data.get("content", "").lower()
        input_type = input_data.get("type", "")
        
        # Safety concerns take priority
        if any(keyword in content for keyword in ["help", "emergency", "lost", "confused", "scared"]):
            return self.safety_agent
        
        # Memory-related requests
        if any(keyword in content for keyword in ["remember", "forgot", "who is", "what is", "when did"]):
            return self.memory_agent
        
        # Routine and schedule requests
        if any(keyword in content for keyword in ["schedule", "appointment", "medicine", "time", "today"]):
            return self.routine_agent
        
        # Communication requests
        if any(keyword in content for keyword in ["call", "message", "family", "doctor"]):
            return self.communication_agent
        
        # Default to memory agent for general conversation
        return self.memory_agent
    
    def _update_interaction_history(self, input_data: Dict[str, Any], response: Dict[str, Any]):
        """Update the interaction history for learning and context."""
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "input": input_data,
            "response": response,
            "agent_used": response.get("agent", "unknown")
        }
        
        # Store in user profile for future reference
        if "interaction_history" not in self.user_profile:
            self.user_profile["interaction_history"] = []
        
        self.user_profile["interaction_history"].append(interaction)
        
        # Keep only last 100 interactions
        if len(self.user_profile["interaction_history"]) > 100:
            self.user_profile["interaction_history"] = self.user_profile["interaction_history"][-100:]
    
    def update_user_profile(self, profile_data: Dict[str, Any]):
        """Update user profile information."""
        self.user_profile.update(profile_data)
    
    def get_user_profile(self) -> Dict[str, Any]:
        """Get current user profile."""
        return self.user_profile.copy()
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get a summary of the current session."""
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "started_at": self.created_at.isoformat(),
            "duration_minutes": (datetime.now() - self.created_at).total_seconds() / 60,
            "interactions_count": len(self.current_context["recent_interactions"]),
            "active_reminders": len(self.current_context["active_reminders"])
        }
