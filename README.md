# PMPT CLI

A beautiful CLI tool that enhances your prompts using AI providers like OpenAI, Anthropic, and OpenRouter.

## Features

- 🤖 Support for multiple AI providers:
  - OpenAI (GPT-4, etc.)
  - Anthropic (Claude)
  - OpenRouter (access to various models)
- ⚙️ Easy configuration management
- 📋 Automatic clipboard integration
- 🔄 Interactive prompt enhancement workflow

## Installation

1. Clone or download the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool:
```bash
python main.py
```

### First Time Setup

When you first run the tool, you'll need to configure your API key:
1. The tool will prompt you for your API key
2. Optionally configure the base URL and model
3. Settings are saved to `~/.pmpt-cli/config.json`

### Commands

- Enter any prompt to enhance it
- Type `config` to reconfigure settings  
- Type `quit` to exit
- Use Ctrl+C to exit at any time

## Configuration

The tool supports three providers:

### OpenAI
- Default model: `gpt-4o`
- Base URL: `https://api.openai.com/v1`
- Requires OpenAI API key

### Anthropic
- Default model: `claude-3-5-sonnet-20241022`  
- Base URL: `https://api.anthropic.com`
- Requires Anthropic API key

### OpenRouter
- Default model: `anthropic/claude-3.5-sonnet`
- Base URL: `https://openrouter.ai/api/v1`
- Requires OpenRouter API key

## Development

Install in development mode:
```bash
pip install -e .
```

## Requirements

- Python 3.8+
- aiohttp
- prompt-toolkit
- rich
