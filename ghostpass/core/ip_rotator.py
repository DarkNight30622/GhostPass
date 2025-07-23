"""
IP Rotator Module

Handles automatic IP rotation with scheduling, geolocation tracking,
and performance optimization.
"""

import asyncio
import logging
import time
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

import requests


class RotationMode(Enum):
    """IP rotation modes."""
    MANUAL = "manual"
    TIMED = "timed"
    INTERVAL = "interval"
    PERFORMANCE = "performance"


@dataclass
class IPInfo:
    """Information about an IP address."""
    ip: str
    country: str
    city: str
    region: str
    isp: str
    latitude: float
    longitude: float
    timestamp: datetime = field(default_factory=datetime.now)
    performance_score: float = 0.0


@dataclass
class RotationConfig:
    """Configuration for IP rotation."""
    mode: RotationMode = RotationMode.MANUAL
    interval_minutes: int = 30
    schedule_times: List[str] = field(default_factory=list)  # HH:MM format
    performance_threshold: float = 0.5
    max_rotation_attempts: int = 3
    cooldown_seconds: int = 60


class IPRotator:
    """
    Manages IP rotation with various modes and performance tracking.
    
    Features:
    - Manual and automatic rotation
    - Scheduled rotation
    - Performance-based rotation
    - IP history tracking
    - Geolocation monitoring
    """
    
    def __init__(self, tor_controller, config: RotationConfig = None):
        self.tor_controller = tor_controller
        self.config = config or RotationConfig()
        self.logger = logging.getLogger(__name__)
        
        self.ip_history: List[IPInfo] = []
        self.current_ip_info: Optional[IPInfo] = None
        self.rotation_task: Optional[asyncio.Task] = None
        self.is_rotating = False
        self.last_rotation_time: Optional[datetime] = None
        
        # Performance tracking
        self.performance_history: Dict[str, List[float]] = {}
        self.rotation_callbacks: List[Callable] = []
    
    async def start_rotation(self) -> bool:
        """Start IP rotation based on configured mode."""
        try:
            if self.config.mode == RotationMode.MANUAL:
                return await self.rotate_ip()
            
            elif self.config.mode == RotationMode.TIMED:
                return await self._start_timed_rotation()
            
            elif self.config.mode == RotationMode.INTERVAL:
                return await self._start_interval_rotation()
            
            elif self.config.mode == RotationMode.PERFORMANCE:
                return await self._start_performance_rotation()
            
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to start rotation: {e}")
            return False
    
    async def rotate_ip(self) -> bool:
        """Manually rotate IP address."""
        try:
            if self.is_rotating:
                self.logger.warning("IP rotation already in progress")
                return False
            
            self.is_rotating = True
            self.logger.info("Starting IP rotation...")
            
            # Store current IP info before rotation
            if self.current_ip_info:
                self.ip_history.append(self.current_ip_info)
            
            # Perform rotation
            success = await self.tor_controller.rotate_ip()
            if not success:
                self.logger.error("IP rotation failed")
                return False
            
            # Wait for new circuit to establish
            await asyncio.sleep(5)
            
            # Get new IP information
            new_ip = await self.tor_controller.get_current_ip()
            if not new_ip:
                self.logger.error("Failed to get new IP after rotation")
                return False
            
            # Get geolocation information
            location_info = await self.tor_controller.get_ip_location(new_ip)
            if location_info:
                self.current_ip_info = IPInfo(
                    ip=new_ip,
                    country=location_info.get('country_name', 'Unknown'),
                    city=location_info.get('city', 'Unknown'),
                    region=location_info.get('region', 'Unknown'),
                    isp=location_info.get('org', 'Unknown'),
                    latitude=location_info.get('latitude', 0.0),
                    longitude=location_info.get('longitude', 0.0)
                )
            else:
                self.current_ip_info = IPInfo(ip=new_ip)
            
            self.last_rotation_time = datetime.now()
            
            # Notify callbacks
            for callback in self.rotation_callbacks:
                try:
                    await callback(self.current_ip_info)
                except Exception as e:
                    self.logger.error(f"Rotation callback error: {e}")
            
            self.logger.info(f"IP rotation successful. New IP: {new_ip} ({self.current_ip_info.country})")
            return True
            
        except Exception as e:
            self.logger.error(f"IP rotation error: {e}")
            return False
        finally:
            self.is_rotating = False
    
    async def _start_timed_rotation(self) -> bool:
        """Start rotation based on scheduled times."""
        if not self.config.schedule_times:
            self.logger.error("No schedule times configured for timed rotation")
            return False
        
        self.rotation_task = asyncio.create_task(self._timed_rotation_loop())
        self.logger.info("Timed rotation started")
        return True
    
    async def _timed_rotation_loop(self):
        """Loop for timed rotation."""
        while True:
            try:
                current_time = datetime.now().strftime("%H:%M")
                
                if current_time in self.config.schedule_times:
                    await self.rotate_ip()
                    # Wait until next day to avoid multiple rotations
                    await asyncio.sleep(3600)  # 1 hour
                else:
                    await asyncio.sleep(60)  # Check every minute
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Timed rotation loop error: {e}")
                await asyncio.sleep(60)
    
    async def _start_interval_rotation(self) -> bool:
        """Start rotation based on time intervals."""
        self.rotation_task = asyncio.create_task(self._interval_rotation_loop())
        self.logger.info(f"Interval rotation started (every {self.config.interval_minutes} minutes)")
        return True
    
    async def _interval_rotation_loop(self):
        """Loop for interval rotation."""
        while True:
            try:
                await asyncio.sleep(self.config.interval_minutes * 60)
                await self.rotate_ip()
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Interval rotation loop error: {e}")
                await asyncio.sleep(60)
    
    async def _start_performance_rotation(self) -> bool:
        """Start rotation based on performance monitoring."""
        self.rotation_task = asyncio.create_task(self._performance_rotation_loop())
        self.logger.info("Performance-based rotation started")
        return True
    
    async def _performance_rotation_loop(self):
        """Loop for performance-based rotation."""
        while True:
            try:
                await asyncio.sleep(300)  # Check every 5 minutes
                
                # Test current connection performance
                performance = await self._test_connection_performance()
                
                if performance < self.config.performance_threshold:
                    self.logger.info(f"Performance below threshold ({performance:.2f}), rotating IP")
                    await self.rotate_ip()
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Performance rotation loop error: {e}")
                await asyncio.sleep(60)
    
    async def _test_connection_performance(self) -> float:
        """Test current connection performance and return score (0-1)."""
        try:
            start_time = time.time()
            
            # Test connection speed
            session = requests.Session()
            session.proxies = {
                'http': f'socks5://127.0.0.1:{self.tor_controller.socks_port}',
                'https': f'socks5://127.0.0.1:{self.tor_controller.socks_port}'
            }
            
            response = session.get('https://httpbin.org/delay/1', timeout=10)
            response_time = time.time() - start_time
            
            # Calculate performance score (lower response time = higher score)
            performance_score = max(0, 1 - (response_time - 1) / 5)  # Normalize to 0-1
            
            # Store performance data
            if self.current_ip_info:
                if self.current_ip_info.ip not in self.performance_history:
                    self.performance_history[self.current_ip_info.ip] = []
                self.performance_history[self.current_ip_info.ip].append(performance_score)
                
                # Update current IP performance
                self.current_ip_info.performance_score = performance_score
            
            return performance_score
            
        except Exception as e:
            self.logger.error(f"Performance test failed: {e}")
            return 0.0
    
    def stop_rotation(self):
        """Stop automatic IP rotation."""
        if self.rotation_task:
            self.rotation_task.cancel()
            self.rotation_task = None
            self.logger.info("IP rotation stopped")
    
    def add_rotation_callback(self, callback: Callable):
        """Add callback function to be called after IP rotation."""
        self.rotation_callbacks.append(callback)
    
    def get_current_ip_info(self) -> Optional[IPInfo]:
        """Get current IP information."""
        return self.current_ip_info
    
    def get_ip_history(self, limit: int = 10) -> List[IPInfo]:
        """Get recent IP history."""
        return self.ip_history[-limit:] if self.ip_history else []
    
    def get_performance_stats(self) -> Dict[str, float]:
        """Get performance statistics for all IPs."""
        stats = {}
        for ip, scores in self.performance_history.items():
            if scores:
                stats[ip] = {
                    'average': sum(scores) / len(scores),
                    'min': min(scores),
                    'max': max(scores),
                    'count': len(scores)
                }
        return stats
    
    def set_rotation_config(self, config: RotationConfig):
        """Update rotation configuration."""
        self.config = config
        self.logger.info(f"Rotation config updated: {config.mode.value}")
    
    def get_rotation_status(self) -> Dict:
        """Get current rotation status."""
        return {
            'mode': self.config.mode.value,
            'is_rotating': self.is_rotating,
            'last_rotation': self.last_rotation_time.isoformat() if self.last_rotation_time else None,
            'current_ip': self.current_ip_info.ip if self.current_ip_info else None,
            'ip_history_count': len(self.ip_history),
            'performance_history_count': len(self.performance_history)
        } 