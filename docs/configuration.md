# GHOST PASS Configuration Guide

This guide covers all configuration options for GHOST PASS.

## Configuration File Location

- **Linux/macOS**: `~/.ghostpass/config.yaml`
- **Windows**: `%USERPROFILE%\.ghostpass\config.yaml`

## Default Configuration

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
  circuit_build_timeout: 30
  use_entry_guards: true
  num_entry_guards: 6
  guard_lifetime: 2592000
  enforce_distinct_subnets: true
  safe_logging: true

encryption:
  algorithm: "Multi-Layer"
  key_size: 32
  salt_size: 16
  iv_size: 12
  tag_size: 16
  iterations: 100000
  enable_tls_tunneling: true
  verify_ssl: true

rotation:
  default_mode: "manual"
  interval_minutes: 30
  schedule_times: []
  performance_threshold: 0.5
  max_rotation_attempts: 3
  cooldown_seconds: 60
  enable_auto_rotation: false

security:
  enable_kill_switch: true
  enable_dns_protection: true
  enable_webrtc_protection: true
  enable_fingerprint_protection: true
  block_trackers: true
  safe_exit_nodes_only: true
  exclude_countries: []

ui:
  theme: "dark"
  refresh_interval: 5
  show_animations: true
  enable_sounds: false
  language: "en"

logging:
  level: "INFO"
  file_path: null
  max_file_size: 10485760
  backup_count: 5
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

portable_mode: false
offline_mode: false
enable_telemetry: false
auto_update: false
```

## Configuration Options

### TOR Settings

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `socks_port` | int | 9050 | TOR SOCKS proxy port |
| `control_port` | int | 9051 | TOR control port |
| `data_directory` | str | "./tor_data" | TOR data directory |
| `max_circuit_dirtiness` | int | 600 | Max circuit lifetime (seconds) |
| `new_circuit_period` | int | 30 | New circuit creation period |
| `use_entry_guards` | bool | true | Use entry guards |
| `num_entry_guards` | int | 6 | Number of entry guards |

### Encryption Settings

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `algorithm` | str | "Multi-Layer" | Encryption algorithm |
| `key_size` | int | 32 | Key size in bytes |
| `salt_size` | int | 16 | Salt size in bytes |
| `iterations` | int | 100000 | PBKDF2 iterations |
| `enable_tls_tunneling` | bool | true | Enable TLS tunneling |

### Rotation Settings

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `default_mode` | str | "manual" | Default rotation mode |
| `interval_minutes` | int | 30 | Auto-rotation interval |
| `performance_threshold` | float | 0.5 | Performance threshold |
| `enable_auto_rotation` | bool | false | Enable auto-rotation |

### Security Settings

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enable_kill_switch` | bool | true | Enable kill switch |
| `enable_dns_protection` | bool | true | Enable DNS protection |
| `safe_exit_nodes_only` | bool | true | Use safe exit nodes only |
| `exclude_countries` | list | [] | Countries to exclude |

## Environment Variables

You can override configuration using environment variables:

```bash
# TOR settings
export GHOSTPASS_TOR_SOCKS_PORT=9050
export GHOSTPASS_TOR_CONTROL_PORT=9051

# Encryption settings
export GHOSTPASS_ENCRYPTION_ALGORITHM="Multi-Layer"
export GHOSTPASS_ENCRYPTION_KEY_SIZE=32

# Security settings
export GHOSTPASS_SECURITY_ENABLE_KILL_SWITCH=true
export GHOSTPASS_SECURITY_SAFE_EXIT_NODES_ONLY=true
```

## Configuration Validation

GHOST PASS validates configuration on startup:

```bash
# Validate configuration
python -c "from ghostpass.config import ConfigManager; cm = ConfigManager(); print('Valid' if cm.validate_config() else 'Invalid')"
```

## Configuration Examples

### High Security Configuration

```yaml
tor:
  socks_port: 9050
  control_port: 9051
  use_entry_guards: true
  num_entry_guards: 10

encryption:
  algorithm: "Multi-Layer"
  key_size: 32
  iterations: 200000

security:
  enable_kill_switch: true
  enable_dns_protection: true
  enable_webrtc_protection: true
  safe_exit_nodes_only: true
  exclude_countries: ["US", "GB", "CA"]

rotation:
  default_mode: "performance"
  performance_threshold: 0.7
  enable_auto_rotation: true
```

### Performance Configuration

```yaml
tor:
  socks_port: 9050
  control_port: 9051
  max_circuit_dirtiness: 300
  new_circuit_period: 15

encryption:
  algorithm: "AES-256-GCM"
  key_size: 32

rotation:
  default_mode: "interval"
  interval_minutes: 15
  enable_auto_rotation: true

ui:
  refresh_interval: 2
  show_animations: false
```

### Development Configuration

```yaml
debug_mode: true

logging:
  level: "DEBUG"
  file_path: "./ghostpass.log"

tor:
  socks_port: 9050
  control_port: 9051
  safe_logging: false

ui:
  show_animations: false
  refresh_interval: 1
```

## Configuration Management

### Import/Export Configuration

```python
from ghostpass.config import ConfigManager

# Export configuration
config_manager = ConfigManager()
config_manager.export_config("backup_config.yaml")

# Import configuration
config_manager.import_config("backup_config.yaml")
```

### Reset to Defaults

```python
from ghostpass.config import ConfigManager

config_manager = ConfigManager()
config_manager.reset_to_defaults()
```

## Troubleshooting

### Common Issues

1. **Configuration not found**: Create the config directory
2. **Invalid configuration**: Check YAML syntax
3. **Permission denied**: Check file permissions
4. **Port conflicts**: Change TOR ports

### Debug Configuration

```bash
# Enable debug mode
export GHOSTPASS_DEBUG=true

# Run with debug logging
python -m ghostpass --verbose
``` 