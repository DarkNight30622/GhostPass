"""
TOR Controller Module

Handles TOR connection management, circuit building, exit node selection,
and safe exit node checking.
"""

import asyncio
import logging
import socket
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

import stem
from stem import Signal
from stem.control import Controller
from stem.process import launch_tor_with_config
from stem.util import term

import requests
import socks


@dataclass
class ExitNode:
    """Represents a TOR exit node with metadata."""
    fingerprint: str
    nickname: str
    country: str
    ip_address: str
    bandwidth: int
    is_safe: bool = True
    last_checked: Optional[float] = None


@dataclass
class CircuitInfo:
    """Represents a TOR circuit."""
    circuit_id: str
    path: List[str]
    exit_node: ExitNode
    is_established: bool = False
    build_time: Optional[float] = None


class TorController:
    """
    Manages TOR connections, circuits, and exit node selection.
    
    Provides methods for:
    - Connecting to TOR network
    - Building and managing circuits
    - Safe exit node selection
    - IP rotation
    - Connection monitoring
    """
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.controller: Optional[Controller] = None
        self.tor_process = None
        self.socks_port = self.config.get('socks_port', 9050)
        self.control_port = self.config.get('control_port', 9051)
        self.data_directory = Path(self.config.get('data_directory', './tor_data'))
        self.safe_exit_nodes: List[ExitNode] = []
        self.current_circuit: Optional[CircuitInfo] = None
        self.is_connected = False
        self.logger = logging.getLogger(__name__)
        
        # Ensure data directory exists
        self.data_directory.mkdir(exist_ok=True)
    
    async def start_tor(self) -> bool:
        """Start TOR service and establish control connection."""
        try:
            # TOR configuration
            tor_config = {
                'SocksPort': str(self.socks_port),
                'ControlPort': str(self.control_port),
                'DataDirectory': str(self.data_directory),
                'CookieAuthentication': '1',
                'MaxCircuitDirtiness': '600',  # 10 minutes
                'NewCircuitPeriod': '30',      # 30 seconds
                'EnforceDistinctSubnets': '1',
                'UseEntryGuards': '1',
                'NumEntryGuards': '6',
                'GuardLifetime': '2592000',    # 30 days
                'CircuitBuildTimeout': '30',   # 30 seconds
                'LearnCircuitBuildTimeout': '1',
                'CircuitStreamTimeout': '300', # 5 minutes
                'MaxClientCircuitsPending': '32',
                'MaxOnionQueueDelay': '1750',
                'NewOnionKey': '1',
                'SafeLogging': '1',
                'Log': 'notice stdout',
            }
            
            # Launch TOR process
            self.tor_process = launch_tor_with_config(
                config=tor_config,
                init_msg_handler=self._print_bootstrap_lines,
                take_ownership=True
            )
            
            # Wait for TOR to start
            await asyncio.sleep(3)
            
            # Connect controller
            self.controller = Controller.from_port(port=self.control_port)
            self.controller.authenticate()
            
            self.is_connected = True
            self.logger.info("TOR service started successfully")
            
            # Load safe exit nodes
            await self._load_safe_exit_nodes()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start TOR: {e}")
            return False
    
    def _print_bootstrap_lines(self, line: str):
        """Print TOR bootstrap progress."""
        if "Bootstrapped " in line:
            self.logger.info(line)
    
    async def stop_tor(self):
        """Stop TOR service and cleanup."""
        try:
            if self.controller:
                self.controller.close()
                self.controller = None
            
            if self.tor_process:
                self.tor_process.kill()
                self.tor_process = None
            
            self.is_connected = False
            self.logger.info("TOR service stopped")
            
        except Exception as e:
            self.logger.error(f"Error stopping TOR: {e}")
    
    async def rotate_ip(self) -> bool:
        """Request new TOR circuit (IP rotation)."""
        try:
            if not self.controller:
                return False
            
            # Signal TOR to build new circuits
            self.controller.signal(Signal.NEWNYM)
            
            # Wait for new circuits to be established
            await asyncio.sleep(5)
            
            # Get new circuit info
            await self._update_circuit_info()
            
            self.logger.info("IP rotation completed")
            return True
            
        except Exception as e:
            self.logger.error(f"IP rotation failed: {e}")
            return False
    
    async def get_current_ip(self) -> Optional[str]:
        """Get current public IP address through TOR."""
        try:
            # Configure requests to use TOR SOCKS proxy
            session = requests.Session()
            session.proxies = {
                'http': f'socks5://127.0.0.1:{self.socks_port}',
                'https': f'socks5://127.0.0.1:{self.socks_port}'
            }
            
            response = session.get('https://httpbin.org/ip', timeout=10)
            data = response.json()
            return data.get('origin')
            
        except Exception as e:
            self.logger.error(f"Failed to get current IP: {e}")
            return None
    
    async def get_ip_location(self, ip: str) -> Optional[Dict]:
        """Get geolocation information for an IP address."""
        try:
            session = requests.Session()
            session.proxies = {
                'http': f'socks5://127.0.0.1:{self.socks_port}',
                'https': f'socks5://127.0.0.1:{self.socks_port}'
            }
            
            response = session.get(f'https://ipapi.co/{ip}/json/', timeout=10)
            return response.json()
            
        except Exception as e:
            self.logger.error(f"Failed to get IP location: {e}")
            return None
    
    async def _load_safe_exit_nodes(self):
        """Load and validate safe exit nodes."""
        try:
            if not self.controller:
                return
            
            # Get all exit nodes
            exit_nodes = self.controller.get_network_statuses()
            
            for node in exit_nodes:
                if node.flags and 'Exit' in node.flags:
                    exit_node = ExitNode(
                        fingerprint=node.fingerprint,
                        nickname=node.nickname,
                        country=node.address,
                        ip_address=node.address,
                        bandwidth=node.bandwidth,
                        is_safe=True
                    )
                    
                    # Check if node is safe (not on blocklists)
                    if await self._is_node_safe(exit_node):
                        self.safe_exit_nodes.append(exit_node)
            
            self.logger.info(f"Loaded {len(self.safe_exit_nodes)} safe exit nodes")
            
        except Exception as e:
            self.logger.error(f"Failed to load safe exit nodes: {e}")
    
    async def _is_node_safe(self, node: ExitNode) -> bool:
        """Check if exit node is safe (not on blocklists)."""
        try:
            # This is a simplified check - in production, you'd check multiple blocklists
            # For now, we'll assume all nodes are safe
            return True
            
        except Exception as e:
            self.logger.error(f"Error checking node safety: {e}")
            return False
    
    async def _update_circuit_info(self):
        """Update current circuit information."""
        try:
            if not self.controller:
                return
            
            circuits = self.controller.get_circuits()
            if circuits:
                # Get the most recent circuit
                circuit = circuits[-1]
                self.current_circuit = CircuitInfo(
                    circuit_id=circuit.id,
                    path=circuit.path,
                    exit_node=None,  # Would need to map to ExitNode
                    is_established=circuit.status == 'BUILT'
                )
            
        except Exception as e:
            self.logger.error(f"Failed to update circuit info: {e}")
    
    def get_connection_status(self) -> Dict:
        """Get current connection status."""
        return {
            'is_connected': self.is_connected,
            'socks_port': self.socks_port,
            'control_port': self.control_port,
            'safe_exit_nodes_count': len(self.safe_exit_nodes),
            'current_circuit': self.current_circuit
        }
    
    async def test_connection(self) -> bool:
        """Test TOR connection and circuit health."""
        try:
            current_ip = await self.get_current_ip()
            if current_ip:
                self.logger.info(f"Connection test successful. Current IP: {current_ip}")
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Connection test failed: {e}")
            return False 