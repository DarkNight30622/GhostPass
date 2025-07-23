"""
GHOST PASS - Privacy-First CLI-Based VPN & IP-Masking Tool

A cross-platform tool that securely routes internet traffic through TOR
with advanced encryption, automatic IP rotation, and zero logging.
"""

__version__ = "0.1.0"
__author__ = "GHOST PASS Team"
__license__ = "MIT"

from .core.tor_controller import TorController
from .core.encryption import EncryptionManager
from .core.ip_rotator import IPRotator
from .ui.dashboard import Dashboard
from .cli.main import main

__all__ = [
    "TorController",
    "EncryptionManager", 
    "IPRotator",
    "Dashboard",
    "main"
] 