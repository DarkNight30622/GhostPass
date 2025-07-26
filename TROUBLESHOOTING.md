# GHOST PASS Troubleshooting Guide

This guide addresses common installation and setup issues with GHOST PASS.

## Issues You Encountered

### 1. `requirements.txt` Not Found Error

**Error:**
```
ERROR: Could not open requirements file: [Errno 2] No such file or directory: 'requirements.txt'
```

**Solution:**
The `requirements.txt` file exists in the project. This error occurs when:
- You're not in the correct directory
- File permissions are incorrect
- The file was corrupted during download

**Fix:**
```bash
# Make sure you're in the ghostpass directory
cd ghostpass

# Check if the file exists
ls -la requirements.txt

# If it doesn't exist, the file is corrupted - re-clone the repository
cd ..
rm -rf ghostpass
git clone https://github.com/ghostpass/ghostpass.git
cd ghostpass
```

### 2. `setup.py` Not Found Error

**Error:**
```
ERROR: file:///home/darknight/ghostpass does not appear to be a Python project: neither 'setup.py' nor 'pyproject.toml' found.
```

**Solution:**
This error occurs when the `setup.py` file is missing or corrupted.

**Fix:**
```bash
# Check if setup.py exists
ls -la setup.py

# If missing, re-clone the repository
cd ..
rm -rf ghostpass
git clone https://github.com/ghostpass/ghostpass.git
cd ghostpass
```

### 3. TOR Configuration Issues

**Error:**
```
[sudo] password for darknight:
Sorry, try again.
```

**Solution:**
You don't need sudo access to configure TOR. Use the provided scripts.

**Fix:**
```bash
# Use the TOR configuration script
./configure_tor.sh

# Or manually configure TOR without sudo
mkdir -p ~/.ghostpass/tor
# Follow the instructions in configure_tor.sh
```

## Quick Fix Solutions

### Option 1: Use the Quick Fix Script

```bash
# Run the quick fix script
./quick_fix.sh
```

### Option 2: Manual Installation

```bash
# 1. Create and activate virtual environment
python3 -m venv ghostpass_env
source ghostpass_env/bin/activate

# 2. Upgrade pip
pip install --upgrade pip

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install the package
pip install -e .
```

### Option 3: Complete Installation

```bash
# Run the complete installation script
./install.sh
```

## TOR Setup

### Method 1: System TOR Service (Recommended)

```bash
# Install TOR
sudo apt update
sudo apt install -y tor

# Start TOR service
sudo systemctl start tor
sudo systemctl enable tor

# Check status
sudo systemctl status tor
```

### Method 2: User-Specific TOR (No sudo required)

```bash
# Configure user TOR
./configure_tor.sh

# Start TOR
~/.ghostpass/tor/start_tor.sh

# Stop TOR
~/.ghostpass/tor/stop_tor.sh
```

## Testing the Installation

### 1. Test Python Package

```bash
# Activate virtual environment
source ghostpass_env/bin/activate

# Test imports
python -c "import ghostpass; print('✅ GHOST PASS imported successfully')"

# Test CLI
python -m ghostpass --help
```

### 2. Test TOR Connection

```bash
# Test SOCKS proxy
curl --socks5 127.0.0.1:9050 https://check.torproject.org/

# Or use the test script
python test_installation.py
```

### 3. Run GHOST PASS

```bash
# Launch interactive dashboard
python -m ghostpass

# Or use CLI commands
python -m ghostpass connect
python -m ghostpass status
python -m ghostpass rotate-ip
```

## Common Issues and Solutions

### Issue: Permission Denied

**Error:**
```
PermissionError: [Errno 13] Permission denied
```

**Solution:**
```bash
# Fix file permissions
chmod +x *.sh
chmod 644 requirements.txt setup.py
```

### Issue: Module Not Found

**Error:**
```
ModuleNotFoundError: No module named 'ghostpass'
```

**Solution:**
```bash
# Make sure virtual environment is activated
source ghostpass_env/bin/activate

# Reinstall the package
pip install -e .
```

### Issue: TOR Connection Failed

**Error:**
```
Connection refused: 127.0.0.1:9050
```

**Solution:**
```bash
# Check if TOR is running
sudo systemctl status tor

# Start TOR if not running
sudo systemctl start tor

# Or use user TOR
~/.ghostpass/tor/start_tor.sh
```

### Issue: Port Already in Use

**Error:**
```
Address already in use: 127.0.0.1:9050
```

**Solution:**
```bash
# Find what's using the port
sudo netstat -tlnp | grep 9050

# Kill the process or use different ports
# Edit TOR configuration to use different ports
```

## File Structure Verification

After installation, your directory should look like this:

```
ghostpass/
├── ghostpass_env/          # Virtual environment
├── ghostpass/              # Main package
├── requirements.txt        # Dependencies
├── setup.py               # Package setup
├── install.sh             # Installation script
├── quick_fix.sh           # Quick fix script
├── configure_tor.sh       # TOR configuration
└── test_installation.py   # Test script
```

## Getting Help

If you continue to experience issues:

1. **Check the logs:**
   ```bash
   sudo journalctl -u tor -f
   ```

2. **Verify file integrity:**
   ```bash
   ls -la *.py *.txt *.sh
   ```

3. **Test individual components:**
   ```bash
   python -c "import stem; print('stem OK')"
   python -c "import socks; print('PySocks OK')"
   ```

4. **Reinstall from scratch:**
   ```bash
   rm -rf ghostpass_env
   ./install.sh
   ```

## Success Indicators

You'll know everything is working when:

- ✅ `python -m ghostpass --help` shows the CLI interface
- ✅ `curl --socks5 127.0.0.1:9050 https://check.torproject.org/` returns TOR confirmation
- ✅ `python -m ghostpass` launches the interactive dashboard
- ✅ No error messages appear during installation

## Next Steps

Once installation is successful:

1. **Learn the basics:**
   ```bash
   python -m ghostpass --help
   ```

2. **Read the documentation:**
   - `README.md` - Main documentation
   - `docs/` - Detailed guides

3. **Start using GHOST PASS:**
   ```bash
   python -m ghostpass
   ``` 