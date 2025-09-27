"""
Pydantic schemas for Messenger AI Assistant
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class MessageType(str, Enum):
    """Message types for WebSocket communication"""
    VIDEO_FRAME = "video_frame"
    AUDIO_CHUNK = "audio_chunk"
    TRANSCRIPT = "transcript"
    SUMMARY = "summary"
    ACTION = "action"
    RELATIONSHIP = "relationship"

class Utterance(BaseModel):
    """Individual utterance in a conversation"""
    id: str = Field(..., description="Unique identifier for the utterance")
    user_id: str = Field(..., description="User who made the utterance")
    text: str = Field(..., description="Text content of the utterance")
    timestamp: datetime = Field(..., description="When the utterance was made")
    confidence: float = Field(default=1.0, description="Confidence score for the utterance")
    speaker: Optional[str] = Field(None, description="Speaker identifier")
    
class Memory(BaseModel):
    """Memory entry in the system"""
    id: str = Field(..., description="Unique identifier for the memory")
    user_id: str = Field(..., description="User this memory belongs to")
    content: str = Field(..., description="Content of the memory")
    memory_type: str = Field(..., description="Type of memory (utterance, summary, action, relationship)")
    timestamp: datetime = Field(..., description="When the memory was created")
    embedding: Optional[List[float]] = Field(None, description="Vector embedding for the memory")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
class ActionItem(BaseModel):
    """Action item extracted from conversation"""
    id: str = Field(..., description="Unique identifier for the action")
    user_id: str = Field(..., description="User this action belongs to")
    description: str = Field(..., description="Description of the action")
    owner: str = Field(..., description="Who is responsible for the action")
    due_hint: Optional[str] = Field(None, description="When the action is due")
    priority: str = Field(default="medium", description="Priority level")
    status: str = Field(default="pending", description="Current status")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="When the action was created")
    
class Person(BaseModel):
    """Person mentioned in conversations"""
    id: str = Field(..., description="Unique identifier for the person")
    name: str = Field(..., description="Name of the person")
    user_id: str = Field(..., description="User who knows this person")
    first_mentioned: datetime = Field(..., description="When this person was first mentioned")
    last_mentioned: datetime = Field(..., description="When this person was last mentioned")
    mention_count: int = Field(default=1, description="How many times this person was mentioned")
    
class RelationshipEdge(BaseModel):
    """Relationship between two people"""
    id: str = Field(..., description="Unique identifier for the relationship")
    user_id: str = Field(..., description="User who knows about this relationship")
    person1_id: str = Field(..., description="First person in the relationship")
    person2_id: str = Field(..., description="Second person in the relationship")
    relationship_type: str = Field(..., description="Type of relationship")
    strength: float = Field(default=0.5, description="Strength of the relationship")
    evidence: List[str] = Field(default_factory=list, description="Evidence for the relationship")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="When the relationship was identified")
    
class ConversationSummary(BaseModel):
    """Summary of a conversation"""
    id: str = Field(..., description="Unique identifier for the summary")
    user_id: str = Field(..., description="User this summary belongs to")
    summary: str = Field(..., description="Summary text")
    key_points: List[str] = Field(default_factory=list, description="Key points from the conversation")
    participants: List[str] = Field(default_factory=list, description="People involved in the conversation")
    duration_minutes: Optional[float] = Field(None, description="Duration of the conversation in minutes")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="When the summary was created")
    
class WebSocketMessage(BaseModel):
    """WebSocket message format"""
    type: MessageType = Field(..., description="Type of message")
    data: str = Field(..., description="Hex-encoded data")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the message was sent")
    frame_count: Optional[int] = Field(None, description="Frame number for video frames")
    connection_id: Optional[str] = Field(None, description="Connection identifier")
    
class ReviveRequest(BaseModel):
    """Request for memory revival"""
    cue: str = Field(..., description="Cue to search for memories")
    limit: int = Field(default=10, description="Maximum number of memories to return")
    user_id: str = Field(default="default", description="User to search memories for")
    
class ReviveResponse(BaseModel):
    """Response for memory revival"""
    cue: str = Field(..., description="Original cue")
    memories: List[Memory] = Field(..., description="Found memories")
    summary: str = Field(..., description="Generated summary")
    count: int = Field(..., description="Number of memories found")
    
class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Health status")
    services: Dict[str, bool] = Field(..., description="Service status")
    connections: int = Field(..., description="Number of active connections")
    memories_count: int = Field(..., description="Number of stored memories")
    
class MemoryStatistics(BaseModel):
    """Memory statistics for a user"""
    user_id: str = Field(..., description="User ID")
    total_memories: int = Field(..., description="Total number of memories")
    total_utterances: int = Field(..., description="Number of utterances")
    total_relationships: int = Field(..., description="Number of relationships")
    last_updated: datetime = Field(..., description="When statistics were last updated")
    
class MemorySearchRequest(BaseModel):
    """Request for memory search"""
    user_id: str = Field(..., description="User to search memories for")
    query: str = Field(default="", description="Search query")
    limit: int = Field(default=10, description="Maximum number of results")
    
class MemorySearchResponse(BaseModel):
    """Response for memory search"""
    user_id: str = Field(..., description="User ID")
    query: str = Field(..., description="Search query")
    memories: List[Memory] = Field(..., description="Found memories")
    total_found: int = Field(..., description="Total number of memories found")
