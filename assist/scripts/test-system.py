#!/usr/bin/env python3
"""
Test script for Messenger AI Assistant system
Run this to verify all components are working correctly
"""

import asyncio
import aiohttp
import json
import sys
import time
from pathlib import Path

class SystemTester:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"
        self.results = {}
    
    async def test_backend_health(self):
        """Test if backend is running and healthy"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/health") as response:
                    if response.status == 200:
                        data = await response.json()
                        self.results['backend_health'] = {
                            'status': 'PASS',
                            'data': data
                        }
                        return True
                    else:
                        self.results['backend_health'] = {
                            'status': 'FAIL',
                            'error': f'HTTP {response.status}'
                        }
                        return False
        except Exception as e:
            self.results['backend_health'] = {
                'status': 'FAIL',
                'error': str(e)
            }
            return False
    
    async def test_websocket_connection(self):
        """Test WebSocket connection"""
        try:
            import websockets
            async with websockets.connect(f"ws://127.0.0.1:8765/ingest") as websocket:
                # Send a test message
                test_message = json.dumps({
                    "type": "test",
                    "data": "test connection"
                })
                await websocket.send(test_message)
                
                self.results['websocket'] = {
                    'status': 'PASS',
                    'message': 'WebSocket connection successful'
                }
                return True
        except Exception as e:
            self.results['websocket'] = {
                'status': 'FAIL',
                'error': str(e)
            }
            return False
    
    async def test_revive_api(self):
        """Test the revive API endpoint"""
        try:
            async with aiohttp.ClientSession() as session:
                test_data = {
                    "cue": "test query",
                    "limit": 5
                }
                async with session.post(
                    f"{self.base_url}/revive",
                    json=test_data
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.results['revive_api'] = {
                            'status': 'PASS',
                            'data': data
                        }
                        return True
                    else:
                        self.results['revive_api'] = {
                            'status': 'FAIL',
                            'error': f'HTTP {response.status}'
                        }
                        return False
        except Exception as e:
            self.results['revive_api'] = {
                'status': 'FAIL',
                'error': str(e)
            }
            return False
    
    async def test_memory_statistics(self):
        """Test memory statistics endpoint"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/memories/default/statistics") as response:
                    if response.status == 200:
                        data = await response.json()
                        self.results['memory_stats'] = {
                            'status': 'PASS',
                            'data': data
                        }
                        return True
                    else:
                        self.results['memory_stats'] = {
                            'status': 'FAIL',
                            'error': f'HTTP {response.status}'
                        }
                        return False
        except Exception as e:
            self.results['memory_stats'] = {
                'status': 'FAIL',
                'error': str(e)
            }
            return False
    
    def check_chrome_extension(self):
        """Check if Chrome extension files exist"""
        extension_path = Path("assist/chrome-ext/dist")
        manifest_path = extension_path / "manifest.json"
        
        if manifest_path.exists():
            self.results['chrome_extension'] = {
                'status': 'PASS',
                'message': 'Extension files found'
            }
            return True
        else:
            self.results['chrome_extension'] = {
                'status': 'FAIL',
                'error': 'Extension not built. Run: make chrome-build'
            }
            return False
    
    def check_environment(self):
        """Check environment variables and configuration"""
        import os
        
        # For simplified mode, we don't require Google Cloud variables
        optional_vars = [
            'GOOGLE_PROJECT_ID',
            'GEMINI_API_KEY'
        ]
        
        missing_vars = []
        for var in optional_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            self.results['environment'] = {
                'status': 'WARN',
                'message': f'Optional environment variables missing: {", ".join(missing_vars)} (simplified mode)'
            }
            return True  # Don't fail for missing optional vars
        else:
            self.results['environment'] = {
                'status': 'PASS',
                'message': 'Environment variables configured'
            }
            return True
    
    async def run_all_tests(self):
        """Run all tests and return results"""
        print("🧪 Testing Messenger AI Assistant System...")
        print("=" * 50)
        
        # Check environment first
        env_ok = self.check_environment()
        print(f"Environment: {'✅' if env_ok else '❌'}")
        
        # Check Chrome extension
        ext_ok = self.check_chrome_extension()
        print(f"Chrome Extension: {'✅' if ext_ok else '❌'}")
        
        # Test backend health
        backend_ok = await self.test_backend_health()
        print(f"Backend Health: {'✅' if backend_ok else '❌'}")
        
        if backend_ok:
            # Test other endpoints
            websocket_ok = await self.test_websocket_connection()
            print(f"WebSocket: {'✅' if websocket_ok else '❌'}")
            
            revive_ok = await self.test_revive_api()
            print(f"Revive API: {'✅' if revive_ok else '❌'}")
            
            memory_ok = await self.test_memory_statistics()
            print(f"Memory Stats: {'✅' if memory_ok else '❌'}")
        
        print("=" * 50)
        
        # Summary
        total_tests = len(self.results)
        passed_tests = sum(1 for result in self.results.values() if result['status'] == 'PASS')
        
        print(f"📊 Results: {passed_tests}/{total_tests} tests passed")
        
        if passed_tests == total_tests:
            print("🎉 All tests passed! System is ready to use.")
            return True
        else:
            print("⚠️  Some tests failed. Check the details above.")
            return False
    
    def print_detailed_results(self):
        """Print detailed test results"""
        print("\n📋 Detailed Results:")
        print("-" * 30)
        
        for test_name, result in self.results.items():
            status_icon = "✅" if result['status'] == 'PASS' else "❌"
            print(f"{status_icon} {test_name.replace('_', ' ').title()}")
            
            if result['status'] == 'PASS':
                if 'message' in result:
                    print(f"   {result['message']}")
            else:
                print(f"   Error: {result['error']}")
            print()

async def main():
    """Main test function"""
    tester = SystemTester()
    
    try:
        success = await tester.run_all_tests()
        tester.print_detailed_results()
        
        if not success:
            print("\n🔧 Troubleshooting Tips:")
            print("1. Make sure the backend is running: make dev")
            print("2. Check your .env file has all required variables")
            print("3. Build the Chrome extension: make chrome-build")
            print("4. Check the logs for detailed error messages")
            sys.exit(1)
        else:
            print("\n🚀 Ready to test the Chrome extension!")
            print("1. Load the extension in Chrome from assist/chrome-ext/dist")
            print("2. Go to messenger.com")
            print("3. Open the extension side panel")
            print("4. Test the recording functionality")
    
    except KeyboardInterrupt:
        print("\n⏹️  Testing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
