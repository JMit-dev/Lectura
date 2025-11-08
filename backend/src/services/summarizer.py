"""Text summarization service using Gemini"""

import logging
from typing import Any, Dict

import google.generativeai as genai

from src.utils.config import settings

logger = logging.getLogger(__name__)


class Summarizer:
    """Text summarization service using Gemini"""

    def __init__(self) -> None:
        """Initialize summarizer with direct Gemini API"""
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not set in environment")

        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash-exp")
        logger.info("Initialized Summarizer with direct Gemini API")

    def summarize(
        self, text: str, format: str | None = None, max_length: int = 500
    ) -> Dict[str, Any]:
        """
        Summarize text using Gemini.

        Args:
            text: Text to summarize
            format: Format of summary (deprecated, ignored if provided)
            max_length: Maximum length of summary in words

        Returns:
            Dict with 'summary' (str), 'original_length' (int), and 'summary_length' (int)

        Raises:
            ValueError: If text is empty
            Exception: If summarization fails
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        try:
            original_length = len(text.split())
            logger.info(f"Summarizing {original_length} words (max: {max_length} words)")

            # Use flexible format with headers, bullets, and paragraphs as needed
            system_prompt = (
                "You are an expert at creating concise, well-structured summaries. "
                "Create clear, organized summaries using the most effective format."
            )
            prompt = (
                f"Summarize the following text using the most effective format. "
                f"Use headers (##), bullet points (•), and short paragraphs where appropriate. "
                f"Maximum {max_length} words. Focus on clarity and organization.\n\n"
                f"Text:\n{text}\n\n"
                f"Summary:"
            )

            # Generate summary using direct Gemini API
            full_prompt = f"{system_prompt}\n\n{prompt}"
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.3,
                    max_output_tokens=max_length * 2,
                ),
            )

            summary = response.text.strip()
            summary_length = len(summary.split())

            logger.info(
                f"Summary generated: {original_length} words -> {summary_length} words "
                f"({summary_length / original_length * 100:.1f}% of original)"
            )

            return {
                "summary": summary,
                "original_length": original_length,
                "summary_length": summary_length,
            }

        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error summarizing text: {str(e)}")
            raise Exception(f"Summarization failed: {str(e)}")
