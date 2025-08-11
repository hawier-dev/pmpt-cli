import json
from pathlib import Path
from dataclasses import dataclass
from typing import Optional


# Predefined providers - base URLs only
PROVIDERS = {
    "openai": {
        "base_url": "https://api.openai.com/v1"
    },
    "anthropic": {
        "base_url": "https://api.anthropic.com"
    },
    "openrouter": {
        "base_url": "https://openrouter.ai/api/v1"
    }
}


@dataclass
class Config:
    """Configuration class"""
    api_key: str = ""
    provider: Optional[str] = None
    base_url: Optional[str] = None
    model: str = ""
    current_style: str = "gentle"
    
    def get_base_url(self) -> str:
        """Get effective base URL"""
        if self.base_url:
            url = self.base_url
            # Remove /chat/completions if it was accidentally included
            if url.endswith('/chat/completions'):
                url = url[:-len('/chat/completions')]
            return url
        if self.provider and self.provider in PROVIDERS:
            return PROVIDERS[self.provider]["base_url"]
        return "https://api.openai.com/v1"
    
    def get_model(self) -> str:
        """Get model - must be explicitly set"""
        return self.model
    
    def get_api_key(self) -> str:
        """Get API key"""
        return self.api_key


class ConfigManager:
    """Manages configuration loading and saving"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".pmpt-cli"
        self.config_file = self.config_dir / "config.json"
        self.config_dir.mkdir(exist_ok=True)
    
    def load_config(self) -> Config:
        """Load configuration from file"""
        if not self.config_file.exists():
            return Config()
        
        try:
            with open(self.config_file, 'r') as f:
                data = json.load(f)
            return Config(**data)
        except Exception:
            return Config()
    
    def save_config(self, config: Config):
        """Save configuration to file"""
        try:
            data = {
                'api_key': config.api_key,
                'model': config.model,
                'current_style': config.current_style
            }
            if config.provider:
                data['provider'] = config.provider
            if config.base_url:
                data['base_url'] = config.base_url
                
            with open(self.config_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def is_configured(self, config: Config) -> bool:
        """Check if configuration is complete"""
        return bool(config.api_key and (config.provider or config.base_url) and config.model)
    
    def get_provider_names(self) -> list:
        """Get list of available provider names"""
        return list(PROVIDERS.keys())