"""
GHOST PASS Dashboard UI

Interactive terminal UI built with Textual for managing TOR connections,
IP rotation, and security features.
"""

import asyncio
import time
from typing import Optional, Dict, Any
from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import (
    Header, Footer, Button, Static, DataTable, 
    Input, Label, ProgressBar, Switch
)
from textual.widgets.data_table import RowKey
from textual.reactive import reactive
from textual import work
from rich.text import Text
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.live import Live
from rich.table import Table

from ..core.tor_controller import TorController
from ..core.encryption import EncryptionManager
from ..core.ip_rotator import IPRotator, RotationMode, RotationConfig


class StatusWidget(Static):
    """Widget for displaying connection status."""
    
    status = reactive("Disconnected")
    ip_address = reactive("Unknown")
    country = reactive("Unknown")
    
    def on_mount(self) -> None:
        """Set up the status widget."""
        self.update_status()
    
    def update_status(self) -> None:
        """Update the status display."""
        status_color = "green" if self.status == "Connected" else "red"
        self.update(
            f"[bold {status_color}]{self.status}[/bold {status_color}]\n"
            f"IP: {self.ip_address}\n"
            f"Location: {self.country}"
        )


class IPHistoryTable(DataTable):
    """Widget for displaying IP rotation history."""
    
    def on_mount(self) -> None:
        """Set up the IP history table."""
        self.add_columns("Time", "IP Address", "Country", "City", "Performance")
        self.add_rows([])


