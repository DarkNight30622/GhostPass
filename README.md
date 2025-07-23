<div align="center">
  <img src="assets/logo.svg" alt="GHOST PASS Logo" width="400" height="200">
</div>

# GHOST PASS 🔒

**Privacy-First CLI-Based VPN & IP-Masking Tool**

A cross-platform, open-source tool that securely routes all internet traffic through the TOR network with advanced encryption, automatic IP rotation, and zero logging.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com/ghostpass/ghostpass)

## 🛡️ Core Features

- **🔐 Full TOR Integration**: SOCKS5 and transparent proxy routing
- **🔒 Multi-Layer Encryption**: AES-256-GCM, ChaCha20-Poly1305, TLS tunneling
- **⚡ Smart Performance**: Fast TOR circuits with fallback mechanisms
- **🛡️ DNS Protection**: Encrypted DNS (DoH/DoT) with leak protection
- **🔌 Kill Switch**: Automatic traffic blocking when connection drops
- **🔄 IP Rotation**: Scheduled and manual IP rotation with geolocation display
- **✅ Safe Exit Nodes**: Avoid flagged nodes and prioritize clean circuits
- **🎛️ Split Tunneling**: Selective application routing
- **🧪 Anonymity Testing**: Comprehensive leak detection
- **📊 Zero Logging**: No telemetry, no history, no sign-in required

## 🛠️ Technology Stack

- **Language**: Python 3.8+
- **TOR Integration**: `stem` library for TOR control
- **Encryption**: `cryptography` for AES-256, ChaCha20
- **UI Framework**: `Textual` for beautiful terminal interface
- **CLI Framework**: `Click` for command-line interface
- **Network**: `requests`, `PySocks` for proxy support
- **System**: `psutil` for process and network monitoring
- **Configuration**: `PyYAML` for config management

## 🔧 Installation

### Linux/macOS (bash)

```bash
# Clone the repository
git clone https://github.com/ghostpass/ghostpass.git
cd ghostpass

# Install TOR (Ubuntu/Debian)
sudo apt update && sudo apt install tor

# Install TOR (macOS)
brew install tor

# Create virtual environment
python3 -m venv ghostpass_env
source ghostpass_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install GHOST PASS
pip install -e .

# Configure TOR
sudo nano /etc/tor/torrc  # Linux
# or
nano /usr/local/etc/tor/torrc  # macOS

# Add these lines:
# SocksPort 9050
# ControlPort 9051
# CookieAuthentication 1

# Start TOR service
sudo systemctl start tor  # Linux
# or
brew services start tor  # macOS
```

### Windows (.exe)

```powershell
# Download the latest release from GitHub
# https://github.com/ghostpass/ghostpass/releases

# Extract and run
ghostpass.exe --help
```

### Python/pip-based Setup

```bash
# Install via pip
pip install ghostpass

# Or install from source
pip install git+https://github.com/ghostpass/ghostpass.git
```

## 📦 Usage Examples

### Basic Commands

```bash
# Connect to TOR network
ghostpass --connect

# Check connection status
ghostpass --status

# Rotate IP address
ghostpass --rotate-ip

# Run anonymity tests
ghostpass --test

# Launch interactive dashboard
ghostpass
```

### Advanced Usage

```bash
# Auto-rotation every 30 minutes
ghostpass --rotate-ip --interval 30

# Scheduled rotation at specific times
ghostpass --rotate-ip --schedule 09:00 --schedule 18:00

# Comprehensive anonymity testing
ghostpass --test --comprehensive

# Configure split tunneling
ghostpass --tunnel --app chrome --exclude updates

# Enable kill switch
ghostpass --killswitch --enable
```

### Interactive Dashboard

```bash
# Launch the beautiful terminal UI
ghostpass

# Navigate with arrow keys
# Press 'q' to quit
```

## 🧪 Testing

```bash
# Run the test suite
python test_ghostpass.py

# Expected output:
# 🧪 GHOST PASS Test Suite
# ==================================================
# ✅ Core modules imported successfully
# ✅ UI modules imported successfully
# ✅ CLI modules imported successfully
# ✅ Config modules imported successfully
# ✅ TOR controller initialized
# ✅ Encryption manager initialized
# ✅ IP rotator initialized
# ✅ UI components imported
# ==================================================
# Test Results: 6/6 tests passed
# 🎉 All tests passed! GHOST PASS is ready to use.
```

## 🔧 Developer Instructions

### Clone and Run Locally

```bash
# Clone the repository
git clone https://github.com/ghostpass/ghostpass.git
cd ghostpass

# Create virtual environment
python3 -m venv ghostpass_env
source ghostpass_env/bin/activate  # Linux/macOS
# or
ghostpass_env\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .

# Run tests
python test_ghostpass.py

# Run the application
python -m ghostpass
```

