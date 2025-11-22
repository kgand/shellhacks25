"""
Pydantic schemas for the Messenger AI Assistant API
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class Utterance(BaseModel):
    """Schema for a transcribed utterance"""
    text: str
    timestamp: str
    connection_id: str
    type: str = "transcript"
    user_id: Optional[str] = "default"
    confidence: Optional[float] = None

class Memory(BaseModel):
    """Schema for a stored memory"""
    content: str
    type: str
    timestamp: str
    connection_id: str
    user_id: Optional[str] = "default"
    created_at: Optional[str] = None

class ActionItem(BaseModel):
    """Schema for an action item"""
    description: str
    owner: str
    due_hint: Optional[str] = None
    status: str = "pending"
    timestamp: str
    connection_id: str
    user_id: Optional[str] = "default"
    created_at: Optional[str] = None

class Person(BaseModel):
    """Schema for a person entity"""
    name: str
    role: Optional[str] = None
    context: Optional[str] = None

class RelationshipEdge(BaseModel):
    """Schema for a relationship between people"""
    person1: str
    person2: str
    relationship_type: str
    evidence: str
    timestamp: str
    connection_id: str
    user_id: Optional[str] = "default"
    created_at: Optional[str] = None

class ReviveRequest(BaseModel):
    """Schema for memory revival request"""
    cue: str = Field(..., description="Text cue to search for relevant memories")
    limit: Optional[int] = Field(10, description="Maximum number of memories to return")
    user_id: Optional[str] = Field("default", description="User ID to filter memories")

class ReviveResponse(BaseModel):
    """Schema for memory revival response"""
    cue: str
    memories: List[Dict[str, Any]]
    recap: str
    count: int

class SessionData(BaseModel):
    """Schema for session information"""
    session_id: str
    start_time: str
    utterance_count: int
    last_activity: str
    status: str = "active"

class HealthResponse(BaseModel):
    """Schema for health check response"""
    status: str
    services: Dict[str, bool]

class WebSocketMessage(BaseModel):
    """Schema for WebSocket messages"""
    type: str
    data: Optional[Dict[str, Any]] = None
    timestamp: Optional[str] = None

class AudioChunk(BaseModel):
    """Schema for audio chunk data"""
    chunk_id: str
    audio_data: bytes
    timestamp: str
    connection_id: str
    format: str = "webm"

class VideoFrame(BaseModel):
    """Schema for video frame data"""
    frame_id: str
    frame_data: bytes
    timestamp: str
    connection_id: str
    format: str = "webm"

class TranscriptChunk(BaseModel):
    """Schema for transcript chunk"""
    text: str
    timestamp: str
    confidence: float
    connection_id: str
    is_final: bool = False

class SummaryData(BaseModel):
    """Schema for conversation summary"""
    summary: str
    key_points: List[str]
    participants: List[str]
    duration: Optional[str] = None
    timestamp: str
    connection_id: str

class EmbeddingData(BaseModel):
    """Schema for embedding data"""
    text: str
    embedding: List[float]
    model: str
    timestamp: str
    connection_id: str

class SearchResult(BaseModel):
    """Schema for search results"""
    query: str
    results: List[Dict[str, Any]]
    total_count: int
    search_time: float
