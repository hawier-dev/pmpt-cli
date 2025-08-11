from openai import AsyncOpenAI
from anthropic import AsyncAnthropic

from .config import Config


class APIClient:
    """Unified API client for all providers"""
    
    def __init__(self, config: Config):
        self.config = config
        self.openai_client = None
        self.anthropic_client = None
        self._setup_clients()
    
    def _setup_clients(self):
        """Setup appropriate clients based on configuration"""
        base_url = self.config.get_base_url()
        
        if "anthropic.com" in base_url:
            # Use Anthropic SDK
            self.anthropic_client = AsyncAnthropic(
                api_key=self.config.api_key
            )
        else:
            # Use OpenAI SDK for OpenAI-compatible APIs
            extra_headers = {}
            if "openrouter.ai" in base_url:
                extra_headers = {
                    "HTTP-Referer": "pmpt-cli",
                    "X-Title": "PMPT CLI"
                }
            
            self.openai_client = AsyncOpenAI(
                api_key=self.config.api_key,
                base_url=base_url,
                default_headers=extra_headers
            )
    
    async def enhance_prompt(self, prompt: str, system_prompt: str = None) -> str:
        """Enhance the given prompt"""
        if system_prompt is None:
            system_prompt = "You are a prompt enhancement assistant. Take the user's prompt and improve it to be clearer and more effective. Return ONLY the enhanced prompt with no additional text, explanations, or commentary."

        if self.anthropic_client:
            return await self._call_anthropic(system_prompt, prompt)
        else:
            return await self._call_openai_compatible(system_prompt, prompt)
    
    async def enhance_prompt_stream(self, prompt: str, system_prompt: str = None):
        """Enhance the given prompt with streaming response"""
        if system_prompt is None:
            system_prompt = "You are a prompt enhancement assistant. Take the user's prompt and improve it to be clearer and more effective. Return ONLY the enhanced prompt with no additional text, explanations, or commentary."

        if self.anthropic_client:
            async for chunk in self._call_anthropic_stream(system_prompt, prompt):
                yield chunk
        else:
            async for chunk in self._call_openai_compatible_stream(system_prompt, prompt):
                yield chunk
    
    async def _call_openai_compatible(self, system_prompt: str, prompt: str) -> str:
        """Call using OpenAI SDK for OpenAI-compatible APIs"""
        try:
            response = await self.openai_client.chat.completions.create(
                model=self.config.get_model(),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"API call failed: {str(e)}")
    
    async def _call_openai_compatible_stream(self, system_prompt: str, prompt: str):
        """Call using OpenAI SDK for OpenAI-compatible APIs with streaming"""
        try:
            response = await self.openai_client.chat.completions.create(
                model=self.config.get_model(),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                stream=True
            )
            async for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            raise Exception(f"API call failed: {str(e)}")

    async def _call_anthropic(self, system_prompt: str, prompt: str) -> str:
        """Call Anthropic API using Anthropic SDK"""
        try:
            response = await self.anthropic_client.messages.create(
                model=self.config.get_model(),
                max_tokens=2000,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text.strip()
        except Exception as e:
            raise Exception(f"Anthropic API call failed: {str(e)}")
    
    async def _call_anthropic_stream(self, system_prompt: str, prompt: str):
        """Call Anthropic API using Anthropic SDK with streaming"""
        try:
            async with self.anthropic_client.messages.stream(
                model=self.config.get_model(),
                max_tokens=2000,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            ) as stream:
                async for text in stream.text_stream:
                    yield text
        except Exception as e:
            raise Exception(f"Anthropic API call failed: {str(e)}")