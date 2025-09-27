#!/usr/bin/env python3
"""
Script to kill Python servers running on the system
Works on Windows, macOS, and Linux
"""

import os
import sys
import signal
import subprocess
import psutil
from typing import List, Tuple

def find_python_processes() -> List[Tuple[int, str, str]]:
    """Find all Python processes and return (pid, name, cmdline)"""
    python_processes = []
    
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                proc_info = proc.info
                name = proc_info['name'].lower()
                cmdline = ' '.join(proc_info['cmdline']) if proc_info['cmdline'] else ''
                
                # Check if it's a Python process
                if ('python' in name or 'python3' in name or 'python.exe' in name):
                    python_processes.append((
                        proc_info['pid'],
                        proc_info['name'],
                        cmdline
                    ))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
                
    except Exception as e:
        print(f"Error finding processes: {e}")
        
    return python_processes

def kill_process(pid: int, force: bool = False) -> bool:
    """Kill a process by PID"""
    try:
        proc = psutil.Process(pid)
        
        if force:
            proc.kill()  # SIGKILL
            print(f"Force killed process {pid}")
        else:
            proc.terminate()  # SIGTERM
            print(f"Terminated process {pid}")
            
        return True
    except psutil.NoSuchProcess:
        print(f"Process {pid} not found")
        return False
    except psutil.AccessDenied:
        print(f"Access denied for process {pid}")
        return False
    except Exception as e:
        print(f"Error killing process {pid}: {e}")
        return False

def kill_python_servers(force: bool = False, interactive: bool = True):
    """Kill Python server processes"""
    print("🔍 Searching for Python processes...")
    
    processes = find_python_processes()
    
    if not processes:
        print("✅ No Python processes found")
        return
    
    print(f"\n📋 Found {len(processes)} Python process(es):")
    print("-" * 80)
    
    server_processes = []
    
    for i, (pid, name, cmdline) in enumerate(processes, 1):
        # Check if it looks like a server process
        is_server = any(keyword in cmdline.lower() for keyword in [
            'app.py', 'server', 'fastapi', 'flask', 'django', 'uvicorn', 
            'gunicorn', 'wsgi', 'asgi', 'http.server', 'python -m http.server',
            'screen_capture', 'gui.py', 'launcher.py'
        ])
        
        status = "🖥️  SERVER" if is_server else "🐍 Python"
        print(f"{i:2d}. {status} | PID: {pid:6d} | {name}")
        print(f"    Command: {cmdline[:100]}{'...' if len(cmdline) > 100 else ''}")
        
        if is_server:
            server_processes.append((pid, name, cmdline))
        print()
    
    if not server_processes:
        print("✅ No Python server processes found")
        return
    
    print(f"🎯 Found {len(server_processes)} server process(es) to kill:")
    
    if interactive:
        response = input("\n❓ Do you want to kill these server processes? (y/N): ").strip().lower()
        if response not in ['y', 'yes']:
            print("❌ Cancelled")
            return
    
    print("\n🔄 Killing server processes...")
    killed_count = 0
    
    for pid, name, cmdline in server_processes:
        print(f"Killing {name} (PID: {pid})...")
        if kill_process(pid, force):
            killed_count += 1
    
    print(f"\n✅ Successfully killed {killed_count}/{len(server_processes)} server processes")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Kill Python server processes")
    parser.add_argument('-f', '--force', action='store_true', 
                       help='Force kill processes (SIGKILL)')
    parser.add_argument('-y', '--yes', action='store_true', 
                       help='Skip confirmation prompt')
    parser.add_argument('-l', '--list', action='store_true', 
                       help='List processes without killing')
    
    args = parser.parse_args()
    
    print("🐍 Python Server Killer")
    print("=" * 50)
    
    if args.list:
        # Just list processes
        processes = find_python_processes()
        if processes:
            print(f"Found {len(processes)} Python processes:")
            for pid, name, cmdline in processes:
                print(f"PID: {pid:6d} | {name} | {cmdline[:80]}")
        else:
            print("No Python processes found")
        return
    
    # Kill processes
    kill_python_servers(force=args.force, interactive=not args.yes)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
