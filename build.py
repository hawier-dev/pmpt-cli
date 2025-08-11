#!/usr/bin/env python3
"""
Build script for creating Windows executable
"""
import subprocess
import sys
import shutil
from pathlib import Path

def build_windows_exe():
    """Build Windows executable using PyInstaller"""
    print("🔨 Building Windows executable...")
    
    # Install PyInstaller if not already installed
    try:
        import PyInstaller
        print("✅ PyInstaller found")
    except ImportError:
        print("📦 Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Build command
    cmd = [
        "pyinstaller",
        "--onefile",                # Single executable
        "--name", "pmpt",           # Output name
        "--console",                # Console application
        "--clean",                  # Clean cache
        "--noconfirm",             # Overwrite without confirmation
        "main.py"
    ]
    
    print(f"🚀 Running: {' '.join(cmd)}")
    subprocess.check_call(cmd)
    
    # Check if build was successful
    exe_path = Path("dist/pmpt.exe")
    if exe_path.exists():
        print(f"✅ Successfully built: {exe_path}")
        print(f"📊 Size: {exe_path.stat().st_size / 1024 / 1024:.1f} MB")
        return str(exe_path)
    else:
        print("❌ Build failed - executable not found")
        return None

if __name__ == "__main__":
    build_windows_exe()