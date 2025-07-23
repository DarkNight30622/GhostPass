#!/usr/bin/env python3
"""
GHOST PASS Build Script

Builds executables for Windows, Linux, and macOS using PyInstaller.
"""

import os
import sys
import platform
import subprocess
from pathlib import Path


def install_dependencies():
    """Install build dependencies."""
    print("📦 Installing build dependencies...")
    
    dependencies = [
        "pyinstaller>=5.13.0",
        "nuitka>=1.8.0",
        "wheel>=0.40.0",
        "setuptools>=65.0.0"
    ]
    
    for dep in dependencies:
        subprocess.run([sys.executable, "-m", "pip", "install", dep], check=True)
    
    print("✅ Build dependencies installed")


def clean_build():
    """Clean previous build artifacts."""
    print("🧹 Cleaning build artifacts...")
    
    dirs_to_clean = ["build", "dist", "__pycache__"]
    files_to_clean = ["*.spec", "*.pyc", "*.pyo"]
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            subprocess.run(["rm", "-rf", dir_name])
    
    for pattern in files_to_clean:
        subprocess.run(["find", ".", "-name", pattern, "-delete"])
    
    print("✅ Build artifacts cleaned")


def build_windows():
    """Build Windows executable."""
    print("🪟 Building Windows executable...")
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=ghostpass.exe",
        "--icon=assets/icon.ico" if os.path.exists("assets/icon.ico") else "",
        "--add-data=ghostpass/config;ghostpass/config",
        "--hidden-import=ghostpass",
        "--hidden-import=ghostpass.core",
        "--hidden-import=ghostpass.ui",
        "--hidden-import=ghostpass.cli",
        "--hidden-import=ghostpass.config",
        "--hidden-import=ghostpass.utils",
        "ghostpass/__main__.py"
    ]
    
    # Remove empty strings
    cmd = [arg for arg in cmd if arg]
    
    subprocess.run(cmd, check=True)
    print("✅ Windows executable built: dist/ghostpass.exe")


def build_linux():
    """Build Linux executable."""
    print("🐧 Building Linux executable...")
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--name=ghostpass",
        "--add-data=ghostpass/config:ghostpass/config",
        "--hidden-import=ghostpass",
        "--hidden-import=ghostpass.core",
        "--hidden-import=ghostpass.ui",
        "--hidden-import=ghostpass.cli",
        "--hidden-import=ghostpass.config",
        "--hidden-import=ghostpass.utils",
        "ghostpass/__main__.py"
    ]
    
    subprocess.run(cmd, check=True)
    print("✅ Linux executable built: dist/ghostpass")


def build_macos():
    """Build macOS application."""
    print("🍎 Building macOS application...")
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=ghostpass.app",
        "--add-data=ghostpass/config:ghostpass/config",
        "--hidden-import=ghostpass",
        "--hidden-import=ghostpass.core",
        "--hidden-import=ghostpass.ui",
        "--hidden-import=ghostpass.cli",
        "--hidden-import=ghostpass.config",
        "--hidden-import=ghostpass.utils",
        "ghostpass/__main__.py"
    ]
    
    subprocess.run(cmd, check=True)
    print("✅ macOS application built: dist/ghostpass.app")


def build_nuitka():
    """Build optimized executable using Nuitka."""
    print("⚡ Building optimized executable with Nuitka...")
    
    cmd = [
        sys.executable, "-m", "nuitka",
        "--onefile",
        "--follow-imports",
        "--include-package=ghostpass",
        "--output-dir=dist",
        "--output-filename=ghostpass_optimized",
        "ghostpass/__main__.py"
    ]
    
    subprocess.run(cmd, check=True)
    print("✅ Optimized executable built: dist/ghostpass_optimized")


def create_package():
    """Create distribution package."""
    print("📦 Creating distribution package...")
    
    # Create dist directory structure
    dist_dir = Path("dist")
    dist_dir.mkdir(exist_ok=True)
    
    # Create platform-specific directories
    platforms = ["windows", "linux", "macos"]
    for platform_name in platforms:
        platform_dir = dist_dir / platform_name
        platform_dir.mkdir(exist_ok=True)
    
    # Copy executables to appropriate directories
    if os.path.exists("dist/ghostpass.exe"):
        os.rename("dist/ghostpass.exe", "dist/windows/ghostpass.exe")
    
    if os.path.exists("dist/ghostpass"):
        os.rename("dist/ghostpass", "dist/linux/ghostpass")
    
    if os.path.exists("dist/ghostpass.app"):
        os.rename("dist/ghostpass.app", "dist/macos/ghostpass.app")
    
    # Copy documentation
    docs_dir = dist_dir / "docs"
    docs_dir.mkdir(exist_ok=True)
    
    if os.path.exists("README.md"):
        subprocess.run(["cp", "README.md", "dist/docs/"])
    
    if os.path.exists("docs"):
        subprocess.run(["cp", "-r", "docs/*", "dist/docs/"])
    
    # Copy license
    if os.path.exists("LICENSE"):
        subprocess.run(["cp", "LICENSE", "dist/"])
    
    print("✅ Distribution package created in dist/")


def main():
    """Main build function."""
    print("🚀 GHOST PASS Build Script")
    print("=" * 50)
    
    # Detect platform
    current_platform = platform.system().lower()
    print(f"🖥️  Current platform: {current_platform}")
    
    try:
        # Install dependencies
        install_dependencies()
        
        # Clean previous builds
        clean_build()
        
        # Build based on platform
        if current_platform == "windows":
            build_windows()
        elif current_platform == "linux":
            build_linux()
        elif current_platform == "darwin":  # macOS
            build_macos()
        else:
            print(f"⚠️  Unknown platform: {current_platform}")
            print("Building generic executable...")
            build_linux()
        
        # Build optimized version
        build_nuitka()
        
        # Create distribution package
        create_package()
        
        print("\n🎉 Build completed successfully!")
        print("📁 Executables are in the dist/ directory")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 