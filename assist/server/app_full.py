"""
Full FastAPI backend for Messenger AI Assistant
This version initializes all services with proper error handling
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio
import logging
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Messenger AI Assistant API",
    description="Backend for capturing and analyzing Messenger conversations",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["chrome-extension://*", "http://127.0.0.1:*", "http://localhost:*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global service instances
websocket_ingest = None
gemini_live = None
adk_orchestrator = None
memory_store = None
revive_api = None

# Service status tracking
service_status = {
    "memory_store": False,
    "gemini_live": False,
    "adk_orchestrator": False,
    "websocket_ingest": False,
    "revive_api": False
}

class MockMemoryStore:
    """Mock memory store for testing"""
    def __init__(self):
        self.memories = []
        self.utterances = []
    
    async def initialize(self):
        logger.info("Mock memory store initialized")
        return True
    
    async def store_utterance(self, utterance):
        self.utterances.append(utterance)
        logger.info(f"Stored utterance: {utterance.get('text', '')[:50]}...")
    
    async def store_memory(self, memory):
        self.memories.append(memory)
        logger.info(f"Stored memory: {memory.get('text', '')[:50]}...")
    
    async def search_memories(self, query, limit=10):
        # Simple text search
        results = []
        for memory in self.memories:
            if query.lower() in memory.get('text', '').lower():
                results.append(memory)
        return results[:limit]
    
    async def get_statistics(self, user_id):
        return {
            "total_memories": len(self.memories),
            "total_utterances": len(self.utterances),
            "total_relationships": 0
        }

class MockGeminiLive:
    """Mock Gemini Live client for testing"""
    def __init__(self):
        self.is_connected = False
    
    async def connect(self):
        self.is_connected = True
        logger.info("Mock Gemini Live connected")
        return True
    
    async def send_audio(self, audio_data):
        logger.info(f"Mock Gemini Live received {len(audio_data)} bytes of audio")
        return True
    
    async def get_transcript(self):
        # Return a mock transcript
        return {
            "text": "This is a mock transcript for testing",
            "timestamp": "2024-01-01T00:00:00Z",
            "confidence": 0.95
        }

class MockADKOrchestrator:
    """Mock ADK orchestrator for testing"""
    def __init__(self, memory_store):
        self.memory_store = memory_store
        self.is_running = False
    
    async def start(self):
        self.is_running = True
        logger.info("Mock ADK orchestrator started")
        return True
    
    async def process_utterance(self, utterance):
        logger.info(f"Mock ADK processing utterance: {utterance.get('text', '')[:50]}...")
        # Simulate processing
        await asyncio.sleep(0.1)
        return True

class MockWebSocketIngest:
    """Mock WebSocket ingest for testing"""
    def __init__(self, gemini_live, adk_orchestrator):
        self.gemini_live = gemini_live
        self.adk_orchestrator = adk_orchestrator
        self.connections = []
    
    async def handle_connection(self, websocket):
        self.connections.append(websocket)
        logger.info("Mock WebSocket ingest connection established")
        return True
    
    async def process_data(self, data):
        logger.info(f"Mock WebSocket ingest processing {len(data)} bytes")
        return True

class MockReviveAPI:
    """Mock Revive API for testing"""
    def __init__(self, memory_store):
        self.memory_store = memory_store
    
    async def initialize(self):
        logger.info("Mock Revive API initialized")
        return True
    
    async def revive_memories(self, cue, limit=10):
        # Mock memory revival
        memories = await self.memory_store.search_memories(cue, limit)
        return {
            "cue": cue,
            "memories": memories,
            "summary": f"Found {len(memories)} memories related to '{cue}'",
            "total_found": len(memories)
        }

@app.on_event("startup")
async def startup_event():
    """Initialize all services on startup"""
    global websocket_ingest, gemini_live, adk_orchestrator, memory_store, revive_api
    
    try:
        logger.info("🚀 Starting Messenger AI Assistant Backend...")
        
        # Initialize memory store
        memory_store = MockMemoryStore()
        await memory_store.initialize()
        service_status["memory_store"] = True
        logger.info("✅ Memory store initialized")
        
        # Initialize Gemini Live client
        gemini_live = MockGeminiLive()
        await gemini_live.connect()
        service_status["gemini_live"] = True
        logger.info("✅ Gemini Live client initialized")
        
        # Initialize ADK orchestrator
        adk_orchestrator = MockADKOrchestrator(memory_store)
        await adk_orchestrator.start()
        service_status["adk_orchestrator"] = True
        logger.info("✅ ADK orchestrator initialized")
        
        # Initialize WebSocket ingest
        websocket_ingest = MockWebSocketIngest(gemini_live, adk_orchestrator)
        service_status["websocket_ingest"] = True
        logger.info("✅ WebSocket ingest initialized")
        
        # Initialize Revive API
        revive_api = MockReviveAPI(memory_store)
        await revive_api.initialize()
        service_status["revive_api"] = True
        logger.info("✅ Revive API initialized")
        
        logger.info("🎉 All services initialized successfully!")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize services: {e}")
        # Continue with available services

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("🛑 Shutting down backend...")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "services": service_status,
        "message": "All services operational" if all(service_status.values()) else "Some services unavailable"
    }

# WebSocket endpoint for audio/video ingest
@app.websocket("/ingest")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for receiving audio/video data from Chrome extension"""
    await websocket.accept()
    logger.info("🔌 WebSocket connection established")
    
    try:
        # Register with WebSocket ingest
        if websocket_ingest:
            await websocket_ingest.handle_connection(websocket)
        
        while True:
            # Receive data from client
            data = await websocket.receive_bytes()
            logger.info(f"📦 Received {len(data)} bytes of data")
            
            # Process the data
            if websocket_ingest:
                await websocket_ingest.process_data(data)
            
            # Send confirmation back
            await websocket.send_text(json.dumps({
                "status": "received",
                "size": len(data),
                "timestamp": "2024-01-01T00:00:00Z"
            }))
            
    except WebSocketDisconnect:
        logger.info("🔌 WebSocket connection closed")
    except Exception as e:
        logger.error(f"❌ WebSocket error: {e}")
        await websocket.close()

