"""
Family Communication Agent

This agent specializes in facilitating communication between individuals
with Alzheimer's disease and their family members, caregivers, and
healthcare providers.
"""

import json
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import asyncio

class FamilyCommunicationAgent:
    """
    Specialized agent for family communication and caregiver coordination.
    Facilitates video calls, message delivery, and family updates.
    """
    
    def __init__(self, user_id: str):
        """
        Initialize the family communication agent.
        
        Args:
            user_id: Unique identifier for the user
        """
        self.user_id = user_id
        self.agent_id = "family_communication"
        
        # Communication database structure
        self.communication_database = {
            "family_members": [],
            "caregivers": [],
            "healthcare_providers": [],
            "recent_calls": [],
            "messages": [],
            "communication_preferences": {}
        }
        
        # Communication settings
        self.communication_settings = {
            "auto_answer_enabled": True,
            "call_recording_enabled": True,
            "message_notifications": True,
            "family_update_frequency": "daily",
            "emergency_contact_priority": True
        }
        
        # Communication templates
        self.communication_templates = {
            "daily_update": {
                "subject": "Daily Update",
                "template": "Good {time_of_day}! Here's how {user_name} is doing today..."
            },
            "medication_reminder": {
                "subject": "Medication Reminder",
                "template": "Reminder: {user_name} needs to take {medication} at {time}"
            },
            "appointment_reminder": {
                "subject": "Appointment Reminder", 
                "template": "Reminder: {user_name} has an appointment with {doctor} at {time}"
            },
            "safety_alert": {
                "subject": "Safety Alert",
                "template": "Safety Alert: {user_name} may need assistance. {details}"
            }
        }
        
        # Initialize with default communication data
        self._initialize_default_communication_data()
    
    async def process_request(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process communication-related requests and provide appropriate assistance.
        
        Args:
            input_data: User input data
            context: Current session context
            
        Returns:
            Response from the family communication agent
        """
        try:
            content = input_data.get("content", "").lower()
            input_type = input_data.get("type", "text")
            
            # Determine the type of communication assistance needed
            if any(keyword in content for keyword in ["call", "phone", "video", "talk to"]):
                return await self._handle_call_request(content, context)
            elif any(keyword in content for keyword in ["message", "text", "send", "tell"]):
                return await self._handle_message_request(content, context)
            elif any(keyword in content for keyword in ["family", "son", "daughter", "spouse"]):
                return await self._handle_family_request(content, context)
            elif any(keyword in content for keyword in ["doctor", "nurse", "medical", "healthcare"]):
                return await self._handle_healthcare_request(content, context)
            elif any(keyword in content for keyword in ["update", "how am i", "status", "report"]):
                return await self._handle_status_request(content, context)
            elif any(keyword in content for keyword in ["help", "assistance", "support"]):
                return await self._handle_support_request(content, context)
            else:
                return await self._handle_general_communication_support(content, context)
                
        except Exception as e:
            return {
                "agent": self.agent_id,
                "error": True,
                "message": f"Error in family communication: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    async def _handle_call_request(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle call requests."""
        # Determine who to call
        call_target = self._identify_call_target(content)
        
        # Get appropriate contacts
        contacts = self._get_contacts_for_call(call_target)
        
        if contacts:
            response_text = self._format_call_response(contacts, call_target)
            # Log the call request
            self._log_call_request(call_target, contacts)
        else:
            response_text = self._format_no_contacts_response(call_target)
        
        return {
            "agent": self.agent_id,
            "type": "call_request",
            "content": response_text,
            "call_target": call_target,
            "contacts_available": len(contacts),
            "timestamp": datetime.now().isoformat()
        }
    
    async def _handle_message_request(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle message requests."""
        # Extract message content and recipient
        message_info = self._extract_message_info(content)
        
        # Get appropriate recipients
        recipients = self._get_message_recipients(message_info["recipient_type"])
        
        if recipients:
            response_text = self._format_message_response(message_info, recipients)
            # Log the message
            self._log_message(message_info, recipients)
        else:
            response_text = self._format_no_recipients_response(message_info["recipient_type"])
        
        return {
            "agent": self.agent_id,
            "type": "message_request",
            "content": response_text,
            "message_info": message_info,
            "recipients_count": len(recipients),
            "timestamp": datetime.now().isoformat()
        }
    
    async def _handle_family_request(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle family-related requests."""
        # Get family information
        family_members = self._get_family_members()
        
        # Determine what family information is needed
        if "who" in content or "family" in content:
            response_text = self._format_family_info(family_members)
        elif "call" in content or "talk" in content:
            response_text = self._format_family_call_options(family_members)
        else:
            response_text = self._format_general_family_response(family_members)
        
        return {
            "agent": self.agent_id,
            "type": "family_request",
            "content": response_text,
            "family_members_count": len(family_members),
            "timestamp": datetime.now().isoformat()
        }
    
    async def _handle_healthcare_request(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle healthcare provider requests."""
        # Get healthcare providers
        healthcare_providers = self._get_healthcare_providers()
        
        # Determine healthcare need
        if "call" in content or "contact" in content:
            response_text = self._format_healthcare_contact_options(healthcare_providers)
        elif "appointment" in content:
            response_text = self._format_appointment_info(healthcare_providers)
        else:
            response_text = self._format_healthcare_info(healthcare_providers)
        
        return {
            "agent": self.agent_id,
            "type": "healthcare_request",
            "content": response_text,
            "providers_count": len(healthcare_providers),
            "timestamp": datetime.now().isoformat()
        }
    
    async def _handle_status_request(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle status update requests."""
        # Generate status update
        status_info = self._generate_status_update(context)
        
        # Determine who to send update to
        update_recipients = self._get_status_update_recipients()
        
        response_text = self._format_status_response(status_info, update_recipients)
        
        # Send status update to family
        await self._send_status_update(status_info, update_recipients)
        
        return {
            "agent": self.agent_id,
            "type": "status_request",
            "content": response_text,
            "status_info": status_info,
            "recipients_count": len(update_recipients),
            "timestamp": datetime.now().isoformat()
        }
    
    async def _handle_support_request(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle support requests."""
        # Determine support type needed
        support_type = self._identify_support_type(content)
        
        # Get appropriate support contacts
        support_contacts = self._get_support_contacts(support_type)
        
        response_text = self._format_support_response(support_contacts, support_type)
        
        return {
            "agent": self.agent_id,
            "type": "support_request",
            "content": response_text,
            "support_type": support_type,
            "contacts_count": len(support_contacts),
            "timestamp": datetime.now().isoformat()
        }
    
    async def _handle_general_communication_support(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle general communication support requests."""
        response_text = self._provide_general_communication_support(content)
        
        return {
            "agent": self.agent_id,
            "type": "general_communication",
            "content": response_text,
            "timestamp": datetime.now().isoformat()
        }
    
    def _identify_call_target(self, content: str) -> str:
        """Identify who the user wants to call."""
        if any(keyword in content for keyword in ["family", "son", "daughter", "spouse", "wife", "husband"]):
            return "family"
        elif any(keyword in content for keyword in ["doctor", "nurse", "medical"]):
            return "healthcare"
        elif any(keyword in content for keyword in ["emergency", "help", "911"]):
            return "emergency"
        else:
            return "general"
    
    def _identify_support_type(self, content: str) -> str:
        """Identify the type of support needed."""
        if any(keyword in content for keyword in ["medical", "health", "doctor"]):
            return "medical"
        elif any(keyword in content for keyword in ["emotional", "lonely", "sad"]):
            return "emotional"
        elif any(keyword in content for keyword in ["practical", "help", "assistance"]):
            return "practical"
        else:
            return "general"
    
    def _extract_message_info(self, content: str) -> Dict[str, Any]:
        """Extract message information from content."""
        # Simple extraction - in a real system, this would use NLP
        message_info = {
            "content": content,
            "recipient_type": "family",
            "urgency": "normal"
        }
        
        if any(keyword in content for keyword in ["urgent", "emergency", "important"]):
            message_info["urgency"] = "high"
        
        if any(keyword in content for keyword in ["doctor", "medical", "healthcare"]):
            message_info["recipient_type"] = "healthcare"
        
        return message_info
    
    def _get_contacts_for_call(self, call_target: str) -> List[Dict[str, Any]]:
        """Get contacts for calling based on target."""
        contacts = []
        
        if call_target == "family":
            contacts = [contact for contact in self.communication_database["family_members"] 
                       if contact.get("active", True)]
        elif call_target == "healthcare":
            contacts = [contact for contact in self.communication_database["healthcare_providers"] 
                       if contact.get("active", True)]
        elif call_target == "emergency":
            contacts = [contact for contact in self.communication_database["family_members"] 
                       if contact.get("priority") == "high"]
        
        return contacts
    
    def _get_message_recipients(self, recipient_type: str) -> List[Dict[str, Any]]:
        """Get message recipients based on type."""
        recipients = []
        
        if recipient_type == "family":
            recipients = [contact for contact in self.communication_database["family_members"] 
                         if contact.get("active", True)]
        elif recipient_type == "healthcare":
            recipients = [contact for contact in self.communication_database["healthcare_providers"] 
                         if contact.get("active", True)]
        
        return recipients
    
    def _get_family_members(self) -> List[Dict[str, Any]]:
        """Get family members information."""
        return [contact for contact in self.communication_database["family_members"] 
                if contact.get("active", True)]
    
    def _get_healthcare_providers(self) -> List[Dict[str, Any]]:
        """Get healthcare providers information."""
        return [contact for contact in self.communication_database["healthcare_providers"] 
                if contact.get("active", True)]
    
    def _get_status_update_recipients(self) -> List[Dict[str, Any]]:
        """Get recipients for status updates."""
        return [contact for contact in self.communication_database["family_members"] 
                if contact.get("wants_updates", True)]
    
    def _get_support_contacts(self, support_type: str) -> List[Dict[str, Any]]:
        """Get support contacts based on type."""
        contacts = []
        
        if support_type == "medical":
            contacts = [contact for contact in self.communication_database["healthcare_providers"] 
                       if contact.get("active", True)]
        elif support_type == "emotional":
            contacts = [contact for contact in self.communication_database["family_members"] 
                       if contact.get("relationship") in ["spouse", "child", "sibling"]]
        else:
            contacts = [contact for contact in self.communication_database["family_members"] 
                       if contact.get("active", True)]
        
        return contacts
    
    def _generate_status_update(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a status update based on current context."""
        current_time = datetime.now()
        
        status_info = {
            "timestamp": current_time.isoformat(),
            "user_mood": context.get("mood", "neutral"),
            "recent_activities": context.get("recent_interactions", [])[-3:],  # Last 3 interactions
            "safety_status": "safe",
            "medication_status": "on_track",
            "overall_wellbeing": "good"
        }
        
        return status_info
    
    def _format_call_response(self, contacts: List[Dict[str, Any]], call_target: str) -> str:
        """Format call response message."""
        if not contacts:
            return f"I don't have contact information for {call_target} right now."
        
        response = f"📞 CALLING {call_target.upper()} 📞\n\n"
        response += "I can help you call:\n\n"
        
        for contact in contacts[:3]:  # Limit to 3 contacts
            response += f"• {contact.get('name', 'Contact')}\n"
            response += f"  Phone: {contact.get('phone', 'No phone')}\n"
            if contact.get('relationship'):
                response += f"  Relationship: {contact['relationship']}\n"
            response += "\n"
        
        response += "I'm initiating the call now."
        return response
    
    def _format_no_contacts_response(self, call_target: str) -> str:
        """Format no contacts response message."""
        return f"I don't have contact information for {call_target} right now. Try calling 911 for emergencies."
    
    def _format_message_response(self, message_info: Dict[str, Any], recipients: List[Dict[str, Any]]) -> str:
        """Format message response message."""
        if not recipients:
            return "I don't have contact information for sending messages right now."
        
        response = "📱 SENDING MESSAGE 📱\n\n"
        response += f"Message: {message_info['content']}\n\n"
        response += f"Sending to {len(recipients)} recipient(s):\n"
        
        for recipient in recipients[:3]:  # Limit to 3 recipients
            response += f"• {recipient.get('name', 'Contact')}\n"
        
        response += "\nMessage sent successfully."
        return response
    
    def _format_no_recipients_response(self, recipient_type: str) -> str:
        """Format no recipients response message."""
        return f"I don't have contact information for {recipient_type} right now."
    
    def _format_family_info(self, family_members: List[Dict[str, Any]]) -> str:
        """Format family information message."""
        if not family_members:
            return "I don't have family information available right now."
        
        response = "👨‍👩‍👧‍👦 YOUR FAMILY 👨‍👩‍👧‍👦\n\n"
        
        for member in family_members:
            response += f"• {member.get('name', 'Family Member')}\n"
            response += f"  Relationship: {member.get('relationship', 'Unknown')}\n"
            if member.get('phone'):
                response += f"  Phone: {member['phone']}\n"
            if member.get('location'):
                response += f"  Location: {member['location']}\n"
            response += "\n"
        
        return response
    
    def _format_family_call_options(self, family_members: List[Dict[str, Any]]) -> str:
        """Format family call options message."""
        if not family_members:
            return "I don't have family contact information available right now."
        
        response = "📞 FAMILY CALL OPTIONS 📞\n\n"
        response += "I can help you call:\n\n"
        
        for member in family_members:
            response += f"• {member.get('name', 'Family Member')} ({member.get('relationship', 'Unknown')})\n"
            if member.get('phone'):
                response += f"  Phone: {member['phone']}\n"
            response += "\n"
        
        response += "Who would you like to call?"
        return response
    
    def _format_general_family_response(self, family_members: List[Dict[str, Any]]) -> str:
        """Format general family response message."""
        if not family_members:
            return "I don't have family information available right now."
        
        return f"Your family includes {len(family_members)} members. I can help you contact them or get more information about them."
    
    def _format_healthcare_contact_options(self, providers: List[Dict[str, Any]]) -> str:
        """Format healthcare contact options message."""
        if not providers:
            return "I don't have healthcare provider information available right now."
        
        response = "🏥 HEALTHCARE CONTACTS 🏥\n\n"
        response += "I can help you contact:\n\n"
        
        for provider in providers:
            response += f"• {provider.get('name', 'Healthcare Provider')}\n"
            response += f"  Type: {provider.get('type', 'Unknown')}\n"
            if provider.get('phone'):
                response += f"  Phone: {provider['phone']}\n"
            response += "\n"
        
        response += "Who would you like to contact?"
        return response
    
    def _format_appointment_info(self, providers: List[Dict[str, Any]]) -> str:
        """Format appointment information message."""
        if not providers:
            return "I don't have healthcare provider information available right now."
        
        response = "📅 APPOINTMENT INFORMATION 📅\n\n"
        response += "Your healthcare providers:\n\n"
        
        for provider in providers:
            response += f"• {provider.get('name', 'Healthcare Provider')}\n"
            if provider.get('next_appointment'):
                response += f"  Next appointment: {provider['next_appointment']}\n"
            response += "\n"
        
        return response
    
    def _format_healthcare_info(self, providers: List[Dict[str, Any]]) -> str:
        """Format healthcare information message."""
        if not providers:
            return "I don't have healthcare provider information available right now."
        
        response = "🏥 YOUR HEALTHCARE TEAM 🏥\n\n"
        
        for provider in providers:
            response += f"• {provider.get('name', 'Healthcare Provider')}\n"
            response += f"  Type: {provider.get('type', 'Unknown')}\n"
            if provider.get('specialty'):
                response += f"  Specialty: {provider['specialty']}\n"
            response += "\n"
        
        return response
    
    def _format_status_response(self, status_info: Dict[str, Any], recipients: List[Dict[str, Any]]) -> str:
        """Format status response message."""
        response = "📊 STATUS UPDATE 📊\n\n"
        response += f"Current status: {status_info.get('overall_wellbeing', 'Unknown')}\n"
        response += f"Mood: {status_info.get('user_mood', 'Unknown')}\n"
        response += f"Safety status: {status_info.get('safety_status', 'Unknown')}\n"
        response += f"Medication status: {status_info.get('medication_status', 'Unknown')}\n\n"
        response += f"Status update sent to {len(recipients)} family members."
        
        return response
    
    def _format_support_response(self, support_contacts: List[Dict[str, Any]], support_type: str) -> str:
        """Format support response message."""
        if not support_contacts:
            return f"I don't have {support_type} support contacts available right now."
        
        response = f"🤝 {support_type.upper()} SUPPORT 🤝\n\n"
        response += "I can connect you with:\n\n"
        
        for contact in support_contacts:
            response += f"• {contact.get('name', 'Support Contact')}\n"
            if contact.get('phone'):
                response += f"  Phone: {contact['phone']}\n"
            if contact.get('specialty'):
                response += f"  Specialty: {contact['specialty']}\n"
            response += "\n"
        
        response += "Who would you like to contact for support?"
        return response
    
    def _provide_general_communication_support(self, content: str) -> str:
        """Provide general communication support."""
        responses = [
            "I'm here to help you communicate with your family and caregivers. What do you need?",
            "I can help you make calls, send messages, or get in touch with your support network. How can I help?",
            "Your family and caregivers are important. I'm here to help you stay connected. What would you like to do?",
            "Communication is important for your wellbeing. I can help you reach out to the right people. What do you need?"
        ]
        
        # Simple response selection based on content
        if "help" in content:
            return responses[0]
        elif "call" in content or "message" in content:
            return responses[1]
        elif "family" in content:
            return responses[2]
        else:
            return responses[3]
    
    def _log_call_request(self, call_target: str, contacts: List[Dict[str, Any]]):
        """Log call request."""
        call_log = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "target": call_target,
            "contacts_requested": len(contacts),
            "status": "initiated"
        }
        self.communication_database["recent_calls"].append(call_log)
    
    def _log_message(self, message_info: Dict[str, Any], recipients: List[Dict[str, Any]]):
        """Log message."""
        message_log = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "content": message_info["content"],
            "recipients": len(recipients),
            "urgency": message_info["urgency"]
        }
        self.communication_database["messages"].append(message_log)
    
    async def _send_status_update(self, status_info: Dict[str, Any], recipients: List[Dict[str, Any]]):
        """Send status update to family members."""
        # In a real system, this would send actual notifications
        print(f"📊 Sending status update to {len(recipients)} family members")
        print(f"Status: {status_info.get('overall_wellbeing', 'Unknown')}")
        print(f"Mood: {status_info.get('user_mood', 'Unknown')}")
    
    def _initialize_default_communication_data(self):
        """Initialize default communication data."""
        # Add default family members
        self.communication_database["family_members"] = [
            {
                "id": "family_001",
                "name": "Sarah (Daughter)",
                "relationship": "daughter",
                "phone": "(555) 123-4567",
                "email": "sarah@email.com",
                "location": "New York",
                "priority": "high",
                "wants_updates": True,
                "active": True
            },
            {
                "id": "family_002",
                "name": "John (Son)",
                "relationship": "son",
                "phone": "(555) 234-5678",
                "email": "john@email.com",
                "location": "California",
                "priority": "high",
                "wants_updates": True,
                "active": True
            }
        ]
        
        # Add default healthcare providers
        self.communication_database["healthcare_providers"] = [
            {
                "id": "health_001",
                "name": "Dr. Smith",
                "type": "primary_care",
                "specialty": "Geriatrics",
                "phone": "(555) 987-6543",
                "email": "dr.smith@clinic.com",
                "next_appointment": "Next Tuesday at 2:00 PM",
                "active": True
            },
            {
                "id": "health_002",
                "name": "Nurse Johnson",
                "type": "nurse",
                "specialty": "Home Care",
                "phone": "(555) 876-5432",
                "email": "nurse.johnson@clinic.com",
                "active": True
            }
        ]
    
    def add_family_member(self, member_data: Dict[str, Any]):
        """Add a new family member."""
        member_data["id"] = str(uuid.uuid4())
        member_data["active"] = True
        self.communication_database["family_members"].append(member_data)
    
    def add_healthcare_provider(self, provider_data: Dict[str, Any]):
        """Add a new healthcare provider."""
        provider_data["id"] = str(uuid.uuid4())
        provider_data["active"] = True
        self.communication_database["healthcare_providers"].append(provider_data)
