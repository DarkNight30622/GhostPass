# Ubuntu Installation Guide - GHOST PASS

Complete step-by-step installation guide for Ubuntu systems.

## Prerequisites

### System Requirements
- Ubuntu 18.04 LTS or later
- Python 3.8 or higher
- Internet connection
- User account with sudo privileges

### Check System
```bash
# Check Ubuntu version
lsb_release -a

# Check Python version
python3 --version

# Check if you have sudo access
sudo -l
```

## Method 1: Quick Installation (Recommended)

### Step 1: Clone the Repository
```bash
# Navigate to home directory
cd ~

# Clone GHOST PASS repository
git clone https://github.com/DarkNight30622/GhostPass.git

# Enter the project directory
cd GhostPass
```

### Step 2: Run Quick Installation
```bash
# Make scripts executable
chmod +x *.sh

# Run quick installation
./quick_fix.sh
```

### Step 3: Configure TOR
```bash
# Configure TOR (no sudo required)
./configure_tor.sh

# Start TOR
~/.ghostpass/tor/start_tor.sh
```

### Step 4: Test Installation
```bash
# Test everything works
python test_installation.py

# Test GHOST PASS
python -m ghostpass --help
```

## Method 2: Manual Installation

### Step 1: Update System
```bash
# Update package list
sudo apt update

# Upgrade existing packages
sudo apt upgrade -y
```

### Step 2: Install System Dependencies
```bash
# Install essential packages
sudo apt install -y python3 python3-pip python3-venv git curl wget

# Install TOR
sudo apt install -y tor

# Install additional dependencies
sudo apt install -y build-essential python3-dev libffi-dev libssl-dev
```

### Step 3: Clone Repository
```bash
# Navigate to home directory
cd ~

# Clone GHOST PASS repository
git clone https://github.com/DarkNight30622/GhostPass.git

# Enter the project directory
cd GhostPass
```

### Step 4: Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv ghostpass_env

# Activate virtual environment
source ghostpass_env/bin/activate

# Verify activation (should show ghostpass_env path)
echo $VIRTUAL_ENV
```

### Step 5: Upgrade pip
```bash
# Upgrade pip to latest version
pip install --upgrade pip
```

### Step 6: Install Python Dependencies
```bash
# Install dependencies from requirements.txt
pip install -r requirements.txt
```

### Step 7: Install GHOST PASS
```bash
# Install GHOST PASS in development mode
pip install -e .
```

### Step 8: Configure TOR (User-Specific)
```bash
# Create TOR configuration directory
mkdir -p ~/.ghostpass/tor

# Create TOR configuration file
cat > ~/.ghostpass/tor/torrc << 'EOF'
# GHOST PASS User TOR Configuration
SocksPort 9050
ControlPort 9051
CookieAuthentication 1
DataDirectory /home/$USER/.ghostpass/tor/data
PidFile /home/$USER/.ghostpass/tor/tor.pid
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

# Create data directory
mkdir -p ~/.ghostpass/tor/data
```

### Step 9: Start TOR
```bash
# Start TOR in background
tor --config ~/.ghostpass/tor/torrc --data ~/.ghostpass/tor/data --pidfile ~/.ghostpass/tor/tor.pid &

# Wait for TOR to start
sleep 5

# Check if TOR is running
ps aux | grep tor
```

### Step 10: Test Installation
```bash
# Test TOR connection
curl --socks5 127.0.0.1:9050 https://check.torproject.org/

# Test GHOST PASS
python -m ghostpass --help

# Run comprehensive test
python test_installation.py
```

## Method 3: Complete Installation Script

### Step 1: Clone and Run
```bash
# Clone repository
cd ~
git clone https://github.com/DarkNight30622/GhostPass.git
cd GhostPass

# Make executable and run
chmod +x install.sh
./install.sh
```

## Verification Commands

### Check Python Installation
```bash
# Check Python version
python3 --version

# Check pip version
pip --version

# Check virtual environment
echo $VIRTUAL_ENV
```

### Check GHOST PASS Installation
```bash
# Test imports
python -c "import ghostpass; print('✅ GHOST PASS imported successfully')"

# Test CLI
python -m ghostpass --help

# Test modules
python -c "from ghostpass.core.tor_controller import TorController; print('✅ TOR Controller OK')"
python -c "from ghostpass.core.encryption import EncryptionManager; print('✅ Encryption OK')"
python -c "from ghostpass.core.ip_rotator import IPRotator; print('✅ IP Rotator OK')"
```

### Check TOR Installation
```bash
# Check TOR version
tor --version

