"""
Cognitive Assistance System for Alzheimer's Support

This package provides a comprehensive AI-powered assistance system designed
to help individuals with Alzheimer's disease and their caregivers. The system
includes specialized agents for memory assistance, routine management, safety
monitoring, and family communication.
"""

from .core_assistant import CognitiveAssistant
from .agents.memory_agent import MemoryAssistanceAgent
from .agents.routine_agent import RoutineManagementAgent
from .agents.safety_agent import SafetyMonitoringAgent
from .agents.communication_agent import FamilyCommunicationAgent

__version__ = "1.0.0"
__author__ = "Cognitive Assistance Team"

__all__ = [
    "CognitiveAssistant",
    "MemoryAssistanceAgent", 
    "RoutineManagementAgent",
    "SafetyMonitoringAgent",
    "FamilyCommunicationAgent"
]
