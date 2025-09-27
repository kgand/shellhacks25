"""
Simplified FastAPI backend for file-based screen capture
No websockets, direct file handling
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import os
import time
import logging
from typing import Dict, List, Optional
from datetime import datetime
import json
import shutil
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app will be initialized with lifespan below

# Global state
class SimpleServiceState:
    def __init__(self):
        self.capture_sessions = {}
        self.uploaded_files = []
        self.is_initialized = False
        self.upload_dir = "uploads"
        self.output_dir = "processed"
        
        # Create directories
        os.makedirs(self.upload_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

state = SimpleServiceState()

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown"""
    # Startup
    logger.info("🚀 Starting Simple Screen Capture Backend...")
    state.is_initialized = True
    logger.info("✅ Backend initialized successfully")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down backend...")

# Add lifespan to app
app = FastAPI(
    title="Simple Screen Capture API",
    description="Backend for file-based screen capture system",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with system information"""
    return {
        "message": "Simple Screen Capture API",
        "version": "2.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "sessions": "/sessions",
            "files": "/files",
            "upload": "/upload/{session_id}",
            "process": "/process/{session_id}",
            "stats": "/stats"
        },
        "documentation": "Visit /docs for API documentation"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "services": {
            "file_upload": True,
            "file_processing": True,
            "session_management": True
        },
        "active_sessions": len(state.capture_sessions),
        "uploaded_files": len(state.uploaded_files)
    }

# Session management endpoints
@app.post("/sessions")
async def create_session(session_data: dict):
    """Create a new capture session"""
    try:
        session_id = f"session_{int(time.time())}"
        state.capture_sessions[session_id] = {
            "id": session_id,
            "created_at": datetime.now().isoformat(),
            "status": "active",
            "files": [],
            "metadata": session_data
        }
        
        logger.info(f"Created session: {session_id}")
        return {
            "session_id": session_id,
            "status": "created",
            "message": "Session created successfully"
        }
    except Exception as e:
        logger.error(f"Error creating session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sessions/{session_id}")
async def get_session(session_id: str):
    """Get session information"""
    if session_id not in state.capture_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return state.capture_sessions[session_id]

@app.get("/sessions")
async def list_sessions():
    """List all sessions"""
    return {
        "sessions": list(state.capture_sessions.values()),
        "total": len(state.capture_sessions)
    }

@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a session"""
    if session_id not in state.capture_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Clean up session files
    session = state.capture_sessions[session_id]
    for file_info in session.get("files", []):
        file_path = file_info.get("path")
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                logger.warning(f"Error deleting file {file_path}: {e}")
    
    del state.capture_sessions[session_id]
    logger.info(f"Deleted session: {session_id}")
    
    return {"status": "deleted", "message": "Session deleted successfully"}

# File upload endpoints
@app.post("/upload/{session_id}")
async def upload_file(session_id: str, file: UploadFile = File(...)):
    """Upload a file to a session"""
    if session_id not in state.capture_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    try:
        # Create session-specific directory
        session_dir = os.path.join(state.upload_dir, session_id)
        os.makedirs(session_dir, exist_ok=True)
        
        # Save file
        file_path = os.path.join(session_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Update session
        file_info = {
            "filename": file.filename,
            "path": file_path,
            "size": os.path.getsize(file_path),
            "uploaded_at": datetime.now().isoformat(),
            "type": file.content_type or "unknown"
        }
        
        state.capture_sessions[session_id]["files"].append(file_info)
        state.uploaded_files.append(file_info)
        
        logger.info(f"Uploaded file: {file.filename} to session {session_id}")
        
        return {
            "status": "uploaded",
            "filename": file.filename,
            "size": file_info["size"],
            "session_id": session_id
        }
        
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files/{session_id}")
async def list_session_files(session_id: str):
    """List files in a session"""
    if session_id not in state.capture_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "session_id": session_id,
        "files": state.capture_sessions[session_id]["files"],
        "total": len(state.capture_sessions[session_id]["files"])
    }

@app.get("/download/{session_id}/{filename}")
async def download_file(session_id: str, filename: str):
    """Download a file from a session"""
    if session_id not in state.capture_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = state.capture_sessions[session_id]
    file_info = None
    
    for file in session["files"]:
        if file["filename"] == filename:
            file_info = file
            break
    
    if not file_info:
        raise HTTPException(status_code=404, detail="File not found")
    
    file_path = file_info["path"]
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found on disk")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type=file_info.get("type", "application/octet-stream")
    )

