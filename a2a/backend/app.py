from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

# Import routes
from routes.websocket import router as websocket_router

# Import cognitive assistance system
from cognitive_assistance_system.a2a_integration import A2ACognitiveIntegration

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(title="Cognitive Assistance System - Alzheimer's Support with A2A ADK")

# Initialize cognitive assistance system
cognitive_system = A2ACognitiveIntegration()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(websocket_router)

# Mount frontend static files
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

# Root endpoint - serve the frontend
@app.get("/")
def serve_index():
    return FileResponse("../frontend/index.html")

# Cognitive assistance endpoints
@app.get("/api/cognitive/config")
def get_cognitive_config():
    """Get cognitive assistance system configuration for A2A ADK."""
    return cognitive_system.get_a2a_config()

@app.get("/api/cognitive/session")
def get_session_summary():
    """Get current session summary."""
    return cognitive_system.get_session_summary()

@app.post("/api/cognitive/profile")
def update_user_profile(profile_data: dict):
    """Update user profile information."""
    cognitive_system.update_user_profile(profile_data)
    return {"status": "success", "message": "Profile updated successfully"}

@app.get("/api/cognitive/profile")
def get_user_profile():
    """Get current user profile."""
    return cognitive_system.get_user_profile()

@app.post("/api/cognitive/reset")
def reset_session():
    """Reset the current session."""
    cognitive_system.reset_session()
    return {"status": "success", "message": "Session reset successfully"}

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
