"""
LLM Client - Abstract interface for different LLM backends

Supports:
- Claude API (via Anthropic SDK) - recommended since you don't have OpenAI subscription
- Local models (via Ollama)
- Other LLM providers
"""

import logging
import os
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import asyncio

logger = logging.getLogger(__name__)


class LLMClient(ABC):
    """Abstract base class for LLM clients"""

    @abstractmethod
    async def analyze(self, prompt: str) -> str:
        """
        Send a prompt to the LLM and get response

        Args:
            prompt: The prompt to send

        Returns:
            Response text from the LLM
        """
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        """Get the name of the model being used"""
        pass


class ClaudeClient(LLMClient):
    """
    Claude API Client

    Uses Anthropic's Claude API - RECOMMENDED for this project
    since you don't have OpenAI subscription

    Requires:
        - ANTHROPIC_API_KEY environment variable
        - anthropic library: pip install anthropic
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-5-sonnet-20241022"):
        """
        Initialize Claude client

        Args:
            api_key: Anthropic API key (falls back to ANTHROPIC_API_KEY env var)
            model: Claude model to use
                  - "claude-3-opus-20250219" (most capable)
                  - "claude-3-5-sonnet-20241022" (good balance, recommended)
                  - "claude-3-haiku-20240307" (faster, cheaper)
        """
        try:
            from anthropic import Anthropic
        except ImportError:
            raise ImportError("Please install anthropic: pip install anthropic")

        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not provided. Either pass api_key parameter "
                "or set ANTHROPIC_API_KEY environment variable"
            )

        self.client = Anthropic(api_key=self.api_key)
        self.model = model
        self.logger = logging.getLogger(__name__)

    async def analyze(self, prompt: str) -> str:
        """
        Send prompt to Claude and get analysis

        Args:
            prompt: The prompt to analyze

        Returns:
            Claude's response
        """
        try:
            self.logger.info(f"Sending prompt to Claude ({self.model})...")

            # Run synchronous API call in executor to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.messages.create(
                    model=self.model,
                    max_tokens=1024,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )
            )

            result = response.content[0].text
            self.logger.info(f"✓ Received response ({len(result)} chars)")
            return result

        except Exception as e:
            self.logger.error(f"Claude API error: {e}")
            raise

    def get_model_name(self) -> str:
        """Get model name"""
        return self.model


class OllamaClient(LLMClient):
    """
    Ollama Local Model Client

    For running local open-source models without API costs

    Requires:
        - Ollama installed: https://ollama.ai
        - Model pulled: ollama pull llama2 (or other model)
        - Ollama server running: ollama serve
    """

    def __init__(self, model: str = "llama2", base_url: str = "http://localhost:11434"):
        """
        Initialize Ollama client

        Args:
            model: Model name (e.g., "llama2", "mistral", "neural-chat")
            base_url: Ollama server URL
        """
        try:
            import requests
        except ImportError:
            raise ImportError("Please install requests: pip install requests")

        self.model = model
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)

        # Verify connection
        try:
            response = requests.get(f"{base_url}/api/tags", timeout=5)
            if response.status_code != 200:
                raise ConnectionError(f"Ollama server not responding: {response.status_code}")
            self.logger.info(f"✓ Connected to Ollama at {base_url}")
        except Exception as e:
            raise ConnectionError(f"Cannot connect to Ollama at {base_url}: {e}")

    async def analyze(self, prompt: str) -> str:
        """
        Send prompt to Ollama model

        Args:
            prompt: The prompt to analyze

        Returns:
            Model's response
        """
        import requests

        try:
            self.logger.info(f"Sending prompt to Ollama ({self.model})...")

            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.7
                },
                timeout=120
            )

            if response.status_code != 200:
                raise Exception(f"Ollama error: {response.status_code}")

            result = response.json().get("response", "")
            self.logger.info(f"✓ Received response ({len(result)} chars)")
            return result

        except Exception as e:
            self.logger.error(f"Ollama error: {e}")
            raise

    def get_model_name(self) -> str:
        """Get model name"""
        return self.model


class MockLLMClient(LLMClient):
    """
    Mock LLM Client for testing without actual API calls

    Useful for development and testing the pipeline structure
    """

    def __init__(self, model: str = "mock-model"):
        """Initialize mock client"""
        self.model = model
        self.logger = logging.getLogger(__name__)

    async def analyze(self, prompt: str) -> str:
        """
        Return mock response based on prompt content

        Args:
            prompt: The prompt

        Returns:
            Mock response
        """
        self.logger.info(f"Sending prompt to Mock LLM ({self.model})...")

        # Create a fake response
        response = """Visual Prompt:
A vibrant, energetic scene with flowing abstract forms in warm amber and golden yellow tones,
capturing the ascending melodic contour of the music. The composition features dynamic movement
from bottom-left to top-right, with ethereal light breaking through layered forms.

Color Palette:
- Primary: Golden amber (#FFD700), warm yellow (#FFEB3B)
- Secondary: Soft bronze (#CD7F32), warm orange (#FF8C00)
- Accent: White highlights for brightness
- Background: Deep blue shadow tones

Compositional Elements:
The scene uses a spiral or ascending diagonal composition, mirroring the ascending melody.
Multiple layers of translucent forms create depth and complexity matching the harmonic progression.
The lighting is warm and inviting, with high contrast areas drawing the eye upward.

Mood & Atmosphere:
Uplifting, energetic, and contemplative. The image conveys movement and positive emotion,
with a sense of journey or progression. The atmosphere feels both celebratory and introspective."""

        self.logger.info(f"✓ Mock response generated ({len(response)} chars)")
        return response

    def get_model_name(self) -> str:
        """Get model name"""
        return self.model


def create_llm_client(provider: str = "claude", **kwargs) -> LLMClient:
    """
    Factory function to create LLM clients

    Args:
        provider: "claude", "ollama", or "mock"
        **kwargs: Provider-specific arguments

    Returns:
        LLMClient instance

    Examples:
        # Use Claude (recommended)
        client = create_llm_client("claude")

        # Use local Ollama
        client = create_llm_client("ollama", model="mistral")

        # Use mock for testing
        client = create_llm_client("mock")
    """
    logger.info(f"Creating LLM client: {provider}")

    if provider == "claude":
        return ClaudeClient(**kwargs)
    elif provider == "ollama":
        return OllamaClient(**kwargs)
    elif provider == "mock":
        return MockLLMClient(**kwargs)
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")


# Configuration helper
def get_recommended_client() -> LLMClient:
    """
    Get recommended client based on available resources

    Returns:
        LLMClient instance (Claude if API key available, else Mock)
    """
    if os.getenv("ANTHROPIC_API_KEY"):
        logger.info("✓ Using Claude (ANTHROPIC_API_KEY found)")
        return create_llm_client("claude")
    else:
        logger.warning("⚠ ANTHROPIC_API_KEY not found, using Ollama client for testing")
        logger.info("   To use Claude: export ANTHROPIC_API_KEY=your_api_key")
        logger.info("   To use local Ollama: ollama pull mistral && ollama serve")
        return create_llm_client("ollama")
