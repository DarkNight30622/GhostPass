"""
System Utilities

Provides system-related utilities for GHOST PASS.
"""

import os
import platform
import psutil
import logging
from typing import Dict, List, Optional
from pathlib import Path


class SystemUtils:
    """
    System utilities for GHOST PASS.
    
    Provides:
    - System information
    - Process management
    - File system operations
    - Platform detection
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def get_system_info(self) -> Dict[str, str]:
        """
        Get comprehensive system information.
        
        Returns:
            Dictionary with system information
        """
        return {
            'platform': platform.system(),
            'platform_version': platform.version(),
            'architecture': platform.machine(),
            'processor': platform.processor(),
            'python_version': platform.python_version(),
            'hostname': platform.node(),
            'username': os.getenv('USERNAME') or os.getenv('USER', 'Unknown')
        }
    
    def get_memory_info(self) -> Dict[str, int]:
        """
        Get memory information.
        
        Returns:
            Dictionary with memory information in bytes
        """
        memory = psutil.virtual_memory()
        return {
            'total': memory.total,
            'available': memory.available,
            'used': memory.used,
            'free': memory.free,
            'percent': memory.percent
        }
    
    def get_disk_info(self, path: str = ".") -> Dict[str, int]:
        """
        Get disk information for a path.
        
        Args:
            path: Path to check disk usage for
        
        Returns:
            Dictionary with disk information in bytes
        """
        disk = psutil.disk_usage(path)
        return {
            'total': disk.total,
            'used': disk.used,
            'free': disk.free,
            'percent': disk.percent
        }
    
    def get_process_info(self, pid: Optional[int] = None) -> Dict[str, any]:
        """
        Get process information.
        
        Args:
            pid: Process ID (current process if None)
        
        Returns:
            Dictionary with process information
        """
        if pid is None:
            process = psutil.Process()
        else:
            process = psutil.Process(pid)
        
        try:
            return {
                'pid': process.pid,
                'name': process.name(),
                'status': process.status(),
                'cpu_percent': process.cpu_percent(),
                'memory_percent': process.memory_percent(),
                'memory_info': process.memory_info()._asdict(),
                'create_time': process.create_time(),
                'num_threads': process.num_threads(),
                'connections': len(process.connections()),
                'open_files': len(process.open_files()),
                'num_fds': process.num_fds() if hasattr(process, 'num_fds') else 0
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return {'error': 'Process not accessible'}
    
    def find_process_by_name(self, name: str) -> List[Dict[str, any]]:
        """
        Find processes by name.
        
        Args:
            name: Process name to search for
        
        Returns:
            List of process information dictionaries
        """
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'status']):
            try:
                if name.lower() in proc.info['name'].lower():
                    processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return processes
    
    def kill_process(self, pid: int) -> bool:
        """
        Kill a process by PID.
        
        Args:
            pid: Process ID to kill
        
        Returns:
            True if successful, False otherwise
        """
        try:
            process = psutil.Process(pid)
            process.terminate()
            process.wait(timeout=5)
            return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
            try:
                process.kill()
                return True
            except:
                return False
    
    def get_network_connections(self) -> List[Dict[str, any]]:
        """
        Get network connections.
        
        Returns:
            List of network connection dictionaries
        """
        connections = []
        for conn in psutil.net_connections():
            try:
                connections.append({
                    'fd': conn.fd,
                    'family': conn.family,
                    'type': conn.type,
                    'laddr': conn.laddr._asdict() if conn.laddr else None,
                    'raddr': conn.raddr._asdict() if conn.raddr else None,
                    'status': conn.status,
                    'pid': conn.pid
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return connections
    
    def get_network_interfaces(self) -> Dict[str, Dict[str, any]]:
        """
        Get network interface information.
        
        Returns:
            Dictionary of network interfaces
        """
        interfaces = {}
        for name, addrs in psutil.net_if_addrs().items():
            interfaces[name] = {
                'addresses': [addr._asdict() for addr in addrs],
                'stats': psutil.net_if_stats()[name]._asdict() if name in psutil.net_if_stats() else None
            }
        return interfaces
    
    def is_port_in_use(self, port: int) -> bool:
        """
        Check if a port is in use.
        
        Args:
            port: Port number to check
        
        Returns:
            True if port is in use, False otherwise
        """
        for conn in psutil.net_connections():
            if conn.laddr and conn.laddr.port == port:
                return True
        return False
    
    def get_free_port(self, start_port: int = 8000, max_attempts: int = 100) -> Optional[int]:
        """
        Find a free port.
        
        Args:
            start_port: Starting port number
            max_attempts: Maximum number of attempts
        
        Returns:
            Free port number or None if not found
        """
        for port in range(start_port, start_port + max_attempts):
            if not self.is_port_in_use(port):
                return port
        return None
    
    def create_directory(self, path: str) -> bool:
        """
        Create directory if it doesn't exist.
        
        Args:
            path: Directory path to create
        
        Returns:
            True if successful, False otherwise
        """
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            self.logger.error(f"Failed to create directory {path}: {e}")
            return False
    
    def get_file_size(self, file_path: str) -> Optional[int]:
        """
        Get file size in bytes.
        
        Args:
            file_path: Path to file
        
        Returns:
            File size in bytes or None if error
        """
        try:
            return os.path.getsize(file_path)
        except OSError:
            return None
    
    def is_windows(self) -> bool:
        """Check if running on Windows."""
        return platform.system().lower() == 'windows'
    
    def is_linux(self) -> bool:
        """Check if running on Linux."""
        return platform.system().lower() == 'linux'
    
    def is_macos(self) -> bool:
        """Check if running on macOS."""
        return platform.system().lower() == 'darwin'
    
    def get_temp_directory(self) -> str:
        """Get system temporary directory."""
        return os.path.join(os.path.expanduser('~'), '.ghostpass', 'temp')
    
    def cleanup_temp_files(self, max_age_hours: int = 24) -> int:
        """
        Clean up temporary files older than specified age.
        
        Args:
            max_age_hours: Maximum age in hours
        
        Returns:
            Number of files cleaned up
        """
        import time
        temp_dir = self.get_temp_directory()
        if not os.path.exists(temp_dir):
            return 0
        
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        cleaned_count = 0
        
        for filename in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, filename)
            try:
                if os.path.isfile(file_path):
                    file_age = current_time - os.path.getmtime(file_path)
                    if file_age > max_age_seconds:
                        os.remove(file_path)
                        cleaned_count += 1
            except OSError:
                continue
        
        return cleaned_count 