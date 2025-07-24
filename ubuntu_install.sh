#!/bin/bash

echo "🐧 GHOST PASS - Ubuntu Installation Script"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root"
   exit 1
fi

print_status "Starting GHOST PASS installation..."

# Step 1: Update system
print_status "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Step 2: Install system dependencies
print_status "Installing system dependencies..."
sudo apt install -y python3 python3-pip python3-venv git curl wget

# Step 3: Install TOR
print_status "Installing TOR service..."
sudo apt install -y tor

# Step 4: Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    print_error "requirements.txt not found. Please run this script from the GhostPass directory."
    exit 1
fi

# Step 5: Create virtual environment
print_status "Creating Python virtual environment..."
python3 -m venv ghostpass_env
source ghostpass_env/bin/activate

# Step 6: Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Step 7: Install Python dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt

# Step 8: Install GHOST PASS
print_status "Installing GHOST PASS..."
pip install -e .

# Step 9: Configure TOR
print_status "Configuring TOR service..."

# Backup original config
sudo cp /etc/tor/torrc /etc/tor/torrc.backup

# Create TOR config for GHOST PASS
sudo tee -a /etc/tor/torrc > /dev/null <<EOF

# GHOST PASS Configuration
SocksPort 9050
ControlPort 9051
CookieAuthentication 1
DataDirectory /var/lib/tor
Log notice file /var/log/tor/notices.log
EOF

# Step 10: Start TOR service
print_status "Starting TOR service..."
sudo systemctl start tor
sudo systemctl enable tor

# Step 11: Verify installation
print_status "Verifying installation..."

# Check TOR status
if sudo systemctl is-active --quiet tor; then
    print_status "TOR service is running"
else
    print_error "TOR service failed to start"
    sudo systemctl status tor
fi

# Test GHOST PASS installation
if command -v ghostpass &> /dev/null; then
    print_status "GHOST PASS installed successfully"
    ghostpass --help
else
    print_error "GHOST PASS installation failed"
fi

# Test TOR connectivity
print_status "Testing TOR connectivity..."
if curl --socks5 localhost:9050 --socks5-hostname localhost:9050 -s https://check.torproject.org/ | grep -q "Congratulations"; then
    print_status "TOR connectivity test passed!"
else
    print_warning "TOR connectivity test failed. This might be normal if TOR is still initializing."
fi

echo ""
echo "🎉 Installation completed!"
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source ghostpass_env/bin/activate"
echo "2. Run GHOST PASS: ghostpass"
echo "3. Or run tests: python test_ghostpass.py"
echo ""
echo "For help: ghostpass --help"
echo "For issues: Check docs/ubuntu_installation.md" 