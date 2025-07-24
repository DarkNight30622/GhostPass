# 🐧 Linux Installation Guide - GHOST PASS

## Supported Distributions

- **Ubuntu/Debian** (20.04+, Debian 11+)
- **CentOS/RHEL/Fedora** (CentOS 8+, RHEL 8+, Fedora 32+)
- **Arch Linux** (latest)
- **OpenSUSE** (Leap 15.3+, Tumbleweed)
- **Other distributions** with Python 3.8+

## Prerequisites

### System Requirements
- Linux kernel 4.0+
- Python 3.8 or higher
- Git
- TOR service
- Package manager (apt, dnf, pacman, zypper)

### Check System Requirements
```bash
# Check Linux distribution
cat /etc/os-release

# Check Python version
python3 --version

# Check Git version
git --version

# Check package manager
which apt dnf pacman zypper 2>/dev/null
```

## Ubuntu/Debian Installation

### Step-by-Step Installation

#### 1. Update System
```bash
sudo apt update && sudo apt upgrade -y
```

#### 2. Install Dependencies
```bash
sudo apt install -y python3 python3-pip python3-venv git curl wget tor
```

#### 3. Clone Repository
```bash
git clone https://github.com/DarkNight30622/GhostPass.git
cd GhostPass
```

#### 4. Create Virtual Environment
```bash
python3 -m venv ghostpass_env
source ghostpass_env/bin/activate
```

#### 5. Install Python Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 6. Install GHOST PASS
```bash
pip install -e .
```

#### 7. Configure TOR
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

#### 8. Start TOR Service
```bash
sudo systemctl start tor
sudo systemctl enable tor
sudo systemctl status tor
```

## CentOS/RHEL/Fedora Installation

### Step-by-Step Installation

#### 1. Update System
```bash
# CentOS/RHEL
sudo dnf update -y

# Fedora
sudo dnf update -y
```

#### 2. Install Dependencies
```bash
sudo dnf install -y python3 python3-pip git tor
```

#### 3. Clone Repository
```bash
git clone https://github.com/DarkNight30622/GhostPass.git
cd GhostPass
```

#### 4. Create Virtual Environment
```bash
python3 -m venv ghostpass_env
source ghostpass_env/bin/activate
```

#### 5. Install Python Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 6. Install GHOST PASS
```bash
pip install -e .
```

#### 7. Configure TOR
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

#### 8. Start TOR Service
```bash
sudo systemctl start tor
sudo systemctl enable tor
sudo systemctl status tor
```

## Arch Linux Installation

### Step-by-Step Installation

#### 1. Update System
```bash
sudo pacman -Syu
```

#### 2. Install Dependencies
```bash
sudo pacman -S python python-pip git tor
```

#### 3. Clone Repository
```bash
git clone https://github.com/DarkNight30622/GhostPass.git
cd GhostPass
```

#### 4. Create Virtual Environment
```bash
python -m venv ghostpass_env
source ghostpass_env/bin/activate
```

#### 5. Install Python Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 6. Install GHOST PASS
```bash
pip install -e .
```

#### 7. Configure TOR
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

#### 8. Start TOR Service
```bash
sudo systemctl start tor
sudo systemctl enable tor
sudo systemctl status tor
```

## OpenSUSE Installation

### Step-by-Step Installation

#### 1. Update System
```bash
sudo zypper update
```

#### 2. Install Dependencies
```bash
sudo zypper install python3 python3-pip git tor
```

#### 3. Clone Repository
```bash
git clone https://github.com/DarkNight30622/GhostPass.git
cd GhostPass
```

#### 4. Create Virtual Environment
```bash
python3 -m venv ghostpass_env
source ghostpass_env/bin/activate
```

#### 5. Install Python Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 6. Install GHOST PASS
```bash
pip install -e .
```

#### 7. Configure TOR
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

#### 8. Start TOR Service
```bash
sudo systemctl start tor
sudo systemctl enable tor
sudo systemctl status tor
```

## Testing Installation

### Verify GHOST PASS Installation
```bash
# Test GHOST PASS
ghostpass --help

# Run tests
python test_ghostpass.py
```

### Verify TOR Connection
```bash
# Test TOR connectivity
curl --socks5 localhost:9050 --socks5-hostname localhost:9050 -s https://check.torproject.org/

# Check TOR status
sudo systemctl status tor
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

### Distribution-Specific Issues

#### Ubuntu/Debian
```bash
# Fix externally-managed-environment error
python3 -m venv ghostpass_env --system-site-packages
```

#### CentOS/RHEL/Fedora
```bash
# Install development tools
sudo dnf groupinstall "Development Tools"
sudo dnf install python3-devel
```

#### Arch Linux
```bash
# Install base-devel for compilation
sudo pacman -S base-devel
```

#### OpenSUSE
```bash
# Install development tools
sudo zypper install -t pattern devel_basis
```

## Network Configuration

### Check TOR Status
```bash
# Test TOR connectivity
curl --socks5 localhost:9050 --socks5-hostname localhost:9050 -s https://check.torproject.org/
```

### Configure Firewall
```bash
# Ubuntu/Debian (ufw)
sudo ufw allow 9050/tcp
sudo ufw allow 9051/tcp

# CentOS/RHEL/Fedora (firewalld)
sudo firewall-cmd --permanent --add-port=9050/tcp
sudo firewall-cmd --permanent --add-port=9051/tcp
sudo firewall-cmd --reload

# Arch Linux (iptables)
sudo iptables -A INPUT -p tcp --dport 9050 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 9051 -j ACCEPT
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
# Stop TOR service
sudo systemctl stop tor
sudo systemctl disable tor

# Remove TOR package
# Ubuntu/Debian
sudo apt remove tor -y

# CentOS/RHEL/Fedora
sudo dnf remove tor -y

# Arch Linux
sudo pacman -R tor

# OpenSUSE
sudo zypper remove tor
```

## Support

If you encounter issues:

1. Check TOR logs: `sudo journalctl -u tor@default.service`
2. Verify TOR is running: `sudo systemctl status tor`
3. Test TOR connectivity: `curl --socks5 localhost:9050 --socks5-hostname localhost:9050 -s https://check.torproject.org/`
4. Check GitHub issues: https://github.com/DarkNight30622/GhostPass/issues

---

**🎉 Success!** GHOST PASS is now installed and ready to use on Linux! 