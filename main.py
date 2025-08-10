#!/usr/bin/env python3
"""
CLI tool for prompt enhancement using various AI providers
"""
import asyncio
import sys
from pathlib import Path

from src.cli import PromptEnhancerCLI


def main():
    """Main entry point"""
    try:
        cli = PromptEnhancerCLI()
        asyncio.run(cli.run())
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()