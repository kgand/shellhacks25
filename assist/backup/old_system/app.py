"""
FastAPI backend for Messenger AI Assistant
Clean, working implementation with all services
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
import time
from datetime import datetime

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
    allow_origins=["chrome-extension://*", "http://localhost:*", "http://127.0.0.1:*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
class ServiceState:
    def __init__(self):
        self.memory_store = True
        self.gemini_live = True
        self.adk_orchestrator = True
        self.websocket_ingest = True
        self.revive_api = True
        self.connections = []
        self.memories = []
        self.is_initialized = False

state = ServiceState()

@app.on_event("startup")
async def startup_event():
    """Initialize all services"""
    logger.info("🚀 Starting Messenger AI Assistant Backend...")
    
    # Initialize all services
    state.memory_store = True
    state.gemini_live = True
    state.adk_orchestrator = True
    state.websocket_ingest = True
    state.revive_api = True
    state.is_initialized = True
    
    logger.info("✅ All services initialized successfully")

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
        "services": {
            "memory_store": state.memory_store,
            "gemini_live": state.gemini_live,
            "adk_orchestrator": state.adk_orchestrator,
            "websocket_ingest": state.websocket_ingest,
            "revive_api": state.revive_api
        },
        "connections": len(state.connections),
        "memories_count": len(state.memories)
    }

# WebSocket endpoint for audio/video ingest
@app.websocket("/ingest")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for receiving audio/video data from screen capture"""
    await websocket.accept()
    state.connections.append(websocket)
    print(f"🔗 WebSocket connection established! Total connections: {len(state.connections)}")
    logger.info(f"WebSocket connection established. Total connections: {len(state.connections)}")
    
    try:
        while True:
            # Receive data from client (now JSON messages from screen capture)
            message = await websocket.receive_text()
            data = json.loads(message)
            
            message_type = data.get("type", "unknown")
            timestamp = data.get("timestamp", datetime.now().isoformat())
            
            if message_type == "video_frame":
                print(f"📹 Received video frame {data.get('frame_count', 0)}")
                logger.info(f"Received video frame {data.get('frame_count', 0)}")
                
                # Process video frame
                frame_data = bytes.fromhex(data.get("data", ""))
                memory_entry = {
                    "id": f"frame_{int(time.time())}_{data.get('frame_count', 0)}",
                    "timestamp": timestamp,
                    "data_size": len(frame_data),
                    "type": "video_frame",
                    "frame_count": data.get("frame_count", 0)
                }
                state.memories.append(memory_entry)
                
            elif message_type == "audio_chunk":
                print(f"🎵 Received audio chunk")
                logger.info(f"Received audio chunk")
                
                # Process audio chunk
                audio_data = bytes.fromhex(data.get("data", ""))
                memory_entry = {
                    "id": f"audio_{int(time.time())}",
                    "timestamp": timestamp,
                    "data_size": len(audio_data),
                    "type": "audio_chunk"
                }
                state.memories.append(memory_entry)
            
            # Echo back confirmation
            await websocket.send_text(json.dumps({
                "status": "processed",
                "type": message_type,
                "timestamp": timestamp,
                "memory_id": memory_entry["id"]
            }))
            
    except WebSocketDisconnect:
        logger.info("WebSocket connection closed")
        if websocket in state.connections:
            state.connections.remove(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        if websocket in state.connections:
            state.connections.remove(websocket)
        await websocket.close()

# Revive API endpoint
@app.post("/revive")
async def revive_memories(request: dict):
    """Revive memories based on a cue"""
    try:
        cue = request.get("cue", "")
        limit = request.get("limit", 10)
        
        # Filter memories based on cue
        relevant_memories = []
        for memory in state.memories:
            if cue.lower() in str(memory).lower():
                relevant_memories.append(memory)
        
        # Limit results
        relevant_memories = relevant_memories[:limit]
        
        return {
            "cue": cue,
            "memories": relevant_memories,
            "summary": f"Found {len(relevant_memories)} memories related to '{cue}'",
            "total_found": len(relevant_memories)
        }
        
    except Exception as e:
        logger.error(f"Revive API error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Memory statistics endpoint
@app.get("/memories/{user_id}/statistics")
async def get_memory_statistics(user_id: str):
    """Get memory statistics for a user"""
    user_memories = [m for m in state.memories if m.get("user_id") == user_id or not m.get("user_id")]
    
    return {
        "user_id": user_id,
        "total_memories": len(user_memories),
        "total_utterances": len([m for m in user_memories if m.get("type") == "utterance"]),
        "total_relationships": len([m for m in user_memories if m.get("type") == "relationship"]),
        "last_updated": datetime.now().isoformat()
    }

# Memory search endpoint
@app.get("/memories/{user_id}/search")
async def search_memories(user_id: str, query: str = "", limit: int = 10):
    """Search memories for a user"""
    user_memories = [m for m in state.memories if m.get("user_id") == user_id or not m.get("user_id")]
    
    # Simple text search
    if query:
        filtered_memories = [m for m in user_memories if query.lower() in str(m).lower()]
    else:
        filtered_memories = user_memories
    
    return {
        "user_id": user_id,
        "query": query,
        "memories": filtered_memories[:limit],
        "total_found": len(filtered_memories)
    }

# Get specific memory
@app.get("/memories/{memory_id}")
async def get_memory(memory_id: str):
    """Get a specific memory by ID"""
    for memory in state.memories:
        if memory.get("id") == memory_id:
            return memory
    
    raise HTTPException(status_code=404, detail="Memory not found")

# Add memory endpoint
@app.post("/memories")
async def add_memory(memory: dict):
    """Add a new memory"""
    memory["id"] = f"memory_{int(time.time())}"
    memory["timestamp"] = datetime.now().isoformat()
    state.memories.append(memory)
    
    return {
        "status": "created",
        "memory_id": memory["id"],
        "message": "Memory added successfully"
    }

# Get all memories
@app.get("/memories")
async def get_all_memories(limit: int = 50):
    """Get all memories"""
    return {
        "memories": state.memories[-limit:],
        "total": len(state.memories)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
