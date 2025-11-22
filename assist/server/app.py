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
from revive_api import ReviveAPI
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
revive_api = None

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global websocket_ingest, gemini_live, adk_orchestrator, memory_store, revive_api
    
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
        
        # Initialize Revive API
        revive_api = ReviveAPI(memory_store)
        await revive_api.initialize()
        
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
            "websocket_ingest": websocket_ingest is not None,
            "revive_api": revive_api is not None
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
        if not revive_api:
            raise HTTPException(status_code=503, detail="Revive API not initialized")
        
        # Use the Revive API to process the request
        result = await revive_api.revive_memories(
            cue=request.cue,
            user_id=request.user_id or "default",
            limit=request.limit or 10
        )
        
        return ReviveResponse(
            cue=result['cue'],
            memories=result['memories'],
            recap=result['recap'],
            count=result['count']
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
        if not revive_api:
            raise HTTPException(status_code=503, detail="Revive API not initialized")
        
        success = await revive_api.delete_memory(memory_id)
        if success:
            return {"message": "Memory deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Memory not found")
            
    except Exception as e:
        logger.error(f"Failed to delete memory: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/memories/{user_id}/statistics")
async def get_memory_statistics(user_id: str):
    """Get memory statistics for a user"""
    try:
        if not revive_api:
            raise HTTPException(status_code=503, detail="Revive API not initialized")
        
        statistics = await revive_api.get_memory_statistics(user_id)
        return statistics
        
    except Exception as e:
        logger.error(f"Failed to get memory statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/memories/{user_id}/search")
async def search_memories(user_id: str, query: str, limit: int = 20):
    """Search memories with advanced filtering"""
    try:
        if not revive_api:
            raise HTTPException(status_code=503, detail="Revive API not initialized")
        
        results = await revive_api.search_memories(query, user_id, limit)
        return {
            "query": query,
            "results": results,
            "count": len(results)
        }
        
    except Exception as e:
        logger.error(f"Failed to search memories: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
