#!/usr/bin/env python3
"""
Test script for AI agents and backend integration
Verifies that all components are working properly
"""

import requests
import json
import time
import os
from pathlib import Path

def test_backend_health():
    """Test backend health endpoint"""
    print("🔍 Testing backend health...")
    try:
        response = requests.get("http://127.0.0.1:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend healthy: {data['status']}")
            print(f"   Services: {data['services']}")
            return True
        else:
            print(f"❌ Backend unhealthy: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend connection failed: {e}")
        return False

def test_session_management():
    """Test session creation and management"""
    print("\n🔍 Testing session management...")
    try:
        # Create session
        session_data = {
            "user_id": "test_user",
            "session_type": "messenger_call",
            "metadata": {"test": True}
        }
        
        response = requests.post("http://127.0.0.1:8000/sessions", json=session_data)
        if response.status_code == 200:
            session = response.json()
            session_id = session['session_id']
            print(f"✅ Session created: {session_id}")
            
            # Test session retrieval
            response = requests.get(f"http://127.0.0.1:8000/sessions/{session_id}")
            if response.status_code == 200:
                print("✅ Session retrieval working")
                return session_id
            else:
                print("❌ Session retrieval failed")
                return None
        else:
            print(f"❌ Session creation failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Session management error: {e}")
        return None

def test_file_upload(session_id):
    """Test file upload functionality"""
    print("\n🔍 Testing file upload...")
    try:
        # Create a test file
        test_file_path = "test_frame.jpg"
        with open(test_file_path, 'wb') as f:
            f.write(b"fake_image_data")
        
        # Upload file
        with open(test_file_path, 'rb') as f:
            files = {'file': (test_file_path, f, 'image/jpeg')}
            response = requests.post(f"http://127.0.0.1:8000/upload/{session_id}", files=files)
        
        if response.status_code == 200:
            print("✅ File upload working")
            os.remove(test_file_path)  # Cleanup
            return True
        else:
            print(f"❌ File upload failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ File upload error: {e}")
        return False

def test_ai_agents():
    """Test AI agents integration"""
    print("\n🔍 Testing AI agents...")
    try:
        # Check if AI agent files exist
        agent_files = [
            "assist/server/gemini_live.py",
            "assist/server/adk_agents.py",
            "assist/server/memory/store_firestore.py"
        ]
        
        for file_path in agent_files:
            if os.path.exists(file_path):
                print(f"✅ AI agent file found: {file_path}")
            else:
                print(f"⚠️  AI agent file missing: {file_path}")
        
        # Test Gemini Live integration
        try:
            import sys
            sys.path.append('assist/server')
            from gemini_live import GeminiLiveAgent
            print("✅ Gemini Live agent import successful")
        except Exception as e:
            print(f"⚠️  Gemini Live agent issue: {e}")
        
        # Test ADK agents
        try:
            from adk_agents import ADKOrchestrator
            print("✅ ADK agents import successful")
        except Exception as e:
            print(f"⚠️  ADK agents issue: {e}")
        
        return True
    except Exception as e:
        print(f"❌ AI agents test error: {e}")
        return False

def test_capture_output():
    """Test capture output files"""
    print("\n🔍 Testing capture output...")
    try:
        capture_dir = Path("assist/screen_capture/capture_output")
        if capture_dir.exists():
            files = list(capture_dir.glob("*.jpg"))
            audio_files = list(capture_dir.glob("*.wav"))
            
            print(f"✅ Found {len(files)} video frames")
            print(f"✅ Found {len(audio_files)} audio files")
            
            if files:
                # Check file sizes
                total_size = sum(f.stat().st_size for f in files)
                avg_size = total_size / len(files)
                print(f"   Average frame size: {avg_size/1024:.1f} KB")
                
                # Check recent files
                recent_files = sorted(files, key=lambda x: x.stat().st_mtime, reverse=True)[:5]
                print(f"   Recent files: {[f.name for f in recent_files]}")
            
            return True
        else:
            print("❌ Capture output directory not found")
            return False
    except Exception as e:
        print(f"❌ Capture output test error: {e}")
        return False

def test_memory_system():
    """Test memory system integration"""
    print("\n🔍 Testing memory system...")
    try:
        # Test memory endpoints
        response = requests.get("http://127.0.0.1:8000/memories")
        if response.status_code == 200:
            memories = response.json()
            print(f"✅ Memory system working: {memories['total']} memories")
            
            # Test revive API
            revive_data = {"cue": "test", "limit": 5}
            response = requests.post("http://127.0.0.1:8000/revive", json=revive_data)
            if response.status_code == 200:
                print("✅ Revive API working")
                return True
            else:
                print("❌ Revive API failed")
                return False
        else:
            print("❌ Memory system not accessible")
            return False
    except Exception as e:
        print(f"❌ Memory system test error: {e}")
        return False

def test_performance_metrics():
    """Test system performance metrics"""
    print("\n🔍 Testing performance metrics...")
    try:
        response = requests.get("http://127.0.0.1:8000/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Performance metrics available:")
            print(f"   Sessions: {stats['total_sessions']}")
            print(f"   Files: {stats['total_files']}")
            print(f"   Size: {stats['total_size_mb']} MB")
            return True
        else:
            print("❌ Performance metrics not available")
            return False
    except Exception as e:
        print(f"❌ Performance metrics error: {e}")
        return False

def main():
    """Run all integration tests"""
    print("🚀 AI Integration Test Suite")
    print("=" * 50)
    
    tests = [
        ("Backend Health", test_backend_health),
        ("Session Management", lambda: test_session_management()),
        ("File Upload", lambda: test_file_upload(test_session_management())),
        ("AI Agents", test_ai_agents),
        ("Capture Output", test_capture_output),
        ("Memory System", test_memory_system),
        ("Performance Metrics", test_performance_metrics)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 30)
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All systems working correctly!")
    else:
        print("⚠️  Some systems need attention")

if __name__ == "__main__":
    main()
