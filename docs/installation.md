# GHOST PASS Installation Guide

This guide will help you install GHOST PASS on your system.

## Prerequisites

- Python 3.8 or higher
- TOR Browser or TOR service
- Windows, Linux, or macOS

## Installation Methods

### Method 1: From Source (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ghostpass/ghostpass.git
   cd ghostpass
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install GHOST PASS:**
   ```bash
   pip install -e .
   ```

4. **Verify installation:**
   ```bash
   python test_ghostpass.py
   ```

### Method 2: Using pip

```bash
pip install ghostpass
```

### Method 3: Using conda

```bash
conda install -c conda-forge ghostpass
```

## TOR Setup

GHOST PASS requires TOR to be installed and configured. Here are the setup instructions for different platforms:

### Windows

1. **Download TOR Browser:**
   - Visit https://www.torproject.org/download/
   - Download and install TOR Browser

2. **Configure TOR for GHOST PASS:**
   - Open TOR Browser
   - Go to `about:config`
   - Set `network.proxy.socks_remote_dns` to `true`
   - Set `network.proxy.socks` to `127.0.0.1`
   - Set `network.proxy.socks_port` to `9050`

### Linux

1. **Install TOR:**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install tor

   # CentOS/RHEL
   sudo yum install tor

   # Arch Linux
   sudo pacman -S tor
   ```

2. **Configure TOR:**
   ```bash
   sudo nano /etc/tor/torrc
   ```

   Add these lines:
   ```
   SocksPort 9050
   ControlPort 9051
   CookieAuthentication 1
   ```

3. **Start TOR service:**
   ```bash
   sudo systemctl enable tor
   sudo systemctl start tor
   ```

### macOS

1. **Install TOR using Homebrew:**
   ```bash
   brew install tor
   ```

2. **Configure TOR:**
   ```bash
   nano /usr/local/etc/tor/torrc
   ```

   Add these lines:
   ```
   SocksPort 9050
   ControlPort 9051
   CookieAuthentication 1
   ```

3. **Start TOR service:**
   ```bash
   brew services start tor
   ```

## Quick Start

1. **Launch GHOST PASS:**
   ```bash
   # Interactive mode
   python -m ghostpass

   # CLI mode
   python -m ghostpass --connect
   ```

2. **Connect to TOR:**
   - In interactive mode: Click "Connect"
   - In CLI mode: Use `--connect` flag

3. **Verify connection:**
   ```bash
   python -m ghostpass --status
   ```

## Configuration

GHOST PASS uses a configuration file located at:
- Windows: `%USERPROFILE%\.ghostpass\config.yaml`
- Linux/macOS: `~/.ghostpass/config.yaml`

### Default Configuration

```yaml
app_name: "GHOST PASS"
version: "0.1.0"
debug_mode: false

tor:
  socks_port: 9050
  control_port: 9051
  data_directory: "./tor_data"
  max_circuit_dirtiness: 600
  new_circuit_period: 30

encryption:
  algorithm: "Multi-Layer"
  key_size: 32
  salt_size: 16
  iv_size: 12
  tag_size: 16
  iterations: 100000

rotation:
  default_mode: "manual"
  interval_minutes: 30
  performance_threshold: 0.5
  max_rotation_attempts: 3

security:
  enable_kill_switch: true
  enable_dns_protection: true
  enable_webrtc_protection: true
  safe_exit_nodes_only: true

ui:
  theme: "dark"
  refresh_interval: 5
  show_animations: true

logging:
  level: "INFO"
  file_path: null
  max_file_size: 10485760
```

## Troubleshooting

### Common Issues

1. **TOR Connection Failed:**
   - Ensure TOR is running
   - Check if ports 9050 and 9051 are available
   - Verify TOR configuration

2. **Permission Denied:**
   - On Linux/macOS, ensure you have proper permissions
   - Try running with `sudo` if necessary

3. **Import Errors:**
   - Ensure all dependencies are installed
   - Check Python version (3.8+ required)
   - Try reinstalling: `pip install --force-reinstall ghostpass`

4. **Port Already in Use:**
   - Check if another TOR instance is running
   - Change ports in configuration
   - Kill existing processes: `pkill tor`

### Getting Help

- Check the [GitHub Issues](https://github.com/ghostpass/ghostpass/issues)
- Read the [Documentation](https://github.com/ghostpass/ghostpass/docs)
- Join our [Discord Community](https://discord.gg/ghostpass)

## Security Notes

- GHOST PASS is designed for privacy and security
- Always verify you're downloading from the official repository
- Keep TOR and GHOST PASS updated
- Use strong passwords for encryption
- Be aware of your local laws regarding TOR usage

## Uninstallation

To uninstall GHOST PASS:

```bash
pip uninstall ghostpass
```

To remove configuration files:

```bash
# Windows
rmdir /s "%USERPROFILE%\.ghostpass"

# Linux/macOS
rm -rf ~/.ghostpass
``` 