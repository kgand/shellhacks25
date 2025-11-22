"""
FastAPI backend for Messenger AI Assistant
Handles WebSocket ingest, Gemini Live integration, and memory management
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio
import logging
from typing import Dict, List
import os
from dotenv import load_dotenv

from ws_ingest import WebSocketIngest
from gemini_live import GeminiLiveClient
from adk_orchestrator import ADKOrchestrator
from memory.store_firestore import FirestoreMemoryStore
from models.schemas import ReviveRequest, ReviveResponse

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

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global websocket_ingest, gemini_live, adk_orchestrator, memory_store
    
    try:
        # Initialize memory store
        memory_store = FirestoreMemoryStore()
        await memory_store.initialize()
        
        # Initialize Gemini Live client
        gemini_live = GeminiLiveClient()
        
        # Initialize ADK orchestrator
        adk_orchestrator = ADKOrchestrator(memory_store)
        
        # Initialize WebSocket ingest
        websocket_ingest = WebSocketIngest(gemini_live, adk_orchestrator)
        
        logger.info("All services initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        raise

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "services": {
            "memory_store": memory_store is not None,
            "gemini_live": gemini_live is not None,
            "adk_orchestrator": adk_orchestrator is not None,
            "websocket_ingest": websocket_ingest is not None
        }
    }

@app.websocket("/ingest")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for receiving audio/video chunks from Chrome extension"""
    await websocket.accept()
    
    try:
        if websocket_ingest:
            await websocket_ingest.handle_connection(websocket)
        else:
            await websocket.close(code=1011, reason="Service not initialized")
            
    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.close(code=1011, reason="Internal server error")

@app.post("/revive", response_model=ReviveResponse)
async def revive_memories(request: ReviveRequest):
    """Retrieve and assemble memories based on a text cue"""
    try:
        if not memory_store:
            raise HTTPException(status_code=503, detail="Memory store not initialized")
        
        # Search for relevant memories
        memories = await memory_store.search_memories(
            query=request.cue,
            limit=request.limit or 10
        )
        
        # Generate stitched recap using Gemini
        if gemini_live:
            recap = await gemini_live.generate_recap(memories, request.cue)
        else:
            recap = "Memory service unavailable"
        
        return ReviveResponse(
            cue=request.cue,
            memories=memories,
            recap=recap,
            count=len(memories)
        )
        
    except Exception as e:
        logger.error(f"Failed to revive memories: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/memories/{user_id}")
async def get_user_memories(user_id: str, limit: int = 50):
    """Get recent memories for a specific user"""
    try:
        if not memory_store:
            raise HTTPException(status_code=503, detail="Memory store not initialized")
        
        memories = await memory_store.get_user_memories(user_id, limit)
        return {"user_id": user_id, "memories": memories, "count": len(memories)}
        
    except Exception as e:
        logger.error(f"Failed to get user memories: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/memories/{memory_id}")
async def delete_memory(memory_id: str):
    """Delete a specific memory"""
    try:
        if not memory_store:
            raise HTTPException(status_code=503, detail="Memory store not initialized")
        
        success = await memory_store.delete_memory(memory_id)
        if success:
            return {"message": "Memory deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Memory not found")
            
    except Exception as e:
        logger.error(f"Failed to delete memory: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
