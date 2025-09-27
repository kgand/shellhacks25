"""
Revive API implementation for memory retrieval and assembly
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import numpy as np
from fastapi import HTTPException

from memory.store_firestore import FirestoreMemoryStore
from memory.pipelines import EmbeddingPipeline, MemoryIndexingPipeline, MemoryRetrievalPipeline
from gemini_live import GeminiLiveClient

logger = logging.getLogger(__name__)

class ReviveAPI:
    """API for retrieving and assembling memories"""
    
    def __init__(self, memory_store: FirestoreMemoryStore):
        self.memory_store = memory_store
        self.embedding_pipeline = None
        self.indexing_pipeline = None
        self.retrieval_pipeline = None
        self.gemini_client = None
        self.is_initialized = False
    
    async def initialize(self):
        """Initialize the revive API"""
        try:
            # Initialize embedding pipeline
            self.embedding_pipeline = EmbeddingPipeline()
            await self.embedding_pipeline.initialize()
            
            # Initialize indexing pipeline
            self.indexing_pipeline = MemoryIndexingPipeline(self.embedding_pipeline)
            await self.indexing_pipeline.initialize()
            
            # Initialize retrieval pipeline
            self.retrieval_pipeline = MemoryRetrievalPipeline(
                self.embedding_pipeline,
                self.indexing_pipeline
            )
            await self.retrieval_pipeline.initialize()
            
            # Initialize Gemini client for recap generation
            self.gemini_client = GeminiLiveClient()
            
            self.is_initialized = True
            logger.info("Revive API initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Revive API: {e}")
            raise
    
    async def revive_memories(self, cue: str, user_id: str = "default", limit: int = 10) -> Dict[str, Any]:
        """Retrieve and assemble memories based on a text cue"""
        try:
            if not self.is_initialized:
                await self.initialize()
            
            # Step 1: Search for relevant memories using embeddings
            relevant_memories = await self._search_memories_by_embedding(cue, user_id, limit)
            
            # Step 2: Get additional memories from Firestore
            firestore_memories = await self.memory_store.search_memories(cue, limit)
            
            # Step 3: Combine and deduplicate memories
            all_memories = self._combine_memories(relevant_memories, firestore_memories)
            
            # Step 4: Generate stitched recap using Gemini
            recap = await self._generate_recap(all_memories, cue)
            
            # Step 5: Extract key insights
            insights = await self._extract_insights(all_memories, cue)
            
            return {
                'cue': cue,
                'memories': all_memories,
                'recap': recap,
                'insights': insights,
                'count': len(all_memories),
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to revive memories: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def _search_memories_by_embedding(self, cue: str, user_id: str, limit: int) -> List[Dict[str, Any]]:
        """Search memories using embedding similarity"""
        try:
            # Get all memories for the user
            all_memories = await self.memory_store.get_user_memories(user_id, 100)
            
            if not all_memories:
                return []
            
            # Index memories if not already indexed
            for memory in all_memories:
                if memory.get('id') not in self.indexing_pipeline.memory_index:
                    await self.indexing_pipeline.index_memory(memory)
            
            # Search for similar memories
            similar_memories = await self.indexing_pipeline.search_similar_memories(cue, limit)
            
            return [result['memory'] for result in similar_memories]
            
        except Exception as e:
            logger.error(f"Failed to search memories by embedding: {e}")
            return []
    
    def _combine_memories(self, embedding_memories: List[Dict], firestore_memories: List[Dict]) -> List[Dict[str, Any]]:
        """Combine and deduplicate memories from different sources"""
        try:
            # Create a set of memory IDs to avoid duplicates
            seen_ids = set()
            combined_memories = []
            
            # Add embedding-based memories first (higher relevance)
            for memory in embedding_memories:
                memory_id = memory.get('id', '')
                if memory_id and memory_id not in seen_ids:
                    combined_memories.append(memory)
                    seen_ids.add(memory_id)
            
            # Add Firestore memories that aren't already included
            for memory in firestore_memories:
                memory_id = memory.get('id', '')
                if memory_id and memory_id not in seen_ids:
                    combined_memories.append(memory)
                    seen_ids.add(memory_id)
            
            # Sort by timestamp (most recent first)
            combined_memories.sort(
                key=lambda x: x.get('timestamp', ''),
                reverse=True
            )
            
            return combined_memories
            
        except Exception as e:
            logger.error(f"Failed to combine memories: {e}")
            return []
    
    async def _generate_recap(self, memories: List[Dict[str, Any]], cue: str) -> str:
        """Generate a stitched recap using Gemini"""
        try:
            if not memories:
                return "No relevant memories found for the given cue."
            
            if not self.gemini_client:
                return "Memory service unavailable."
            
            # Prepare context for recap generation
            context = self._prepare_memory_context(memories, cue)
            
            # Generate recap using Gemini
            recap = await self.gemini_client.generate_recap(memories, cue)
            
            return recap
            
        except Exception as e:
            logger.error(f"Failed to generate recap: {e}")
            return f"Error generating recap: {str(e)}"
    
    def _prepare_memory_context(self, memories: List[Dict[str, Any]], cue: str) -> str:
        """Prepare memory context for recap generation"""
        try:
            context_parts = [
                f"User Query: {cue}",
                "",
                "Relevant Memories:",
                ""
            ]
            
            for i, memory in enumerate(memories, 1):
                content = memory.get('content', memory.get('text', ''))
                timestamp = memory.get('timestamp', 'Unknown')
                memory_type = memory.get('type', 'memory')
                
                context_parts.append(f"{i}. [{memory_type}] {content}")
                context_parts.append(f"   Timestamp: {timestamp}")
                context_parts.append("")
            
            return "\n".join(context_parts)
            
        except Exception as e:
            logger.error(f"Failed to prepare memory context: {e}")
            return f"Error preparing context: {str(e)}"
    
    async def _extract_insights(self, memories: List[Dict[str, Any]], cue: str) -> Dict[str, Any]:
        """Extract key insights from memories"""
        try:
            insights = {
                'key_topics': [],
                'participants': [],
                'time_range': None,
                'memory_types': [],
                'relevance_scores': []
            }
            
            if not memories:
                return insights
            
            # Extract key topics
            topics = set()
            for memory in memories:
                content = memory.get('content', memory.get('text', ''))
                if 'project' in content.lower():
                    topics.add('Project Management')
                if 'meeting' in content.lower():
                    topics.add('Meetings')
                if 'deadline' in content.lower():
                    topics.add('Deadlines')
            
            insights['key_topics'] = list(topics)
            
            # Extract participants
            participants = set()
            for memory in memories:
                if 'participants' in memory:
                    participants.update(memory['participants'])
                if 'speaker' in memory:
                    participants.add(memory['speaker'])
            
            insights['participants'] = list(participants)
            
            # Extract time range
            timestamps = [memory.get('timestamp', '') for memory in memories if memory.get('timestamp')]
            if timestamps:
                timestamps.sort()
                insights['time_range'] = {
                    'earliest': timestamps[0],
                    'latest': timestamps[-1]
                }
            
            # Extract memory types
            memory_types = set()
            for memory in memories:
                memory_type = memory.get('type', 'unknown')
                memory_types.add(memory_type)
            
            insights['memory_types'] = list(memory_types)
            
            # Calculate relevance scores (simplified)
            for memory in memories:
                # In production, this would use actual relevance scoring
                relevance_score = 0.8  # Placeholder
                insights['relevance_scores'].append({
                    'memory_id': memory.get('id', ''),
                    'score': relevance_score
                })
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to extract insights: {e}")
            return {}
    
    async def get_memory_statistics(self, user_id: str = "default") -> Dict[str, Any]:
        """Get statistics about user's memories"""
        try:
            # Get all memories for the user
            all_memories = await self.memory_store.get_user_memories(user_id, 1000)
            
            if not all_memories:
                return {
                    'total_memories': 0,
                    'memory_types': {},
                    'time_range': None,
                    'recent_activity': []
                }
            
            # Calculate statistics
            total_memories = len(all_memories)
            
            # Count memory types
            memory_types = {}
            for memory in all_memories:
                memory_type = memory.get('type', 'unknown')
                memory_types[memory_type] = memory_types.get(memory_type, 0) + 1
            
            # Get time range
            timestamps = [memory.get('timestamp', '') for memory in all_memories if memory.get('timestamp')]
            time_range = None
            if timestamps:
                timestamps.sort()
                time_range = {
                    'earliest': timestamps[0],
                    'latest': timestamps[-1]
                }
            
            # Get recent activity (last 10 memories)
            recent_memories = sorted(all_memories, key=lambda x: x.get('timestamp', ''), reverse=True)[:10]
            recent_activity = [
                {
                    'id': memory.get('id', ''),
                    'type': memory.get('type', ''),
                    'timestamp': memory.get('timestamp', ''),
                    'preview': memory.get('content', memory.get('text', ''))[:100]
                }
                for memory in recent_memories
            ]
            
            return {
                'total_memories': total_memories,
                'memory_types': memory_types,
                'time_range': time_range,
                'recent_activity': recent_activity
            }
            
        except Exception as e:
            logger.error(f"Failed to get memory statistics: {e}")
            return {}
    
    async def search_memories(self, query: str, user_id: str = "default", limit: int = 20) -> List[Dict[str, Any]]:
        """Search memories with advanced filtering"""
        try:
            if not self.is_initialized:
                await self.initialize()
            
            # Search using embedding similarity
            embedding_results = await self._search_memories_by_embedding(query, user_id, limit)
            
            # Search using Firestore text search
            firestore_results = await self.memory_store.search_memories(query, limit)
            
            # Combine and rank results
            combined_results = self._combine_memories(embedding_results, firestore_results)
            
            return combined_results[:limit]
            
        except Exception as e:
            logger.error(f"Failed to search memories: {e}")
            return []
    
    async def delete_memory(self, memory_id: str) -> bool:
        """Delete a specific memory"""
        try:
            # Delete from Firestore
            success = await self.memory_store.delete_memory(memory_id)
            
            # Remove from indexing pipeline
            if success:
                await self.indexing_pipeline.remove_memory_from_index(memory_id)
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to delete memory: {e}")
            return False
