"""
Memory Assistance Agent

This agent specializes in helping individuals with Alzheimer's disease
with memory-related tasks, reminiscence therapy, and cognitive support.
"""

import json
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import asyncio

class MemoryAssistanceAgent:
    """
    Specialized agent for memory assistance and cognitive support.
    Provides reminiscence therapy, memory prompts, and cognitive exercises.
    """
    
    def __init__(self, user_id: str):
        """
        Initialize the memory assistance agent.
        
        Args:
            user_id: Unique identifier for the user
        """
        self.user_id = user_id
        self.agent_id = "memory_assistance"
        
        # Memory database structure
        self.memory_database = {
            "personal_memories": [],
            "family_members": [],
            "important_places": [],
            "life_events": [],
            "daily_facts": [],
            "preferences": {}
        }
        
        # Cognitive exercises
        self.cognitive_exercises = {
            "word_association": [],
            "memory_games": [],
            "reminiscence_prompts": []
        }
        
        # Initialize with default memories and exercises
        self._initialize_default_content()
    
    async def process_request(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process memory-related requests and provide appropriate assistance.
        
        Args:
            input_data: User input data
            context: Current session context
            
        Returns:
            Response from the memory assistance agent
        """
        try:
            content = input_data.get("content", "").lower()
            input_type = input_data.get("type", "text")
            
            # Determine the type of memory assistance needed
            if "remember" in content or "forgot" in content:
                return await self._handle_memory_prompt(content, context)
            elif "who is" in content or "what is" in content:
                return await self._handle_fact_recall(content, context)
            elif "tell me about" in content or "story" in content:
                return await self._handle_reminiscence(content, context)
            elif "exercise" in content or "game" in content:
                return await self._handle_cognitive_exercise(content, context)
            else:
                return await self._handle_general_memory_support(content, context)
                
        except Exception as e:
            return {
                "agent": self.agent_id,
                "error": True,
                "message": f"Error in memory assistance: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    async def _handle_memory_prompt(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle requests for memory prompts and reminders."""
        # Extract key information from the request
        memory_type = self._identify_memory_type(content)
        
        if memory_type == "personal":
            memories = self._get_personal_memories(content)
            response_text = self._format_memory_response(memories, "personal")
        elif memory_type == "family":
            family_info = self._get_family_information(content)
            response_text = self._format_family_response(family_info)
        else:
            response_text = self._provide_general_memory_support(content)
        
        return {
            "agent": self.agent_id,
            "type": "memory_prompt",
            "content": response_text,
            "memories_retrieved": len(memories) if 'memories' in locals() else 0,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _handle_fact_recall(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle requests for specific fact recall."""
        # Identify what information is being requested
        fact_type = self._identify_fact_type(content)
        
        if fact_type == "person":
            person_info = self._get_person_information(content)
            response_text = self._format_person_response(person_info)
        elif fact_type == "place":
            place_info = self._get_place_information(content)
            response_text = self._format_place_response(place_info)
        elif fact_type == "event":
            event_info = self._get_event_information(content)
            response_text = self._format_event_response(event_info)
        else:
            response_text = "I'm here to help you remember. Could you tell me more about what you'd like to recall?"
        
        return {
            "agent": self.agent_id,
            "type": "fact_recall",
            "content": response_text,
            "fact_type": fact_type,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _handle_reminiscence(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle reminiscence therapy requests."""
        # Select appropriate reminiscence prompts
        prompts = self._get_reminiscence_prompts(content)
        
        response_text = self._format_reminiscence_response(prompts)
        
        return {
            "agent": self.agent_id,
            "type": "reminiscence",
            "content": response_text,
            "prompts_provided": len(prompts),
            "timestamp": datetime.now().isoformat()
        }
    
    async def _handle_cognitive_exercise(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle cognitive exercise requests."""
        # Select appropriate cognitive exercise
        exercise = self._get_cognitive_exercise(content)
        
        response_text = self._format_exercise_response(exercise)
        
        return {
            "agent": self.agent_id,
            "type": "cognitive_exercise",
            "content": response_text,
            "exercise_type": exercise.get("type", "unknown"),
            "timestamp": datetime.now().isoformat()
        }
    
    async def _handle_general_memory_support(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle general memory support requests."""
        # Provide gentle memory support and encouragement
        response_text = self._provide_encouraging_memory_support(content)
        
        return {
            "agent": self.agent_id,
            "type": "general_support",
            "content": response_text,
            "timestamp": datetime.now().isoformat()
        }
    
    def _identify_memory_type(self, content: str) -> str:
        """Identify the type of memory being requested."""
        if any(word in content for word in ["family", "mother", "father", "son", "daughter", "spouse"]):
            return "family"
        elif any(word in content for word in ["childhood", "school", "work", "marriage"]):
            return "personal"
        else:
            return "general"
    
    def _identify_fact_type(self, content: str) -> str:
        """Identify the type of fact being requested."""
        if any(word in content for word in ["who is", "who was", "person"]):
            return "person"
        elif any(word in content for word in ["where is", "place", "location"]):
            return "place"
        elif any(word in content for word in ["when did", "what happened", "event"]):
            return "event"
        else:
            return "general"
    
    def _get_personal_memories(self, content: str) -> List[Dict[str, Any]]:
        """Retrieve relevant personal memories."""
        # This would typically query a database
        # For now, return sample memories
        return [
            {
                "id": "mem_001",
                "type": "childhood",
                "description": "Playing in the backyard with siblings",
                "date": "1950s",
                "importance": "high"
            },
            {
                "id": "mem_002", 
                "type": "school",
                "description": "First day of school",
                "date": "1955",
                "importance": "medium"
            }
        ]
    
    def _get_family_information(self, content: str) -> List[Dict[str, Any]]:
        """Retrieve family member information."""
        return [
            {
                "name": "Sarah",
                "relationship": "daughter",
                "age": "45",
                "location": "New York",
                "contact": "sarah@email.com"
            },
            {
                "name": "John",
                "relationship": "son", 
                "age": "42",
                "location": "California",
                "contact": "john@email.com"
            }
        ]
    
    def _get_person_information(self, content: str) -> Dict[str, Any]:
        """Get information about a specific person."""
        # Extract person name from content
        # This would typically query a database
        return {
            "name": "Sarah",
            "relationship": "daughter",
            "recent_contact": "Last week",
            "important_notes": "Lives in New York, works as a teacher"
        }
    
    def _get_place_information(self, content: str) -> Dict[str, Any]:
        """Get information about a specific place."""
        return {
            "name": "Home",
            "address": "123 Main Street",
            "description": "Your house where you've lived for 30 years",
            "directions": "Turn left at the corner, go two blocks"
        }
    
    def _get_event_information(self, content: str) -> Dict[str, Any]:
        """Get information about a specific event."""
        return {
            "event": "Wedding Anniversary",
            "date": "June 15th",
            "year": "1965",
            "description": "Your 50th wedding anniversary celebration"
        }
    
    def _get_reminiscence_prompts(self, content: str) -> List[Dict[str, Any]]:
        """Get reminiscence therapy prompts."""
        return [
            {
                "prompt": "Tell me about your favorite childhood toy",
                "category": "childhood",
                "difficulty": "easy"
            },
            {
                "prompt": "What was your first job like?",
                "category": "work",
                "difficulty": "medium"
            }
        ]
    
    def _get_cognitive_exercise(self, content: str) -> Dict[str, Any]:
        """Get a cognitive exercise."""
        return {
            "type": "word_association",
            "exercise": "I'll say a word, and you tell me the first thing that comes to mind",
            "words": ["home", "family", "love", "happy"],
            "instructions": "Take your time, there are no wrong answers"
        }
    
    def _format_memory_response(self, memories: List[Dict[str, Any]], memory_type: str) -> str:
        """Format memory response for user."""
        if not memories:
            return "I'm here to help you remember. Take your time, and I'll be patient with you."
        
        response = f"I found some {memory_type} memories for you:\n\n"
        for memory in memories[:3]:  # Limit to 3 memories
            response += f"• {memory['description']} ({memory['date']})\n"
        
        response += "\nWould you like to tell me more about any of these?"
        return response
    
    def _format_family_response(self, family_info: List[Dict[str, Any]]) -> str:
        """Format family information response."""
        if not family_info:
            return "I'm here to help you remember your family. Take your time."
        
        response = "Here's information about your family:\n\n"
        for member in family_info:
            response += f"• {member['name']} - your {member['relationship']} (age {member['age']})\n"
        
        return response
    
    def _format_person_response(self, person_info: Dict[str, Any]) -> str:
        """Format person information response."""
        return f"{person_info['name']} is your {person_info['relationship']}. {person_info['important_notes']}"
    
    def _format_place_response(self, place_info: Dict[str, Any]) -> str:
        """Format place information response."""
        return f"{place_info['name']} is located at {place_info['address']}. {place_info['description']}"
    
    def _format_event_response(self, event_info: Dict[str, Any]) -> str:
        """Format event information response."""
        return f"{event_info['event']} was on {event_info['date']}, {event_info['year']}. {event_info['description']}"
    
    def _format_reminiscence_response(self, prompts: List[Dict[str, Any]]) -> str:
        """Format reminiscence response."""
        if not prompts:
            return "Let's talk about your memories. What would you like to share?"
        
        response = "Let's take a gentle walk down memory lane. Here are some things we can talk about:\n\n"
        for prompt in prompts:
            response += f"• {prompt['prompt']}\n"
        
        response += "\nTake your time, and tell me whatever comes to mind."
        return response
    
    def _format_exercise_response(self, exercise: Dict[str, Any]) -> str:
        """Format cognitive exercise response."""
        response = f"Let's do a gentle {exercise['type']} exercise. {exercise['instructions']}\n\n"
        response += f"Here's the exercise: {exercise['exercise']}\n\n"
        response += "Ready when you are!"
        return response
    
    def _provide_encouraging_memory_support(self, content: str) -> str:
        """Provide encouraging memory support."""
        responses = [
            "I'm here to help you remember. Take your time, there's no rush.",
            "Memory can be tricky sometimes, but we'll work through this together.",
            "It's okay if you don't remember right away. I'm patient and here to help.",
            "Let's take this one step at a time. What would you like to remember?"
        ]
        
        # Simple response selection based on content
        if "help" in content:
            return responses[0]
        elif "forgot" in content:
            return responses[1]
        elif "remember" in content:
            return responses[2]
        else:
            return responses[3]
    
    def _initialize_default_content(self):
        """Initialize default memories and exercises."""
        # Add some default reminiscence prompts
        self.cognitive_exercises["reminiscence_prompts"] = [
            "Tell me about your favorite childhood memory",
            "What was your first job like?",
            "Tell me about your wedding day",
            "What was your favorite holiday tradition?",
            "Tell me about your children when they were young"
        ]
        
        # Add some default cognitive exercises
        self.cognitive_exercises["word_association"] = [
            {"word": "home", "associations": ["family", "comfort", "love"]},
            {"word": "spring", "associations": ["flowers", "renewal", "growth"]},
            {"word": "music", "associations": ["dancing", "singing", "joy"]}
        ]
    
    def add_memory(self, memory_data: Dict[str, Any]):
        """Add a new memory to the database."""
        memory_data["id"] = str(uuid.uuid4())
        memory_data["created_at"] = datetime.now().isoformat()
        self.memory_database["personal_memories"].append(memory_data)
    
    def update_family_member(self, member_data: Dict[str, Any]):
        """Update family member information."""
        for member in self.memory_database["family_members"]:
            if member["name"] == member_data["name"]:
                member.update(member_data)
                return
        
        # Add new family member if not found
        member_data["id"] = str(uuid.uuid4())
        self.memory_database["family_members"].append(member_data)