# Check TOR service status
sudo systemctl status tor

# Check TOR ports
netstat -tlnp | grep 9050
netstat -tlnp | grep 9051

# Test TOR connection
curl --socks5 127.0.0.1:9050 https://check.torproject.org/
```

### Check Dependencies
```bash
# List installed packages
pip list

# Check specific packages
python -c "import stem; print('✅ Stem OK')"
python -c "import socks; print('✅ PySocks OK')"
python -c "import textual; print('✅ Textual OK')"
python -c "import rich; print('✅ Rich OK')"
python -c "import cryptography; print('✅ Cryptography OK')"
```

## Usage Commands

### Start GHOST PASS
```bash
# Interactive dashboard
python -m ghostpass

# CLI mode
python -m ghostpass connect
python -m ghostpass status
python -m ghostpass rotate-ip
```

### TOR Management
```bash
# Start TOR (user-specific)
~/.ghostpass/tor/start_tor.sh

# Stop TOR
~/.ghostpass/tor/stop_tor.sh

# Check TOR status
ps aux | grep tor
```

### Testing Commands
```bash
# Run all tests
python test_installation.py

# Test specific functionality
python -m ghostpass test

# Test connection
python -m ghostpass status
```

## Troubleshooting Commands

### Fix Common Issues
```bash
# Fix permissions
chmod +x *.sh
chmod 644 requirements.txt setup.py

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Clean and reinstall
rm -rf ghostpass_env
python3 -m venv ghostpass_env
source ghostpass_env/bin/activate
pip install -r requirements.txt
pip install -e .
```

### Check Logs
```bash
# Check TOR logs
sudo journalctl -u tor -f

# Check user TOR logs
tail -f ~/.ghostpass/tor/data/tor.log

# Check Python errors
python -m ghostpass 2>&1 | tee error.log
```

### Reset Configuration
```bash
# Remove user TOR configuration
rm -rf ~/.ghostpass

# Reconfigure TOR
./configure_tor.sh

# Restart TOR
~/.ghostpass/tor/start_tor.sh
```

## Uninstall Commands

### Remove GHOST PASS
```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf ~/GhostPass/ghostpass_env

# Remove project directory
rm -rf ~/GhostPass

# Remove user TOR configuration
rm -rf ~/.ghostpass
```

### Remove System TOR (if installed)
```bash
# Stop TOR service
sudo systemctl stop tor
sudo systemctl disable tor

# Remove TOR package
sudo apt remove --purge tor -y

# Clean up
sudo apt autoremove -y
```

## Complete Installation Script

Here's a complete script you can run:

```bash
#!/bin/bash
# Complete GHOST PASS Installation Script for Ubuntu

set -e

echo "🚀 Installing GHOST PASS on Ubuntu..."

# Update system
echo "📦 Updating system..."
sudo apt update && sudo apt upgrade -y

# Install dependencies
echo "📦 Installing dependencies..."
sudo apt install -y python3 python3-pip python3-venv git curl wget tor

# Clone repository
echo "📥 Cloning repository..."
cd ~
git clone https://github.com/DarkNight30622/GhostPass.git
cd GhostPass

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3 -m venv ghostpass_env
source ghostpass_env/bin/activate

# Install Python packages
echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .

# Configure TOR
echo "🔧 Configuring TOR..."
./configure_tor.sh

# Start TOR
echo "🚀 Starting TOR..."
~/.ghostpass/tor/start_tor.sh

# Test installation
echo "🧪 Testing installation..."
python test_installation.py

echo "✅ Installation complete!"
echo "🚀 Run: python -m ghostpass"
```

## Success Indicators

You'll know the installation is successful when:

- ✅ `python -m ghostpass --help` shows CLI interface
- ✅ `curl --socks5 127.0.0.1:9050 https://check.torproject.org/` returns TOR confirmation
- ✅ `python test_installation.py` passes all tests
- ✅ `python -m ghostpass` launches interactive dashboard

## Next Steps

After successful installation:

1. **Learn the basics**: `python -m ghostpass --help`
2. **Read documentation**: Check `README.md` and `docs/`
3. **Start using**: `python -m ghostpass`
4. **Get help**: Check `TROUBLESHOOTING.md` if you encounter issues

---

**🎉 GHOST PASS is now ready to use on Ubuntu!** 