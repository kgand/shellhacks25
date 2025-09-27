#!/usr/bin/env python3
"""
Real-time system monitoring script
Shows live status of capture system and AI agents
"""

import requests
import time
import os
from pathlib import Path
from datetime import datetime

def get_system_status():
    """Get current system status"""
    try:
        response = requests.get("http://127.0.0.1:8000/health", timeout=2)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def get_capture_stats():
    """Get capture statistics"""
    try:
        response = requests.get("http://127.0.0.1:8000/stats", timeout=2)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def get_recent_files():
    """Get recent capture files"""
    try:
        capture_dir = Path("assist/screen_capture/capture_output")
        if capture_dir.exists():
            files = list(capture_dir.glob("*.jpg"))
            audio_files = list(capture_dir.glob("*.wav"))
            
            # Sort by modification time
            files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            audio_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            return {
                'video_files': len(files),
                'audio_files': len(audio_files),
                'latest_video': files[0].name if files else None,
                'latest_audio': audio_files[0].name if audio_files else None,
                'total_size': sum(f.stat().st_size for f in files + audio_files)
            }
        return None
    except:
        return None

def monitor_loop():
    """Main monitoring loop"""
    print("🔍 Messenger AI Assistant Monitor")
    print("=" * 40)
    print("Press Ctrl+C to stop monitoring")
    print()
    
    try:
        while True:
            # Clear screen (works on most terminals)
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print("🔍 Messenger AI Assistant Monitor")
            print("=" * 40)
            print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
            print()
            
            # Backend status
            status = get_system_status()
            if status:
                print("🖥️  Backend Status:")
                print(f"   Status: {status['status']}")
                print(f"   Services: {status['services']}")
                print(f"   Connections: {status['connections']}")
                print(f"   Memories: {status['memories_count']}")
            else:
                print("❌ Backend: Not accessible")
            
            print()
            
            # Capture stats
            stats = get_capture_stats()
            if stats:
                print("📊 Capture Statistics:")
                print(f"   Sessions: {stats['total_sessions']}")
                print(f"   Files: {stats['total_files']}")
                print(f"   Size: {stats['total_size_mb']} MB")
                print(f"   Active Sessions: {stats['active_sessions']}")
            else:
                print("❌ Capture Stats: Not available")
            
            print()
            
            # File monitoring
            files = get_recent_files()
            if files:
                print("📁 Recent Files:")
                print(f"   Video Files: {files['video_files']}")
                print(f"   Audio Files: {files['audio_files']}")
                if files['latest_video']:
                    print(f"   Latest Video: {files['latest_video']}")
                if files['latest_audio']:
                    print(f"   Latest Audio: {files['latest_audio']}")
                print(f"   Total Size: {files['total_size']/1024/1024:.1f} MB")
            else:
                print("❌ Files: No capture output found")
            
            print()
            print("Press Ctrl+C to stop...")
            
            time.sleep(2)  # Update every 2 seconds
            
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped")

if __name__ == "__main__":
    monitor_loop()
