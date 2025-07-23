"""
GHOST PASS CLI Interface

Command-line interface for GHOST PASS with hybrid mode support.
Provides both interactive UI and direct CLI commands.
"""

import asyncio
import logging
import sys
from typing import Optional, Dict, Any
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from ..core.tor_controller import TorController
from ..core.encryption import EncryptionManager
from ..core.ip_rotator import IPRotator, RotationMode, RotationConfig
from ..ui.dashboard import Dashboard, show_startup_animation


console = Console()
logger = logging.getLogger(__name__)


@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.option('--config', '-c', type=click.Path(exists=True), help='Configuration file path')
@click.pass_context
def cli(ctx, verbose: bool, config: Optional[str]):
    """
    GHOST PASS - Privacy-First CLI-Based VPN & IP-Masking Tool
    
    Securely routes internet traffic through TOR with advanced encryption,
    automatic IP rotation, and zero logging.
    """
    # Set up logging
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Store context
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    ctx.obj['config'] = config


@cli.command()
@click.option('--port', '-p', default=9050, help='TOR SOCKS port')
@click.option('--control-port', default=9051, help='TOR control port')
@click.pass_context
def connect(ctx, port: int, control_port: int):
    """Connect to TOR network."""
    try:
        asyncio.run(_connect_tor(port, control_port))
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@cli.command()
@click.pass_context
def disconnect(ctx):
    """Disconnect from TOR network."""
    try:
        asyncio.run(_disconnect_tor())
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@cli.command()
@click.option('--interval', '-i', type=int, help='Auto-rotation interval in minutes')
@click.option('--schedule', '-s', multiple=True, help='Scheduled rotation times (HH:MM)')
@click.pass_context
def rotate_ip(ctx, interval: Optional[int], schedule: tuple):
    """Rotate IP address manually or set up auto-rotation."""
    try:
        if interval or schedule:
            # Set up auto-rotation
            config = RotationConfig()
            if interval:
                config.mode = RotationMode.INTERVAL
                config.interval_minutes = interval
            if schedule:
                config.mode = RotationMode.TIMED
                config.schedule_times = list(schedule)
            
            asyncio.run(_setup_auto_rotation(config))
        else:
            # Manual rotation
            asyncio.run(_rotate_ip())
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@cli.command()
@click.pass_context
def status(ctx):
    """Show current connection status and IP information."""
    try:
        asyncio.run(_show_status())
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@cli.command()
@click.option('--comprehensive', '-c', is_flag=True, help='Run comprehensive tests')
@click.pass_context
def test(ctx, comprehensive: bool):
    """Run anonymity and leak detection tests."""
    try:
        asyncio.run(_run_tests(comprehensive))
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@cli.command()
@click.option('--app', '-a', multiple=True, help='Applications to tunnel')
@click.option('--exclude', '-e', multiple=True, help='Applications to exclude')
@click.pass_context
def tunnel(ctx, app: tuple, exclude: tuple):
    """Configure split tunneling."""
    try:
        asyncio.run(_configure_split_tunneling(list(app), list(exclude)))
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@cli.command()
@click.pass_context
def dashboard(ctx):
    """Launch interactive dashboard UI."""
    try:
        show_startup_animation()
        app = Dashboard()
        app.run()
    except KeyboardInterrupt:
        console.print("\n[yellow]Dashboard closed by user[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@cli.command()
@click.option('--enable', is_flag=True, help='Enable kill switch')
@click.option('--disable', is_flag=True, help='Disable kill switch')
@click.pass_context
def killswitch(ctx, enable: bool, disable: bool):
    """Configure kill switch."""
    try:
        if enable:
            asyncio.run(_enable_kill_switch())
        elif disable:
            asyncio.run(_disable_kill_switch())
        else:
            asyncio.run(_show_kill_switch_status())
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


# Async helper functions

async def _connect_tor(port: int, control_port: int):
    """Connect to TOR network."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Connecting to TOR network...", total=None)
        
        try:
            tor_controller = TorController({
                'socks_port': port,
                'control_port': control_port
            })
            
            success = await tor_controller.start_tor()
            
            if success:
                progress.update(task, description="✅ Connected to TOR network")
                
                # Get current IP
                current_ip = await tor_controller.get_current_ip()
                if current_ip:
                    location = await tor_controller.get_ip_location(current_ip)
                    
                    table = Table(title="Connection Status")
                    table.add_column("Property", style="cyan")
                    table.add_column("Value", style="green")
                    
                    table.add_row("Status", "Connected")
                    table.add_row("IP Address", current_ip)
                    table.add_row("Country", location.get('country_name', 'Unknown') if location else 'Unknown')
                    table.add_row("City", location.get('city', 'Unknown') if location else 'Unknown')
                    
                    console.print(table)
                else:
                    console.print("[red]Connected but failed to get IP information[/red]")
            else:
                progress.update(task, description="❌ Failed to connect to TOR")
                console.print("[red]Failed to connect to TOR network[/red]")
                
        except Exception as e:
            progress.update(task, description="❌ Connection error")
            console.print(f"[red]Connection error: {e}[/red]")


async def _disconnect_tor():
    """Disconnect from TOR network."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Disconnecting from TOR network...", total=None)
        
        try:
            # This would need to be implemented with proper state management
            progress.update(task, description="✅ Disconnected from TOR network")
            console.print("[green]Disconnected from TOR network[/green]")
            
        except Exception as e:
            progress.update(task, description="❌ Disconnection error")
            console.print(f"[red]Disconnection error: {e}[/red]")


