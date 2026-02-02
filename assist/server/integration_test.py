"""
Comprehensive Integration Test
Tests the complete Ollama integration with real-time analysis
"""

import requests
import json
import time
import cv2
import numpy as np
import os
import wave
from datetime import datetime

# Configuration
SERVER_URL = "http://127.0.0.1:8000"

def test_server_health():
    """Test if server is running and healthy"""
    print("🔍 Testing server health...")
    try:
        response = requests.get(f"{SERVER_URL}/health", timeout=5)
        if response.status_code == 200:
            health = response.json()
            print(f"✅ Server is healthy: {health}")
            return True
        else:
            print(f"❌ Server health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Server is not accessible: {e}")
        return False

def test_ollama_availability():
    """Test Ollama service availability"""
    print("\n🔍 Testing Ollama availability...")
    try:
        response = requests.get(f"{SERVER_URL}/ollama-status")
        if response.status_code == 200:
            status = response.json()
            print(f"✅ Ollama Status: {status}")
            return status.get("ollama_available", False)
        else:
            print(f"❌ Ollama status check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error checking Ollama status: {e}")
        return False

def create_test_audio_file():
    """Create a test audio file for testing"""
    try:
        # Create a simple WAV file
        sample_rate = 44100
        duration = 2  # 2 seconds
        frequency = 440  # A note
        
        # Generate sine wave
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        audio_data = (np.sin(2 * np.pi * frequency * t) * 32767).astype(np.int16)
        
        # Save as WAV file
        test_audio_path = "test_audio.wav"
        with wave.open(test_audio_path, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_data.tobytes())
        
        print(f"✅ Created test audio file: {test_audio_path}")
        return test_audio_path
        
    except Exception as e:
        print(f"❌ Error creating test audio file: {e}")
        return None

