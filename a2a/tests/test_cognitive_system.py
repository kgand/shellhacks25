#!/usr/bin/env python3
"""
Test suite for the Cognitive Assistance System
"""

import unittest
import asyncio
import sys
from pathlib import Path

# Add the backend directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from cognitive_assistance_system import CognitiveAssistant
from cognitive_assistance_system.a2a_integration import A2ACognitiveIntegration
from cognitive_assistance_system.agents.memory_agent import MemoryAssistanceAgent
from cognitive_assistance_system.agents.routine_agent import RoutineManagementAgent
from cognitive_assistance_system.agents.safety_agent import SafetyMonitoringAgent
from cognitive_assistance_system.agents.communication_agent import FamilyCommunicationAgent

class TestCognitiveAssistant(unittest.TestCase):
    """Test the main cognitive assistant"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.assistant = CognitiveAssistant("test_user_123")
    
    def test_initialization(self):
        """Test assistant initialization"""
        self.assertEqual(self.assistant.user_id, "test_user_123")
        self.assertIsNotNone(self.assistant.session_id)
        self.assertIsNotNone(self.assistant.memory_agent)
        self.assertIsNotNone(self.assistant.routine_agent)
        self.assertIsNotNone(self.assistant.safety_agent)
        self.assertIsNotNone(self.assistant.communication_agent)
    
    def test_user_profile_management(self):
        """Test user profile operations"""
        # Test initial profile
        profile = self.assistant.get_user_profile()
        self.assertIn("name", profile)
        self.assertIn("age", profile)
        self.assertIn("stage", profile)
        
        # Test profile update
        new_profile = {
            "name": "Test User",
            "age": 75,
            "stage": "moderate"
        }
        self.assistant.update_user_profile(new_profile)
        updated_profile = self.assistant.get_user_profile()
        self.assertEqual(updated_profile["name"], "Test User")
        self.assertEqual(updated_profile["age"], 75)
    
    async def test_process_user_input(self):
        """Test user input processing"""
        # Test memory request
        input_data = {
            "type": "text",
            "content": "I forgot who my daughter is"
        }
        response = await self.assistant.process_user_input(input_data)
        self.assertIn("agent", response)
        self.assertIn("content", response)
        self.assertIn("timestamp", response)
    
    def test_session_summary(self):
        """Test session summary generation"""
        summary = self.assistant.get_session_summary()
        self.assertIn("session_id", summary)
        self.assertIn("user_id", summary)
        self.assertIn("started_at", summary)
        self.assertIn("duration_minutes", summary)

class TestMemoryAgent(unittest.TestCase):
    """Test the memory assistance agent"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.agent = MemoryAssistanceAgent("test_user_123")
    
    async def test_memory_prompt_handling(self):
        """Test memory prompt processing"""
        input_data = {
            "type": "text",
            "content": "I remember playing in the backyard as a child"
        }
        context = {"time_of_day": "14:00", "mood": "nostalgic"}
        
        response = await self.agent.process_request(input_data, context)
        self.assertEqual(response["agent"], "memory_assistance")
        self.assertIn("content", response)
    
    def test_memory_database_operations(self):
        """Test memory database operations"""
        # Test adding memory
        memory_data = {
            "type": "childhood",
            "description": "Playing in the backyard",
            "date": "1950s",
            "importance": "high"
        }
        self.agent.add_memory(memory_data)
        
        # Test family member update
        family_data = {
            "name": "Sarah",
            "relationship": "daughter",
            "age": "45"
        }
        self.agent.update_family_member(family_data)

