"""
FastAPI backend for Messenger AI Assistant
File-based screen capture with AI processing pipeline
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
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
import cv2
import numpy as np
import base64

# Import Ollama components
from ollama_client import OllamaClient
from realtime_analyzer import RealtimeAnalyzer
from audio_processor import AudioProcessor
from summarization_service import SummarizationService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app will be initialized with lifespan below

# Global state
class MessengerAIServiceState:
    def __init__(self):
        self.capture_sessions = {}
        self.uploaded_files = []
        self.is_initialized = False
        self.upload_dir = "uploads"
        self.output_dir = "processed"
        
        # Ollama components
        self.ollama_client = OllamaClient()
        self.realtime_analyzer = RealtimeAnalyzer()
        self.audio_processor = AudioProcessor()
        self.summarization_service = SummarizationService()
        
        # Create directories
        os.makedirs(self.upload_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

state = MessengerAIServiceState()

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown"""
    # Startup
    logger.info("🚀 Starting Messenger AI Assistant Backend...")
    state.is_initialized = True
    logger.info("✅ Backend initialized successfully")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down backend...")

# Add lifespan to app
app = FastAPI(
    title="Messenger AI Assistant API",
    description="Backend for AI-powered screen capture and analysis",
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
        "message": "Messenger AI Assistant API",
        "version": "2.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "sessions": "/sessions",
            "files": "/files",
            "upload": "/upload/{session_id}",
            "process": "/process/{session_id}",
            "stats": "/stats",
            "ollama": {
                "analyze_frame": "/analyze-frame",
                "process_text": "/process-text",
                "summarize": "/summarize",
                "start_analysis": "/start-analysis/{session_id}",
                "stop_analysis": "/stop-analysis",
                "analysis_status": "/analysis-status"
            },
            "audio": {
                "process_audio": "/process-audio",
                "transcribe_file": "/transcribe-file",
                "audio_status": "/audio-status"
            },
            "summarization": {
                "generate_summary": "/generate-summary/{session_id}",
                "comprehensive_summary": "/comprehensive-summary",
                "summary_status": "/summary-status"
            }
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

# Ollama AI Analysis Endpoints
@app.post("/analyze-frame")
async def analyze_frame(
    image: UploadFile = File(...),
    system_prompt: str = Form(None),
    user_query: str = Form(None)
):
    """Analyze a single frame using Ollama VLM"""
    try:
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")
        
        # Read and process image
        contents = await image.read()
        img_np = np.frombuffer(contents, np.uint8)
        frame = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
        
        if frame is None:
            raise HTTPException(status_code=400, detail="Could not decode image.")
        
        # Analyze frame
        analysis = state.ollama_client.analyze_frame(
            frame, 
            system_prompt=system_prompt,
            user_query=user_query
        )
        
        return {
            "status": "analyzed",
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error analyzing frame: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process-text")
async def process_text(
    prompt: str = Form(...),
    system_prompt: str = Form(None)
):
    """Process text using Ollama LLM"""
    try:
        result = state.ollama_client.process_text(
            prompt=prompt,
            system_prompt=system_prompt
        )
        
        return {
            "status": "processed",
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error processing text: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize")
async def summarize_content(
    content: str = Form(...),
    system_prompt: str = Form(None)
):
    """Summarize content using Ollama LLM"""
    try:
        summary = state.ollama_client.summarize_content(
            content=content,
            system_prompt=system_prompt
        )
        
        return {
            "status": "summarized",
            "summary": summary,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error summarizing content: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/start-analysis/{session_id}")
async def start_realtime_analysis(session_id: str):
    """Start real-time analysis for a session"""
    try:
        if session_id not in state.capture_sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Check if Ollama is available
        if not state.ollama_client.is_available():
            raise HTTPException(status_code=503, detail="Ollama is not available")
        
        # Start analysis
        success = state.realtime_analyzer.start_analysis(session_id)
        
        if success:
            return {
                "status": "started",
                "session_id": session_id,
                "message": "Real-time analysis started"
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to start analysis")
            
    except Exception as e:
        logger.error(f"Error starting analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/stop-analysis")
async def stop_realtime_analysis():
    """Stop real-time analysis"""
    try:
        state.realtime_analyzer.stop_analysis()
        
        return {
            "status": "stopped",
            "message": "Real-time analysis stopped"
        }
        
    except Exception as e:
        logger.error(f"Error stopping analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analysis-status")
async def get_analysis_status():
    """Get current analysis status"""
    try:
        results = state.realtime_analyzer.get_analysis_results()
        
        return {
            "status": "success",
            "analysis": results
        }
        
    except Exception as e:
        logger.error(f"Error getting analysis status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ollama-status")
async def get_ollama_status():
    """Get Ollama service status"""
    try:
        is_available = state.ollama_client.is_available()
        models = state.ollama_client.get_models() if is_available else {}
        
        return {
            "status": "available" if is_available else "unavailable",
            "ollama_available": is_available,
            "models": models
        }
        
    except Exception as e:
        logger.error(f"Error checking Ollama status: {e}")
        return {
            "status": "error",
            "ollama_available": False,
            "error": str(e)
        }

# Audio Processing Endpoints
@app.post("/process-audio")
async def process_audio_file(audio_file: UploadFile = File(...)):
    """Process an audio file for transcription"""
    try:
        if not audio_file.content_type.startswith("audio/"):
            raise HTTPException(status_code=400, detail="Invalid file type. Please upload an audio file.")
        
        # Save uploaded file temporarily
        temp_path = f"temp_audio_{int(time.time())}.wav"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(audio_file.file, buffer)
        
        try:
            # Process audio file
            result = state.audio_processor.process_audio_file(temp_path)
            
            return {
                "status": "processed",
                "filename": audio_file.filename,
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
        
    except Exception as e:
        logger.error(f"Error processing audio file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transcribe-file")
async def transcribe_audio_file(file_path: str = Form(...)):
    """Transcribe an audio file by path"""
    try:
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Audio file not found")
        
        # Process audio file
        result = state.audio_processor.process_audio_file(file_path)
        
        return {
            "status": "transcribed",
            "file_path": file_path,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error transcribing audio file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/audio-status")
async def get_audio_status():
    """Get audio processing status"""
    try:
        cache = state.audio_processor.get_transcription_cache()
        supported_formats = state.audio_processor.get_supported_formats()
        
        return {
            "status": "available",
            "supported_formats": supported_formats,
            "cached_transcriptions": len(cache),
            "processor_ready": True
        }
        
    except Exception as e:
        logger.error(f"Error getting audio status: {e}")
        return {
            "status": "error",
            "processor_ready": False,
            "error": str(e)
        }

# Summarization Endpoints
@app.post("/generate-summary/{session_id}")
async def generate_session_summary(session_id: str):
    """Generate comprehensive summary for a session"""
    try:
        if session_id not in state.capture_sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Get current analysis results
        analysis_results = state.realtime_analyzer.get_analysis_results()
        
        # Generate session summary
        summary_result = state.summarization_service.generate_session_summary(
            session_id=session_id,
            analysis_results=analysis_results
        )
        
        return {
            "status": "generated",
            "session_id": session_id,
            "summary": summary_result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error generating session summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/comprehensive-summary")
async def get_comprehensive_summary():
    """Get current comprehensive summary"""
    try:
        analysis_results = state.realtime_analyzer.get_analysis_results()
        comprehensive_summary = analysis_results.get("comprehensive_summary")
        
        if comprehensive_summary:
            return {
                "status": "available",
                "summary": comprehensive_summary,
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "status": "not_available",
                "message": "No comprehensive summary available yet",
                "timestamp": datetime.now().isoformat()
            }
        
    except Exception as e:
        logger.error(f"Error getting comprehensive summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/summary-status")
async def get_summary_status():
    """Get summarization service status"""
    try:
        stats = state.summarization_service.get_summary_statistics()
        
        return {
            "status": "available",
            "statistics": stats,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting summary status: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