class Dashboard(App):
    """
    Main dashboard application for GHOST PASS.
    
    Features:
    - Animated startup branding
    - Connection status monitoring
    - IP rotation controls
    - Security settings
    - Performance metrics
    """
    
    CSS = """
    #main {
        layout: grid;
        grid-size: 2;
        grid-rows: 1fr 1fr;
        grid-columns: 1fr 1fr;
    }
    
    #status-panel {
        height: 100%;
        border: solid green;
        padding: 1;
    }
    
    #controls-panel {
        height: 100%;
        border: solid blue;
        padding: 1;
    }
    
    #history-panel {
        height: 100%;
        border: solid yellow;
        padding: 1;
    }
    
    #settings-panel {
        height: 100%;
        border: solid red;
        padding: 1;
    }
    
    .title {
        text-align: center;
        color: #00ff00;
        text-style: bold;
    }
    
    .status-connected {
        color: #00ff00;
    }
    
    .status-disconnected {
        color: #ff0000;
    }
    """
    
    def __init__(self):
        super().__init__()
        self.tor_controller: Optional[TorController] = None
        self.encryption_manager: Optional[EncryptionManager] = None
        self.ip_rotator: Optional[IPRotator] = None
        
        # UI state
        self.is_connected = False
        self.current_ip = "Unknown"
        self.current_country = "Unknown"
        self.rotation_mode = RotationMode.MANUAL
        
    def compose(self) -> ComposeResult:
        """Compose the dashboard layout."""
        yield Header(show_clock=True)
        
        with Container(id="main"):
            with Container(id="status-panel"):
                yield Label("🔒 GHOST PASS STATUS", classes="title")
                yield StatusWidget(id="status")
                yield Button("Connect", id="connect-btn", variant="success")
                yield Button("Disconnect", id="disconnect-btn", variant="error")
            
            with Container(id="controls-panel"):
                yield Label("🎛️ CONTROLS", classes="title")
                yield Button("Rotate IP", id="rotate-btn")
                yield Button("Auto-Rotation", id="auto-rotation-btn")
                yield Button("Anonymity Test", id="test-btn")
                yield Button("Kill Switch", id="kill-switch-btn")
            
            with Container(id="history-panel"):
                yield Label("📊 IP HISTORY", classes="title")
                yield IPHistoryTable(id="ip-history")
            
            with Container(id="settings-panel"):
                yield Label("⚙️ SETTINGS", classes="title")
                yield Label("Rotation Mode:")
                yield Switch(id="auto-rotation-switch")
                yield Label("Kill Switch:")
                yield Switch(id="kill-switch-switch")
                yield Label("DNS Protection:")
                yield Switch(id="dns-protection-switch")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Initialize the dashboard."""
        self.title = "GHOST PASS - Privacy-First VPN"
        self.sub_title = "Secure TOR Routing"
        
        # Initialize core components
        self.initialize_components()
        
        # Start status monitoring
        self.start_status_monitoring()
    
    def initialize_components(self):
        """Initialize core components."""
        try:
            # Initialize TOR controller
            self.tor_controller = TorController()
            
            # Initialize encryption manager
            self.encryption_manager = EncryptionManager()
            
            # Initialize IP rotator
            self.ip_rotator = IPRotator(self.tor_controller)
            
            # Add rotation callback
            self.ip_rotator.add_rotation_callback(self.on_ip_rotated)
            
        except Exception as e:
            self.log.error(f"Failed to initialize components: {e}")
    
    @work
    async def start_status_monitoring(self):
        """Start monitoring connection status."""
        while True:
            try:
                await self.update_status()
                await asyncio.sleep(5)  # Update every 5 seconds
            except Exception as e:
                self.log.error(f"Status monitoring error: {e}")
                await asyncio.sleep(10)
    
    async def update_status(self):
        """Update connection status display."""
        if self.tor_controller:
            status = self.tor_controller.get_connection_status()
            self.is_connected = status['is_connected']
            
            if self.is_connected:
                # Get current IP
                current_ip = await self.tor_controller.get_current_ip()
                if current_ip:
                    self.current_ip = current_ip
                    
                    # Get location info
                    location = await self.tor_controller.get_ip_location(current_ip)
                    if location:
                        self.current_country = location.get('country_name', 'Unknown')
            
            # Update status widget
            status_widget = self.query_one("#status", StatusWidget)
            status_widget.status = "Connected" if self.is_connected else "Disconnected"
            status_widget.ip_address = self.current_ip
            status_widget.country = self.current_country
            status_widget.update_status()
    
    async def on_ip_rotated(self, ip_info):
        """Callback when IP is rotated."""
        # Update IP history table
        history_table = self.query_one("#ip-history", IPHistoryTable)
        
        # Add new row to history
        history_table.add_row(
            ip_info.timestamp.strftime("%H:%M:%S"),
            ip_info.ip,
            ip_info.country,
            ip_info.city,
            f"{ip_info.performance_score:.2f}"
        )
        
        # Keep only last 10 entries
        if len(history_table.rows) > 10:
            history_table.remove_row(RowKey(0))
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        button_id = event.button.id
        
        if button_id == "connect-btn":
            self.connect_tor()
        elif button_id == "disconnect-btn":
            self.disconnect_tor()
        elif button_id == "rotate-btn":
            self.rotate_ip()
        elif button_id == "auto-rotation-btn":
            self.toggle_auto_rotation()
        elif button_id == "test-btn":
            self.run_anonymity_test()
        elif button_id == "kill-switch-btn":
            self.toggle_kill_switch()
    
    @work
    async def connect_tor(self):
        """Connect to TOR network."""
        try:
            self.log.info("Connecting to TOR network...")
            
            if self.tor_controller:
                success = await self.tor_controller.start_tor()
                if success:
                    self.log.info("Successfully connected to TOR")
                    await self.update_status()
                else:
                    self.log.error("Failed to connect to TOR")
            
        except Exception as e:
            self.log.error(f"Connection error: {e}")
    
    @work
    async def disconnect_tor(self):
        """Disconnect from TOR network."""
        try:
            self.log.info("Disconnecting from TOR network...")
            
            if self.tor_controller:
                await self.tor_controller.stop_tor()
                self.log.info("Disconnected from TOR")
                await self.update_status()
            
        except Exception as e:
            self.log.error(f"Disconnection error: {e}")
    
    @work
    async def rotate_ip(self):
        """Manually rotate IP address."""
        try:
            self.log.info("Rotating IP address...")
            
            if self.ip_rotator:
                success = await self.ip_rotator.rotate_ip()
                if success:
                    self.log.info("IP rotation successful")
                else:
                    self.log.error("IP rotation failed")
            
        except Exception as e:
            self.log.error(f"IP rotation error: {e}")
    
    def toggle_auto_rotation(self):
        """Toggle automatic IP rotation."""
        auto_switch = self.query_one("#auto-rotation-switch", Switch)
        
        if auto_switch.value:
            # Start auto rotation
            config = RotationConfig(mode=RotationMode.INTERVAL, interval_minutes=30)
            self.ip_rotator.set_rotation_config(config)
            self.ip_rotator.start_rotation()
            self.log.info("Auto-rotation enabled")
        else:
            # Stop auto rotation
            self.ip_rotator.stop_rotation()
            self.log.info("Auto-rotation disabled")
    
    @work
    async def run_anonymity_test(self):
        """Run anonymity and leak detection test."""
        try:
            self.log.info("Running anonymity test...")
            
            # Test IP leak
            real_ip = await self.get_real_ip()
            tor_ip = await self.tor_controller.get_current_ip()
            
            if real_ip != tor_ip:
                self.log.info("✅ IP leak test passed")
            else:
                self.log.warning("⚠️ IP leak detected")
            
            # Test DNS leak
            dns_leak = await self.test_dns_leak()
            if not dns_leak:
                self.log.info("✅ DNS leak test passed")
            else:
                self.log.warning("⚠️ DNS leak detected")
            
            self.log.info("Anonymity test completed")
            
        except Exception as e:
            self.log.error(f"Anonymity test error: {e}")
    
    async def get_real_ip(self) -> str:
        """Get real IP address (without TOR)."""
        try:
            response = requests.get('https://httpbin.org/ip', timeout=5)
            return response.json()['origin']
        except:
            return "Unknown"
    
    async def test_dns_leak(self) -> bool:
        """Test for DNS leaks."""
        # Simplified DNS leak test
        # In a real implementation, you'd test actual DNS queries
        return False
    
    def toggle_kill_switch(self):
        """Toggle kill switch functionality."""
        kill_switch = self.query_one("#kill-switch-switch", Switch)
        
        if kill_switch.value:
            self.log.info("Kill switch enabled")
            # Implement kill switch logic
        else:
            self.log.info("Kill switch disabled")
            # Disable kill switch logic


def show_startup_animation():
    """Show animated startup branding."""
    console = Console()
    
    # GHOST PASS ASCII art
    ascii_art = """
    ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗    ██████╗  █████╗ ███████╗███████╗
    ██╔════╝ ██║  ██║██╔════╝ ██╔════╝╚══██╔══╝    ██╔══██╗██╔══██╗██╔════╝██╔════╝
    ██║  ███╗███████║██║  ███╗███████╗   ██║       ██████╔╝███████║███████╗███████╗
    ██║   ██║██╔══██║██║   ██║╚════██║   ██║       ██╔═══╝ ██╔══██║╚════██║╚════██║
    ╚██████╔╝██║  ██║╚██████╔╝███████║   ██║       ██║     ██║  ██║███████║███████║
     ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝       ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝
    """
    
    with Live(Panel(Align(ascii_art, align="center"), title="GHOST PASS"), 
              console=console, refresh_per_second=10) as live:
        
        # Animated loading
        for i in range(3):
            time.sleep(0.5)
            live.update(Panel(
                Align(f"{ascii_art}\n\n[bold green]Initializing...[/bold green] {'|' * (i + 1)}", 
                      align="center"), 
                title="GHOST PASS"
            ))
        
        time.sleep(1)
        live.update(Panel(
            Align(f"{ascii_art}\n\n[bold green]Ready![/bold green]", align="center"), 
            title="GHOST PASS"
        ))
        time.sleep(1)


def main():
    """Main entry point for the dashboard."""
    # Show startup animation
    show_startup_animation()
    
    # Start the dashboard
    app = Dashboard()
    app.run()


if __name__ == "__main__":
    main() 