class TestRoutineAgent(unittest.TestCase):
    """Test the routine management agent"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.agent = RoutineManagementAgent("test_user_123")
    
    async def test_medication_requests(self):
        """Test medication-related requests"""
        input_data = {
            "type": "text",
            "content": "What medicine do I need to take?"
        }
        context = {"time_of_day": "08:00"}
        
        response = await self.agent.process_request(input_data, context)
        self.assertEqual(response["agent"], "routine_management")
        self.assertIn("content", response)
    
    def test_medication_management(self):
        """Test medication management"""
        # Test adding medication
        medication_data = {
            "name": "Test Medication",
            "dosage": "1 tablet",
            "scheduled_time": "08:00",
            "instructions": "Take with breakfast"
        }
        self.agent.add_medication(medication_data)
        
        # Test adding appointment
        appointment_data = {
            "doctor_name": "Dr. Smith",
            "date": "2024-01-15",
            "time": "14:00",
            "location": "Medical Center"
        }
        self.agent.add_appointment(appointment_data)

class TestSafetyAgent(unittest.TestCase):
    """Test the safety monitoring agent"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.agent = SafetyMonitoringAgent("test_user_123")
    
    async def test_emergency_handling(self):
        """Test emergency request handling"""
        input_data = {
            "type": "text",
            "content": "I need help! I fell down!"
        }
        context = {"time_of_day": "15:30", "location": "home"}
        
        response = await self.agent.process_request(input_data, context)
        self.assertEqual(response["agent"], "safety_monitoring")
        self.assertIn("content", response)
    
    def test_emergency_contact_management(self):
        """Test emergency contact management"""
        # Test adding emergency contact
        contact_data = {
            "name": "Emergency Contact",
            "phone": "911",
            "type": "emergency",
            "priority": "critical"
        }
        self.agent.add_emergency_contact(contact_data)
        
        # Test medical info update
        medical_data = {
            "conditions": ["Alzheimer's Disease"],
            "medications": ["Donepezil"],
            "allergies": ["None"]
        }
        self.agent.update_medical_info(medical_data)

class TestCommunicationAgent(unittest.TestCase):
    """Test the family communication agent"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.agent = FamilyCommunicationAgent("test_user_123")
    
    async def test_call_requests(self):
        """Test call request handling"""
        input_data = {
            "type": "text",
            "content": "I want to call my daughter"
        }
        context = {"time_of_day": "10:00"}
        
        response = await self.agent.process_request(input_data, context)
        self.assertEqual(response["agent"], "family_communication")
        self.assertIn("content", response)
    
    def test_contact_management(self):
        """Test contact management"""
        # Test adding family member
        family_data = {
            "name": "Sarah",
            "relationship": "daughter",
            "phone": "(555) 123-4567",
            "email": "sarah@email.com"
        }
        self.agent.add_family_member(family_data)
        
        # Test adding healthcare provider
        provider_data = {
            "name": "Dr. Smith",
            "type": "primary_care",
            "specialty": "Geriatrics",
            "phone": "(555) 987-6543"
        }
        self.agent.add_healthcare_provider(provider_data)

class TestA2AIntegration(unittest.TestCase):
    """Test the A2A ADK integration"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.integration = A2ACognitiveIntegration("test_user_123")
    
    def test_initialization(self):
        """Test integration initialization"""
        self.assertEqual(self.integration.user_id, "test_user_123")
        self.assertIsNotNone(self.integration.cognitive_assistant)
        self.assertIsNotNone(self.integration.a2a_config)
    
    def test_a2a_config(self):
        """Test A2A configuration"""
        config = self.integration.get_a2a_config()
        self.assertIn("systemPrompt", config)
        self.assertIn("voice", config)
        self.assertIn("googleSearch", config)
        self.assertIn("allowInterruptions", config)
    
    async def test_multimodal_processing(self):
        """Test multimodal input processing"""
        input_data = {
            "type": "text",
            "content": "Hello, I need help remembering something"
        }
        
        response = await self.integration.process_multimodal_input(input_data)
        self.assertIn("text", response)
        self.assertIn("agent", response)
        self.assertIn("timestamp", response)
    
    def test_session_management(self):
        """Test session management"""
        summary = self.integration.get_session_summary()
        self.assertIn("session_id", summary)
        self.assertIn("user_id", summary)
        self.assertIn("start_time", summary)
        self.assertIn("metrics", summary)

def run_async_test(test_func):
    """Helper to run async tests"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(test_func())
    finally:
        loop.close()

# Add async test methods to test classes
TestCognitiveAssistant.test_process_user_input = run_async_test(TestCognitiveAssistant.test_process_user_input)
TestMemoryAgent.test_memory_prompt_handling = run_async_test(TestMemoryAgent.test_memory_prompt_handling)
TestRoutineAgent.test_medication_requests = run_async_test(TestRoutineAgent.test_medication_requests)
TestSafetyAgent.test_emergency_handling = run_async_test(TestSafetyAgent.test_emergency_handling)
TestCommunicationAgent.test_call_requests = run_async_test(TestCommunicationAgent.test_call_requests)
TestA2AIntegration.test_multimodal_processing = run_async_test(TestA2AIntegration.test_multimodal_processing)

if __name__ == "__main__":
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestCognitiveAssistant,
        TestMemoryAgent,
        TestRoutineAgent,
        TestSafetyAgent,
        TestCommunicationAgent,
        TestA2AIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
