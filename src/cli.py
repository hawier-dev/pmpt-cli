from typing import Optional
from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.completion import WordCompleter
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Confirm, Prompt
import questionary

from .config import Config, ConfigManager
from .providers import APIClient
from .clipboard import ClipboardManager
from .language_detector import LanguageDetector


class PromptEnhancerCLI:
    """Main CLI application"""
    
    def __init__(self):
        self.console = Console()
        self.config_manager = ConfigManager()
        self.clipboard_manager = ClipboardManager()
        self.language_detector = LanguageDetector()
        self.config = self.config_manager.load_config()
        
        self.style = Style.from_dict({
            'title': '#00aa00 bold',
            'subtitle': '#888888',
            'prompt': '#0088ff bold',
            'enhanced': '#00ff88',
            'error': '#ff0088 bold',
        })
        
        # Enhancement styles
        self.enhancement_styles = {
            "gentle": {
                "name": "Gentle",
                "color": "#90EE90",
                "description": "Softly improves grammar and clarity while keeping original tone",
                "prompt": "Gently improve the user's prompt by fixing grammar, improving clarity, and making it more specific while maintaining the original intent and tone. Return ONLY the enhanced prompt."
            },
            "professional": {
                "name": "Professional", 
                "color": "#4169E1",
                "description": "Transforms prompts into formal, business-appropriate language",
                "prompt": "Transform the user's prompt into a clear, professional, and well-structured request suitable for business or formal contexts. Return ONLY the enhanced prompt."
            },
            "creative": {
                "name": "Creative",
                "color": "#FF69B4", 
                "description": "Adds imaginative flair and vivid descriptions to prompts",
                "prompt": "Enhance the user's prompt by adding creative flair, vivid descriptions, and imaginative elements while preserving the core request. Return ONLY the enhanced prompt."
            },
            "technical": {
                "name": "Technical",
                "color": "#FFA500",
                "description": "Makes prompts precise with technical specifications and details",
                "prompt": "Refine the user's prompt to be precise, detailed, and technically accurate with clear specifications and requirements. Return ONLY the enhanced prompt."
            },
            "concise": {
                "name": "Concise",
                "color": "#20B2AA",
                "description": "Reduces prompts to essential information, brief and clear",
                "prompt": "Make the user's prompt as clear and brief as possible while retaining all essential information and meaning. Return ONLY the enhanced prompt."
            }
        }
        
        # Create command completer
        from prompt_toolkit.completion import Completer, Completion
        
        class CommandCompleter(Completer):
            def __init__(self):
                self.commands = ['/style', '/config', '/quit']
            
            def get_completions(self, document, complete_event):
                text_before_cursor = document.text_before_cursor
                
                # Only complete if line starts with /
                if text_before_cursor.startswith('/'):
                    for command in self.commands:
                        if command.startswith(text_before_cursor):
                            yield Completion(
                                command,
                                start_position=-len(text_before_cursor)
                            )
        
        completer = CommandCompleter()
        
        # Create prompt session with multiline support and completion
        self.prompt_session = PromptSession(
            multiline=True,
            completer=completer
        )
    
    async def run(self):
        """Main application loop"""
        try:
            # Check if this is first run (no config file)
            if not self.config_manager.config_file.exists():
                self._show_initial_setup()
                if not await self._configure_provider():
                    return
            
            self._show_welcome()
            
            while True:
                try:
                    # Check if configured
                    if not self.config_manager.is_configured(self.config):
                        self._show_configuration_needed()
                        if not await self._configure_provider():
                            break
                    
                    # Get user prompt
                    user_prompt = await self._get_user_prompt()
                    if user_prompt is None:
                        break
                    if not user_prompt:
                        continue
                    
                    # Enhance prompt
                    enhanced_prompt = await self._enhance_prompt(user_prompt)
                    if not enhanced_prompt:
                        continue
                    
                    # Show enhanced prompt
                    self._display_enhanced_prompt(enhanced_prompt)
                    
                    # Ask to copy to clipboard
                    if Confirm.ask("[yellow]Copy enhanced prompt to clipboard?[/yellow]", default=True):
                        if self.clipboard_manager.copy_to_clipboard(enhanced_prompt):
                            self.console.print("[green]✓ Copied to clipboard![/green]")
                        else:
                            self.console.print("[red]✗ Failed to copy to clipboard[/red]")
                    
                    self.console.print("\n" + "─" * 50 + "\n")
                    
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    self.console.print(f"[red]Error: {e}[/red]")
                    
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Goodbye![/yellow]")
    
    def _show_welcome(self):
        """Display welcome message"""
        title = Text("PMPT CLI", style="bold cyan")
        
        current_style_name = self.enhancement_styles[self.config.current_style]['name']
        detected_language = self.language_detector.detect_language()
        
        if self.config.provider:
            subtitle = f"Provider: {self.config.provider} | Model: {self.config.get_model()} | Style: {current_style_name}"
        else:
            subtitle = f"Base URL: {self.config.get_base_url()} | Model: {self.config.get_model()} | Style: {current_style_name}"
        
        if detected_language:
            subtitle += f" | Language: {detected_language.title()}"
        
        panel = Panel(
            f"[bold cyan]{title}[/bold cyan]\n"
            f"[dim]{subtitle}[/dim]\n\n"
            "[bold]How to use:[/bold]\n"
            "• Enter your prompt and get an enhanced version\n"
            "• [yellow]Enter[/yellow] - New line\n"
            "• [yellow]Meta+Enter[/yellow] - Process prompt\n\n"
            "[bold]Available commands:[/bold]\n"
            "• [green]/config[/green] - Settings\n"
            "• [green]/style[/green] - Change enhancement style\n"
            "• [green]/quit[/green] - Exit application",
            title="🚀 Welcome",
            title_align="left",
            border_style="cyan",
            padding=(1, 2)
        )
        self.console.print(panel)
        self.console.print()
    
    def _show_initial_setup(self):
        """Show initial setup welcome message"""
        panel = Panel(
            "[bold cyan]Welcome to PMPT CLI![/bold cyan]\n\n"
            "This is your first time running the tool.\n"
            "Let's set up your AI provider configuration.\n\n"
            "[dim]You'll need to provide:[/dim]\n"
            "• API key for your chosen provider\n"
            "• Provider name (openai, anthropic, openrouter) or custom base URL\n" 
            "• Model name (e.g., gpt-4o, claude-3-5-sonnet-20241022)",
            title="Initial Setup",
            border_style="green"
        )
        self.console.print(panel)
        self.console.print()
    
    def _show_configuration_needed(self):
        """Show configuration needed message"""
        self.console.print("[yellow]⚠ Configuration incomplete[/yellow]")
    
    async def _configure_provider(self) -> bool:
        """Configure API settings"""
        try:
            self.console.print("[bold]Configuration:[/bold]")
            
            # Step 1: Choose provider with menu
            self.console.print("\n[bold cyan]Step 1: Choose Provider[/bold cyan]")
            
            provider_choice = await questionary.select(
                "Select your AI provider:",
                choices=[
                    questionary.Choice("OpenAI", value="openai"),
                    questionary.Choice("Anthropic (Claude)", value="anthropic"), 
                    questionary.Choice("OpenRouter", value="openrouter"),
                    questionary.Choice("Custom (enter base URL)", value="custom")
                ],
                style=questionary.Style([
                    ('highlighted', 'fg:#00aa00 bold'),
                    ('pointer', 'fg:#00aa00 bold'),
                    ('question', 'bold')
                ])
            ).ask_async()
            
            if not provider_choice:
                self.console.print("[yellow]Configuration cancelled[/yellow]")
                return False
            
            # Configure provider or custom URL
            if provider_choice == "custom":
                self.console.print("\n[bold cyan]Custom Provider Configuration[/bold cyan]")
                base_url = await self.prompt_session.prompt_async("Enter base URL: ", is_password=False)
                base_url = base_url.strip()
                if not base_url:
                    self.console.print("[red]Base URL is required[/red]")
                    return False
                
                self.config.provider = None
                self.config.base_url = base_url
                self.console.print(f"[green]✓ Using custom URL: {base_url}[/green]")
            else:
                self.config.provider = provider_choice
                self.config.base_url = None
                self.console.print(f"[green]✓ Using {provider_choice} provider[/green]")
            
            # Step 2: Get API key
            self.console.print("\n[bold cyan]Step 2: API Key[/bold cyan]")
            api_key = await self.prompt_session.prompt_async("Enter your API key: ", is_password=True)
            api_key = api_key.strip()
            if not api_key:
                self.console.print("[red]API key is required[/red]")
                return False
            
            # Step 3: Get model
            self.console.print("\n[bold cyan]Step 3: Model Name[/bold cyan]")
            
            model = await self.prompt_session.prompt_async("Enter model name: ", is_password=False)
            model = model.strip()
            if not model:
                self.console.print("[red]Model is required[/red]")
                return False
            
            # Save configuration
            self.config.api_key = api_key
            self.config.model = model
            self.config_manager.save_config(self.config)
            
            self.console.print(f"\n[green]✓ Configuration saved successfully![/green]")
            self.console.print(f"Provider: {self.config.provider or 'Custom'}")
            self.console.print(f"Base URL: {self.config.get_base_url()}")
            self.console.print(f"Model: {self.config.model}")
            
            return True
            
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Configuration cancelled[/yellow]")
            return False
        except Exception as e:
            self.console.print(f"[red]Configuration error: {e}[/red]")
            return False
    
    async def _select_style(self):
        """Show style selection menu"""
        try:
            style_choice = await questionary.select(
                "Select enhancement style:",
                choices=[
                    questionary.Choice(f"{style_info['name']} - {style_info['description']}", value=style_key)
                    for style_key, style_info in self.enhancement_styles.items()
                ],
                default=self.config.current_style,
                style=questionary.Style([
                    ('highlighted', 'fg:#00aa00 bold'),
                    ('pointer', 'fg:#00aa00 bold'),
                    ('question', 'bold')
                ])
            ).ask_async()
            
            if style_choice:
                self.config.current_style = style_choice
                self.config_manager.save_config(self.config)
                style_name = self.enhancement_styles[style_choice]['name']
                self.console.print(f"[green]✓ Style changed to: {style_name}[/green]")
        except KeyboardInterrupt:
            pass

    async def _get_user_prompt(self) -> Optional[str]:
        """Get prompt from user"""
        try:
            current_style = self.enhancement_styles[self.config.current_style]
            style_color = current_style['color']
            style_name = current_style['name']
            
            # Use formatted text instead of HTML to avoid parsing errors
            from prompt_toolkit.formatted_text import FormattedText
            
            color_map = {
                "#90EE90": "ansibrightgreen",
                "#4169E1": "ansiblue", 
                "#FF69B4": "ansibrightmagenta",
                "#FFA500": "ansiyellow",
                "#20B2AA": "ansicyan"
            }
            
            pt_color = color_map.get(style_color, "ansiwhite")
            colored_prompt = FormattedText([
                (f'bold {pt_color}', style_name),
                ('', ' | Your prompt: ')
            ])
            
            # Use prompt_toolkit with multiline for proper paste support
            user_input = await self.prompt_session.prompt_async(
                colored_prompt
            )
            user_input = user_input.strip()
            
            if user_input.lower() == '/quit':
                return None
            elif user_input.lower() == '/config':
                await self._configure_provider()
                return ""
            elif user_input.lower() == '/style':
                await self._select_style()
                return ""
            # Legacy support for old commands
            elif user_input.lower() == 'quit':
                return None
            elif user_input.lower() == 'config':
                await self._configure_provider()
                return ""
            
            return user_input if user_input else ""
            
        except KeyboardInterrupt:
            return None
        except EOFError:
            return None
    
    async def _enhance_prompt(self, user_prompt: str) -> Optional[str]:
        """Enhance user prompt using AI"""
        if not user_prompt:
            return ""
        
        try:
            client = APIClient(self.config)
            current_style = self.enhancement_styles[self.config.current_style]
            
            # Add language context to the system prompt
            language_context = self.language_detector.get_language_context()
            enhanced_system_prompt = current_style['prompt']
            if language_context:
                enhanced_system_prompt += f" The user is working on a {language_context}, so consider this context when enhancing their prompt."
            
            with self.console.status(f"[bold green]Enhancing prompt ({current_style['name']})..."):
                enhanced = await client.enhance_prompt(user_prompt, enhanced_system_prompt)
            
            return enhanced
            
        except Exception as e:
            self.console.print(f"[red]Enhancement failed: {e}[/red]")
            return None
    
    def _display_enhanced_prompt(self, enhanced_prompt: str):
        """Display the enhanced prompt"""
        current_style = self.enhancement_styles[self.config.current_style]
        
        # Create white text for the prompt content
        styled_prompt = Text(enhanced_prompt, style="white")
        
        panel = Panel(
            styled_prompt,
            title=f"Enhanced Prompt ({current_style['name']})",
            border_style="green",
            title_align="left"
        )
        self.console.print("\n")
        self.console.print(panel)