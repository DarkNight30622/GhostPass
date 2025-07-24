# 🍎 macOS Installation Guide - GHOST PASS

## Prerequisites

### System Requirements
- macOS 10.15+ (Catalina or later)
- Homebrew package manager
- Python 3.8 or higher
- Git
- Terminal.app or iTerm2

### Check System Requirements
```bash
# Check macOS version
sw_vers

# Check Python version
python3 --version

# Check Git version
git --version

# Check if Homebrew is installed
brew --version
```

## Step-by-Step Installation

### 1. Install Homebrew (if not installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Add Homebrew to PATH (if needed)
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

### 2. Install Python and Git
```bash
# Install Python
brew install python

# Install Git
brew install git

# Verify installations
python3 --version
git --version
```

### 3. Install TOR
```bash
# Install TOR service
brew install tor

# Verify TOR installation
tor --version
```

### 4. Clone the Repository
```bash
# Clone from your repository
git clone https://github.com/DarkNight30622/GhostPass.git
cd GhostPass
```

### 5. Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv ghostpass_env

# Activate virtual environment
source ghostpass_env/bin/activate
```

### 6. Upgrade pip
```bash
pip install --upgrade pip
```

### 7. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 8. Install GHOST PASS
```bash
pip install -e .
```

### 9. Configure TOR
```bash
# Edit TOR configuration
nano /usr/local/etc/tor/torrc
```

Add these lines to `/usr/local/etc/tor/torrc`:
```
# GHOST PASS Configuration
SocksPort 9050
ControlPort 9051
CookieAuthentication 1
DataDirectory /usr/local/var/lib/tor
Log notice file /usr/local/var/log/tor/notices.log
```

### 10. Start TOR Service
```bash
# Start TOR service
brew services start tor

# Check TOR status
brew services list | grep tor
```

### 11. Verify Installation
```bash
# Test GHOST PASS installation
ghostpass --help

# Test TOR connection
curl --socks5 localhost:9050 --socks5-hostname localhost:9050 -s https://check.torproject.org/
```

## Testing GHOST PASS

### Run the Application
```bash
# Interactive UI mode
ghostpass

# CLI mode
ghostpass --help
ghostpass connect
ghostpass status
```

### Test Core Functionality
```bash
# Run the test suite
python test_ghostpass.py
```

## Troubleshooting

### Common Issues

#### 1. Homebrew Not Found
```bash
# Add Homebrew to PATH
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
source ~/.zshrc
```

#### 2. Permission Denied Errors
```bash
# Fix permissions
sudo chown -R $(whoami) /usr/local/bin /usr/local/lib /usr/local/sbin
chmod u+w /usr/local/bin /usr/local/lib /usr/local/sbin
```

#### 3. Python Module Not Found
```bash
# Ensure virtual environment is activated
source ghostpass_env/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### 4. TOR Service Issues
```bash
# Check TOR service status
brew services list | grep tor

# Restart TOR service
brew services restart tor

# Check TOR logs
tail -f /usr/local/var/log/tor/notices.log
```

#### 5. Port Already in Use
```bash
# Check what's using port 9050
lsof -i :9050

# Kill conflicting process
sudo pkill -f tor
brew services start tor
```

### Network Configuration

#### Check TOR Status
```bash
# Test TOR connectivity
curl --socks5 localhost:9050 --socks5-hostname localhost:9050 -s https://check.torproject.org/
```

#### Configure macOS Firewall
```bash
# Allow TOR through firewall (System Preferences > Security & Privacy > Firewall)
# Add TOR to allowed applications
```

## Development Setup

### Install Development Dependencies
```bash
pip install -r requirements.txt
pip install pytest black flake8 mypy
```

### Run Tests
```bash
pytest test_ghostpass.py -v
```

### Code Formatting
```bash
black ghostpass/
flake8 ghostpass/
```

## Uninstallation

### Remove GHOST PASS
```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf ghostpass_env

# Remove installation
pip uninstall ghostpass -y
```

### Remove TOR
```bash
# Stop TOR service
brew services stop tor

# Remove TOR
brew uninstall tor
```

## Advanced Configuration

### Using TOR Browser Instead of TOR Service
```bash
# Download TOR Browser from: https://www.torproject.org/download/
# Extract and run TOR Browser
# Configure SOCKS proxy in applications to use localhost:9050
```

### Custom TOR Configuration
```bash
# Create custom TOR config
mkdir -p ~/.tor
nano ~/.tor/torrc

# Add custom settings:
# SocksPort 9050
# ControlPort 9051
# CookieAuthentication 1
# DataDirectory ~/.tor/data
# Log notice file ~/.tor/notices.log
```

## Support

If you encounter issues:

1. Check TOR logs: `tail -f /usr/local/var/log/tor/notices.log`
2. Verify TOR is running: `brew services list | grep tor`
3. Test TOR connectivity: `curl --socks5 localhost:9050 --socks5-hostname localhost:9050 -s https://check.torproject.org/`
4. Check GitHub issues: https://github.com/DarkNight30622/GhostPass/issues

---

**🎉 Success!** GHOST PASS is now installed and ready to use on macOS! 