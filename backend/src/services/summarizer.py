"""Text summarization service using Gemini"""

import logging
from typing import Dict

from src.services.gemini import GeminiClient

logger = logging.getLogger(__name__)


class Summarizer:
    """Text summarization service using Gemini"""

    def __init__(self) -> None:
        """Initialize summarizer with Gemini client"""
        self.gemini_client = GeminiClient()
        logger.info("Initialized Summarizer with Gemini")

    def summarize(
        self, text: str, format: str = "bullet_points", max_length: int = 500
    ) -> Dict[str, int]:
        """
        Summarize text using Gemini.

        Args:
            text: Text to summarize
            format: Format of summary ('bullet_points' or 'paragraph')
            max_length: Maximum length of summary in words

        Returns:
            Dict with 'summary', 'original_length', and 'summary_length'

        Raises:
            ValueError: If text is empty or format is invalid
            Exception: If summarization fails
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        if format not in ["bullet_points", "paragraph"]:
            raise ValueError(f"Invalid format: {format}. Must be 'bullet_points' or 'paragraph'")

        try:
            original_length = len(text.split())
            logger.info(
                f"Summarizing {original_length} words in {format} format "
                f"(max: {max_length} words)"
            )

            # Create prompt based on format
            if format == "bullet_points":
                system_prompt = (
                    "You are an expert at creating concise, informative summaries. "
                    "Create bullet-point summaries that capture key ideas."
                )
                prompt = (
                    f"Summarize the following text as clear bullet points. "
                    f"Maximum {max_length} words. Focus on the main ideas and key takeaways.\n\n"
                    f"Text:\n{text}\n\n"
                    f"Summary (bullet points):"
                )
            else:  # paragraph
                system_prompt = (
                    "You are an expert at creating concise, flowing summaries. "
                    "Create paragraph-form summaries that capture the essence of the content."
                )
                prompt = (
                    f"Summarize the following text in a concise paragraph. "
                    f"Maximum {max_length} words. Capture the main ideas clearly.\n\n"
                    f"Text:\n{text}\n\n"
                    f"Summary:"
                )

            # Generate summary using Gemini
            result = self.gemini_client.generate_text(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.3,  # Lower temperature for more focused summaries
                max_tokens=max_length * 2,  # Rough token estimate
            )

            summary = result["text"].strip()
            summary_length = len(summary.split())

            logger.info(
                f"Summary generated: {original_length} words -> {summary_length} words "
                f"({summary_length/original_length*100:.1f}% of original)"
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
