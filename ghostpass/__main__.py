"""
GHOST PASS Main Entry Point

This module allows running GHOST PASS directly with:
    python -m ghostpass

It provides both CLI and interactive UI modes.
"""

import sys
import asyncio
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from ghostpass.cli.main import main as cli_main
from ghostpass.ui.dashboard import Dashboard, show_startup_animation


def main():
    """
    Main entry point for GHOST PASS.
    
    If command line arguments are provided, runs in CLI mode.
    Otherwise, launches the interactive dashboard.
    """
    
    # Check if CLI arguments are provided
    if len(sys.argv) > 1:
        # CLI mode
        cli_main()
    else:
        # Interactive UI mode
        try:
            show_startup_animation()
            app = Dashboard()
            app.run()
        except KeyboardInterrupt:
            print("\n[yellow]GHOST PASS closed by user[/yellow]")
        except Exception as e:
            print(f"[red]Error: {e}[/red]")
            sys.exit(1)


if __name__ == "__main__":
    main() 