#!/usr/bin/env python3
"""
CLI tool for prompt enhancement using various AI providers
"""
import asyncio
import sys
from pathlib import Path
import click

from src.cli import PromptEnhancerCLI
from src.version import UpdateChecker, __version__
from src.config import ConfigManager


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """PMPT CLI - AI-powered prompt enhancement tool"""
    if ctx.invoked_subcommand is None:
        # Default behavior - run the interactive CLI
        try:
            app = PromptEnhancerCLI()
            asyncio.run(app.run())
        except KeyboardInterrupt:
            click.echo("\nGoodbye!")
        except Exception as e:
            click.echo(f"Error: {e}", err=True)


@cli.command()
def version():
    """Show version information"""
    click.echo(f"PMPT CLI version {__version__}")


@cli.command()
def update():
    """Check for updates and install if available"""
    import subprocess
    
    async def check_and_update():
        checker = UpdateChecker()
        update_info = await checker.check_for_updates()
        
        if update_info:
            click.echo(f"🎉 New version available: {update_info['latest_version']} (current: {update_info['current_version']})")
            if update_info['release_notes']:
                click.echo(f"\n📝 Release Notes:\n{update_info['release_notes']}")
            
            # Ask user if they want to update
            if click.confirm("\n🔄 Do you want to update now?", default=True):
                click.echo("📥 Downloading and installing update...")
                try:
                    import platform
                    system = platform.system().lower()
                    
                    if system == "windows":
                        # Use PowerShell script for Windows
                        install_url = "https://raw.githubusercontent.com/hawier-dev/pmpt-cli/main/install.ps1"
                        result = subprocess.run([
                            "powershell", "-Command",
                            f"Invoke-WebRequest -UseBasicParsing -Uri '{install_url}' | Invoke-Expression -ArgumentList '-Force'"
                        ], check=True, capture_output=True, text=True)
                        click.echo("✅ Update completed successfully!")
                        click.echo("🎉 Update is ready to use immediately!")
                    else:
                        # Use Bash script for Linux/macOS
                        install_url = "https://raw.githubusercontent.com/hawier-dev/pmpt-cli/main/install.sh"
                        result = subprocess.run([
                            "bash", "-c", f"curl -fsSL {install_url} | bash"
                        ], check=True, capture_output=True, text=True)
                        click.echo("✅ Update completed successfully!")
                        click.echo("🎉 Update is ready to use immediately!")
                        
                except subprocess.CalledProcessError as e:
                    click.echo(f"❌ Update failed: {e}", err=True)
                    click.echo(f"📥 You can manually download from: {update_info['release_url']}")
                except Exception as e:
                    click.echo(f"❌ Update error: {e}", err=True)
                    click.echo(f"📥 You can manually download from: {update_info['release_url']}")
            else:
                click.echo(f"📥 You can manually update later from: {update_info['release_url']}")
        else:
            click.echo(f"✅ You're running the latest version ({__version__})")
    
    try:
        asyncio.run(check_and_update())
    except Exception as e:
        click.echo(f"❌ Failed to check for updates: {e}", err=True)


@cli.command()
def config():
    """View or reconfigure settings"""
    import questionary
    
    choice = questionary.select(
        "Configuration options:",
        choices=[
            "View current configuration",
            "Reconfigure settings",
            "Back"
        ]
    ).ask()
    
    if choice == "View current configuration":
        config_manager = ConfigManager()
        config = config_manager.load_config()
        
        click.echo("\n📋 Current Configuration:")
        click.echo(f"• Provider: {config.provider or 'Custom'}")
        click.echo(f"• Base URL: {config.get_base_url()}")
        click.echo(f"• Model: {config.get_model()}")
        click.echo(f"• Current Style: {config.current_style}")
        click.echo(f"• API Key: {'Set' if config.get_api_key() else 'Not set'}")
        
    elif choice == "Reconfigure settings":
        try:
            app = PromptEnhancerCLI()
            asyncio.run(app._configure_provider())
            click.echo("✅ Configuration updated!")
        except Exception as e:
            click.echo(f"❌ Configuration failed: {e}", err=True)


def main():
    """Main entry point"""
    cli()


if __name__ == "__main__":
    main()