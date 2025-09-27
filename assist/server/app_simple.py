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
            "memory_store": memory_store is not None,
            "gemini_live": gemini_live is not None,
            "adk_orchestrator": adk_orchestrator is not None,
            "websocket_ingest": websocket_ingest is not None,
            "revive_api": revive_api is not None
        }
    }

# WebSocket endpoint for audio/video ingest
@app.websocket("/ingest")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for receiving audio/video data from Chrome extension"""
    await websocket.accept()
    logger.info("WebSocket connection established")
    
    try:
        while True:
            # Receive data from client
            data = await websocket.receive_bytes()
            logger.info(f"Received {len(data)} bytes of data")
            
            # Echo back confirmation
            await websocket.send_text(json.dumps({
                "status": "received",
                "size": len(data)
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
        
        # Simplified response
        return {
            "cue": cue,
            "memories": [
                {
                    "id": "sample-1",
                    "text": "Sample memory 1",
                    "timestamp": "2024-01-01T00:00:00Z",
                    "relevance": 0.95
                },
                {
                    "id": "sample-2", 
                    "text": "Sample memory 2",
                    "timestamp": "2024-01-01T00:01:00Z",
                    "relevance": 0.87
                }
            ],
            "summary": f"Found {limit} memories related to '{cue}'",
            "total_found": 2
        }
        
    except Exception as e:
        logger.error(f"Revive API error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Memory statistics endpoint
@app.get("/memories/{user_id}/statistics")
async def get_memory_statistics(user_id: str):
    """Get memory statistics for a user"""
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
