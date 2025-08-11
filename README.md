# PMPT

AI-powered prompt enhancement tool that improves your prompts using OpenAI, Anthropic, and OpenRouter APIs.

![Demo](demo.gif)

## Features

- 🤖 **Multiple AI Providers**: OpenAI, Anthropic (Claude), OpenRouter
- 🎨 **Enhancement Styles**: Gentle, Structured, Creative  
- 🔍 **Smart Environment Detection**: Automatically detects your project's programming environment
- ⌨️ **Command Completion**: Tab completion for commands
- 📋 **Clipboard Integration**: Automatic copying to clipboard
- ⚙️ **Easy Configuration**: First-run setup wizard

## Installation

### Via pip (Recommended)

```bash
pip install pmpt-cli
```

### Linux/macOS (Bash)

Run the installation script:

```bash
curl -fsSL https://raw.githubusercontent.com/hawier-dev/pmpt-cli/main/install.sh | bash
```

### Manual Installation

```bash
git clone https://github.com/hawier-dev/pmpt-cli.git
cd pmpt-cli  
pip install -e .
```

## Usage

Simply run:
```bash
pmpt
```

### First Time Setup
The tool will automatically guide you through configuration:
1. Choose your AI provider (OpenAI/Anthropic/OpenRouter/Custom)
2. Enter your API key
3. Specify your model
4. Settings are saved to `~/.pmpt-cli/config.json`

## Configuration

### Supported Providers
- **OpenAI**: GPT models via OpenAI API
- **Anthropic**: Claude models via Anthropic API  
- **OpenRouter**: Access to various models
- **Custom**: Any OpenAI-compatible API

### Configuration File
Located at `~/.pmpt-cli/config.json`:
```json
{
  "api_key": "your-api-key",
  "provider": "openai", 
  "model": "gpt-4o",
  "current_style": "gentle"
}
```

## Requirements

- **Python 3.8+** (add to PATH during installation)
- **Git** (for installation scripts)
- **API key** for chosen provider (OpenAI, Anthropic, OpenRouter, etc.)

## Development

```bash
git clone https://github.com/hawier-dev/pmpt-cli.git
cd pmpt-cli
pip install -e .
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