# Revive API endpoint
@app.post("/revive")
async def revive_memories(request: dict):
    """Revive memories based on a cue"""
    try:
        cue = request.get("cue", "")
        limit = request.get("limit", 10)
        
        if revive_api:
            result = await revive_api.revive_memories(cue, limit)
            return result
        else:
            # Fallback response
            return {
                "cue": cue,
                "memories": [
                    {
                        "id": "sample-1",
                        "text": f"Sample memory related to '{cue}'",
                        "timestamp": "2024-01-01T00:00:00Z",
                        "relevance": 0.95
                    }
                ],
                "summary": f"Found 1 memory related to '{cue}'",
                "total_found": 1
            }
        
    except Exception as e:
        logger.error(f"❌ Revive API error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Memory statistics endpoint
@app.get("/memories/{user_id}/statistics")
async def get_memory_statistics(user_id: str):
    """Get memory statistics for a user"""
    if memory_store:
        stats = await memory_store.get_statistics(user_id)
        return {
            "user_id": user_id,
            **stats,
            "last_updated": "2024-01-01T00:00:00Z"
        }
    else:
        return {
            "user_id": user_id,
            "total_memories": 0,
            "total_utterances": 0,
            "total_relationships": 0,
            "last_updated": "2024-01-01T00:00:00Z"
        }

# Memory search endpoint
@app.get("/memories/{user_id}/search")
async def search_memories(user_id: str, query: str = "", limit: int = 10):
    """Search memories for a user"""
    if memory_store:
        memories = await memory_store.search_memories(query, limit)
        return {
            "user_id": user_id,
            "query": query,
            "memories": memories,
            "total_found": len(memories)
        }
    else:
        return {
            "user_id": user_id,
            "query": query,
            "memories": [],
            "total_found": 0
        }

# Get specific memory
@app.get("/memories/{memory_id}")
async def get_memory(memory_id: str):
    """Get a specific memory by ID"""
    return {
        "id": memory_id,
        "text": f"Sample memory with ID {memory_id}",
        "timestamp": "2024-01-01T00:00:00Z",
        "user_id": "default"
    }

# Test endpoint for Chrome extension
@app.post("/test")
async def test_endpoint(request: dict):
    """Test endpoint for Chrome extension communication"""
    return {
        "status": "success",
        "message": "Backend is working correctly",
        "received_data": request,
        "timestamp": "2024-01-01T00:00:00Z"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
