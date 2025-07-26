# GHOST PASS - Solution to Your Installation Issues

This document provides step-by-step solutions to the specific errors you encountered.

## Your Errors and Solutions

### Error 1: `requirements.txt` Not Found
```
ERROR: Could not open requirements file: [Errno 2] No such file or directory: 'requirements.txt'
```

**Solution:**
The file exists but might be corrupted. Run these commands:

```bash
# Make sure you're in the ghostpass directory
cd ghostpass

# Check if the file exists
ls -la requirements.txt

# If it doesn't exist or is corrupted, re-clone
cd ..
rm -rf ghostpass
git clone https://github.com/ghostpass/ghostpass.git
cd ghostpass
```

### Error 2: `setup.py` Not Found
```
ERROR: file:///home/darknight/ghostpass does not appear to be a Python project: neither 'setup.py' nor 'pyproject.toml' found.
```

**Solution:**
Same issue as above. The file exists but is corrupted.

```bash
# Re-clone the repository (same as above)
cd ..
rm -rf ghostpass
git clone https://github.com/ghostpass/ghostpass.git
cd ghostpass
```

### Error 3: TOR Configuration (sudo password issues)
```
[sudo] password for darknight:
Sorry, try again.
```

**Solution:**
You don't need sudo access. Use the provided scripts:

```bash
# Configure TOR without sudo
./configure_tor.sh

# Start TOR without sudo
~/.ghostpass/tor/start_tor.sh
```

## Complete Solution (Step-by-Step)

### Step 1: Fix the Repository
```bash
# Go back to home directory
cd ~

# Remove corrupted repository
rm -rf ghostpass

# Re-clone the repository
git clone https://github.com/ghostpass/ghostpass.git

# Enter the directory
cd ghostpass
```

### Step 2: Verify Files Exist
```bash
# Check if files exist
ls -la requirements.txt setup.py

# You should see both files listed
```

### Step 3: Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv ghostpass_env

# Activate it
source ghostpass_env/bin/activate
```

### Step 4: Install Dependencies
```bash
# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### Step 5: Install GHOST PASS
```bash
# Install in development mode
pip install -e .
```

### Step 6: Configure TOR (No sudo required)
```bash
# Configure TOR
./configure_tor.sh

# Start TOR
~/.ghostpass/tor/start_tor.sh
```

### Step 7: Test Installation
```bash
# Test the installation
python test_installation.py

# Or test manually
python -m ghostpass --help
```

## Quick Fix (Alternative)

If you want to skip the manual steps, use the provided scripts:

```bash
# Quick fix for immediate issues
./quick_fix.sh

# Or complete installation
./install.sh
```

## Verify Everything Works

After installation, test these commands:

```bash
# 1. Test CLI
python -m ghostpass --help

# 2. Test TOR connection
curl --socks5 127.0.0.1:9050 https://check.torproject.org/

# 3. Launch GHOST PASS
python -m ghostpass
```

## Expected Output

When everything works correctly:

1. **CLI Help:**
   ```
   Usage: python -m ghostpass [OPTIONS] COMMAND [ARGS]...
   
   GHOST PASS - Privacy-First CLI-Based VPN & IP-Masking Tool
   ```

2. **TOR Test:**
   ```
   Congratulations. This browser is configured to use Tor.
   ```

3. **GHOST PASS Dashboard:**
   ```
   🚀 GHOST PASS Dashboard
   [Interactive terminal UI appears]
   ```

## If You Still Have Issues

1. **Check file permissions:**
   ```bash
   chmod +x *.sh
   chmod 644 requirements.txt setup.py
   ```

2. **Check Python version:**
   ```bash
   python3 --version  # Should be 3.8 or higher
   ```

3. **Check virtual environment:**
   ```bash
   echo $VIRTUAL_ENV  # Should show path to ghostpass_env
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
   - `TROUBLESHOOTING.md` - Detailed troubleshooting

3. **Start using GHOST PASS:**
   ```bash
   python -m ghostpass
   ```

## Support

If you continue to have issues:

1. Check `TROUBLESHOOTING.md` for detailed solutions
2. Run `python test_installation.py` to identify specific problems
3. Check the logs: `sudo journalctl -u tor -f` (if using system TOR) 