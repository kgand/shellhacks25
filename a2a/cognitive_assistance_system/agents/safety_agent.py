"""
Safety Monitoring Agent

This agent specializes in safety monitoring and emergency assistance
for individuals with Alzheimer's disease, including fall detection,
wandering prevention, and emergency response.
"""

import json
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import asyncio

class SafetyMonitoringAgent:
    """
    Specialized agent for safety monitoring and emergency assistance.
    Provides fall detection, wandering alerts, emergency contacts,
    and safety reminders.
    """
    
    def __init__(self, user_id: str):
        """
        Initialize the safety monitoring agent.
        
        Args:
            user_id: Unique identifier for the user
        """
        self.user_id = user_id
        self.agent_id = "safety_monitoring"
        
        # Safety database structure
        self.safety_database = {
            "emergency_contacts": [],
            "medical_info": {},
            "safety_rules": [],
            "location_history": [],
            "incident_reports": [],
            "safety_reminders": []
        }
        
        # Safety monitoring settings
        self.safety_settings = {
            "fall_detection_enabled": True,
            "wandering_alerts_enabled": True,
            "location_tracking_enabled": True,
            "emergency_auto_dial": True,
            "safety_check_interval": 30  # minutes
        }
        
        # Emergency response protocols
        self.emergency_protocols = {
            "fall_detected": {
                "immediate_response": "Check if user is responsive",
                "escalation_time": 5,  # minutes
                "contacts_to_notify": ["primary_caregiver", "emergency_services"]
            },
            "wandering_detected": {
                "immediate_response": "Alert caregivers and provide location",
                "escalation_time": 10,  # minutes
                "contacts_to_notify": ["family", "neighbors"]
            },
            "medical_emergency": {
                "immediate_response": "Call emergency services",
                "escalation_time": 1,  # minutes
                "contacts_to_notify": ["emergency_services", "medical_contacts"]
            }
        }
        
        # Initialize with default safety data
        self._initialize_default_safety_data()
    
    async def process_request(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process safety-related requests and provide appropriate assistance.
        
        Args:
            input_data: User input data
            context: Current session context
            
        Returns:
            Response from the safety monitoring agent
        """
        try:
            content = input_data.get("content", "").lower()
            input_type = input_data.get("type", "text")
            
            # Determine the type of safety assistance needed
            if any(keyword in content for keyword in ["help", "emergency", "911", "call"]):
                return await self._handle_emergency_request(content, context)
            elif any(keyword in content for keyword in ["lost", "where am i", "location", "home"]):
                return await self._handle_location_request(content, context)
            elif any(keyword in content for keyword in ["fall", "hurt", "pain", "injured"]):
                return await self._handle_fall_incident(content, context)
            elif any(keyword in content for keyword in ["safe", "danger", "scared", "afraid"]):
                return await self._handle_safety_concern(content, context)
            elif any(keyword in content for keyword in ["contact", "family", "call someone"]):
                return await self._handle_contact_request(content, context)
            elif any(keyword in content for keyword in ["medicine", "medical", "doctor", "hospital"]):
                return await self._handle_medical_request(content, context)
            else:
                return await self._handle_general_safety_support(content, context)
                
        except Exception as e:
            return {
                "agent": self.agent_id,
                "error": True,
                "message": f"Error in safety monitoring: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    async def _handle_emergency_request(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle emergency requests."""
        # Determine emergency type
        emergency_type = self._identify_emergency_type(content)
        
        # Get appropriate emergency contacts
        emergency_contacts = self._get_emergency_contacts(emergency_type)
        
        # Format emergency response
        response_text = self._format_emergency_response(emergency_type, emergency_contacts)
        
        # Log the emergency
        self._log_emergency_incident(emergency_type, content)
        
        return {
            "agent": self.agent_id,
            "type": "emergency",
            "content": response_text,
            "emergency_type": emergency_type,
            "contacts_notified": len(emergency_contacts),
            "timestamp": datetime.now().isoformat()
        }
    
    async def _handle_location_request(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle location and navigation requests."""
        # Get current location information
        current_location = self._get_current_location()
        home_location = self._get_home_location()
        
        # Determine if user is lost or needs directions
        if "lost" in content or "where am i" in content:
            response_text = self._format_location_help(current_location, home_location)
        elif "home" in content:
            response_text = self._format_directions_home(current_location, home_location)
        else:
            response_text = self._format_location_info(current_location)
        
        return {
            "agent": self.agent_id,
            "type": "location",
            "content": response_text,
            "current_location": current_location,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _handle_fall_incident(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle fall incident reports."""
        # Assess fall severity
        fall_severity = self._assess_fall_severity(content)
        
        # Get appropriate response based on severity
        if fall_severity == "severe":
            response_text = self._format_severe_fall_response()
            # Trigger emergency protocol
            await self._trigger_emergency_protocol("fall_detected")
        else:
            response_text = self._format_minor_fall_response()
        
        # Log the incident
        self._log_fall_incident(fall_severity, content)
        
        return {
            "agent": self.agent_id,
            "type": "fall_incident",
            "content": response_text,
            "fall_severity": fall_severity,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _handle_safety_concern(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle general safety concerns."""
        # Identify safety concern type
        concern_type = self._identify_safety_concern(content)
        
        # Get appropriate safety guidance
        safety_guidance = self._get_safety_guidance(concern_type)
        
        response_text = self._format_safety_guidance(safety_guidance, concern_type)
        
        return {
            "agent": self.agent_id,
            "type": "safety_concern",
            "content": response_text,
            "concern_type": concern_type,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _handle_contact_request(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle requests to contact family or caregivers."""
        # Determine who to contact
        contact_type = self._identify_contact_type(content)
        
        # Get appropriate contacts
        contacts = self._get_contacts_by_type(contact_type)
        
        response_text = self._format_contact_response(contacts, contact_type)
        
        return {
            "agent": self.agent_id,
            "type": "contact_request",
            "content": response_text,
            "contact_type": contact_type,
            "contacts_available": len(contacts),
            "timestamp": datetime.now().isoformat()
        }
    
    async def _handle_medical_request(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle medical-related requests."""
        # Get medical information
        medical_info = self._get_medical_information()
        
        # Determine medical need
        medical_need = self._identify_medical_need(content)
        
        if medical_need == "emergency":
            response_text = self._format_medical_emergency_response()
            await self._trigger_emergency_protocol("medical_emergency")
        else:
            response_text = self._format_medical_info_response(medical_info, medical_need)
        
        return {
            "agent": self.agent_id,
            "type": "medical",
            "content": response_text,
            "medical_need": medical_need,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _handle_general_safety_support(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle general safety support requests."""
        response_text = self._provide_general_safety_support(content)
        
        return {
            "agent": self.agent_id,
            "type": "general_safety",
            "content": response_text,
            "timestamp": datetime.now().isoformat()
        }
    
    def _identify_emergency_type(self, content: str) -> str:
        """Identify the type of emergency."""
        if any(keyword in content for keyword in ["medical", "heart", "chest", "breathing"]):
            return "medical"
        elif any(keyword in content for keyword in ["fire", "smoke", "burn"]):
            return "fire"
        elif any(keyword in content for keyword in ["intruder", "stranger", "break in"]):
            return "security"
        else:
            return "general"
    
    def _identify_safety_concern(self, content: str) -> str:
        """Identify the type of safety concern."""
        if any(keyword in content for keyword in ["dark", "night", "scared"]):
            return "environmental"
        elif any(keyword in content for keyword in ["stranger", "unknown", "suspicious"]):
            return "security"
        elif any(keyword in content for keyword in ["stairs", "floor", "slippery"]):
            return "physical"
        else:
            return "general"
    
    def _identify_contact_type(self, content: str) -> str:
        """Identify the type of contact needed."""
        if any(keyword in content for keyword in ["family", "son", "daughter", "spouse"]):
            return "family"
        elif any(keyword in content for keyword in ["doctor", "medical", "nurse"]):
            return "medical"
        elif any(keyword in content for keyword in ["neighbor", "friend", "help"]):
            return "community"
        else:
            return "emergency"
    
    def _identify_medical_need(self, content: str) -> str:
        """Identify the medical need."""
        if any(keyword in content for keyword in ["emergency", "urgent", "severe", "pain"]):
            return "emergency"
        elif any(keyword in content for keyword in ["medicine", "medication", "pill"]):
            return "medication"
        elif any(keyword in content for keyword in ["appointment", "doctor", "visit"]):
            return "appointment"
        else:
            return "general"
    
    def _get_emergency_contacts(self, emergency_type: str) -> List[Dict[str, Any]]:
        """Get emergency contacts based on type."""
        contacts = []
        
        for contact in self.safety_database["emergency_contacts"]:
            if contact.get("active", True):
                if emergency_type == "medical" and contact.get("type") == "medical":
                    contacts.append(contact)
                elif emergency_type == "general" and contact.get("priority") == "high":
                    contacts.append(contact)
                elif contact.get("type") == "emergency":
                    contacts.append(contact)
        
        return contacts
    
    def _get_current_location(self) -> Dict[str, Any]:
        """Get current location information."""
        # This would typically integrate with GPS or location services
        return {
            "address": "123 Main Street, Anytown, USA",
            "coordinates": {"lat": 40.7128, "lng": -74.0060},
            "landmarks": ["Near the park", "Across from the library"],
            "safety_status": "safe"
        }
    
    def _get_home_location(self) -> Dict[str, Any]:
        """Get home location information."""
        return {
            "address": "456 Home Street, Anytown, USA",
            "coordinates": {"lat": 40.7589, "lng": -73.9851},
            "landmarks": ["Blue house with white shutters", "Next to the big oak tree"],
            "directions": "Turn left at the corner, go two blocks, house on the right"
        }
    
    def _assess_fall_severity(self, content: str) -> str:
        """Assess the severity of a fall incident."""
        if any(keyword in content for keyword in ["can't move", "bleeding", "severe pain", "unconscious"]):
            return "severe"
        elif any(keyword in content for keyword in ["hurt", "pain", "bruise"]):
            return "moderate"
        else:
            return "minor"
    
    def _get_safety_guidance(self, concern_type: str) -> Dict[str, Any]:
        """Get safety guidance based on concern type."""
        guidance_map = {
            "environmental": {
                "title": "Environmental Safety",
                "tips": [
                    "Turn on lights in dark areas",
                    "Use night lights in hallways",
                    "Keep pathways clear of obstacles"
                ]
            },
            "security": {
                "title": "Security Safety",
                "tips": [
                    "Don't open the door to strangers",
                    "Call family or emergency services if needed",
                    "Stay in a safe, well-lit area"
                ]
            },
            "physical": {
                "title": "Physical Safety",
                "tips": [
                    "Use handrails on stairs",
                    "Wear non-slip shoes",
                    "Take your time when walking"
                ]
            }
        }
        
        return guidance_map.get(concern_type, {
            "title": "General Safety",
            "tips": [
                "Stay calm and take deep breaths",
                "Call for help if you need it",
                "You are safe and help is available"
            ]
        })
    
    def _get_contacts_by_type(self, contact_type: str) -> List[Dict[str, Any]]:
        """Get contacts by type."""
        contacts = []
        
        for contact in self.safety_database["emergency_contacts"]:
            if contact.get("type") == contact_type and contact.get("active", True):
                contacts.append(contact)
        
        return contacts
    
    def _get_medical_information(self) -> Dict[str, Any]:
        """Get medical information."""
        return self.safety_database.get("medical_info", {
            "conditions": ["Alzheimer's Disease"],
            "medications": ["Donepezil", "Memantine"],
            "allergies": ["None known"],
            "emergency_contact": "Dr. Smith - (555) 123-4567"
        })
    
    def _format_emergency_response(self, emergency_type: str, contacts: List[Dict[str, Any]]) -> str:
        """Format emergency response message."""
        if emergency_type == "medical":
            response = "🚨 MEDICAL EMERGENCY DETECTED 🚨\n\n"
            response += "I'm calling emergency services immediately.\n"
            response += "Stay calm and try to stay still.\n\n"
        else:
            response = "🚨 EMERGENCY ASSISTANCE 🚨\n\n"
            response += "I'm here to help you. Let me contact the right people.\n\n"
        
        if contacts:
            response += "I'm notifying:\n"
            for contact in contacts:
                response += f"• {contact.get('name', 'Contact')} - {contact.get('phone', 'No phone')}\n"
        
        response += "\nHelp is on the way. You're not alone."
        return response
    
    def _format_location_help(self, current_location: Dict[str, Any], home_location: Dict[str, Any]) -> str:
        """Format location help message."""
        response = "📍 LOCATION ASSISTANCE 📍\n\n"
        response += f"You are currently at: {current_location.get('address', 'Unknown location')}\n"
        
        if current_location.get('landmarks'):
            response += f"Nearby landmarks: {', '.join(current_location['landmarks'])}\n"
        
        response += f"\nYour home is at: {home_location.get('address', 'Unknown')}\n"
        response += f"Directions home: {home_location.get('directions', 'Ask for help')}\n\n"
        response += "You're safe. Take your time getting home."
        return response
    
    def _format_directions_home(self, current_location: Dict[str, Any], home_location: Dict[str, Any]) -> str:
        """Format directions home message."""
        response = "🏠 DIRECTIONS HOME 🏠\n\n"
        response += f"Your home is at: {home_location.get('address', 'Unknown')}\n"
        response += f"Directions: {home_location.get('directions', 'Ask for help')}\n\n"
        response += "Take your time and be safe."
        return response
    
    def _format_location_info(self, location: Dict[str, Any]) -> str:
        """Format location information message."""
        response = "📍 YOUR LOCATION 📍\n\n"
        response += f"You are at: {location.get('address', 'Unknown location')}\n"
        
        if location.get('landmarks'):
            response += f"Landmarks: {', '.join(location['landmarks'])}\n"
        
        response += f"Safety status: {location.get('safety_status', 'Unknown')}"
        return response
    
    def _format_severe_fall_response(self) -> str:
        """Format severe fall response message."""
        response = "🚨 FALL DETECTED - SEVERE 🚨\n\n"
        response += "I'm calling emergency services immediately.\n"
        response += "Try to stay still and don't move if you're in pain.\n"
        response += "Help is on the way.\n\n"
        response += "Emergency services: 911"
        return response
    
    def _format_minor_fall_response(self) -> str:
        """Format minor fall response message."""
        response = "⚠️ FALL DETECTED ⚠️\n\n"
        response += "Are you okay? Can you move?\n"
        response += "If you're hurt, I can call for help.\n"
        response += "Take your time getting up safely.\n\n"
        response += "Let me know if you need assistance."
        return response
    
    def _format_safety_guidance(self, guidance: Dict[str, Any], concern_type: str) -> str:
        """Format safety guidance message."""
        response = f"🛡️ {guidance.get('title', 'Safety Guidance')} 🛡️\n\n"
        response += "Here are some safety tips:\n\n"
        
        for tip in guidance.get('tips', []):
            response += f"• {tip}\n"
        
        response += "\nYou're safe. Take your time and be careful."
        return response
    
    def _format_contact_response(self, contacts: List[Dict[str, Any]], contact_type: str) -> str:
        """Format contact response message."""
        if not contacts:
            return "I don't have contact information available right now. Try calling 911 for emergencies."
        
        response = f"📞 {contact_type.title()} CONTACTS 📞\n\n"
        
        for contact in contacts:
            response += f"• {contact.get('name', 'Contact')}\n"
            response += f"  Phone: {contact.get('phone', 'No phone')}\n"
            if contact.get('relationship'):
                response += f"  Relationship: {contact['relationship']}\n"
            response += "\n"
        
        response += "I can help you call any of these contacts."
        return response
    
    def _format_medical_emergency_response(self) -> str:
        """Format medical emergency response message."""
        response = "🚨 MEDICAL EMERGENCY 🚨\n\n"
        response += "I'm calling emergency services immediately.\n"
        response += "Stay calm and try to stay still.\n"
        response += "Help is on the way.\n\n"
        response += "Emergency: 911"
        return response
    
    def _format_medical_info_response(self, medical_info: Dict[str, Any], medical_need: str) -> str:
        """Format medical information response message."""
        response = "🏥 MEDICAL INFORMATION 🏥\n\n"
        
        if medical_need == "medication":
            response += "Your medications:\n"
            for med in medical_info.get('medications', []):
                response += f"• {med}\n"
        elif medical_need == "appointment":
            response += "Your next medical appointment information is available.\n"
        else:
            response += "Your medical information:\n"
            response += f"Conditions: {', '.join(medical_info.get('conditions', []))}\n"
            response += f"Allergies: {', '.join(medical_info.get('allergies', []))}\n"
        
        response += f"\nEmergency contact: {medical_info.get('emergency_contact', 'Not available')}"
        return response
    
    def _provide_general_safety_support(self, content: str) -> str:
        """Provide general safety support."""
        responses = [
            "I'm here to keep you safe. What do you need help with?",
            "Your safety is my priority. How can I help you?",
            "I'm monitoring your safety. Is everything okay?",
            "I'm here to help you stay safe. What's concerning you?"
        ]
        
        # Simple response selection based on content
        if "help" in content:
            return responses[0]
        elif "safe" in content:
            return responses[1]
        elif "okay" in content:
            return responses[2]
        else:
            return responses[3]
    
    def _log_emergency_incident(self, emergency_type: str, content: str):
        """Log emergency incident."""
        incident = {
            "id": str(uuid.uuid4()),
            "type": emergency_type,
            "timestamp": datetime.now().isoformat(),
            "description": content,
            "severity": "high"
        }
        self.safety_database["incident_reports"].append(incident)
    
    def _log_fall_incident(self, severity: str, content: str):
        """Log fall incident."""
        incident = {
            "id": str(uuid.uuid4()),
            "type": "fall",
            "severity": severity,
            "timestamp": datetime.now().isoformat(),
            "description": content
        }
        self.safety_database["incident_reports"].append(incident)
    
    async def _trigger_emergency_protocol(self, protocol_type: str):
        """Trigger emergency protocol."""
        protocol = self.emergency_protocols.get(protocol_type, {})
        
        # Log the protocol activation
        print(f"🚨 EMERGENCY PROTOCOL ACTIVATED: {protocol_type}")
        print(f"Immediate response: {protocol.get('immediate_response', 'Unknown')}")
        print(f"Escalation time: {protocol.get('escalation_time', 0)} minutes")
        print(f"Contacts to notify: {protocol.get('contacts_to_notify', [])}")
    
    def _initialize_default_safety_data(self):
        """Initialize default safety data."""
        # Add default emergency contacts
        self.safety_database["emergency_contacts"] = [
            {
                "id": "contact_001",
                "name": "Sarah (Daughter)",
                "phone": "(555) 123-4567",
                "type": "family",
                "priority": "high",
                "active": True
            },
            {
                "id": "contact_002",
                "name": "Dr. Smith",
                "phone": "(555) 987-6543",
                "type": "medical",
                "priority": "high",
                "active": True
            },
            {
                "id": "contact_003",
                "name": "Emergency Services",
                "phone": "911",
                "type": "emergency",
                "priority": "critical",
                "active": True
            }
        ]
        
        # Add default medical information
        self.safety_database["medical_info"] = {
            "conditions": ["Alzheimer's Disease", "High Blood Pressure"],
            "medications": ["Donepezil", "Lisinopril"],
            "allergies": ["Penicillin"],
            "emergency_contact": "Dr. Smith - (555) 987-6543"
        }
    
    def add_emergency_contact(self, contact_data: Dict[str, Any]):
        """Add a new emergency contact."""
        contact_data["id"] = str(uuid.uuid4())
        contact_data["active"] = True
        self.safety_database["emergency_contacts"].append(contact_data)
    
    def update_medical_info(self, medical_data: Dict[str, Any]):
        """Update medical information."""
        self.safety_database["medical_info"].update(medical_data)
