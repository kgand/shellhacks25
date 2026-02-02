"""
Summarization Service
Provides comprehensive summarization of Messenger conversations combining visual and audio analysis
"""

import os
import time
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import json

from ollama_client import OllamaClient
from audio_processor import AudioProcessor

logger = logging.getLogger(__name__)

class SummarizationService:
    """Service for generating comprehensive summaries of Messenger conversations"""
    
    def __init__(self):
        self.ollama_client = OllamaClient()
        self.audio_processor = AudioProcessor()
        
        # Summarization settings
        self.max_summary_length = 400
        self.summary_update_interval = 30  # Update summary every 30 seconds
        self.last_summary_time = 0
        
    def generate_comprehensive_summary(
        self, 
        frame_analyses: List[Dict[str, Any]], 
        audio_transcriptions: List[Dict[str, Any]],
        session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive summary combining visual and audio analysis
        
        Args:
            frame_analyses: List of frame analysis results
            audio_transcriptions: List of audio transcription results
            session_context: Optional session context information
            
        Returns:
            Dict containing comprehensive summary
        """
        try:
            # Combine all content
            combined_content = self._combine_analysis_content(
                frame_analyses, 
                audio_transcriptions, 
                session_context
            )
            
            # Generate different types of summaries
            summaries = {
                "brief": self._generate_brief_summary(combined_content),
                "detailed": self._generate_detailed_summary(combined_content),
                "key_points": self._extract_key_points(combined_content),
                "timeline": self._generate_timeline_summary(frame_analyses, audio_transcriptions)
            }
            
            # Generate overall summary
            overall_summary = self._generate_overall_summary(combined_content)
            
            result = {
                "status": "success",
                "generated_at": datetime.now().isoformat(),
                "overall_summary": overall_summary,
                "summaries": summaries,
                "content_stats": {
                    "frame_count": len(frame_analyses),
                    "audio_count": len(audio_transcriptions),
                    "total_duration": self._calculate_total_duration(audio_transcriptions)
                }
            }
            
            logger.info("Generated comprehensive summary")
            return result
            
        except Exception as e:
            logger.error(f"Error generating comprehensive summary: {e}")
            return {
                "status": "error",
                "message": str(e),
                "generated_at": datetime.now().isoformat()
            }
    
    def _combine_analysis_content(
        self, 
        frame_analyses: List[Dict[str, Any]], 
        audio_transcriptions: List[Dict[str, Any]], 
        session_context: Optional[Dict[str, Any]]
    ) -> str:
        """Combine all analysis content into a single text"""
        try:
            content_parts = []
            
            # Add session context if available
            if session_context:
                content_parts.append(f"Session Context: {json.dumps(session_context, indent=2)}")
            
            # Add frame analyses
            if frame_analyses:
                content_parts.append("Visual Analysis:")
                for i, analysis in enumerate(frame_analyses[-10:]):  # Last 10 analyses
                    timestamp = analysis.get("timestamp", "Unknown")
                    frame_analysis = analysis.get("analysis", "")
                    content_parts.append(f"  Frame {i+1} ({timestamp}): {frame_analysis}")
            
            # Add audio transcriptions
            if audio_transcriptions:
                content_parts.append("\nAudio Transcriptions:")
                for i, transcription in enumerate(audio_transcriptions):
                    file_path = transcription.get("file_path", "Unknown")
                    transcription_text = transcription.get("transcription", "")
                    duration = transcription.get("duration", 0)
                    content_parts.append(f"  Audio {i+1} ({os.path.basename(file_path)}, {duration:.1f}s): {transcription_text}")
            
            return "\n".join(content_parts)
            
        except Exception as e:
            logger.error(f"Error combining analysis content: {e}")
            return "Error combining content"
    
    def _generate_brief_summary(self, content: str) -> str:
        """Generate a brief summary (under 200 characters)"""
        try:
            prompt = f"""Summarize this Messenger conversation in under 200 characters. Focus on the main topic and key points discussed.

Content:
{content}

Brief Summary:"""
            
            summary = self.ollama_client.process_text(prompt)
            return summary[:200]  # Ensure it's under 200 characters
            
        except Exception as e:
            logger.error(f"Error generating brief summary: {e}")
            return "Brief summary generation failed"
    
    def _generate_detailed_summary(self, content: str) -> str:
        """Generate a detailed summary (under 400 characters)"""
        try:
            prompt = f"""Provide a detailed summary of this Messenger conversation. Include key topics, people involved, important information discussed, and any notable events or decisions.

Content:
{content}

Detailed Summary:"""
            
            summary = self.ollama_client.process_text(prompt)
            return summary[:400]  # Ensure it's under 400 characters
            
        except Exception as e:
            logger.error(f"Error generating detailed summary: {e}")
            return "Detailed summary generation failed"
    
    def _extract_key_points(self, content: str) -> List[str]:
        """Extract key points from the conversation"""
        try:
            prompt = f"""Extract the key points from this Messenger conversation. List them as bullet points, maximum 5 points.

Content:
{content}

Key Points:"""
            
            key_points_text = self.ollama_client.process_text(prompt)
            
            # Parse key points (simple parsing)
            key_points = []
            for line in key_points_text.split('\n'):
                line = line.strip()
                if line and (line.startswith('-') or line.startswith('•') or line.startswith('*')):
                    key_points.append(line[1:].strip())
                elif line and len(line) > 10:  # Non-empty substantial line
                    key_points.append(line)
            
            return key_points[:5]  # Maximum 5 key points
            
        except Exception as e:
            logger.error(f"Error extracting key points: {e}")
            return ["Key points extraction failed"]
    
    def _generate_timeline_summary(
        self, 
        frame_analyses: List[Dict[str, Any]], 
        audio_transcriptions: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate a timeline summary of events"""
        try:
            timeline = []
            
            # Add frame events
            for analysis in frame_analyses[-20:]:  # Last 20 analyses
                timeline.append({
                    "timestamp": analysis.get("timestamp", "Unknown"),
                    "type": "visual",
                    "description": analysis.get("analysis", ""),
                    "source": "frame_analysis"
                })
            
            # Add audio events
            for transcription in audio_transcriptions:
                timeline.append({
                    "timestamp": transcription.get("processed_at", "Unknown"),
                    "type": "audio",
                    "description": f"Audio conversation ({transcription.get('duration', 0):.1f}s)",
                    "source": "audio_transcription"
                })
            
            # Sort by timestamp
            timeline.sort(key=lambda x: x.get("timestamp", ""))
            
            return timeline[-10:]  # Last 10 events
            
        except Exception as e:
            logger.error(f"Error generating timeline summary: {e}")
            return []
    
    def _generate_overall_summary(self, content: str) -> str:
        """Generate the overall summary"""
        try:
            prompt = f"""Create a comprehensive summary of this Messenger conversation. Include:
1. Main topic of discussion
2. People involved and their roles
3. Key decisions or outcomes
4. Important information shared
5. Overall mood or tone

Keep the summary concise but informative, under 300 characters.

Content:
{content}

Overall Summary:"""
            
            summary = self.ollama_client.process_text(prompt)
            return summary[:300]  # Ensure it's under 300 characters
            
        except Exception as e:
            logger.error(f"Error generating overall summary: {e}")
            return "Overall summary generation failed"
    
    def _calculate_total_duration(self, audio_transcriptions: List[Dict[str, Any]]) -> float:
        """Calculate total audio duration"""
        try:
            total_duration = 0
            for transcription in audio_transcriptions:
                duration = transcription.get("duration", 0)
                if isinstance(duration, (int, float)):
                    total_duration += duration
            return total_duration
        except Exception as e:
            logger.error(f"Error calculating total duration: {e}")
            return 0.0
    
    def should_update_summary(self) -> bool:
        """Check if summary should be updated based on time interval"""
        current_time = time.time()
        return (current_time - self.last_summary_time) >= self.summary_update_interval
    
    def update_summary_timestamp(self):
        """Update the last summary timestamp"""
        self.last_summary_time = time.time()
    
    def generate_session_summary(self, session_id: str, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary for a specific session"""
        try:
            frame_analyses = analysis_results.get("frame_analysis_results", [])
            audio_analyses = analysis_results.get("audio_analysis_results", [])
            
            # Generate comprehensive summary
            summary_result = self.generate_comprehensive_summary(
                frame_analyses=frame_analyses,
                audio_transcriptions=audio_analyses,
                session_context={"session_id": session_id}
            )
            
            # Save summary to file
            self._save_summary_to_file(session_id, summary_result)
            
            return summary_result
            
        except Exception as e:
            logger.error(f"Error generating session summary: {e}")
            return {
                "status": "error",
                "message": str(e),
                "session_id": session_id
            }
    
    def _save_summary_to_file(self, session_id: str, summary_result: Dict[str, Any]):
        """Save summary result to file"""
        try:
            # Create session directory
            session_dir = f"processed/{session_id}"
            os.makedirs(session_dir, exist_ok=True)
            
            # Save summary
            summary_file = os.path.join(session_dir, "conversation_summary.json")
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary_result, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved conversation summary to: {summary_file}")
            
        except Exception as e:
            logger.error(f"Error saving summary to file: {e}")
    
    def get_summary_statistics(self) -> Dict[str, Any]:
        """Get summarization service statistics"""
        return {
            "service_ready": True,
            "max_summary_length": self.max_summary_length,
            "update_interval": self.summary_update_interval,
            "last_summary_time": self.last_summary_time,
            "ollama_available": self.ollama_client.is_available()
        }
