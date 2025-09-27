"""
Real-time Messenger Analysis Service
Processes captured frames and audio in real-time using Ollama
"""

import os
import time
import threading
import logging
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime
import json
import cv2
import numpy as np
from pathlib import Path

from ollama_client import OllamaClient
from audio_processor import AudioProcessor
from summarization_service import SummarizationService

logger = logging.getLogger(__name__)

class RealtimeAnalyzer:
    """Real-time analyzer for Messenger content"""
    
    def __init__(self, output_dir: str = "processed"):
        self.ollama_client = OllamaClient()
        self.audio_processor = AudioProcessor()
        self.summarization_service = SummarizationService()
        self.output_dir = output_dir
        self.is_analyzing = False
        self.analysis_thread = None
        self.frame_analysis_results = []
        self.audio_transcription = ""
        self.audio_analysis_results = []
        self.summary = ""
        self.comprehensive_summary = None
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Analysis settings
        self.target_fps = 0.5  # Process every 2 seconds
        self.analysis_interval = 1.0 / self.target_fps
        
        # Callbacks
        self.on_frame_analyzed: Optional[Callable] = None
        self.on_summary_updated: Optional[Callable] = None
        
    def start_analysis(self, session_id: str) -> bool:
        """
        Start real-time analysis for a session
        
        Args:
            session_id: Session ID to analyze
            
        Returns:
            True if started successfully, False otherwise
        """
        if self.is_analyzing:
            logger.warning("Analysis already in progress")
            return False
        
        if not self.ollama_client.is_available():
            logger.error("Ollama is not available")
            return False
        
        try:
            self.session_id = session_id
            self.is_analyzing = True
            self.frame_analysis_results = []
            self.audio_transcription = ""
            self.audio_analysis_results = []
            self.summary = ""
            self.comprehensive_summary = None
            
            # Start analysis thread
            self.analysis_thread = threading.Thread(
                target=self._analysis_loop, 
                daemon=True
            )
            self.analysis_thread.start()
            
            logger.info(f"Started real-time analysis for session: {session_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start analysis: {e}")
            self.is_analyzing = False
            return False
    
    def stop_analysis(self):
        """Stop real-time analysis"""
        if not self.is_analyzing:
            return
        
        self.is_analyzing = False
        
        if self.analysis_thread:
            self.analysis_thread.join()
        
        logger.info("Real-time analysis stopped")
    
    def _analysis_loop(self):
        """Main analysis loop"""
        last_analysis_time = time.time()
        
        try:
            while self.is_analyzing:
                current_time = time.time()
                
                # Check if it's time for next analysis
                if current_time - last_analysis_time >= self.analysis_interval:
                    self._analyze_captured_content()
                    last_analysis_time = current_time
                
                # Sleep briefly to avoid busy waiting
                time.sleep(0.1)
                
        except Exception as e:
            logger.error(f"Error in analysis loop: {e}")
        finally:
            self.is_analyzing = False
    
    def _analyze_captured_content(self):
        """Analyze captured frames and audio"""
        try:
            # Find captured files
            capture_dir = self._find_capture_directory()
            if not capture_dir:
                return
            
            # Analyze latest frames
            self._analyze_latest_frames(capture_dir)
            
            # Process audio if available
            self._process_audio_files(capture_dir)
            
            # Generate summary if we have enough data
            if len(self.frame_analysis_results) > 0:
                self._generate_summary()
            
            # Generate comprehensive summary periodically
            if self.summarization_service.should_update_summary():
                self._generate_comprehensive_summary()
                
        except Exception as e:
            logger.error(f"Error analyzing captured content: {e}")
    
    def _find_capture_directory(self) -> Optional[str]:
        """Find the capture output directory"""
        possible_paths = [
            "../screen_capture/capture_output",
            "screen_capture/capture_output",
            "capture_output",
            "../capture_output"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def _analyze_latest_frames(self, capture_dir: str):
        """Analyze the latest captured frames"""
        try:
            # Get all frame files
            frame_files = [f for f in os.listdir(capture_dir) if f.endswith('.jpg')]
            if not frame_files:
                return
            
            # Sort by modification time to get latest
            frame_files.sort(key=lambda x: os.path.getmtime(os.path.join(capture_dir, x)))
            
            # Analyze the most recent frame
            latest_frame = frame_files[-1]
            frame_path = os.path.join(capture_dir, latest_frame)
            
            # Load and analyze frame
            frame = cv2.imread(frame_path)
            if frame is not None:
                # Messenger-specific analysis prompt
                system_prompt = """You are analyzing a Messenger video call or chat interface. 
                Focus on identifying people, their expressions, gestures, and any text or UI elements visible.
                Describe the scene concisely in under 200 characters."""
                
                user_query = "What do you see in this Messenger interface? Focus on people, expressions, and any visible text."
                
                analysis = self.ollama_client.analyze_frame(
                    frame, 
                    system_prompt=system_prompt,
                    user_query=user_query
                )
                
                # Store analysis result
                result = {
                    "timestamp": datetime.now().isoformat(),
                    "frame_file": latest_frame,
                    "analysis": analysis
                }
                
                self.frame_analysis_results.append(result)
                
                # Keep only last 50 results to avoid memory issues
                if len(self.frame_analysis_results) > 50:
                    self.frame_analysis_results = self.frame_analysis_results[-50:]
                
                # Call callback if set
                if self.on_frame_analyzed:
                    self.on_frame_analyzed(result)
                
                logger.info(f"Analyzed frame: {latest_frame}")
                
        except Exception as e:
            logger.error(f"Error analyzing frames: {e}")
    
    def _process_audio_files(self, capture_dir: str):
        """Process audio files for transcription"""
        try:
            # Get audio files
            audio_files = [f for f in os.listdir(capture_dir) if f.endswith('.wav')]
            if not audio_files:
                return
            
            # Process the most recent audio file
            latest_audio = max(audio_files, key=lambda x: os.path.getmtime(os.path.join(capture_dir, x)))
            audio_path = os.path.join(capture_dir, latest_audio)
            
            # Check if we've already processed this file
            if any(result.get("file_path") == audio_path for result in self.audio_analysis_results):
                return
            
            # Process audio file
            audio_result = self.audio_processor.process_audio_file(audio_path)
            
            if audio_result["status"] == "success":
                self.audio_analysis_results.append(audio_result)
                
                # Update combined transcription
                if audio_result.get("transcription"):
                    if self.audio_transcription:
                        self.audio_transcription += f"\n\n--- {latest_audio} ---\n"
                    else:
                        self.audio_transcription = f"--- {latest_audio} ---\n"
                    self.audio_transcription += audio_result["transcription"]
                
                logger.info(f"Processed audio file: {latest_audio}")
                
        except Exception as e:
            logger.error(f"Error processing audio: {e}")
    
    def _generate_summary(self):
        """Generate summary of analyzed content"""
        try:
            if not self.frame_analysis_results:
                return
            
            # Combine frame analyses
            frame_analyses = [result["analysis"] for result in self.frame_analysis_results[-10:]]  # Last 10 analyses
            combined_content = "\n".join([
                f"Frame {i+1}: {analysis}" 
                for i, analysis in enumerate(frame_analyses)
            ])
            
            # Add audio transcription if available
            if self.audio_transcription:
                combined_content += f"\n\nAudio: {self.audio_transcription}"
            
            # Generate summary
            summary_prompt = """Summarize this Messenger conversation content. 
            Focus on key topics discussed, people involved, and important information.
            Keep it concise and under 400 characters."""
            
            self.summary = self.ollama_client.summarize_content(
                combined_content,
                system_prompt=summary_prompt
            )
            
            # Call callback if set
            if self.on_summary_updated:
                self.on_summary_updated(self.summary)
            
            logger.info("Generated summary of analyzed content")
            
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
    
    def _generate_comprehensive_summary(self):
        """Generate comprehensive summary using the summarization service"""
        try:
            if not self.frame_analysis_results and not self.audio_analysis_results:
                return
            
            # Generate comprehensive summary
            self.comprehensive_summary = self.summarization_service.generate_comprehensive_summary(
                frame_analyses=self.frame_analysis_results,
                audio_transcriptions=self.audio_analysis_results,
                session_context={"session_id": getattr(self, 'session_id', None)}
            )
            
            # Update timestamp
            self.summarization_service.update_summary_timestamp()
            
            # Call callback if set
            if self.on_summary_updated:
                self.on_summary_updated(self.comprehensive_summary)
            
            logger.info("Generated comprehensive summary")
            
        except Exception as e:
            logger.error(f"Error generating comprehensive summary: {e}")
    
    def get_analysis_results(self) -> Dict[str, Any]:
        """Get current analysis results"""
        return {
            "session_id": getattr(self, 'session_id', None),
            "is_analyzing": self.is_analyzing,
            "frame_analyses": len(self.frame_analysis_results),
            "latest_analysis": self.frame_analysis_results[-1] if self.frame_analysis_results else None,
            "audio_analyses": len(self.audio_analysis_results),
            "audio_transcription": self.audio_transcription,
            "summary": self.summary,
            "comprehensive_summary": self.comprehensive_summary,
            "timestamp": datetime.now().isoformat()
        }
    
    def save_analysis_results(self, session_id: str):
        """Save analysis results to file"""
        try:
            results = self.get_analysis_results()
            results["frame_analysis_results"] = self.frame_analysis_results
            results["audio_analysis_results"] = self.audio_analysis_results
            
            # Save to session directory
            session_dir = os.path.join(self.output_dir, session_id)
            os.makedirs(session_dir, exist_ok=True)
            
            results_file = os.path.join(session_dir, "analysis_results.json")
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved analysis results to: {results_file}")
            
        except Exception as e:
            logger.error(f"Error saving analysis results: {e}")
    
    def set_analysis_callback(self, callback_type: str, callback: Callable):
        """Set callback for analysis events"""
        if callback_type == "frame_analyzed":
            self.on_frame_analyzed = callback
        elif callback_type == "summary_updated":
            self.on_summary_updated = callback
        else:
            logger.warning(f"Unknown callback type: {callback_type}")
