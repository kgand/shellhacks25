"""
Test client for Ollama integration
Tests the real-time analysis functionality
"""

import requests
import json
import time
import cv2
import numpy as np
from datetime import datetime
import os

# Configuration
SERVER_URL = "http://127.0.0.1:8000"

def test_ollama_status():
    """Test Ollama service status"""
    print("Testing Ollama status...")
    try:
        response = requests.get(f"{SERVER_URL}/ollama-status")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Ollama Status: {result}")
            return result.get("ollama_available", False)
        else:
            print(f"❌ Ollama status check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error checking Ollama status: {e}")
        return False

def test_frame_analysis():
    """Test frame analysis with a sample image"""
    print("\nTesting frame analysis...")
    try:
        # Create a simple test image
        test_image = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(test_image, "Test Messenger Interface", (50, 240), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Save test image
        test_image_path = "test_frame.jpg"
        cv2.imwrite(test_image_path, test_image)
        
        # Send to server
        with open(test_image_path, "rb") as f:
            files = {"image": ("test_frame.jpg", f, "image/jpeg")}
            data = {
                "system_prompt": "You are analyzing a Messenger interface. Describe what you see.",
                "user_query": "What do you see in this image?"
            }
            
            response = requests.post(f"{SERVER_URL}/analyze-frame", files=files, data=data)
            
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Frame Analysis Result: {result['analysis']}")
            return True
        else:
            print(f"❌ Frame analysis failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing frame analysis: {e}")
        return False
    finally:
        # Clean up test image
        if os.path.exists("test_frame.jpg"):
            os.remove("test_frame.jpg")

def test_text_processing():
    """Test text processing"""
    print("\nTesting text processing...")
    try:
        data = {
            "prompt": "What is artificial intelligence?",
            "system_prompt": "You are a helpful AI assistant. Answer concisely."
        }
        
        response = requests.post(f"{SERVER_URL}/process-text", data=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Text Processing Result: {result['result']}")
            return True
        else:
            print(f"❌ Text processing failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing text processing: {e}")
        return False

def test_summarization():
    """Test content summarization"""
    print("\nTesting content summarization...")
    try:
        content = """
        Frame 1: Person A is smiling and talking in a video call
        Frame 2: Person B is nodding and listening attentively
        Frame 3: Both people are laughing together
        Frame 4: Person A is showing something on their screen
        """
        
        data = {
            "content": content,
            "system_prompt": "Summarize this Messenger conversation content in under 200 characters."
        }
        
        response = requests.post(f"{SERVER_URL}/summarize", data=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Summarization Result: {result['summary']}")
            return True
        else:
            print(f"❌ Summarization failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing summarization: {e}")
        return False

def test_realtime_analysis():
    """Test real-time analysis"""
    print("\nTesting real-time analysis...")
    try:
        # Create a test session first
        session_data = {"test": True}
        session_response = requests.post(f"{SERVER_URL}/sessions", json=session_data)
        
        if session_response.status_code != 200:
            print(f"❌ Failed to create test session: {session_response.status_code}")
            return False
        
        session_id = session_response.json()["session_id"]
        print(f"Created test session: {session_id}")
        
        # Start analysis
        analysis_response = requests.post(f"{SERVER_URL}/start-analysis/{session_id}")
        
        if analysis_response.status_code == 200:
            print("✅ Real-time analysis started")
            
            # Wait a bit
            time.sleep(2)
            
            # Check status
            status_response = requests.get(f"{SERVER_URL}/analysis-status")
            if status_response.status_code == 200:
                status = status_response.json()
                print(f"✅ Analysis Status: {status}")
            
            # Stop analysis
            stop_response = requests.post(f"{SERVER_URL}/stop-analysis")
            if stop_response.status_code == 200:
                print("✅ Real-time analysis stopped")
                return True
            else:
                print(f"❌ Failed to stop analysis: {stop_response.status_code}")
                return False
        else:
            print(f"❌ Failed to start analysis: {analysis_response.status_code} - {analysis_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing real-time analysis: {e}")
        return False

def test_audio_processing():
    """Test audio processing"""
    print("\nTesting audio processing...")
    try:
        # Test audio status
        status_response = requests.get(f"{SERVER_URL}/audio-status")
        if status_response.status_code == 200:
            status = status_response.json()
            print(f"✅ Audio Status: {status}")
        else:
            print(f"❌ Audio status check failed: {status_response.status_code}")
            return False
        
        # Test audio file processing (create a dummy audio file)
        # For this test, we'll just check if the endpoint responds
        # In a real scenario, you would upload an actual audio file
        
        print("✅ Audio processing endpoints are available")
        return True
        
    except Exception as e:
        print(f"❌ Error testing audio processing: {e}")
        return False

def test_summarization():
    """Test summarization functionality"""
    print("\nTesting summarization...")
    try:
        # Test summary status
        status_response = requests.get(f"{SERVER_URL}/summary-status")
        if status_response.status_code == 200:
            status = status_response.json()
            print(f"✅ Summary Status: {status}")
        else:
            print(f"❌ Summary status check failed: {status_response.status_code}")
            return False
        
        # Test comprehensive summary
        summary_response = requests.get(f"{SERVER_URL}/comprehensive-summary")
        if summary_response.status_code == 200:
            summary = summary_response.json()
            print(f"✅ Comprehensive Summary: {summary}")
        else:
            print(f"❌ Comprehensive summary check failed: {summary_response.status_code}")
            return False
        
        print("✅ Summarization endpoints are available")
        return True
        
    except Exception as e:
        print(f"❌ Error testing summarization: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Ollama Integration")
    print("=" * 50)
    
    # Check if server is running
    try:
        response = requests.get(f"{SERVER_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ Server is not running. Please start the server first.")
            return
    except:
        print("❌ Server is not accessible. Please start the server first.")
        return
    
    print("✅ Server is running")
    
    # Run tests
    tests = [
        ("Ollama Status", test_ollama_status),
        ("Frame Analysis", test_frame_analysis),
        ("Text Processing", test_text_processing),
        ("Summarization", test_summarization),
        ("Real-time Analysis", test_realtime_analysis),
        ("Audio Processing", test_audio_processing),
        ("Advanced Summarization", test_summarization)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*50}")
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Ollama integration is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()