### Edit Configuration

```bash
# Configuration file location
# Linux/macOS: ~/.ghostpass/config.yaml
# Windows: %USERPROFILE%\.ghostpass\config.yaml

# Example configuration
cat > ~/.ghostpass/config.yaml << EOF
app_name: "GHOST PASS"
version: "0.1.0"
debug_mode: false

tor:
  socks_port: 9050
  control_port: 9051
  data_directory: "./tor_data"

encryption:
  algorithm: "Multi-Layer"
  key_size: 32
  salt_size: 16

rotation:
  default_mode: "manual"
  interval_minutes: 30

security:
  enable_kill_switch: true
  enable_dns_protection: true
  safe_exit_nodes_only: true
EOF
```

## 📁 Project Structure

```
ghostpass/
├── core/                 # Core functionality
│   ├── tor_controller.py # TOR connection management
│   ├── encryption.py     # Multi-layer encryption
│   └── ip_rotator.py     # IP rotation system
├── ui/                   # User interface
│   └── dashboard.py      # Textual-based dashboard
├── cli/                  # Command-line interface
│   └── main.py          # Click-based CLI
├── config/              # Configuration management
│   └── settings.py      # YAML/JSON config handling
├── utils/               # Utilities
│   ├── network.py       # Network testing & diagnostics
│   ├── security.py      # Security utilities
│   └── system.py        # System utilities
└── __main__.py          # Entry point
```

## 🚀 Building Executables

### Using PyInstaller

```bash
# Install PyInstaller
pip install pyinstaller

# Build for Windows
pyinstaller --onefile --windowed ghostpass/__main__.py --name ghostpass.exe

# Build for Linux
pyinstaller --onefile ghostpass/__main__.py --name ghostpass

# Build for macOS
pyinstaller --onefile --windowed ghostpass/__main__.py --name ghostpass.app
```

### Using Nuitka

```bash
# Install Nuitka
pip install nuitka

# Build optimized executable
python -m nuitka --onefile ghostpass/__main__.py
```

## 📊 Cross-Platform Support

| Platform | Status | Installation | Executable |
|----------|--------|--------------|------------|
| **Windows** | ✅ Full Support | pip/executable | `.exe` |
| **Linux** | ✅ Full Support | pip/package | `.bin` |
| **macOS** | ✅ Full Support | pip/package | `.app` |
| **WSL** | ✅ Full Support | pip | Python |

## 🔐 Security Features

- **Zero Logging**: No telemetry, no history tracking
- **Multi-Layer Encryption**: AES-256-GCM + ChaCha20-Poly1305
- **DNS Leak Protection**: Encrypted DNS with leak detection
- **WebRTC Protection**: Prevents WebRTC IP leaks
- **Kill Switch**: Automatic traffic blocking on connection loss
- **Safe Exit Nodes**: Avoids flagged TOR nodes
- **Split Tunneling**: Selective application routing

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/your-username/ghostpass.git
cd ghostpass

# Create feature branch
git checkout -b feature/amazing-feature

# Make your changes
# Add tests
# Update documentation

# Commit and push
git commit -m "Add amazing feature"
git push origin feature/amazing-feature

# Create Pull Request
```

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 GHOST PASS Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## ⚠️ Disclaimer

This tool is for educational and privacy purposes only. Users are responsible for complying with local laws and regulations regarding TOR usage and network privacy.

## 🆘 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/ghostpass/ghostpass/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ghostpass/ghostpass/discussions)
- **Wiki**: [GitHub Wiki](https://github.com/ghostpass/ghostpass/wiki)

## ☕ Support GHOST PASS

If you find GHOST PASS useful, consider supporting its development:

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://coff.ee/draknight) [![Buy Me A Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://buymeacoffee.com/draknight)

- **Ko-fi**: [https://coff.ee/draknight](https://coff.ee/draknight)
- **Buy Me a Coffee**: [https://buymeacoffee.com/draknight](https://buymeacoffee.com/draknight)

Your support helps us maintain and improve GHOST PASS for everyone! 💙

## 🙏 Acknowledgments

- [TOR Project](https://www.torproject.org/) for the TOR network
- [Textual](https://textual.textualize.io/) for the beautiful terminal UI
- [Click](https://click.palletsprojects.com/) for the CLI framework
- [Cryptography](https://cryptography.io/) for encryption libraries
- **Our amazing sponsors** for supporting development

---

**Built with ❤️ for privacy advocates, journalists, and developers**

**GHOST PASS - Your Digital Privacy Guardian** 🔒