# Processing endpoints
@app.post("/process/{session_id}")
async def process_session(session_id: str):
    """Process files in a session"""
    if session_id not in state.capture_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    try:
        session = state.capture_sessions[session_id]
        files = session["files"]
        
        # Create processed directory
        processed_dir = os.path.join(state.output_dir, session_id)
        os.makedirs(processed_dir, exist_ok=True)
        
        processed_files = []
        
        for file_info in files:
            file_path = file_info["path"]
            if os.path.exists(file_path):
                # Copy to processed directory
                processed_path = os.path.join(processed_dir, file_info["filename"])
                shutil.copy2(file_path, processed_path)
                
                processed_files.append({
                    "original": file_info,
                    "processed": processed_path,
                    "processed_at": datetime.now().isoformat()
                })
        
        # Update session status
        session["status"] = "processed"
        session["processed_files"] = processed_files
        
        logger.info(f"Processed session {session_id}: {len(processed_files)} files")
        
        return {
            "status": "processed",
            "session_id": session_id,
            "processed_files": len(processed_files),
            "message": "Session processed successfully"
        }
        
    except Exception as e:
        logger.error(f"Error processing session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Auto-process captured files endpoint
@app.post("/auto-process")
async def auto_process_captured_files():
    """Automatically process captured files from capture_output directory"""
    try:
        # Try multiple possible paths for capture_output
        possible_paths = [
            "../screen_capture/capture_output",
            "screen_capture/capture_output", 
            "capture_output",
            "../capture_output"
        ]
        
        capture_output_dir = None
        for path in possible_paths:
            if os.path.exists(path):
                capture_output_dir = path
                break
        
        if not capture_output_dir:
            raise HTTPException(status_code=404, detail="Capture output directory not found in any expected location")
        
        logger.info(f"Found capture output directory: {capture_output_dir}")
        
        # Create a new session for auto-processing
        session_id = f"auto_session_{int(time.time())}"
        state.capture_sessions[session_id] = {
            "id": session_id,
            "created_at": datetime.now().isoformat(),
            "status": "processing",
            "files": [],
            "metadata": {"type": "auto_processed", "source_dir": capture_output_dir}
        }
        
        # Find all captured files
        captured_files = []
        for filename in os.listdir(capture_output_dir):
            file_path = os.path.join(capture_output_dir, filename)
            if os.path.isfile(file_path):
                file_info = {
                    "filename": filename,
                    "path": file_path,
                    "size": os.path.getsize(file_path),
                    "uploaded_at": datetime.now().isoformat(),
                    "type": "image/jpeg" if filename.endswith('.jpg') else "audio/wav" if filename.endswith('.wav') else "unknown"
                }
                captured_files.append(file_info)
                state.capture_sessions[session_id]["files"].append(file_info)
        
        logger.info(f"Found {len(captured_files)} captured files to process")
        
        if not captured_files:
            return {
                "status": "no_files",
                "session_id": session_id,
                "processed_files": 0,
                "message": "No captured files found to process"
            }
        
        # Process the files
        processed_dir = os.path.join(state.output_dir, session_id)
        os.makedirs(processed_dir, exist_ok=True)
        
        processed_files = []
        for file_info in captured_files:
            file_path = file_info["path"]
            if os.path.exists(file_path):
                # Copy to processed directory
                processed_path = os.path.join(processed_dir, file_info["filename"])
                shutil.copy2(file_path, processed_path)
                
                processed_files.append({
                    "original": file_info,
                    "processed": processed_path,
                    "processed_at": datetime.now().isoformat()
                })
        
        # Update session status
        state.capture_sessions[session_id]["status"] = "processed"
        state.capture_sessions[session_id]["processed_files"] = processed_files
        
        logger.info(f"Auto-processed {len(processed_files)} captured files")
        
        return {
            "status": "processed",
            "session_id": session_id,
            "processed_files": len(processed_files),
            "message": f"Auto-processed {len(processed_files)} captured files successfully"
        }
        
    except Exception as e:
        logger.error(f"Error auto-processing captured files: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Manual trigger for processing captured files
@app.post("/trigger-process")
async def trigger_process_captured_files():
    """Manually trigger processing of captured files"""
    return await auto_process_captured_files()

# Statistics endpoints
@app.get("/stats")
async def get_statistics():
    """Get system statistics"""
    total_files = sum(len(session["files"]) for session in state.capture_sessions.values())
    total_size = 0
    
    for session in state.capture_sessions.values():
        for file_info in session["files"]:
            total_size += file_info.get("size", 0)
    
    return {
        "total_sessions": len(state.capture_sessions),
        "total_files": total_files,
        "total_size_bytes": total_size,
        "total_size_mb": round(total_size / (1024 * 1024), 2),
        "active_sessions": len([s for s in state.capture_sessions.values() if s["status"] == "active"]),
        "processed_sessions": len([s for s in state.capture_sessions.values() if s["status"] == "processed"])
    }

# Cleanup endpoints
@app.post("/cleanup")
async def cleanup_old_files():
    """Clean up old files and sessions"""
    try:
        current_time = time.time()
        cleanup_threshold = 24 * 60 * 60  # 24 hours
        
        cleaned_sessions = []
        cleaned_files = 0
        
        for session_id, session in list(state.capture_sessions.items()):
            session_time = datetime.fromisoformat(session["created_at"]).timestamp()
            if current_time - session_time > cleanup_threshold:
                # Clean up session files
                for file_info in session.get("files", []):
                    file_path = file_info.get("path")
                    if file_path and os.path.exists(file_path):
                        try:
                            os.remove(file_path)
                            cleaned_files += 1
                        except Exception as e:
                            logger.warning(f"Error deleting file {file_path}: {e}")
                
                del state.capture_sessions[session_id]
                cleaned_sessions.append(session_id)
        
        logger.info(f"Cleanup completed: {len(cleaned_sessions)} sessions, {cleaned_files} files")
        
        return {
            "status": "cleaned",
            "sessions_removed": len(cleaned_sessions),
            "files_removed": cleaned_files,
            "message": "Cleanup completed successfully"
        }
        
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# File management endpoints
@app.get("/files")
async def list_all_files():
    """List all uploaded files"""
    all_files = []
    for session in state.capture_sessions.values():
        all_files.extend(session["files"])
    
    return {
        "files": all_files,
        "total": len(all_files)
    }

@app.delete("/files/{session_id}/{filename}")
async def delete_file(session_id: str, filename: str):
    """Delete a specific file"""
    if session_id not in state.capture_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = state.capture_sessions[session_id]
    file_info = None
    file_index = None
    
    for i, file in enumerate(session["files"]):
        if file["filename"] == filename:
            file_info = file
            file_index = i
            break
    
    if not file_info:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Delete file from disk
    file_path = file_info["path"]
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            logger.warning(f"Error deleting file {file_path}: {e}")
    
    # Remove from session
    del session["files"][file_index]
    
    logger.info(f"Deleted file: {filename} from session {session_id}")
    
    return {
        "status": "deleted",
        "filename": filename,
        "session_id": session_id
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
