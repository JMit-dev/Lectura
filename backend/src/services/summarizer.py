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
        self, text: str, format: str | None = None, max_length: int = 1200
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
            character_count = len(text)

            # Adapt the target summary length based on transcript size.
            # Default to at least 600 words, allow up to 4,000 for very large lectures.
            adaptive_target = max(
                600,
                min(4000, int(max(character_count / 30, original_length * 0.2))),
            )
            target_words = max(max_length, adaptive_target)

            logger.info(
                "Summarizing %s words (%s chars) with target summary length %s words",
                original_length,
                character_count,
                target_words,
            )

            # Use flexible format with headers, bullets, and paragraphs as needed
            system_prompt = (
                "You are a meticulous university note-taker who converts raw lecture transcripts "
                "into comprehensive, Markdown-formatted study notes. "
                "You filter out jokes, greetings, administrative chatter, and schedule reminders, "
                "focusing exclusively on instructional content."
            )
            prompt = (
                "You will receive a full lecture transcript that may include professor banter, "
                "attendance checks, or other irrelevant chatter.\n\n"
                "Create extremely detailed Markdown notes that capture every meaningful concept, "
                "definition, example, formula, and explanation from the LESSON ONLY.\n"
                "Follow these rules:\n"
                "1. Ignore filler dialogue, jokes, personal stories, or small talk.\n"
                "2. Exclude logistics like quiz/test dates, homework reminders, "
                "or grading info unless they clarify a concept.\n"
                "3. Use Markdown: start with `## Overview`, then add `###` "
                "sections per major topic.\n"
                "   Within each section use bullets, numbered steps, tables, "
                "or nested lists to capture supporting details.\n"
                "4. Highlight key definitions, theorems, and formulas with "
                "bold labels or inline code.\n"
                "5. Merge repeated explanations so the notes stay cohesive "
                "and non-redundant while still covering every major point.\n"
                f"6. Produce a highly detailed summary up to ~{target_words} "
                "words (scale detail with lecture length) "
                "so that no important lecture topic is omitted.\n\n"
                "Transcript:\n"
                f"{text}\n\n"
                "Return ONLY Markdown-formatted notes."
            )

            # Generate summary using direct Gemini API
            full_prompt = f"{system_prompt}\n\n{prompt}"
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.25,
                    max_output_tokens=min(target_words * 4, 12000),
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