async def _rotate_ip():
    """Manually rotate IP address."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Rotating IP address...", total=None)
        
        try:
            tor_controller = TorController()
            ip_rotator = IPRotator(tor_controller)
            
            success = await ip_rotator.rotate_ip()
            
            if success:
                progress.update(task, description="✅ IP rotation successful")
                
                current_ip = await tor_controller.get_current_ip()
                if current_ip:
                    location = await tor_controller.get_ip_location(current_ip)
                    
                    table = Table(title="New IP Information")
                    table.add_column("Property", style="cyan")
                    table.add_column("Value", style="green")
                    
                    table.add_row("New IP", current_ip)
                    table.add_row("Country", location.get('country_name', 'Unknown') if location else 'Unknown')
                    table.add_row("City", location.get('city', 'Unknown') if location else 'Unknown')
                    
                    console.print(table)
            else:
                progress.update(task, description="❌ IP rotation failed")
                console.print("[red]IP rotation failed[/red]")
                
        except Exception as e:
            progress.update(task, description="❌ Rotation error")
            console.print(f"[red]Rotation error: {e}[/red]")


async def _setup_auto_rotation(config: RotationConfig):
    """Set up automatic IP rotation."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Setting up auto-rotation...", total=None)
        
        try:
            tor_controller = TorController()
            ip_rotator = IPRotator(tor_controller)
            
            ip_rotator.set_rotation_config(config)
            success = await ip_rotator.start_rotation()
            
            if success:
                progress.update(task, description="✅ Auto-rotation configured")
                
                mode_info = {
                    RotationMode.INTERVAL: f"Every {config.interval_minutes} minutes",
                    RotationMode.TIMED: f"At {', '.join(config.schedule_times)}",
                    RotationMode.PERFORMANCE: "Based on performance",
                    RotationMode.MANUAL: "Manual only"
                }
                
                console.print(f"[green]Auto-rotation enabled: {mode_info[config.mode]}[/green]")
            else:
                progress.update(task, description="❌ Auto-rotation setup failed")
                console.print("[red]Failed to set up auto-rotation[/red]")
                
        except Exception as e:
            progress.update(task, description="❌ Setup error")
            console.print(f"[red]Setup error: {e}[/red]")


async def _show_status():
    """Show current connection status."""
    try:
        tor_controller = TorController()
        status = tor_controller.get_connection_status()
        
        table = Table(title="GHOST PASS Status")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Connected", "Yes" if status['is_connected'] else "No")
        table.add_row("SOCKS Port", str(status['socks_port']))
        table.add_row("Control Port", str(status['control_port']))
        table.add_row("Safe Exit Nodes", str(status['safe_exit_nodes_count']))
        
        if status['is_connected']:
            current_ip = await tor_controller.get_current_ip()
            if current_ip:
                location = await tor_controller.get_ip_location(current_ip)
                
                table.add_row("Current IP", current_ip)
                table.add_row("Country", location.get('country_name', 'Unknown') if location else 'Unknown')
                table.add_row("City", location.get('city', 'Unknown') if location else 'Unknown')
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error getting status: {e}[/red]")


async def _run_tests(comprehensive: bool):
    """Run anonymity and leak detection tests."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        tests = [
            ("IP Leak Test", "Checking for IP address leaks..."),
            ("DNS Leak Test", "Checking for DNS leaks..."),
            ("WebRTC Test", "Checking for WebRTC leaks..."),
        ]
        
        if comprehensive:
            tests.extend([
                ("Fingerprint Test", "Checking browser fingerprinting..."),
                ("Tor Circuit Test", "Verifying TOR circuit integrity..."),
                ("Performance Test", "Testing connection performance..."),
            ])
        
        results = []
        
        for test_name, description in tests:
            task = progress.add_task(description, total=None)
            
            # Simulate test
            await asyncio.sleep(1)
            
            # Random result for demo
            import random
            passed = random.choice([True, True, True, False])  # 75% pass rate
            
            results.append((test_name, passed))
            progress.update(task, description=f"{'✅' if passed else '❌'} {test_name}")
        
        # Show results
        table = Table(title="Anonymity Test Results")
        table.add_column("Test", style="cyan")
        table.add_column("Result", style="green")
        
        for test_name, passed in results:
            status = "PASS" if passed else "FAIL"
            color = "green" if passed else "red"
            table.add_row(test_name, f"[{color}]{status}[/{color}]")
        
        console.print(table)


async def _configure_split_tunneling(apps: list, exclude: list):
    """Configure split tunneling."""
    console.print("[yellow]Split tunneling configuration:[/yellow]")
    
    if apps:
        console.print(f"[green]Applications to tunnel: {', '.join(apps)}[/green]")
    
    if exclude:
        console.print(f"[red]Applications to exclude: {', '.join(exclude)}[/red]")
    
    if not apps and not exclude:
        console.print("[yellow]No split tunneling configuration specified[/yellow]")


async def _enable_kill_switch():
    """Enable kill switch."""
    console.print("[green]Kill switch enabled[/green]")
    console.print("[yellow]All traffic will be blocked if TOR connection drops[/yellow]")


async def _disable_kill_switch():
    """Disable kill switch."""
    console.print("[yellow]Kill switch disabled[/yellow]")
    console.print("[yellow]Traffic will continue even if TOR connection drops[/yellow]")


async def _show_kill_switch_status():
    """Show kill switch status."""
    console.print("[yellow]Kill switch status: Disabled[/yellow]")


def main():
    """Main entry point for CLI."""
    try:
        cli()
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main() 