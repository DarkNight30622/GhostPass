# 🪟 Windows Installation Guide - GHOST PASS

## Prerequisites

### System Requirements
- Windows 10/11 (64-bit)
- Python 3.8 or higher
- Git for Windows
- TOR Browser or TOR service
- PowerShell 5.0 or higher

### Check System Requirements
```powershell
# Check Windows version
winver

# Check Python version
python --version

# Check Git version
git --version

# Check PowerShell version
$PSVersionTable.PSVersion
```

## Step-by-Step Installation

### 1. Install Python
```powershell
# Option A: Download from python.org
# Visit: https://www.python.org/downloads/
# Download Python 3.8+ and install with "Add to PATH" checked

# Option B: Install via Microsoft Store
# Search for "Python" in Microsoft Store and install

# Verify installation
python --version
pip --version
```

### 2. Install Git for Windows
```powershell
# Download from: https://git-scm.com/download/win
# Or install via winget
winget install Git.Git

# Verify installation
git --version
```

### 3. Clone the Repository
```powershell
# Clone from your repository
git clone https://github.com/DarkNight30622/GhostPass.git
cd GhostPass
```

### 4. Create Virtual Environment
```powershell
# Create virtual environment
python -m venv ghostpass_env

# Activate virtual environment
ghostpass_env\Scripts\activate
```

### 5. Upgrade pip
```powershell
python -m pip install --upgrade pip
```

### 6. Install Python Dependencies
```powershell
pip install -r requirements.txt
```

### 7. Install GHOST PASS
```powershell
pip install -e .
```

### 8. Install TOR

#### Option A: TOR Browser (Recommended for beginners)
```powershell
# Download TOR Browser from: https://www.torproject.org/download/
# Extract to C:\Users\[username]\Desktop\Tor\
# Run tor.exe to start TOR service
```

#### Option B: TOR Service (Advanced users)
```powershell
# Install via chocolatey (if available)
choco install tor

# Or download TOR service from: https://www.torproject.org/download/tor/
```

### 9. Configure TOR

#### For TOR Browser:
Create `C:\Users\[username]\Desktop\Tor\torrc`:
```
SocksPort 9050
ControlPort 9051
CookieAuthentication 1
DataDirectory C:\Users\[username]\Desktop\Tor\Data
Log notice file C:\Users\[username]\Desktop\Tor\notices.log
```

#### For TOR Service:
Edit `C:\ProgramData\Tor\torrc`:
```
SocksPort 9050
ControlPort 9051
CookieAuthentication 1
DataDirectory C:\ProgramData\Tor\Data
Log notice file C:\ProgramData\Tor\notices.log
```

### 10. Start TOR Service
```powershell
# For TOR Browser: Run tor.exe manually
# For TOR Service: Start as Windows service
```

### 11. Verify Installation
```powershell
# Test GHOST PASS installation
ghostpass --help

# Test TOR connection (if TOR is running)
curl --socks5 localhost:9050 --socks5-hostname localhost:9050 -s https://check.torproject.org/
```

## Testing GHOST PASS

### Run the Application
```powershell
# Interactive UI mode
ghostpass

# CLI mode
ghostpass --help
ghostpass connect
ghostpass status
```

### Test Core Functionality
```powershell
# Run the test suite
python test_ghostpass.py
```

## Troubleshooting

### Common Issues

#### 1. Python Not Found
```powershell
# Add Python to PATH manually
# System Properties > Environment Variables > Path > Add Python installation directory
```

#### 2. Permission Denied Errors
```powershell
# Run PowerShell as Administrator
# Or change execution policy
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 3. Virtual Environment Issues
```powershell
# Recreate virtual environment
deactivate
Remove-Item -Recurse -Force ghostpass_env
python -m venv ghostpass_env
ghostpass_env\Scripts\activate
```

#### 4. TOR Connection Issues
```powershell
# Check if TOR is running
netstat -an | findstr 9050

# Test TOR connectivity
curl --socks5 localhost:9050 --socks5-hostname localhost:9050 -s https://check.torproject.org/
```

#### 5. Module Not Found Errors
```powershell
# Ensure virtual environment is activated
ghostpass_env\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Network Configuration

#### Check TOR Status
```powershell
# Test TOR connectivity
curl --socks5 localhost:9050 --socks5-hostname localhost:9050 -s https://check.torproject.org/
```

#### Configure Windows Firewall
```powershell
# Allow TOR ports (run as Administrator)
netsh advfirewall firewall add rule name="TOR SOCKS" dir=in action=allow protocol=TCP localport=9050
netsh advfirewall firewall add rule name="TOR Control" dir=in action=allow protocol=TCP localport=9051
```

## Development Setup

### Install Development Dependencies
```powershell
pip install -r requirements.txt
pip install pytest black flake8 mypy
```

### Run Tests
```powershell
pytest test_ghostpass.py -v
```

### Code Formatting
```powershell
black ghostpass/
flake8 ghostpass/
```

## Uninstallation

### Remove GHOST PASS
```powershell
# Deactivate virtual environment
deactivate

# Remove virtual environment
Remove-Item -Recurse -Force ghostpass_env

# Remove installation
pip uninstall ghostpass -y
```

### Remove TOR (optional)
```powershell
# Stop TOR service
# Remove TOR installation directory
```

## Support

If you encounter issues:

1. Check Windows Event Viewer for TOR errors
2. Verify TOR is running: `netstat -an | findstr 9050`
3. Test TOR connectivity: `curl --socks5 localhost:9050 --socks5-hostname localhost:9050 -s https://check.torproject.org/`
4. Check GitHub issues: https://github.com/DarkNight30622/GhostPass/issues

---

**🎉 Success!** GHOST PASS is now installed and ready to use on Windows! 