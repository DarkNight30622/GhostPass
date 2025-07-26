# 🐧 Ubuntu Installation Guide - GHOST PASS

Complete step-by-step installation guide for Ubuntu systems with all the latest fixes and improvements.

## 📋 Prerequisites

### System Requirements
- **Ubuntu 18.04 LTS or later** (20.04 LTS recommended)
- **Python 3.8 or higher**
- **Internet connection**
- **User account with sudo privileges**

### Check Your System
```bash
# Check Ubuntu version
lsb_release -a

# Check Python version
python3 --version

# Check if you have sudo access
sudo -l
```

## 🚀 Installation Methods

### Method 1: Quick Installation (Recommended)

This is the fastest and most reliable method using our automated scripts.

#### Step 1: Clone the Repository
```bash
# Navigate to home directory
cd ~

# Clone GHOST PASS repository
git clone https://github.com/DarkNight30622/GhostPass.git

# Enter the project directory
cd GhostPass
```

#### Step 2: Run Quick Installation
```bash
# Make scripts executable
chmod +x *.sh

# Run quick installation (handles everything automatically)
./quick_fix.sh
```

#### Step 3: Configure TOR (No sudo required)
```bash
# Configure TOR with user-specific setup
./configure_tor.sh

# Start TOR
~/.ghostpass/tor/start_tor.sh
```

#### Step 4: Test Installation
```bash
# Test everything works
python test_installation.py

# Test GHOST PASS
python -m ghostpass --help
```

### Method 2: Complete Installation

For users who want full control over the installation process.

#### Step 1: Update System
```bash
# Update package list
sudo apt update

# Upgrade existing packages
sudo apt upgrade -y
```

#### Step 2: Install System Dependencies
```bash
# Install essential packages
sudo apt install -y python3 python3-pip python3-venv git curl wget

# Install TOR
sudo apt install -y tor

# Install additional dependencies for compilation
sudo apt install -y build-essential python3-dev libffi-dev libssl-dev
```

#### Step 3: Clone Repository
```bash
# Navigate to home directory
cd ~

# Clone GHOST PASS repository
git clone https://github.com/DarkNight30622/GhostPass.git

# Enter the project directory
cd GhostPass
```

#### Step 4: Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv ghostpass_env

# Activate virtual environment
source ghostpass_env/bin/activate

# Verify activation (should show ghostpass_env path)
echo $VIRTUAL_ENV
```

#### Step 5: Upgrade pip
```bash
# Upgrade pip to latest version
pip install --upgrade pip
```

#### Step 6: Install Python Dependencies
```bash
# Install dependencies from requirements.txt
pip install -r requirements.txt
```

#### Step 7: Install GHOST PASS
```bash
# Install GHOST PASS in development mode
pip install -e .
```

#### Step 8: Configure TOR (User-Specific)
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

#### Step 9: Start TOR
```bash
# Start TOR in background
tor --config ~/.ghostpass/tor/torrc --data ~/.ghostpass/tor/data --pidfile ~/.ghostpass/tor/tor.pid --ignore-missing-torrc &

# Wait for TOR to start
sleep 5

# Check if TOR is running
ps aux | grep tor
```

#### Step 10: Test Installation
```bash
# Test TOR connection
curl --socks5 127.0.0.1:9050 https://check.torproject.org/

# Test GHOST PASS
python -m ghostpass --help

# Run comprehensive test
python test_installation.py
```

### Method 3: Automated Installation Script

For the most comprehensive installation with all features.

```bash
# Clone repository
cd ~
git clone https://github.com/DarkNight30622/GhostPass.git
cd GhostPass

# Make executable and run complete installation
chmod +x install.sh
./install.sh
```

## 🧪 Verification Commands

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

## 🚀 Usage After Installation

### Start GHOST PASS
```bash
# Interactive dashboard
python -m ghostpass

# CLI commands
python -m ghostpass connect
python -m ghostpass status
python -m ghostpass rotate-ip
python -m ghostpass test
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

## 🔧 TOR Configuration

