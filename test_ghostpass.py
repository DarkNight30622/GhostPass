#!/usr/bin/env python3
"""
Simple test script for GHOST PASS

This script tests basic functionality and verifies the installation.
"""

import sys
import asyncio
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from ghostpass import TorController, EncryptionManager, IPRotator
        print("✅ Core modules imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import core modules: {e}")
        return False
    
    try:
        from ghostpass.ui import Dashboard
        print("✅ UI modules imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import UI modules: {e}")
        return False
    
    try:
        from ghostpass.cli import main
        print("✅ CLI modules imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import CLI modules: {e}")
        return False
    
    try:
        from ghostpass.config import get_config
        print("✅ Config modules imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import config modules: {e}")
        return False
    
    return True


def test_config():
    """Test configuration loading."""
    print("\nTesting configuration...")
    
    try:
        from ghostpass.config import get_config, ConfigManager
        
        # Test default config
        config = get_config()
        print(f"✅ Default config loaded: {config.app_name} v{config.version}")
        
        # Test config manager
        config_manager = ConfigManager()
        print("✅ Config manager initialized")
        
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False


async def test_tor_controller():
    """Test TOR controller initialization."""
    print("\nTesting TOR controller...")
    
    try:
        from ghostpass.core import TorController
        
        controller = TorController()
        print("✅ TOR controller initialized")
        
        # Test configuration
        config = controller.get_connection_status()
        print(f"✅ TOR config: SOCKS port {config['socks_port']}, Control port {config['control_port']}")
        
        return True
    except Exception as e:
        print(f"❌ TOR controller test failed: {e}")
        return False


async def test_encryption():
    """Test encryption manager."""
    print("\nTesting encryption...")
    
    try:
        from ghostpass.core import EncryptionManager
        
        manager = EncryptionManager()
        print("✅ Encryption manager initialized")
        
        # Test key generation
        master_key = manager.generate_master_key("test_password")
        print(f"✅ Master key generated: {len(master_key)} bytes")
        
        # Test session key derivation
        session_key = manager.derive_session_key("test_session")
        print(f"✅ Session key derived: {len(session_key)} bytes")
        
        # Test encryption/decryption
        test_data = b"Hello, GHOST PASS!"
        encrypted = manager.encrypt_aes(test_data)
        decrypted = manager.decrypt_aes(encrypted)
        
        if decrypted == test_data:
            print("✅ AES encryption/decryption test passed")
        else:
            print("❌ AES encryption/decryption test failed")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Encryption test failed: {e}")
        return False


async def test_ip_rotator():
    """Test IP rotator initialization."""
    print("\nTesting IP rotator...")
    
    try:
        from ghostpass.core import IPRotator, TorController
        
        tor_controller = TorController()
        rotator = IPRotator(tor_controller)
        print("✅ IP rotator initialized")
        
        # Test configuration
        status = rotator.get_rotation_status()
        print(f"✅ Rotation status: {status['mode']}")
        
        return True
    except Exception as e:
        print(f"❌ IP rotator test failed: {e}")
        return False


def test_ui_components():
    """Test UI components."""
    print("\nTesting UI components...")
    
    try:
        from ghostpass.ui import show_startup_animation
        print("✅ UI components imported")
        
        # Note: We won't actually run the animation in tests
        # to avoid blocking the test process
        print("✅ UI components test passed (animation skipped)")
        
        return True
    except Exception as e:
        print(f"❌ UI components test failed: {e}")
        return False


async def main():
    """Run all tests."""
    print("🧪 GHOST PASS Test Suite")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Config Test", test_config),
        ("TOR Controller Test", test_tor_controller),
        ("Encryption Test", test_encryption),
        ("IP Rotator Test", test_ip_rotator),
        ("UI Components Test", test_ui_components),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            
            if result:
                passed += 1
            else:
                print(f"❌ {test_name} failed")
                
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! GHOST PASS is ready to use.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return False


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        sys.exit(1) 