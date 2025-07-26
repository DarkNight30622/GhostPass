#!/usr/bin/env python3
"""
GHOST PASS Installation Test Script

This script verifies that GHOST PASS is properly installed and configured.
Run this after installation to ensure everything is working.
"""

import sys
import os
import asyncio
import subprocess
from pathlib import Path

def print_status(message, status="INFO"):
    """Print a status message with color coding."""
    colors = {
        "INFO": "\033[94m",    # Blue
        "SUCCESS": "\033[92m", # Green
        "WARNING": "\033[93m", # Yellow
        "ERROR": "\033[91m",   # Red
        "RESET": "\033[0m"     # Reset
    }
    print(f"{colors.get(status, colors['INFO'])}[{status}] {message}{colors['RESET']}")

def test_python_version():
    """Test Python version compatibility."""
    print_status("Testing Python version...", "INFO")
    
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print_status(f"Python {version.major}.{version.minor}.{version.micro} is compatible", "SUCCESS")
        return True
    else:
        print_status(f"Python {version.major}.{version.minor}.{version.micro} is not compatible (requires 3.8+)", "ERROR")
        return False

def test_imports():
    """Test if all required modules can be imported."""
    print_status("Testing module imports...", "INFO")
    
    required_modules = [
        ("ghostpass", "Main GHOST PASS module"),
        ("ghostpass.core.tor_controller", "TOR Controller"),
        ("ghostpass.core.encryption", "Encryption Manager"),
        ("ghostpass.core.ip_rotator", "IP Rotator"),
        ("ghostpass.cli.main", "CLI Interface"),
        ("ghostpass.ui.dashboard", "Dashboard UI"),
        ("stem", "TOR control library"),
        ("socks", "SOCKS proxy library"),
        ("textual", "Terminal UI library"),
        ("rich", "Rich text library"),
        ("cryptography", "Cryptography library"),
        ("requests", "HTTP library"),
    ]
    
    failed_imports = []
    
    for module, description in required_modules:
        try:
            __import__(module)
            print_status(f"✅ {description} imported successfully", "SUCCESS")
        except ImportError as e:
            print_status(f"❌ Failed to import {description}: {e}", "ERROR")
            failed_imports.append(module)
    
    if failed_imports:
        print_status(f"Failed to import {len(failed_imports)} modules", "ERROR")
        return False
    else:
        print_status("All modules imported successfully", "SUCCESS")
        return True

def test_cli_interface():
    """Test if the CLI interface is accessible."""
    print_status("Testing CLI interface...", "INFO")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "ghostpass", "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0 and "GHOST PASS" in result.stdout:
            print_status("✅ CLI interface is working", "SUCCESS")
            return True
        else:
            print_status(f"❌ CLI interface failed: {result.stderr}", "ERROR")
            return False
    except subprocess.TimeoutExpired:
        print_status("❌ CLI interface timed out", "ERROR")
        return False
    except Exception as e:
        print_status(f"❌ CLI interface error: {e}", "ERROR")
        return False

def test_tor_connection():
    """Test TOR connection."""
    print_status("Testing TOR connection...", "INFO")
    
    try:
        import socket
        import socks
        
        # Test SOCKS connection
        sock = socks.socksocket()
        sock.set_proxy(socks.SOCKS5, "127.0.0.1", 9050)
        sock.settimeout(10)
        
        # Try to connect to a test site
        sock.connect(("check.torproject.org", 80))
        sock.send(b"GET / HTTP/1.1\r\nHost: check.torproject.org\r\n\r\n")
        response = sock.recv(1024)
        sock.close()
        
        if b"Congratulations" in response:
            print_status("✅ TOR connection working and confirmed", "SUCCESS")
            return True
        elif b"HTTP" in response:
            print_status("⚠️  TOR connection established but not confirmed", "WARNING")
            return True
        else:
            print_status("❌ TOR connection failed to get proper response", "ERROR")
            return False
    except Exception as e:
        print_status(f"❌ TOR connection failed: {e}", "ERROR")
        return False

def test_tor_service():
    """Test if TOR service is running."""
    print_status("Testing TOR service...", "INFO")
    
    try:
        # Check if TOR is listening on port 9050
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex(('127.0.0.1', 9050))
        sock.close()
        
        if result == 0:
            print_status("✅ TOR service is running on port 9050", "SUCCESS")
            return True
        else:
            print_status("❌ TOR service is not running on port 9050", "ERROR")
            return False
    except Exception as e:
        print_status(f"❌ Error checking TOR service: {e}", "ERROR")
        return False

def test_file_structure():
    """Test if all required files exist."""
    print_status("Testing file structure...", "INFO")
    
    required_files = [
        "requirements.txt",
        "setup.py",
        "ghostpass/__init__.py",
        "ghostpass/__main__.py",
        "ghostpass/cli/main.py",
        "ghostpass/core/tor_controller.py",
        "ghostpass/core/encryption.py",
        "ghostpass/core/ip_rotator.py",
        "ghostpass/ui/dashboard.py",
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            print_status(f"✅ {file_path} exists", "SUCCESS")
        else:
            print_status(f"❌ {file_path} missing", "ERROR")
            missing_files.append(file_path)
    
    if missing_files:
        print_status(f"Missing {len(missing_files)} required files", "ERROR")
        return False
    else:
        print_status("All required files present", "SUCCESS")
        return True

def test_virtual_environment():
    """Test if running in a virtual environment."""
    print_status("Testing virtual environment...", "INFO")
    
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print_status("✅ Running in virtual environment", "SUCCESS")
        return True
    else:
        print_status("⚠️  Not running in virtual environment (this is OK for system installs)", "WARNING")
        return True

def main():
    """Main test function."""
    print("🧪 GHOST PASS Installation Test")
    print("=" * 40)
    print()
    
    tests = [
        ("Python Version", test_python_version),
        ("File Structure", test_file_structure),
        ("Virtual Environment", test_virtual_environment),
        ("Module Imports", test_imports),
        ("CLI Interface", test_cli_interface),
        ("TOR Service", test_tor_service),
        ("TOR Connection", test_tor_connection),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_status(f"Test failed with exception: {e}", "ERROR")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 TEST SUMMARY")
    print("=" * 40)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print_status("🎉 All tests passed! GHOST PASS is ready to use.", "SUCCESS")
        print("\n📋 Usage examples:")
        print("  python -m ghostpass                    # Launch interactive dashboard")
        print("  python -m ghostpass connect            # Connect to TOR")
        print("  python -m ghostpass status             # Show status")
        print("  python -m ghostpass rotate-ip          # Rotate IP")
        print("  python -m ghostpass test               # Run tests")
        return True
    else:
        print_status(f"❌ {total - passed} tests failed. Please check the issues above.", "ERROR")
        print("\n🔧 Troubleshooting:")
        print("  - Run: ./quick_fix.sh")
        print("  - Or: ./install.sh")
        print("  - Check: TROUBLESHOOTING.md")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 