import platform
import subprocess
from rich.console import Console


class ClipboardManager:
    """Manages clipboard operations across platforms"""
    
    def __init__(self):
        self.console = Console()
        self.system = platform.system()
    
    def copy_to_clipboard(self, text: str) -> bool:
        """Copy text to clipboard"""
        try:
            if self.system == "Darwin":  # macOS
                subprocess.run(["pbcopy"], input=text.encode(), check=True)
            elif self.system == "Windows":
                subprocess.run(["clip"], input=text.encode(), shell=True, check=True)
            elif self.system == "Linux":
                # Try xclip first, then xsel
                try:
                    subprocess.run(["xclip", "-selection", "clipboard"], 
                                 input=text.encode(), check=True)
                except FileNotFoundError:
                    try:
                        subprocess.run(["xsel", "--clipboard", "--input"], 
                                     input=text.encode(), check=True)
                    except FileNotFoundError:
                        self.console.print("[red]No clipboard utility found. Please install xclip or xsel.[/red]")
                        return False
            else:
                self.console.print(f"[red]Clipboard not supported on {self.system}[/red]")
                return False
            
            return True
        except subprocess.CalledProcessError:
            self.console.print("[red]Failed to copy to clipboard[/red]")
            return False
        except Exception as e:
            self.console.print(f"[red]Clipboard error: {e}[/red]")
            return False