### User-Specific TOR Setup (Recommended)
```bash
# Configure TOR without sudo
./configure_tor.sh

# Start TOR
~/.ghostpass/tor/start_tor.sh

# Stop TOR
~/.ghostpass/tor/stop_tor.sh
```

### System TOR Service (Alternative)
```bash
# Install TOR
sudo apt install -y tor

# Start TOR service
sudo systemctl start tor
sudo systemctl enable tor

# Check status
sudo systemctl status tor
```

## 🛠️ Troubleshooting

### Common Issues and Solutions

#### Issue: TOR Configuration Error
```bash
# Error: "Unknown option 'config'"
# Solution: Use the fixed configuration
./configure_tor.sh
~/.ghostpass/tor/start_tor.sh
```

#### Issue: Permission Denied
```bash
# Fix file permissions
chmod +x *.sh
chmod 644 requirements.txt setup.py
```

#### Issue: Module Not Found
```bash
# Make sure virtual environment is activated
source ghostpass_env/bin/activate

# Reinstall the package
pip install -e .
```

#### Issue: TOR Connection Failed
```bash
# Check if TOR is running
sudo systemctl status tor

# Start TOR if not running
sudo systemctl start tor

# Or use user TOR
~/.ghostpass/tor/start_tor.sh
```

#### Issue: Port Already in Use
```bash
# Find what's using the port
sudo netstat -tlnp | grep 9050

# Kill the process or use different ports
# Edit TOR configuration to use different ports
```

### Advanced Troubleshooting

#### Check Logs
```bash
# Check TOR logs
sudo journalctl -u tor -f

# Check user TOR logs
tail -f ~/.ghostpass/tor/data/tor.log

# Check Python errors
python -m ghostpass 2>&1 | tee error.log
```

#### Reset Configuration
```bash
# Remove user TOR configuration
rm -rf ~/.ghostpass

# Reconfigure TOR
./configure_tor.sh

# Restart TOR
~/.ghostpass/tor/start_tor.sh
```

#### Complete Reinstall
```bash
# Remove everything and start fresh
deactivate
rm -rf ~/GhostPass
rm -rf ~/.ghostpass

# Reinstall from scratch
cd ~
git clone https://github.com/DarkNight30622/GhostPass.git
cd GhostPass
./install.sh
```

## 📊 Success Indicators

You'll know everything is working when:

- ✅ `python -m ghostpass --help` shows CLI interface
- ✅ `curl --socks5 127.0.0.1:9050 https://check.torproject.org/` returns TOR confirmation
- ✅ `python -m ghostpass` launches interactive dashboard
- ✅ `python test_installation.py` passes all tests

## 🔄 Uninstall Commands

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

## 📚 Additional Resources

### Documentation
- `README.md` - Main project documentation
- `SOLUTION.md` - Step-by-step solutions for common errors
- `TROUBLESHOOTING.md` - Detailed troubleshooting guide
- `docs/` - Platform-specific guides

### Scripts
- `install.sh` - Complete installation
- `quick_fix.sh` - Quick problem resolution
- `configure_tor.sh` - TOR setup
- `test_installation.py` - Verification testing

### External Resources
- [GitHub Repository](https://github.com/DarkNight30622/GhostPass)
- [TOR Project](https://www.torproject.org/)
- [Python Documentation](https://docs.python.org/)

## 🎯 Next Steps

After successful installation:

1. **Learn the basics**: `python -m ghostpass --help`
2. **Read the documentation**: Check `README.md` and other guides
3. **Start using GHOST PASS**: `python -m ghostpass`
4. **Get help**: Check `TROUBLESHOOTING.md` if you encounter issues

---

## 🎉 Installation Complete!

Congratulations! You've successfully installed GHOST PASS on Ubuntu. The installation includes:

- ✅ **GHOST PASS** - Privacy-first VPN and IP-masking tool
- ✅ **TOR Integration** - Secure anonymous browsing
- ✅ **User-Specific Configuration** - No sudo required for TOR
- ✅ **Comprehensive Testing** - Automated verification
- ✅ **Excellent Documentation** - Clear guides and troubleshooting

**🚀 Ready to use: `python -m ghostpass`** 