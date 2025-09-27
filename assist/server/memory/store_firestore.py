"""
Firestore memory storage implementation
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Firestore imports
try:
    from google.cloud import firestore
    from google.cloud.firestore import Client
    FIRESTORE_AVAILABLE = True
except ImportError:
    logger.warning("Firestore not available, using fallback storage")
    FIRESTORE_AVAILABLE = False

class FirestoreMemoryStore:
    """Firestore-based memory storage"""
    
    def __init__(self, project_id: Optional[str] = None):
        self.project_id = project_id or os.getenv('GOOGLE_PROJECT_ID')
        self.db = None
        self.is_initialized = False
        
    async def initialize(self):
        """Initialize Firestore connection"""
        try:
            if not FIRESTORE_AVAILABLE:
                logger.warning("Firestore not available, using fallback")
                self.is_initialized = True
                return True
                
            if not self.project_id:
                logger.error("GOOGLE_PROJECT_ID not found in environment variables")
                return False
                
            # Initialize Firestore client
            self.db = firestore.Client(project=self.project_id)
            self.is_initialized = True
            logger.info("Firestore memory store initialized")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Firestore: {e}")
            return False
    
    async def store_memory(self, memory: Dict[str, Any]) -> str:
        """Store a memory in Firestore"""
        try:
            if not self.is_initialized or not self.db:
                logger.warning("Firestore not initialized, using fallback")
                return f"memory_{int(datetime.utcnow().timestamp())}"
            
            # Add timestamp if not present
            if 'timestamp' not in memory:
                memory['timestamp'] = datetime.utcnow()
            
            # Store in Firestore
            doc_ref = self.db.collection('memories').add(memory)
            memory_id = doc_ref[1].id
            
            logger.info(f"Stored memory in Firestore: {memory_id}")
            return memory_id
            
        except Exception as e:
            logger.error(f"Failed to store memory in Firestore: {e}")
            return f"memory_{int(datetime.utcnow().timestamp())}"
    
    async def retrieve_memories(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve memories from Firestore"""
        try:
            if not self.is_initialized or not self.db:
                logger.warning("Firestore not initialized, returning empty list")
                return []
            
            # Simple text search in Firestore
            memories = []
            docs = self.db.collection('memories').limit(limit).stream()
            
            for doc in docs:
                memory = doc.to_dict()
                memory['id'] = doc.id
                
                # Simple text matching
                if query.lower() in str(memory).lower():
                    memories.append(memory)
            
            logger.info(f"Retrieved {len(memories)} memories from Firestore")
            return memories
            
        except Exception as e:
            logger.error(f"Failed to retrieve memories from Firestore: {e}")
            return []
    
    async def update_memory(self, memory_id: str, updates: Dict[str, Any]) -> bool:
        """Update a memory in Firestore"""
        try:
            if not self.is_initialized or not self.db:
                logger.warning("Firestore not initialized")
                return False
            
            # Update memory
            doc_ref = self.db.collection('memories').document(memory_id)
            doc_ref.update(updates)
            
            logger.info(f"Updated memory in Firestore: {memory_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update memory in Firestore: {e}")
            return False
    
    async def delete_memory(self, memory_id: str) -> bool:
        """Delete a memory from Firestore"""
        try:
            if not self.is_initialized or not self.db:
                logger.warning("Firestore not initialized")
                return False
            
            # Delete memory
            self.db.collection('memories').document(memory_id).delete()
            
            logger.info(f"Deleted memory from Firestore: {memory_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete memory from Firestore: {e}")
            return False
    
    async def get_memory_statistics(self, user_id: str) -> Dict[str, Any]:
        """Get memory statistics for a user"""
        try:
            if not self.is_initialized or not self.db:
                logger.warning("Firestore not initialized")
                return {
                    "user_id": user_id,
                    "total_memories": 0,
                    "total_utterances": 0,
                    "total_relationships": 0,
                    "last_updated": datetime.utcnow().isoformat()
                }
            
            # Count memories by type
            memories = self.db.collection('memories').where('user_id', '==', user_id).stream()
            
            total_memories = 0
            total_utterances = 0
            total_relationships = 0
            
            for doc in memories:
                memory = doc.to_dict()
                total_memories += 1
                
                if memory.get('memory_type') == 'utterance':
                    total_utterances += 1
                elif memory.get('memory_type') == 'relationship':
                    total_relationships += 1
            
            return {
                "user_id": user_id,
                "total_memories": total_memories,
                "total_utterances": total_utterances,
                "total_relationships": total_relationships,
                "last_updated": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to get memory statistics: {e}")
            return {
                "user_id": user_id,
                "total_memories": 0,
                "total_utterances": 0,
                "total_relationships": 0,
                "last_updated": datetime.utcnow().isoformat()
            }

# Global memory store instance
memory_store = FirestoreMemoryStore()

async def initialize_memory_store():
    """Initialize the memory store"""
    return await memory_store.initialize()

async def store_memory(memory: Dict[str, Any]) -> str:
    """Store a memory"""
    return await memory_store.store_memory(memory)

async def retrieve_memories(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Retrieve memories"""
    return await memory_store.retrieve_memories(query, limit)

async def get_memory_statistics(user_id: str) -> Dict[str, Any]:
    """Get memory statistics"""
    return await memory_store.get_memory_statistics(user_id)
