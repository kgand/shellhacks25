"""
Firestore memory store for persistent long-term memory
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import os

try:
    from google.cloud import firestore
    from google.cloud.firestore_v1.base_query import FieldFilter
except ImportError:
    firestore = None
    FieldFilter = None

logger = logging.getLogger(__name__)

class FirestoreMemoryStore:
    def __init__(self):
        self.db = None
        self.project_id = os.getenv("GOOGLE_PROJECT_ID")
        self.credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        
        if not self.project_id:
            raise ValueError("GOOGLE_PROJECT_ID environment variable is required")
    
    async def initialize(self):
        """Initialize Firestore client"""
        try:
            if firestore is None:
                raise ImportError("google-cloud-firestore package is required")
            
            # Initialize Firestore client
            if self.credentials_path:
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials_path
            
            self.db = firestore.Client(project=self.project_id)
            
            # Test connection
            await self._test_connection()
            
            logger.info("Firestore memory store initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Firestore: {e}")
            raise
    
    async def _test_connection(self):
        """Test Firestore connection"""
        try:
            # Try to read from a test collection
            test_ref = self.db.collection('_test').document('_test')
            test_ref.set({'test': True})
            test_ref.delete()
            
        except Exception as e:
            logger.error(f"Firestore connection test failed: {e}")
            raise
    
    async def store_utterance(self, utterance: Dict[str, Any]) -> str:
        """Store a transcribed utterance"""
        try:
            doc_ref = self.db.collection('utterances').document()
            
            utterance_data = {
                'text': utterance['text'],
                'timestamp': utterance['timestamp'],
                'connection_id': utterance['connection_id'],
                'type': utterance.get('type', 'transcript'),
                'created_at': datetime.utcnow().isoformat(),
                'user_id': utterance.get('user_id', 'default')
            }
            
            doc_ref.set(utterance_data)
            
            logger.info(f"Stored utterance: {utterance['text'][:50]}...")
            return doc_ref.id
            
        except Exception as e:
            logger.error(f"Failed to store utterance: {e}")
            raise
    
    async def store_memory(self, memory: Dict[str, Any]) -> str:
        """Store a processed memory"""
        try:
            doc_ref = self.db.collection('memories').document()
            
            memory_data = {
                'content': memory['content'],
                'type': memory['type'],
                'timestamp': memory['timestamp'],
                'connection_id': memory['connection_id'],
                'created_at': datetime.utcnow().isoformat(),
                'user_id': memory.get('user_id', 'default')
            }
            
            doc_ref.set(memory_data)
            
            logger.info(f"Stored memory: {memory['content'][:50]}...")
            return doc_ref.id
            
        except Exception as e:
            logger.error(f"Failed to store memory: {e}")
            raise
    
    async def store_action(self, action: Dict[str, Any]) -> str:
        """Store an action item"""
        try:
            doc_ref = self.db.collection('actions').document()
            
            action_data = {
                'description': action['description'],
                'owner': action['owner'],
                'due_hint': action.get('due_hint'),
                'status': action['status'],
                'timestamp': action['timestamp'],
                'connection_id': action['connection_id'],
                'created_at': datetime.utcnow().isoformat(),
                'user_id': action.get('user_id', 'default')
            }
            
            doc_ref.set(action_data)
            
            logger.info(f"Stored action: {action['description']}")
            return doc_ref.id
            
        except Exception as e:
            logger.error(f"Failed to store action: {e}")
            raise
    
    async def store_relationship(self, relationship: Dict[str, Any]) -> str:
        """Store a relationship"""
        try:
            doc_ref = self.db.collection('relationships').document()
            
            relationship_data = {
                'person1': relationship['person1'],
                'person2': relationship['person2'],
                'relationship_type': relationship['relationship_type'],
                'evidence': relationship['evidence'],
                'timestamp': relationship['timestamp'],
                'connection_id': relationship['connection_id'],
                'created_at': datetime.utcnow().isoformat(),
                'user_id': relationship.get('user_id', 'default')
            }
            
            doc_ref.set(relationship_data)
            
            logger.info(f"Stored relationship: {relationship['person1']} - {relationship['person2']}")
            return doc_ref.id
            
        except Exception as e:
            logger.error(f"Failed to store relationship: {e}")
            raise
    
    async def get_recent_utterances(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent utterances"""
        try:
            query = self.db.collection('utterances').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(limit)
            docs = query.stream()
            
            utterances = []
            for doc in docs:
                utterance = doc.to_dict()
                utterance['id'] = doc.id
                utterances.append(utterance)
            
            return utterances
            
        except Exception as e:
            logger.error(f"Failed to get recent utterances: {e}")
            return []
    
    async def get_user_memories(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get memories for a specific user"""
        try:
            query = self.db.collection('memories').where('user_id', '==', user_id).order_by('timestamp', direction=firestore.Query.DESCENDING).limit(limit)
            docs = query.stream()
            
            memories = []
            for doc in docs:
                memory = doc.to_dict()
                memory['id'] = doc.id
                memories.append(memory)
            
            return memories
            
        except Exception as e:
            logger.error(f"Failed to get user memories: {e}")
            return []
    
    async def search_memories(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search memories by text content"""
        try:
            # Simple text search - in production, you'd use vector search
            query_ref = self.db.collection('memories')
            docs = query_ref.stream()
            
            results = []
            for doc in docs:
                memory = doc.to_dict()
                if query.lower() in memory.get('content', '').lower():
                    memory['id'] = doc.id
                    results.append(memory)
                    
                    if len(results) >= limit:
                        break
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to search memories: {e}")
            return []
    
    async def update_session(self, session_id: str, session_data: Dict[str, Any]):
        """Update session information"""
        try:
            doc_ref = self.db.collection('sessions').document(session_id)
            doc_ref.set(session_data, merge=True)
            
        except Exception as e:
            logger.error(f"Failed to update session: {e}")
    
    async def delete_memory(self, memory_id: str) -> bool:
        """Delete a specific memory"""
        try:
            doc_ref = self.db.collection('memories').document(memory_id)
            doc_ref.delete()
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete memory: {e}")
            return False