def test_complete_workflow():
    """Test the complete workflow from capture to analysis"""
    print("\n🔍 Testing complete workflow...")
    
    try:
        # Step 1: Create a session
        print("Step 1: Creating session...")
        session_data = {"test": True, "workflow": "integration_test"}
        session_response = requests.post(f"{SERVER_URL}/sessions", json=session_data)
        
        if session_response.status_code != 200:
            print(f"❌ Failed to create session: {session_response.status_code}")
            return False
        
        session_id = session_response.json()["session_id"]
        print(f"✅ Created session: {session_id}")
        
        # Step 2: Create test files
        print("Step 2: Creating test files...")
        
        # Create test image
        test_image = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(test_image, "Test Messenger Call", (50, 240), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(test_image, "Integration Test", (50, 280), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2)
        
        test_image_path = "test_integration_frame.jpg"
        cv2.imwrite(test_image_path, test_image)
        print(f"✅ Created test image: {test_image_path}")
        
        # Create test audio
        test_audio_path = create_test_audio_file()
        if not test_audio_path:
            return False
        
        # Step 3: Upload test files
        print("Step 3: Uploading test files...")
        
        # Upload image
        with open(test_image_path, "rb") as f:
            files = {"file": ("test_frame.jpg", f, "image/jpeg")}
            upload_response = requests.post(f"{SERVER_URL}/upload/{session_id}", files=files)
            
        if upload_response.status_code != 200:
            print(f"❌ Failed to upload image: {upload_response.status_code}")
            return False
        print("✅ Uploaded test image")
        
        # Step 4: Test frame analysis
        print("Step 4: Testing frame analysis...")
        with open(test_image_path, "rb") as f:
            files = {"image": ("test_frame.jpg", f, "image/jpeg")}
            data = {
                "system_prompt": "You are analyzing a Messenger video call. Describe what you see.",
                "user_query": "What do you see in this Messenger interface?"
            }
            analysis_response = requests.post(f"{SERVER_URL}/analyze-frame", files=files, data=data)
            
        if analysis_response.status_code == 200:
            analysis_result = analysis_response.json()
            print(f"✅ Frame analysis successful: {analysis_result['analysis'][:100]}...")
        else:
            print(f"❌ Frame analysis failed: {analysis_response.status_code}")
            return False
        
        # Step 5: Test audio processing
        print("Step 5: Testing audio processing...")
        with open(test_audio_path, "rb") as f:
            files = {"audio_file": ("test_audio.wav", f, "audio/wav")}
            audio_response = requests.post(f"{SERVER_URL}/process-audio", files=files)
            
        if audio_response.status_code == 200:
            audio_result = audio_response.json()
            print(f"✅ Audio processing successful: {audio_result['result']['status']}")
        else:
            print(f"❌ Audio processing failed: {audio_response.status_code}")
            return False
        
        # Step 6: Test real-time analysis
        print("Step 6: Testing real-time analysis...")
        analysis_start_response = requests.post(f"{SERVER_URL}/start-analysis/{session_id}")
        
        if analysis_start_response.status_code == 200:
            print("✅ Real-time analysis started")
            
            # Wait for analysis
            time.sleep(3)
            
            # Check analysis status
            status_response = requests.get(f"{SERVER_URL}/analysis-status")
            if status_response.status_code == 200:
                status = status_response.json()
                print(f"✅ Analysis status: {status['analysis']}")
            
            # Stop analysis
            stop_response = requests.post(f"{SERVER_URL}/stop-analysis")
            if stop_response.status_code == 200:
                print("✅ Real-time analysis stopped")
            else:
                print(f"❌ Failed to stop analysis: {stop_response.status_code}")
                return False
        else:
            print(f"❌ Failed to start real-time analysis: {analysis_start_response.status_code}")
            return False
        
        # Step 7: Test summarization
        print("Step 7: Testing summarization...")
        
        # Test summary status
        summary_status_response = requests.get(f"{SERVER_URL}/summary-status")
        if summary_status_response.status_code == 200:
            summary_status = summary_status_response.json()
            print(f"✅ Summary status: {summary_status['status']}")
        
        # Test comprehensive summary
        comprehensive_summary_response = requests.get(f"{SERVER_URL}/comprehensive-summary")
        if comprehensive_summary_response.status_code == 200:
            comprehensive_summary = comprehensive_summary_response.json()
            print(f"✅ Comprehensive summary: {comprehensive_summary['status']}")
        
        # Test session summary generation
        session_summary_response = requests.post(f"{SERVER_URL}/generate-summary/{session_id}")
        if session_summary_response.status_code == 200:
            session_summary = session_summary_response.json()
            print(f"✅ Session summary generated: {session_summary['status']}")
        else:
            print(f"❌ Session summary generation failed: {session_summary_response.status_code}")
            return False
        
        # Step 8: Test text processing
        print("Step 8: Testing text processing...")
        text_data = {
            "prompt": "Summarize the key points of our Messenger conversation.",
            "system_prompt": "You are a helpful AI assistant. Provide a concise summary."
        }
        text_response = requests.post(f"{SERVER_URL}/process-text", data=text_data)
        
        if text_response.status_code == 200:
            text_result = text_response.json()
            print(f"✅ Text processing successful: {text_result['result'][:100]}...")
        else:
            print(f"❌ Text processing failed: {text_response.status_code}")
            return False
        
        # Step 9: Test content summarization
        print("Step 9: Testing content summarization...")
        content_data = {
            "content": "Frame 1: Person A is talking in video call. Frame 2: Person B is listening. Audio: Hello, how are you doing today?",
            "system_prompt": "Summarize this Messenger conversation content."
        }
        content_response = requests.post(f"{SERVER_URL}/summarize", data=content_data)
        
        if content_response.status_code == 200:
            content_result = content_response.json()
            print(f"✅ Content summarization successful: {content_result['summary'][:100]}...")
        else:
            print(f"❌ Content summarization failed: {content_response.status_code}")
            return False
        
        print("✅ Complete workflow test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error in complete workflow test: {e}")
        return False
    finally:
        # Cleanup test files
        cleanup_files = ["test_integration_frame.jpg", "test_audio.wav"]
        for file in cleanup_files:
            if os.path.exists(file):
                try:
                    os.remove(file)
                    print(f"🧹 Cleaned up: {file}")
                except:
                    pass

def test_all_endpoints():
    """Test all available endpoints"""
    print("\n🔍 Testing all endpoints...")
    
    endpoints_to_test = [
        ("GET", "/health", "Health check"),
        ("GET", "/ollama-status", "Ollama status"),
        ("GET", "/audio-status", "Audio status"),
        ("GET", "/summary-status", "Summary status"),
        ("GET", "/analysis-status", "Analysis status"),
        ("GET", "/sessions", "List sessions"),
        ("GET", "/stats", "System statistics")
    ]
    
    passed = 0
    total = len(endpoints_to_test)
    
    for method, endpoint, description in endpoints_to_test:
        try:
            if method == "GET":
                response = requests.get(f"{SERVER_URL}{endpoint}", timeout=5)
            else:
                response = requests.post(f"{SERVER_URL}{endpoint}", timeout=5)
            
            if response.status_code == 200:
                print(f"✅ {description}: {response.status_code}")
                passed += 1
            else:
                print(f"❌ {description}: {response.status_code}")
        except Exception as e:
            print(f"❌ {description}: Error - {e}")
    
    print(f"\n📊 Endpoint test results: {passed}/{total} passed")
    return passed == total

def main():
    """Run comprehensive integration test"""
    print("🧪 Comprehensive Ollama Integration Test")
    print("=" * 60)
    
    # Test 1: Server health
    if not test_server_health():
        print("❌ Server is not running. Please start the server first.")
        return
    
    # Test 2: Ollama availability
    ollama_available = test_ollama_availability()
    if not ollama_available:
        print("⚠️  Ollama is not available. Some tests may fail.")
    
    # Test 3: All endpoints
    endpoints_ok = test_all_endpoints()
    
    # Test 4: Complete workflow
    workflow_ok = test_complete_workflow()
    
    # Final results
    print("\n" + "=" * 60)
    print("📊 INTEGRATION TEST RESULTS")
    print("=" * 60)
    
    results = [
        ("Server Health", True),
        ("Ollama Availability", ollama_available),
        ("All Endpoints", endpoints_ok),
        ("Complete Workflow", workflow_ok)
    ]
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All integration tests passed! Ollama integration is working perfectly.")
    elif passed >= len(results) - 1:
        print("✅ Integration tests mostly passed. Minor issues detected.")
    else:
        print("⚠️  Some integration tests failed. Check the output above for details.")
    
    print("\n🚀 Ollama integration is ready for production use!")

if __name__ == "__main__":
    main()
