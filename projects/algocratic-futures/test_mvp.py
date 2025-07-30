#!/usr/bin/env python3
"""
Quick test to verify MVP components are working
"""

import subprocess
import sys
import os

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    try:
        import adventurelib
        print("✅ adventurelib")
    except ImportError:
        print("❌ adventurelib missing")
        return False
    
    try:
        import fastapi
        print("✅ fastapi")
    except ImportError:
        print("❌ fastapi missing")
        return False
    
    try:
        import yaml
        print("✅ yaml")
    except ImportError:
        print("❌ yaml missing")
        return False
    
    return True

def test_mud_syntax():
    """Test that the MUD game has valid Python syntax"""
    print("\nTesting MUD syntax...")
    result = subprocess.run(
        [sys.executable, "-m", "py_compile", "backend/mud_game.py"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("✅ MUD game syntax valid")
        return True
    else:
        print("❌ MUD game syntax error:")
        print(result.stderr)
        return False

def test_room_files():
    """Test that room YAML files exist"""
    print("\nTesting room files...")
    room_files = [
        "rooms/boardwalk_arcade/arcade_main.yaml",
        "rooms/anonymous_sysop/micromuse_apartment.yaml",
    ]
    
    all_exist = True
    for room_file in room_files:
        if os.path.exists(room_file):
            print(f"✅ {room_file}")
        else:
            print(f"❌ {room_file} missing")
            all_exist = False
    
    return all_exist

def test_backend_syntax():
    """Test backend Python files"""
    print("\nTesting backend syntax...")
    backend_files = [
        "backend/app.py",
        "backend/clearance_system.py",
        "backend/agent_system.py",
        "backend/room_system.py",
        "backend/terminal_integration.py"
    ]
    
    all_valid = True
    for py_file in backend_files:
        if os.path.exists(py_file):
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", py_file],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"✅ {py_file}")
            else:
                print(f"❌ {py_file} syntax error")
                all_valid = False
        else:
            print(f"⚠️  {py_file} not found")
    
    return all_valid

def main():
    print("AlgoCratic Futures MVP Test Suite")
    print("=" * 40)
    
    tests_passed = 0
    tests_total = 4
    
    if test_imports():
        tests_passed += 1
    
    if test_mud_syntax():
        tests_passed += 1
    
    if test_room_files():
        tests_passed += 1
    
    if test_backend_syntax():
        tests_passed += 1
    
    print("\n" + "=" * 40)
    print(f"Tests passed: {tests_passed}/{tests_total}")
    
    if tests_passed == tests_total:
        print("\n✅ All tests passed! MVP is ready.")
        return 0
    else:
        print("\n❌ Some tests failed. Check output above.")
        return 1

if __name__ == "__main__":
    # Change to project directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    sys.exit(main())