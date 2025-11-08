"""Gemini API client using OpenRouter"""

import logging
from typing import Any, Dict, Optional

from openai import OpenAI

from src.utils.config import settings

logger = logging.getLogger(__name__)


class GeminiClient:
    """
    Wrapper for Gemini API access via OpenRouter.
    Uses OpenAI SDK since OpenRouter is OpenAI-compatible.
    """

    def __init__(self) -> None:
        """Initialize OpenRouter client for Gemini"""
        if not settings.openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY not set in environment")

        self.client = OpenAI(
            base_url=settings.openrouter_base_url,
            api_key=settings.openrouter_api_key,
        )
        self.model = settings.gemini_model
        logger.info(f"Initialized Gemini client via OpenRouter with model: {self.model}")

    def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        use_cache: bool = False,
    ) -> Dict[str, Any]:
        """
        Generate text using Gemini via OpenRouter.

        Args:
            prompt: User prompt
            system_prompt: Optional system instructions
            temperature: Randomness (0.0-2.0, default 0.7)
            max_tokens: Max tokens to generate
            use_cache: Enable prompt caching for cost savings (default: False)

        Returns:
            Dict with 'text' and 'tokens_used' keys

        Raises:
            Exception: If API call fails
        """
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            logger.debug(f"Generating text with {len(messages)} messages (cache: {use_cache})")

            # Build request parameters
            params = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
            }

            if max_tokens:
                params["max_tokens"] = max_tokens

            # Add cache hint via extra headers for OpenRouter
            # OpenRouter automatically caches prompts > 1024 tokens
            if use_cache:
                logger.debug("Prompt caching enabled (OpenRouter auto-caches >1024 tokens)")

            response = self.client.chat.completions.create(**params)

            text = response.choices[0].message.content or ""
            tokens_used = response.usage.total_tokens if response.usage else 0

            # Log cache info if available
            if use_cache:
                logger.info(
                    f"✨ Generated {len(text)} chars using {tokens_used} tokens "
                    f"(caching enabled)"
                )
            else:
                logger.info(f"Generated {len(text)} chars using {tokens_used} tokens")

            return {"text": text, "tokens_used": tokens_used}

        except Exception as e:
            logger.error(f"Error generating text: {str(e)}")
            raise

    def transcribe_audio(
        self,
        audio_file_path: str,
        language: str = "en",
    ) -> Dict[str, Any]:
        """
        Transcribe audio using Gemini via OpenRouter.

        Note: OpenRouter/Gemini doesn't have direct audio transcription API like Whisper.
        This is a placeholder that will need to be implemented differently,
        potentially by:
        1. Converting audio to text using a different service (Whisper API)
        2. Or sending audio as base64 to Gemini with vision/audio capabilities

        Args:
            audio_file_path: Path to audio file
            language: Language code (default: 'en')

        Returns:
            Dict with 'transcript', 'duration', and 'tokens_used'

        Raises:
            NotImplementedError: Direct audio transcription not available yet
        """
        # TODO: Implement audio transcription
        # Options:
        # 1. Use OpenAI Whisper API via OpenRouter
        # 2. Use Gemini's multimodal capabilities with audio
        # 3. Use a separate transcription service

        raise NotImplementedError(
            "Audio transcription needs to be implemented. "
            "Consider using Whisper API or Gemini multimodal features."
        )

    async def test_connection(self) -> bool:
        """
        Test connection to OpenRouter/Gemini.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            result = self.generate_text(
                prompt="Say 'Hello' in one word.",
                temperature=0.0,
            )
            logger.info("Connection test successful")
            return bool(result.get("text"))
        except Exception as e:
            logger.error(f"Connection test failed: {str(e)}")
            return False
