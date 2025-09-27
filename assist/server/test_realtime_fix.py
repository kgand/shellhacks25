#!/usr/bin/env python3
"""
Test script to verify real-time analysis fixes
"""

import requests
import time
import json
from datetime import datetime

def test_realtime_analysis_fix():
    """Test the real-time analysis fixes"""
    base_url = "http://127.0.0.1:8000"
    
    print("🔧 Testing Real-time Analysis Fixes")
    print("=" * 50)
    
    # Test 1: Check server health
    print("1. Checking server health...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running")
        else:
            print(f"❌ Server health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        return
    
    # Test 2: Check Ollama status
    print("\n2. Checking Ollama status...")
    try:
        response = requests.get(f"{base_url}/ollama-status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("ollama_available"):
                print("✅ Ollama is available")
            else:
                print("❌ Ollama is not available - this will prevent real-time analysis")
        else:
            print(f"❌ Ollama status check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking Ollama: {e}")
    
    # Test 3: Check analysis status
    print("\n3. Checking analysis status...")
    try:
        response = requests.get(f"{base_url}/analysis-status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            analysis = data.get("analysis", {})
            
            print(f"   Analysis active: {analysis.get('is_analyzing', False)}")
            print(f"   Frame analyses: {analysis.get('frame_analyses', 0)}")
            print(f"   Audio analyses: {analysis.get('audio_analyses', 0)}")
            print(f"   Real-time outputs: {analysis.get('realtime_outputs_count', 0)}")
            print(f"   Analysis stream active: {analysis.get('analysis_stream_active', False)}")
            
            if analysis.get('is_analyzing') and analysis.get('realtime_outputs_count', 0) == 0:
                print("⚠️  WARNING: Analysis is active but no real-time outputs detected")
                print("   This suggests the capture directory detection may still have issues")
            elif analysis.get('realtime_outputs_count', 0) > 0:
                print("✅ Real-time analysis is working correctly")
        else:
            print(f"❌ Analysis status check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking analysis status: {e}")
    
    # Test 4: Test real-time outputs
    print("\n4. Testing real-time outputs...")
    try:
        response = requests.get(f"{base_url}/realtime-outputs?limit=5", timeout=5)
        if response.status_code == 200:
            data = response.json()
            outputs = data.get("outputs", [])
            
            print(f"   Found {len(outputs)} real-time outputs")
            
            if outputs:
                print("   Recent outputs:")
                for i, output in enumerate(outputs[-3:], 1):  # Show last 3
                    timestamp = output.get("timestamp", "Unknown")
                    output_type = output.get("type", "unknown")
                    content = output.get("content", "No content")
                    
                    print(f"   {i}. [{timestamp}] {output_type.upper()}")
                    print(f"      {content[:100]}{'...' if len(content) > 100 else ''}")
                    print()
            else:
                print("   No real-time outputs available yet")
        else:
            print(f"❌ Real-time outputs check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting real-time outputs: {e}")
    
    # Test 5: Test capture directory detection
    print("\n5. Testing capture directory detection...")
    try:
        import os
        possible_paths = [
            "capture_output",
            "../capture_output",
            "../screen_capture/capture_output",
            "screen_capture/capture_output"
        ]
        
        found_paths = []
        for path in possible_paths:
            if os.path.exists(path):
                frame_count = len([f for f in os.listdir(path) if f.endswith('.jpg')])
                found_paths.append(f"{path} ({frame_count} frames)")
        
        if found_paths:
            print("✅ Found capture directories:")
            for path in found_paths:
                print(f"   - {path}")
        else:
            print("❌ No capture directories found")
            print("   This will prevent real-time analysis from working")
    except Exception as e:
        print(f"❌ Error checking capture directories: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Real-time Analysis Fix Test Complete")
    print("\nIf real-time analysis is still not working:")
    print("1. Ensure Ollama is running: ollama serve")
    print("2. Check that capture_output directory exists and has frames")
    print("3. Verify the server is running from the correct directory")
    print("4. Check server logs for any error messages")

if __name__ == "__main__":
    test_realtime_analysis_fix()
