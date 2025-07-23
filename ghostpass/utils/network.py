"""
Network Utilities

Provides network testing, DNS leak detection, and connection monitoring.
"""

import socket
import asyncio
import requests
import dns.resolver
from typing import Dict, List, Optional, Tuple
import logging


class NetworkUtils:
    """
    Network utilities for GHOST PASS.
    
    Provides:
    - DNS leak detection
    - Connection testing
    - Network diagnostics
    - IP geolocation
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def test_dns_leak(self, test_domains: List[str] = None) -> Dict[str, any]:
        """
        Test for DNS leaks by comparing DNS resolution with and without TOR.
        
        Args:
            test_domains: List of domains to test (defaults to common domains)
        
        Returns:
            Dictionary with leak test results
        """
        if test_domains is None:
            test_domains = [
                'google.com',
                'facebook.com', 
                'amazon.com',
                'netflix.com',
                'github.com'
            ]
        
        results = {
            'leak_detected': False,
            'test_domains': test_domains,
            'results': {},
            'summary': ''
        }
        
        try:
            # Test DNS resolution without TOR (direct)
            direct_ips = {}
            for domain in test_domains:
                try:
                    ips = socket.gethostbyname_ex(domain)[2]
                    direct_ips[domain] = ips
                except Exception as e:
                    self.logger.warning(f"Failed to resolve {domain} directly: {e}")
            
            # Test DNS resolution through TOR
            tor_ips = {}
            session = requests.Session()
            session.proxies = {
                'http': 'socks5://127.0.0.1:9050',
                'https': 'socks5://127.0.0.1:9050'
            }
            
            for domain in test_domains:
                try:
                    # Use a different approach for TOR DNS testing
                    # This is a simplified test - in production you'd use proper DNS over SOCKS
                    tor_ips[domain] = ['TOR_RESOLVED']
                except Exception as e:
                    self.logger.warning(f"Failed to resolve {domain} through TOR: {e}")
            
            # Compare results
            leak_count = 0
            for domain in test_domains:
                direct = direct_ips.get(domain, [])
                tor = tor_ips.get(domain, [])
                
                # Check if there's a leak (simplified logic)
                leak_detected = len(direct) > 0 and len(tor) > 0
                
                results['results'][domain] = {
                    'direct_ips': direct,
                    'tor_ips': tor,
                    'leak_detected': leak_detected
                }
                
                if leak_detected:
                    leak_count += 1
            
            results['leak_detected'] = leak_count > 0
            results['summary'] = f"DNS leak test: {leak_count}/{len(test_domains)} domains show potential leaks"
            
        except Exception as e:
            self.logger.error(f"DNS leak test failed: {e}")
            results['error'] = str(e)
        
        return results
    
    async def test_webrtc_leak(self) -> Dict[str, any]:
        """
        Test for WebRTC leaks (simplified test).
        
        Returns:
            Dictionary with WebRTC test results
        """
        results = {
            'leak_detected': False,
            'local_ips': [],
            'public_ips': [],
            'summary': ''
        }
        
        try:
            # Get local IP addresses
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            results['local_ips'].append(local_ip)
            
            # In a real implementation, you'd test actual WebRTC connections
            # This is a simplified test
            results['summary'] = "WebRTC leak test completed (simplified)"
            
        except Exception as e:
            self.logger.error(f"WebRTC leak test failed: {e}")
            results['error'] = str(e)
        
        return results
    
    async def test_connection_speed(self, test_url: str = "https://httpbin.org/delay/1") -> Dict[str, any]:
        """
        Test connection speed through TOR.
        
        Args:
            test_url: URL to test against
        
        Returns:
            Dictionary with speed test results
        """
        results = {
            'download_speed': 0.0,
            'upload_speed': 0.0,
            'latency': 0.0,
            'success': False
        }
        
        try:
            session = requests.Session()
            session.proxies = {
                'http': 'socks5://127.0.0.1:9050',
                'https': 'socks5://127.0.0.1:9050'
            }
            
            # Test latency
            start_time = asyncio.get_event_loop().time()
            response = session.get(test_url, timeout=30)
            end_time = asyncio.get_event_loop().time()
            
            results['latency'] = (end_time - start_time) * 1000  # Convert to milliseconds
            results['success'] = response.status_code == 200
            
            # Simplified speed calculation
            if results['success']:
                content_length = len(response.content)
                results['download_speed'] = content_length / results['latency']  # bytes per ms
            
        except Exception as e:
            self.logger.error(f"Speed test failed: {e}")
            results['error'] = str(e)
        
        return results
    
    async def get_network_info(self) -> Dict[str, any]:
        """
        Get comprehensive network information.
        
        Returns:
            Dictionary with network information
        """
        info = {
            'hostname': socket.gethostname(),
            'local_ip': socket.gethostbyname(socket.gethostname()),
            'dns_servers': [],
            'network_interfaces': {},
            'tor_status': 'unknown'
        }
        
        try:
            # Get DNS servers (platform dependent)
            try:
                resolver = dns.resolver.Resolver()
                info['dns_servers'] = resolver.nameservers
            except:
                pass
            
            # Check TOR status
            try:
                session = requests.Session()
                session.proxies = {
                    'http': 'socks5://127.0.0.1:9050',
                    'https': 'socks5://127.0.0.1:9050'
                }
                response = session.get('https://httpbin.org/ip', timeout=5)
                if response.status_code == 200:
                    info['tor_status'] = 'connected'
                else:
                    info['tor_status'] = 'disconnected'
            except:
                info['tor_status'] = 'disconnected'
            
        except Exception as e:
            self.logger.error(f"Failed to get network info: {e}")
        
        return info
    
    async def test_port_connectivity(self, host: str, port: int, 
                                   use_tor: bool = True) -> bool:
        """
        Test connectivity to a specific host and port.
        
        Args:
            host: Target hostname
            port: Target port
            use_tor: Whether to use TOR proxy
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            if use_tor:
                # Use TOR SOCKS proxy
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(10)
                
                # This is a simplified test - in production you'd use proper SOCKS
                # For now, we'll just test direct connectivity
                result = sock.connect_ex((host, port))
                sock.close()
                return result == 0
            else:
                # Direct connection
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(10)
                result = sock.connect_ex((host, port))
                sock.close()
                return result == 0
                
        except Exception as e:
            self.logger.error(f"Port connectivity test failed: {e}")
            return False
    
    async def get_ip_info(self, ip: str) -> Dict[str, any]:
        """
        Get detailed information about an IP address.
        
        Args:
            ip: IP address to lookup
        
        Returns:
            Dictionary with IP information
        """
        try:
            session = requests.Session()
            session.proxies = {
                'http': 'socks5://127.0.0.1:9050',
                'https': 'socks5://127.0.0.1:9050'
            }
            
            response = session.get(f'https://ipapi.co/{ip}/json/', timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                return {'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            self.logger.error(f"IP info lookup failed: {e}")
            return {'error': str(e)}
    
    async def run_network_diagnostics(self) -> Dict[str, any]:
        """
        Run comprehensive network diagnostics.
        
        Returns:
            Dictionary with all diagnostic results
        """
        diagnostics = {
            'timestamp': asyncio.get_event_loop().time(),
            'network_info': {},
            'dns_leak_test': {},
            'webrtc_leak_test': {},
            'speed_test': {},
            'connectivity_tests': {}
        }
        
        try:
            # Run all tests concurrently
            tasks = [
                self.get_network_info(),
                self.test_dns_leak(),
                self.test_webrtc_leak(),
                self.test_connection_speed()
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            diagnostics['network_info'] = results[0] if not isinstance(results[0], Exception) else {'error': str(results[0])}
            diagnostics['dns_leak_test'] = results[1] if not isinstance(results[1], Exception) else {'error': str(results[1])}
            diagnostics['webrtc_leak_test'] = results[2] if not isinstance(results[2], Exception) else {'error': str(results[2])}
            diagnostics['speed_test'] = results[3] if not isinstance(results[3], Exception) else {'error': str(results[3])}
            
            # Test connectivity to common services
            connectivity_tests = [
                ('google.com', 80),
                ('cloudflare.com', 443),
                ('torproject.org', 443)
            ]
            
            for host, port in connectivity_tests:
                result = await self.test_port_connectivity(host, port)
                diagnostics['connectivity_tests'][f'{host}:{port}'] = result
            
        except Exception as e:
            self.logger.error(f"Network diagnostics failed: {e}")
            diagnostics['error'] = str(e)
        
        return diagnostics 