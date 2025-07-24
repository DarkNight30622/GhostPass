# 🐧 Ubuntu Installation Guide - GHOST PASS

## Prerequisites

### System Requirements
- Ubuntu 20.04 LTS or later
- Python 3.8 or higher
- Git
- TOR service

### Check Python Version
```bash
python3 --version
# Should be 3.8 or higher
```

## Step-by-Step Installation

### 1. Update System Packages
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Install Required System Dependencies
```bash
sudo apt install -y python3 python3-pip python3-venv git curl wget
```

### 3. Install TOR Service
```bash
sudo apt install -y tor
```

### 4. Clone the Repository
```bash
# Clone from your actual repository
git clone https://github.com/DarkNight30622/GhostPass.git
cd GhostPass
```

### 5. Create Virtual Environment
```bash
python3 -m venv ghostpass_env
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

### 9. Configure TOR Service
```bash
# Backup original config
sudo cp /etc/tor/torrc /etc/tor/torrc.backup

# Edit TOR configuration
sudo nano /etc/tor/torrc
```

Add these lines to `/etc/tor/torrc`:
```
# GHOST PASS Configuration
SocksPort 9050
ControlPort 9051
CookieAuthentication 1
DataDirectory /var/lib/tor
Log notice file /var/log/tor/notices.log
```

### 10. Start TOR Service
```bash
# Start TOR service
sudo systemctl start tor

# Enable TOR to start on boot
sudo systemctl enable tor

# Check TOR status
sudo systemctl status tor
```

### 11. Verify Installation
```bash
# Test GHOST PASS installation
ghostpass --help

# Test TOR connection
curl --socks5 localhost:9050 --socks5-hostname localhost:9050 -s https://check.torproject.org/ | grep -q "Congratulations" && echo "TOR is working!" || echo "TOR connection failed"
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

#### 1. Permission Denied Errors
```bash
# Fix file permissions
sudo chown -R $USER:$USER /home/$USER/GhostPass
chmod +x setup.py
```

#### 2. TOR Service Not Starting
```bash
# Check TOR logs
sudo journalctl -u tor@default.service -f

# Restart TOR service
sudo systemctl restart tor
```

#### 3. Python Module Not Found
```bash
# Ensure virtual environment is activated
source ghostpass_env/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### 4. Port Already in Use
```bash
# Check what's using port 9050
sudo netstat -tlnp | grep 9050

# Kill conflicting process
sudo pkill -f tor
sudo systemctl start tor
```

### Network Configuration

#### Check TOR Status
```bash
# Test TOR connectivity
curl --socks5 localhost:9050 --socks5-hostname localhost:9050 -s https://check.torproject.org/
```

#### Configure Firewall (if needed)
```bash
# Allow TOR ports
sudo ufw allow 9050/tcp
sudo ufw allow 9051/tcp
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

### Remove TOR (optional)
```bash
sudo systemctl stop tor
sudo systemctl disable tor
sudo apt remove tor -y
```

## Support

If you encounter issues:

1. Check the logs: `sudo journalctl -u tor@default.service`
2. Verify TOR is running: `sudo systemctl status tor`
3. Test TOR connectivity: `curl --socks5 localhost:9050 --socks5-hostname localhost:9050 -s https://check.torproject.org/`
4. Check GitHub issues: https://github.com/DarkNight30622/GhostPass/issues

---

**🎉 Success!** GHOST PASS is now installed and ready to use on Ubuntu! 