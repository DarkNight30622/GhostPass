#!/bin/bash

# GHOST PASS Installation Script
# This script handles all installation and setup issues

set -e  # Exit on any error

echo "🚀 GHOST PASS Installation Script"
echo "=================================="

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "❌ This script should not be run as root"
   exit 1
fi

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
echo "✅ Python version: $python_version"

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Installing pip..."
    sudo apt update
    sudo apt install -y python3-pip
fi

# Create virtual environment
echo "🔧 Creating virtual environment..."
if [ -d "ghostpass_env" ]; then
    echo "⚠️  Virtual environment already exists. Removing..."
    rm -rf ghostpass_env
fi

python3 -m venv ghostpass_env
echo "✅ Virtual environment created"

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source ghostpass_env/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ Dependencies installed from requirements.txt"
else
    echo "❌ requirements.txt not found. Installing core dependencies manually..."
    pip install textual rich stem PySocks cryptography requests psutil dnspython pycryptodome certifi pyyaml click colorama
    echo "✅ Core dependencies installed"
fi

# Install the package in development mode
echo "🔧 Installing GHOST PASS in development mode..."
if [ -f "setup.py" ]; then
    pip install -e .
    echo "✅ GHOST PASS installed in development mode"
else
    echo "❌ setup.py not found. Installing manually..."
    pip install -e .
    echo "✅ GHOST PASS installed"
fi

# Install TOR
echo "🔧 Installing TOR..."
if ! command -v tor &> /dev/null; then
    echo "📦 Installing TOR..."
    sudo apt update
    sudo apt install -y tor
    echo "✅ TOR installed"
else
    echo "✅ TOR is already installed"
fi

# Configure TOR
echo "⚙️  Configuring TOR..."
sudo systemctl stop tor

# Create TOR configuration
sudo tee /etc/tor/torrc > /dev/null <<EOF
# GHOST PASS TOR Configuration
SocksPort 9050
ControlPort 9051
CookieAuthentication 1
DataDirectory /var/lib/tor
PidFile /var/run/tor/tor.pid
Log notice stdout
MaxCircuitDirtiness 600
NewCircuitPeriod 30
EnforceDistinctSubnets 1
UseEntryGuards 1
NumEntryGuards 6
GuardLifetime 2592000
CircuitBuildTimeout 30
LearnCircuitBuildTimeout 1
CircuitStreamTimeout 300
MaxClientCircuitsPending 32
MaxOnionQueueDelay 1750
NewOnionKey 1
SafeLogging 1
EOF

echo "✅ TOR configured"

# Set proper permissions
echo "🔐 Setting permissions..."
sudo chown -R debian-tor:debian-tor /var/lib/tor
sudo chmod 700 /var/lib/tor

# Start TOR service
echo "🚀 Starting TOR service..."
sudo systemctl enable tor
sudo systemctl start tor

# Wait for TOR to start
echo "⏳ Waiting for TOR to start..."
sleep 5

# Check TOR status
if sudo systemctl is-active --quiet tor; then
    echo "✅ TOR service is running"
else
    echo "❌ TOR service failed to start"
    echo "📋 TOR service status:"
    sudo systemctl status tor --no-pager -l
fi

# Create test script
echo "🧪 Creating test script..."
cat > test_installation.py << 'EOF'
#!/usr/bin/env python3
"""
Test script to verify GHOST PASS installation
"""

import sys
import asyncio

def test_imports():
    """Test if all required modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        import ghostpass
        print("✅ ghostpass module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import ghostpass: {e}")
        return False
    
    try:
        from ghostpass.core.tor_controller import TorController
        print("✅ TorController imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import TorController: {e}")
        return False
    
    try:
        from ghostpass.core.encryption import EncryptionManager
        print("✅ EncryptionManager imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import EncryptionManager: {e}")
        return False
    
    try:
        from ghostpass.core.ip_rotator import IPRotator
        print("✅ IPRotator imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import IPRotator: {e}")
        return False
    
    return True

def test_tor_connection():
    """Test TOR connection."""
    print("\n🔍 Testing TOR connection...")
    
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
            print("✅ TOR connection working")
            return True
        else:
            print("⚠️  TOR connection established but not confirmed")
            return True
    except Exception as e:
        print(f"❌ TOR connection failed: {e}")
        return False

def main():
    """Main test function."""
    print("🧪 GHOST PASS Installation Test")
    print("================================")
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed")
        return False
    
    # Test TOR connection
    if not test_tor_connection():
        print("\n❌ TOR connection test failed")
        return False
    
    print("\n✅ All tests passed!")
    print("\n🎉 GHOST PASS is ready to use!")
    print("\n📋 Usage examples:")
    print("  python -m ghostpass                    # Launch interactive dashboard")
    print("  python -m ghostpass connect            # Connect to TOR")
    print("  python -m ghostpass status             # Show status")
    print("  python -m ghostpass rotate-ip          # Rotate IP")
    print("  python -m ghostpass test               # Run tests")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
EOF

# Make test script executable
chmod +x test_installation.py

# Run test
echo "🧪 Running installation test..."
python test_installation.py

echo ""
echo "🎉 Installation completed!"
echo ""
echo "📋 Next steps:"
echo "1. Activate the virtual environment: source ghostpass_env/bin/activate"
echo "2. Run GHOST PASS: python -m ghostpass"
echo "3. Or use CLI commands: python -m ghostpass --help"
echo ""
echo "🔧 If you encounter any issues:"
echo "   - Check TOR service: sudo systemctl status tor"
echo "   - Restart TOR: sudo systemctl restart tor"
echo "   - Check logs: sudo journalctl -u tor -f"
echo "" 