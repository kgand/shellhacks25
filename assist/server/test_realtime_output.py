#!/usr/bin/env python3
"""
Test script for real-time output functionality
Demonstrates how to monitor real-time AI analysis outputs
"""

import requests
import time
import json
from datetime import datetime

def test_realtime_outputs():
    """Test the real-time output functionality"""
    base_url = "http://127.0.0.1:8000"
    
    print("🧪 Testing Real-time Output Functionality")
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
                print("❌ Ollama is not available")
        else:
            print(f"❌ Ollama status check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking Ollama: {e}")
    
    # Test 3: Get current analysis status
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
            
            if analysis.get('latest_realtime_output'):
                latest = analysis['latest_realtime_output']
                print(f"   Latest output: {latest.get('type', 'unknown')} - {latest.get('content', 'No content')[:100]}...")
        else:
            print(f"❌ Analysis status check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking analysis status: {e}")
    
    # Test 4: Get real-time outputs
    print("\n4. Getting real-time outputs...")
    try:
        response = requests.get(f"{base_url}/realtime-outputs?limit=10", timeout=5)
        if response.status_code == 200:
            data = response.json()
            outputs = data.get("outputs", [])
            
            print(f"   Found {len(outputs)} real-time outputs")
            
            if outputs:
                print("\n   Recent outputs:")
                for i, output in enumerate(outputs[-5:], 1):  # Show last 5
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
    
    # Test 5: Get latest real-time output
    print("\n5. Getting latest real-time output...")
    try:
        response = requests.get(f"{base_url}/latest-realtime-output", timeout=5)
        if response.status_code == 200:
            data = response.json()
            
            if data.get("status") == "success":
                output = data.get("output", {})
                print(f"   Latest output type: {output.get('type', 'unknown')}")
                print(f"   Latest output content: {output.get('content', 'No content')[:150]}...")
            else:
                print(f"   {data.get('message', 'No output available')}")
        else:
            print(f"❌ Latest output check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting latest output: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Real-time Output Test Complete")
    print("\nTo see live real-time outputs:")
    print("1. Start the screen capture GUI")
    print("2. Click 'Start AI Analysis'")
    print("3. Click 'View Real-time Output' to see live updates")
    print("4. Or monitor the activity log for real-time updates")

if __name__ == "__main__":
    test_realtime_outputs()
