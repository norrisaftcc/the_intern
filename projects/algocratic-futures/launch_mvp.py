#!/usr/bin/env python3
"""
AlgoCratic Futures MVP Launcher
Gets the boardwalk arcade up and running quickly
"""

import os
import sys
import subprocess
import time

def check_requirements():
    """Check if required packages are installed"""
    try:
        import adventurelib
        import fastapi
        import yaml
        print("✅ All requirements installed")
        return True
    except ImportError as e:
        print(f"❌ Missing requirement: {e}")
        print("Installing requirements...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"])
        return False

def launch_options():
    print("""
╔═══════════════════════════════════════════════════════════════╗
║           ALGOCRATIC FUTURES - MVP LAUNCH OPTIONS             ║
╚═══════════════════════════════════════════════════════════════╝

1. Terminal MUD (adventurelib) - Pier & Arcade Tutorial
2. Terminal MUD (room system) - Full room exploration with YAML
3. Web Interface (FastAPI) - Full corporate experience  
4. Both adventurelib + web (recommended for development)

Select option (1-4): """, end="")
    
    choice = input().strip()
    return choice

def launch_terminal_mud():
    """Launch the adventurelib version"""
    print("\n🎮 Starting Terminal MUD (adventurelib)...")
    print("=" * 60)
    os.chdir("backend")
    subprocess.run([sys.executable, "mud_game.py"])

def launch_room_system_mud():
    """Launch the room system version"""
    print("\n🏢 Starting Terminal MUD (room system)...")
    print("=" * 60)
    os.chdir("backend")
    subprocess.run([sys.executable, "terminal_mud.py"])

def launch_web_interface():
    """Launch the FastAPI backend"""
    print("\n🌐 Starting Web Interface...")
    print("Backend starting on http://localhost:8000")
    print("Open frontend/index.html in a browser")
    print("=" * 60)
    os.chdir("backend")
    subprocess.run([sys.executable, "app.py"])

def launch_both():
    """Launch both in separate processes"""
    print("\n🚀 Starting both systems...")
    
    # Start backend in background
    backend_process = subprocess.Popen(
        [sys.executable, "backend/app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    print("Backend started on http://localhost:8000")
    time.sleep(2)  # Give backend time to start
    
    # Open browser
    try:
        import webbrowser
        webbrowser.open("file://" + os.path.abspath("frontend/index.html"))
    except:
        print("Please open frontend/index.html in your browser")
    
    print("\nPress Ctrl+C to stop all services")
    
    try:
        # Keep running
        backend_process.wait()
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        backend_process.terminate()

def main():
    print("""
    ╔═════════════════════════════════════════════════════════╗
    ║                                                         ║
    ║     ░█▀█ █░░ █▀▀ █▀█ █▀▀ █▀█ ▄▀█ ▀█▀ █ █▀▀           ║
    ║     ░█▄█ █▄▄ █▄█ █▄█ █▄▄ █▀▄ █▀█ ░█░ █ █▄▄           ║
    ║                                                         ║
    ║     ░█▀▀ █░█ ▀█▀ █░█ █▀█ █▀▀ █▀                      ║
    ║     ░█▄▄ █▄█ ░█░ █▄█ █▀▄ ██▄ ▄█                      ║
    ║                                                         ║
    ║     Your Learning is Our Asset™                        ║
    ║     MVP: Boardwalk Arcade Tutorial                     ║
    ╚═════════════════════════════════════════════════════════╝
    """)
    
    # Check requirements
    if not check_requirements():
        print("\nRequirements installed. Please run again.")
        return
    
    # Get launch choice
    choice = launch_options()
    
    if choice == "1":
        launch_terminal_mud()
    elif choice == "2":
        launch_room_system_mud()
    elif choice == "3":
        launch_web_interface()
    elif choice == "4":
        launch_both()
    else:
        print("Invalid choice. Defaulting to terminal MUD.")
        launch_terminal_mud()

if __name__ == "__main__":
    # Change to project directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    main()