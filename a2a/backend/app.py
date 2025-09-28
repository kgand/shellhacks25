from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

# Import routes
from routes.websocket import router as websocket_router

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(title="Google A2A ADK Multimodal API")

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

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
