"""Version information and update checking for PMPT CLI"""

import asyncio
import aiohttp
import json
from packaging import version
from typing import Optional, Dict, Any


__version__ = "0.1.6"


class UpdateChecker:
    """Check for updates from GitHub releases"""
    
    def __init__(self):
        self.github_api = "https://api.github.com/repos/hawier-dev/pmpt-cli/releases/latest"
        self.current_version = __version__
    
    async def check_for_updates(self) -> Optional[Dict[str, Any]]:
        """Check if a newer version is available"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.github_api, timeout=5) as response:
                    if response.status != 200:
                        return None
                    
                    data = await response.json()
                    latest_version = data.get('tag_name', '').lstrip('v')
                    
                    if not latest_version:
                        return None
                    
                    # Compare versions
                    if version.parse(latest_version) > version.parse(self.current_version):
                        return {
                            'latest_version': latest_version,
                            'current_version': self.current_version,
                            'release_url': data.get('html_url', ''),
                            'release_notes': data.get('body', ''),
                            'download_url': data.get('tarball_url', '')
                        }
                    
                    return None
                    
        except (aiohttp.ClientError, asyncio.TimeoutError, json.JSONDecodeError):
            return None
    
    def get_current_version(self) -> str:
        """Get current version string"""
        return self.current_version