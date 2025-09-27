# Run using python3 assist/agents/adk_agents.py

import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import os

from google.cloud import firestore
from datetime import datetime

from agent_tools.tools import store_insights

from google.adk.agents import Agent

logger = logging.getLogger(__name__)


# -------------------------------
# Video Parser and Agent Orchestrator
# -------------------------------


class ADKOrchestrator:
    """ADK Orchestrator for managing agents and memory bank"""

    def __init__(self, location: str = "us-central1"):
        self.location = location
        self.data = None
        self.agents = {}
        self.is_running = False
        self.processing_queue = asyncio.Queue()
        self.id = 0
        self.insights = {
            "face": {"face_id": "", "embedding": [], "timestamp": ""},
            "location": "",
            "summary": "",
        }

    async def initialize(self):
        """Initialize the orchestrator"""
        try:
            # Initialize
            self.is_running = True
            logger.info("ADK Orchestrator initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize ADK Orchestrator: {e}")
            raise

    async def start(self):
        """Start the orchestrator"""
        if not self.is_running:
            await self.initialize()

        # Pull from Firestore DB packaged images (this may be already split up into just face sections)
        TestData = {
            "face": {
                "face_id": "face1",
                "timestamp": "2025-09-27T16:00:00Z",
                "bbox": [100, 50, 150, 100],
                "embedding": [0.12, 0.93, ...],
            },
            "audio_uri": "gs://bucket/vid123_audio.wav",
            "location": "Sample Location",
        }
        test_id = self.id
        self.id += 1

        # Call tool to split audio and images (process data function below) (TODO May not need)

        # Initialize agents (here use A2A) passing images and audio out

        res = await ctx.send_task(
            target="video_agent",
            task="face_detection",
            payload={"video_" + str(test_id): TestData["face"]},
        )

        self.insights["face"] = res  # Store face insights

        res = await ctx.send_task(
            target="audio_agent",
            task="process_audio",
            payload={"audio_" + str(test_id): TestData["audio_uri"]},
        )

        self.insights["summary"] = res  # Store audio insights

        # Call function to save location and other relevant data to output FirsestorDB that agents also send results too
        self.insights["location"] = TestData["location"]
        store_insights(self.insights)
        self.insights = {}  # reset for next

        # Start next processing loop once above finishes (TODO)
        asyncio.create_task(self._processing_loop())
        logger.info("ADK Orchestrator started")

    async def stop(self):
        """Stop the orchestrator"""
        self.is_running = False

        # Stop all agents
        for agent in self.agents.values():
            await agent.stop()

        logger.info("ADK Orchestrator stopped")

    async def _processing_loop(self):
        """Main processing loop that will call next batch of data"""
        while self.is_running:
            try:
                # Get next item from database
                # Set self.data equal to this

                # Process through pipeline
                await self.start()

            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error in processing loop: {e}")

    async def get_memories(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get memories from the memory bank"""
        if self.memory_bank:
            return await self.memory_bank.retrieve_memories(query, limit)
        return []

    async def store_memory(self, memory: Dict[str, Any]) -> str:
        """Store a memory in the memory bank"""
        if self.memory_bank:
            return await self.memory_bank.store_memory(memory)
        return ""


# Agent Setup:
# Have Data from Meta Glasses to Firestore
# For very video we call main agent
# Main Agent gets Video from firestore and puts in MemoryBank
# Main Agent then calls sub agents BUT uses A2A and instead only passes only the specific filtered data from the MemoryBank
# NOTE: For Video we just pass video, audio we can just pass audio, each agent only gets what they need
# Then instead of using classes which each need their own memory bank, we use those primary big agents and then call the other small single purpose agents as tools and treat them like functions.
# Finally we take all that data and change that MemoryWriterAgent to just a tool that uploads memories.

# -------------------------------
# Agent Template
# -------------------------------


class ADKAgent:
    """Base ADK Agent class"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.is_running = False
        self.agent = None

    async def initialize(self):
        """Initialize the agent"""
        self.is_running = True
        logger.info(f"Agent {self.name} initialized")

    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process data and return results"""
        raise NotImplementedError("Subclasses must implement process method")

    async def stop(self):
        """Stop the agent"""
        self.is_running = False
        logger.info(f"Agent {self.name} stopped")


# -------------------------------
# Agents
# -------------------------------


class VideoAgent(ADKAgent):
    """Agent for processing video data"""

    def __init__(self, name: str = "VideoAgent"):
        self.name = name
        self.agent = Agent(name="video_agent")

    async def initialize(self):
        await super().initialize()
        # Initialize video processing model or resources
        logger.info("Video agent initialized")

    def register_tasks(self):
        # Register a task for face detection
        @self.agent.task(name="face_detection")
        async def face_detection(ctx: Context, video_id: str):

            # Call your existing processing function
            result = await self.process(video_frames)

            return result

    async def process(self, video_frames: List[Any]) -> Dict[str, Any]:
        # Your actual face detection / video processing logic
        return {
            "message": "Processed video frames",
            "count": len(video_frames),
            "faces": [{"id": "face1"}, {"id": "face2"}],
            "timestamp": datetime.utcnow().isoformat(),
        }


class AudioAgent(ADKAgent):
    """Audio processing agent exposed via ADK Agent tasks."""

    def __init__(self, memory=None):
        self.agent = Agent(name="audio_agent", memory=memory)
        self.register_tasks()
        self.agent = Agent(name="audio_agent")

    def register_tasks(self):
        @self.agent.task(name="process_audio")
        async def process_audio(ctx: Context, video_id: str):
            # Call your existing processing function
            result = await self.process(video_frames)

            return result

    async def process(self, audio_frames: List[float]) -> Dict[str, Any]:
        # Stub: replace with real transcription / audio analysis
        return {"message": "Processed audio frames", "count": len(audio_frames)}


orchestrator = ADKOrchestrator()
orchestrator.initialize()
orchestrator.start()
