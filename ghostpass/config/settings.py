"""
Configuration Module

Handles configuration management for GHOST PASS including
YAML/JSON config files, default settings, and environment variables.
"""

import os
import json
import yaml
from typing import Dict, Any, Optional
from pathlib import Path
from dataclasses import dataclass, field, asdict
from enum import Enum


class LogLevel(Enum):
    """Logging levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class EncryptionAlgorithm(Enum):
    """Supported encryption algorithms."""
    AES_256_GCM = "AES-256-GCM"
    CHACHA20_POLY1305 = "ChaCha20-Poly1305"
    MULTI_LAYER = "Multi-Layer"


@dataclass
class TorConfig:
    """TOR configuration settings."""
    socks_port: int = 9050
    control_port: int = 9051
    data_directory: str = "./tor_data"
    max_circuit_dirtiness: int = 600
    new_circuit_period: int = 30
    circuit_build_timeout: int = 30
    use_entry_guards: bool = True
    num_entry_guards: int = 6
    guard_lifetime: int = 2592000
    enforce_distinct_subnets: bool = True
    safe_logging: bool = True


@dataclass
class EncryptionConfig:
    """Encryption configuration settings."""
    algorithm: EncryptionAlgorithm = EncryptionAlgorithm.MULTI_LAYER
    key_size: int = 32
    salt_size: int = 16
    iv_size: int = 12
    tag_size: int = 16
    iterations: int = 100000
    enable_tls_tunneling: bool = True
    verify_ssl: bool = True


@dataclass
class RotationConfig:
    """IP rotation configuration settings."""
    default_mode: str = "manual"
    interval_minutes: int = 30
    schedule_times: list = field(default_factory=list)
    performance_threshold: float = 0.5
    max_rotation_attempts: int = 3
    cooldown_seconds: int = 60
    enable_auto_rotation: bool = False


@dataclass
class SecurityConfig:
    """Security configuration settings."""
    enable_kill_switch: bool = True
    enable_dns_protection: bool = True
    enable_webrtc_protection: bool = True
    enable_fingerprint_protection: bool = True
    block_trackers: bool = True
    safe_exit_nodes_only: bool = True
    exclude_countries: list = field(default_factory=list)


@dataclass
class UIConfig:
    """User interface configuration settings."""
    theme: str = "dark"
    refresh_interval: int = 5
    show_animations: bool = True
    enable_sounds: bool = False
    language: str = "en"


@dataclass
class LoggingConfig:
    """Logging configuration settings."""
    level: LogLevel = LogLevel.INFO
    file_path: Optional[str] = None
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


@dataclass
class GhostPassConfig:
    """Main configuration class for GHOST PASS."""
    
    # Core settings
    app_name: str = "GHOST PASS"
    version: str = "0.1.0"
    debug_mode: bool = False
    
    # Component configurations
    tor: TorConfig = field(default_factory=TorConfig)
    encryption: EncryptionConfig = field(default_factory=EncryptionConfig)
    rotation: RotationConfig = field(default_factory=RotationConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    ui: UIConfig = field(default_factory=UIConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    
    # Advanced settings
    portable_mode: bool = False
    offline_mode: bool = False
    enable_telemetry: bool = False
    auto_update: bool = False


class ConfigManager:
    """
    Manages configuration loading, saving, and validation.
    
    Supports:
    - YAML configuration files
    - JSON configuration files
    - Environment variables
    - Default settings
    - Configuration validation
    """
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._get_default_config_path()
        self.config = GhostPassConfig()
        self._load_config()
    
    def _get_default_config_path(self) -> str:
        """Get default configuration file path."""
        config_dir = Path.home() / ".ghostpass"
        config_dir.mkdir(exist_ok=True)
        return str(config_dir / "config.yaml")
    
    def _load_config(self):
        """Load configuration from file or create default."""
        try:
            if os.path.exists(self.config_path):
                self._load_from_file()
            else:
                self._create_default_config()
        except Exception as e:
            print(f"Warning: Could not load config from {self.config_path}: {e}")
            print("Using default configuration")
    
    def _load_from_file(self):
        """Load configuration from file."""
        file_path = Path(self.config_path)
        
        if file_path.suffix.lower() == '.yaml' or file_path.suffix.lower() == '.yml':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        elif file_path.suffix.lower() == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            raise ValueError(f"Unsupported config file format: {file_path.suffix}")
        
        self._update_config_from_dict(data)
    
    def _create_default_config(self):
        """Create default configuration file."""
        self._save_config()
    
    def _save_config(self):
        """Save current configuration to file."""
        try:
            file_path = Path(self.config_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            data = self._config_to_dict()
            
            if file_path.suffix.lower() == '.yaml' or file_path.suffix.lower() == '.yml':
                with open(file_path, 'w', encoding='utf-8') as f:
                    yaml.dump(data, f, default_flow_style=False, indent=2)
            elif file_path.suffix.lower() == '.json':
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
            
        except Exception as e:
            print(f"Warning: Could not save config to {self.config_path}: {e}")
    
    def _config_to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        data = asdict(self.config)
        
        # Convert enums to strings
        data['encryption']['algorithm'] = data['encryption']['algorithm'].value
        data['logging']['level'] = data['logging']['level'].value
        
        return data
    
    def _update_config_from_dict(self, data: Dict[str, Any]):
        """Update configuration from dictionary."""
        # Update TOR config
        if 'tor' in data:
            tor_data = data['tor']
            for key, value in tor_data.items():
                if hasattr(self.config.tor, key):
                    setattr(self.config.tor, key, value)
        
        # Update encryption config
        if 'encryption' in data:
            enc_data = data['encryption']
            for key, value in enc_data.items():
                if hasattr(self.config.encryption, key):
                    if key == 'algorithm':
                        value = EncryptionAlgorithm(value)
                    setattr(self.config.encryption, key, value)
        
        # Update rotation config
        if 'rotation' in data:
            rot_data = data['rotation']
            for key, value in rot_data.items():
                if hasattr(self.config.rotation, key):
                    setattr(self.config.rotation, key, value)
        
        # Update security config
        if 'security' in data:
            sec_data = data['security']
            for key, value in sec_data.items():
                if hasattr(self.config.security, key):
                    setattr(self.config.security, key, value)
        
        # Update UI config
        if 'ui' in data:
            ui_data = data['ui']
            for key, value in ui_data.items():
                if hasattr(self.config.ui, key):
                    setattr(self.config.ui, key, value)
        
        # Update logging config
        if 'logging' in data:
            log_data = data['logging']
            for key, value in log_data.items():
                if hasattr(self.config.logging, key):
                    if key == 'level':
                        value = LogLevel(value)
                    setattr(self.config.logging, key, value)
        
        # Update core settings
        for key in ['app_name', 'version', 'debug_mode', 'portable_mode', 
                   'offline_mode', 'enable_telemetry', 'auto_update']:
            if key in data:
                setattr(self.config, key, data[key])
    
    def get_tor_config(self) -> Dict[str, Any]:
        """Get TOR configuration as dictionary."""
        return asdict(self.config.tor)
    
    def get_encryption_config(self) -> Dict[str, Any]:
        """Get encryption configuration as dictionary."""
        config = asdict(self.config.encryption)
        config['algorithm'] = config['algorithm'].value
        return config
    
    def get_rotation_config(self) -> Dict[str, Any]:
        """Get rotation configuration as dictionary."""
        return asdict(self.config.rotation)
    
    def get_security_config(self) -> Dict[str, Any]:
        """Get security configuration as dictionary."""
        return asdict(self.config.security)
    
    def get_ui_config(self) -> Dict[str, Any]:
        """Get UI configuration as dictionary."""
        return asdict(self.config.ui)
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration as dictionary."""
        config = asdict(self.config.logging)
        config['level'] = config['level'].value
        return config
    
    def update_tor_config(self, **kwargs):
        """Update TOR configuration."""
        for key, value in kwargs.items():
            if hasattr(self.config.tor, key):
                setattr(self.config.tor, key, value)
        self._save_config()
    
    def update_encryption_config(self, **kwargs):
        """Update encryption configuration."""
        for key, value in kwargs.items():
            if hasattr(self.config.encryption, key):
                if key == 'algorithm':
                    value = EncryptionAlgorithm(value)
                setattr(self.config.encryption, key, value)
        self._save_config()
    
    def update_rotation_config(self, **kwargs):
        """Update rotation configuration."""
        for key, value in kwargs.items():
            if hasattr(self.config.rotation, key):
                setattr(self.config.rotation, key, value)
        self._save_config()
    
    def update_security_config(self, **kwargs):
        """Update security configuration."""
        for key, value in kwargs.items():
            if hasattr(self.config.security, key):
                setattr(self.config.security, key, value)
        self._save_config()
    
    def validate_config(self) -> bool:
        """Validate configuration settings."""
        try:
            # Validate TOR config
            if not (1024 <= self.config.tor.socks_port <= 65535):
                raise ValueError("Invalid SOCKS port")
            if not (1024 <= self.config.tor.control_port <= 65535):
                raise ValueError("Invalid control port")
            
            # Validate encryption config
            if self.config.encryption.key_size not in [16, 24, 32]:
                raise ValueError("Invalid key size")
            
            # Validate rotation config
            if self.config.rotation.interval_minutes < 1:
                raise ValueError("Invalid rotation interval")
            
            return True
            
        except Exception as e:
            print(f"Configuration validation failed: {e}")
            return False
    
    def reset_to_defaults(self):
        """Reset configuration to default values."""
        self.config = GhostPassConfig()
        self._save_config()
    
    def export_config(self, path: str):
        """Export configuration to file."""
        data = self._config_to_dict()
        
        file_path = Path(path)
        if file_path.suffix.lower() == '.yaml' or file_path.suffix.lower() == '.yml':
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, indent=2)
        elif file_path.suffix.lower() == '.json':
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        else:
            raise ValueError(f"Unsupported export format: {file_path.suffix}")
    
    def import_config(self, path: str):
        """Import configuration from file."""
        file_path = Path(path)
        
        if file_path.suffix.lower() == '.yaml' or file_path.suffix.lower() == '.yml':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        elif file_path.suffix.lower() == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            raise ValueError(f"Unsupported import format: {file_path.suffix}")
        
        self._update_config_from_dict(data)
        self._save_config()


# Global configuration instance
config_manager = ConfigManager()


def get_config() -> GhostPassConfig:
    """Get global configuration instance."""
    return config_manager.config


def get_tor_config() -> Dict[str, Any]:
    """Get TOR configuration."""
    return config_manager.get_tor_config()


def get_encryption_config() -> Dict[str, Any]:
    """Get encryption configuration."""
    return config_manager.get_encryption_config()


def get_rotation_config() -> Dict[str, Any]:
    """Get rotation configuration."""
    return config_manager.get_rotation_config()


def get_security_config() -> Dict[str, Any]:
    """Get security configuration."""
    return config_manager.get_security_config()


def get_ui_config() -> Dict[str, Any]:
    """Get UI configuration."""
    return config_manager.get_ui_config()


def get_logging_config() -> Dict[str, Any]:
    """Get logging configuration."""
    return config_manager.get_logging_config() 