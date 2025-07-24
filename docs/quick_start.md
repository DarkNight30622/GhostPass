# ⚡ Quick Start Guide - GHOST PASS

## 🚀 One-Command Installation

### Ubuntu/Debian
```bash
# Download and run installation script
curl -sSL https://raw.githubusercontent.com/DarkNight30622/GhostPass/main/ubuntu_install.sh | bash
```

### Windows (PowerShell)
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/DarkNight30622/GhostPass/main/windows_install.ps1" -OutFile "install.ps1"
.\install.ps1
```

### macOS
```bash
# Download and run installation script
curl -sSL https://raw.githubusercontent.com/DarkNight30622/GhostPass/main/macos_install.sh | bash
```

## 📋 Manual Quick Installation

### 1. Clone Repository
```bash
git clone https://github.com/DarkNight30622/GhostPass.git
cd GhostPass
```

### 2. Install Dependencies

#### Ubuntu/Debian
```bash
sudo apt update && sudo apt install -y python3 python3-pip python3-venv git tor
```

#### Windows
```powershell
# Install Python from python.org
# Install Git from git-scm.com
# Download TOR Browser from torproject.org
```

#### macOS
```bash
brew install python git tor
```

### 3. Setup Python Environment
```bash
# Create virtual environment
python3 -m venv ghostpass_env

# Activate environment
source ghostpass_env/bin/activate  # Linux/macOS
ghostpass_env\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

### 4. Configure TOR

#### Linux
```bash
sudo nano /etc/tor/torrc
# Add: SocksPort 9050, ControlPort 9051, CookieAuthentication 1
sudo systemctl start tor
```

#### macOS
```bash
nano /usr/local/etc/tor/torrc
# Add: SocksPort 9050, ControlPort 9051, CookieAuthentication 1
brew services start tor
```

#### Windows
```powershell
# Create torrc file in TOR Browser directory
# Add: SocksPort 9050, ControlPort 9051, CookieAuthentication 1
# Start TOR Browser
```

## 🎯 First Run

### Activate Environment
```bash
# Linux/macOS
source ghostpass_env/bin/activate

# Windows
ghostpass_env\Scripts\activate
```

### Run GHOST PASS
```bash
# Interactive UI mode
ghostpass

# CLI mode
ghostpass --help
```

## 🔧 Basic Commands

### Connection Management
```bash
ghostpass connect          # Connect to TOR network
ghostpass disconnect       # Disconnect from TOR
ghostpass status           # Show connection status
```

### IP Management
```bash
ghostpass rotate-ip        # Rotate to new IP
ghostpass show-ip          # Show current IP and location
ghostpass auto-rotate 300  # Auto-rotate every 5 minutes
```

### Security Testing
```bash
ghostpass test             # Run anonymity test
ghostpass test-dns         # Test DNS leak protection
ghostpass test-webrtc      # Test WebRTC leak protection
```

### Configuration
```bash
ghostpass config           # Open configuration menu
ghostpass kill-switch on   # Enable kill switch
ghostpass split-tunnel     # Configure split tunneling
```

## 🧪 Testing Your Installation

### Test GHOST PASS
```bash
# Run test suite
python test_ghostpass.py

# Test basic functionality
ghostpass --help
ghostpass status
```

### Test TOR Connection
```bash
# Test TOR connectivity
curl --socks5 localhost:9050 --socks5-hostname localhost:9050 -s https://check.torproject.org/

# Should show "Congratulations" if working
```

### Test IP Anonymity
```bash
# Check your IP before connecting
curl -s https://ipinfo.io/ip

# Connect to TOR
ghostpass connect

# Check your IP after connecting
curl --socks5 localhost:9050 --socks5-hostname localhost:9050 -s https://ipinfo.io/ip
```

## 🚨 Troubleshooting Quick Fixes

### Common Issues

#### 1. "Command not found: ghostpass"
```bash
# Ensure virtual environment is activated
source ghostpass_env/bin/activate  # Linux/macOS
ghostpass_env\Scripts\activate     # Windows

# Reinstall GHOST PASS
pip install -e .
```

#### 2. "TOR connection failed"
```bash
# Check TOR service status
sudo systemctl status tor  # Linux
brew services list | grep tor  # macOS

# Restart TOR service
sudo systemctl restart tor  # Linux
brew services restart tor   # macOS
```

#### 3. "Module not found"
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### 4. "Permission denied"
```bash
# Fix permissions
sudo chown -R $USER:$USER /home/$USER/GhostPass  # Linux
```

## 📚 Next Steps

### Read Full Documentation
- [Ubuntu Installation Guide](ubuntu_installation.md)
- [Windows Installation Guide](windows_installation.md)
- [macOS Installation Guide](macOS_installation.md)
- [Linux Installation Guide](linux_installation.md)

### Advanced Features
- Configure split tunneling
- Set up custom TOR circuits
- Enable pluggable transports
- Configure DNS over HTTPS

### Development
- [Contributing Guide](../CONTRIBUTING.md)
- [Development Setup](../docs/development.md)
- [API Documentation](../docs/api.md)

## 🆘 Need Help?

### Quick Support
1. Check [Troubleshooting Guide](troubleshooting.md)
2. Run `ghostpass --help` for command options
3. Check TOR status: `curl --socks5 localhost:9050 --socks5-hostname localhost:9050 -s https://check.torproject.org/`

### Community Support
- [GitHub Issues](https://github.com/DarkNight30622/GhostPass/issues)
- [GitHub Discussions](https://github.com/DarkNight30622/GhostPass/discussions)
- [Documentation](https://github.com/DarkNight30622/GhostPass#readme)

---

**🎉 You're ready to use GHOST PASS!** Start with `ghostpass` to launch the interactive interface. 