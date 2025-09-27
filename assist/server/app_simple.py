"""
Simplified FastAPI backend for Messenger AI Assistant
This version works without complex dependencies
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio
import logging
from typing import Dict, List
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Mock service classes for simplified testing
class MockMemoryStore:
    def __init__(self):
        self.memories = []
        self.utterances = []
    
    async def initialize(self):
        pass
    
    async def store_utterance(self, utterance):
        self.utterances.append(utterance)
        return True
    
    async def store_memory(self, memory):
        self.memories.append(memory)
        return True
    
    async def search_memories(self, query, limit=10):
        return self.memories[:limit]
    
    async def get_statistics(self, user_id):
        return {
            "total_memories": len(self.memories),
            "total_utterances": len(self.utterances),
            "total_relationships": 0,
            "last_updated": "2024-01-01T00:00:00Z"
        }

class MockGeminiLive:
    def __init__(self):
        self.is_connected = True
    
    async def connect(self):
        self.is_connected = True
    
    async def send_audio(self, audio_data):
        return {"transcript": "Mock transcript", "confidence": 0.95}
    
    async def disconnect(self):
        self.is_connected = False

class MockADKOrchestrator:
    def __init__(self):
        self.is_running = True
    
    async def start(self):
        self.is_running = True
    
    async def stop(self):
        self.is_running = False
    
    async def process_utterance(self, utterance):
        return {"processed": True, "summary": "Mock processing complete"}

class MockWebSocketIngest:
    def __init__(self):
        self.connections = []
    
    async def handle_connection(self, websocket):
        self.connections.append(websocket)
        return True
    
    async def process_data(self, data):
        return {"status": "processed", "size": len(data)}

class MockReviveAPI:
    def __init__(self):
        self.memories = [
            {"id": "1", "text": "Sample conversation about project planning", "timestamp": "2024-01-01T00:00:00Z", "relevance": 0.95},
            {"id": "2", "text": "Discussion about meeting schedule", "timestamp": "2024-01-01T00:01:00Z", "relevance": 0.87},
            {"id": "3", "text": "Budget allocation discussion", "timestamp": "2024-01-01T00:02:00Z", "relevance": 0.92}
        ]
    
    async def initialize(self):
        pass
    
    async def revive_memories(self, cue, limit=10):
        # Simple keyword matching for demo
        relevant_memories = []
        for memory in self.memories:
            if any(word.lower() in memory["text"].lower() for word in cue.split()):
                relevant_memories.append(memory)
        
        return {
            "cue": cue,
            "memories": relevant_memories[:limit],
            "summary": f"Found {len(relevant_memories)} memories related to '{cue}'",
            "total_found": len(relevant_memories)
        }

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
    allow_origins=["chrome-extension://*", "http://localhost:*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
websocket_ingest = None
gemini_live = None
adk_orchestrator = None
memory_store = None
revive_api = None

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global websocket_ingest, gemini_live, adk_orchestrator, memory_store, revive_api
    
    try:
        logger.info("Starting simplified backend...")
        
        # Initialize mock services for testing
        memory_store = MockMemoryStore()
        gemini_live = MockGeminiLive()
        adk_orchestrator = MockADKOrchestrator()
        websocket_ingest = MockWebSocketIngest()
        revive_api = MockReviveAPI()
        
        logger.info("All services initialized successfully (simplified mode)")
        
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        # Continue with limited functionality

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down backend...")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "services": {
            "memory_store": memory_store is not None and hasattr(memory_store, 'memories'),
            "gemini_live": gemini_live is not None and hasattr(gemini_live, 'is_connected'),
            "adk_orchestrator": adk_orchestrator is not None and hasattr(adk_orchestrator, 'is_running'),
            "websocket_ingest": websocket_ingest is not None and hasattr(websocket_ingest, 'connections'),
            "revive_api": revive_api is not None and hasattr(revive_api, 'memories')
        }
    }

# WebSocket endpoint for audio/video ingest
@app.websocket("/ingest")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for receiving audio/video data from Chrome extension"""
    await websocket.accept()
    logger.info("WebSocket connection established")
    
    # Register connection with WebSocket ingest
    if websocket_ingest:
        await websocket_ingest.handle_connection(websocket)
    
    try:
        while True:
            # Receive data from client
            data = await websocket.receive_bytes()
            logger.info(f"Received {len(data)} bytes of data")
            
            # Process data through mock services
            if websocket_ingest:
                result = await websocket_ingest.process_data(data)
                
                # Simulate processing through ADK orchestrator
                if adk_orchestrator:
                    await adk_orchestrator.process_utterance({
                        "text": "Mock processed audio",
                        "timestamp": "2024-01-01T00:00:00Z"
                    })
                
                # Store in memory
                if memory_store:
                    await memory_store.store_utterance({
                        "text": "Mock utterance from audio",
                        "timestamp": "2024-01-01T00:00:00Z"
                    })
            
            # Echo back confirmation with processing results
            await websocket.send_text(json.dumps({
                "status": "received",
                "size": len(data),
                "processed": True,
                "transcript": "Mock transcript from audio processing"
            }))
            
    except WebSocketDisconnect:
        logger.info("WebSocket connection closed")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.close()

# Revive API endpoint
@app.post("/revive")
async def revive_memories(request: dict):
    """Revive memories based on a cue"""
    try:
        cue = request.get("cue", "")
        limit = request.get("limit", 10)
        
        # Use mock revive API
        if revive_api:
            result = await revive_api.revive_memories(cue, limit)
            return result
        else:
            # Fallback response
            return {
                "cue": cue,
                "memories": [],
                "summary": f"No revive API available",
                "total_found": 0
            }
        
    except Exception as e:
        logger.error(f"Revive API error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Memory statistics endpoint
@app.get("/memories/{user_id}/statistics")
async def get_memory_statistics(user_id: str):
    """Get memory statistics for a user"""
    if memory_store:
        stats = await memory_store.get_statistics(user_id)
        return {
            "user_id": user_id,
            **stats
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
        "text": "Sample memory",
        "timestamp": "2024-01-01T00:00:00Z",
        "user_id": "default"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
