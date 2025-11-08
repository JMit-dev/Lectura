"""Flashcard generation service using Gemini with TOON format for token savings"""

import json
import logging
import re
from typing import Any, Dict, List

import google.generativeai as genai

from src.models.schemas import Flashcard
from src.services.toon import TOONParser, get_toon_flashcard_prompt
from src.utils.config import settings

logger = logging.getLogger(__name__)


class FlashcardGenerator:
    """Flashcard generation service using Gemini with TOON optimization"""

    def __init__(self) -> None:
        """Initialize flashcard generator with direct Gemini API"""
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not set in environment")

        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash-exp")
        logger.info("Initialized FlashcardGenerator with direct Gemini API + TOON format")

    def generate_flashcards(
        self, text: str, count: int | None = None, difficulty: str = "medium", use_toon: bool = True
    ) -> Dict[str, Any]:
        """
        Generate flashcards from text using Gemini.

        Args:
            text: Source text to generate flashcards from
            count: Number of flashcards to generate (1-50).
                   If None, auto-calculated based on text length.
            difficulty: Difficulty level ('easy', 'medium', 'hard')
            use_toon: Use TOON format for 40-50% token savings (default: True)

        Returns:
            Dict with 'flashcards' list and 'tokens_saved' statistics

        Raises:
            ValueError: If text is empty, count invalid, or difficulty invalid
            Exception: If flashcard generation fails
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        # Auto-calculate count if not provided (1 flashcard per ~100 words)
        if count is None:
            word_count = len(text.split())
            count = max(5, min(50, word_count // 100))
            logger.info(f"Auto-calculated flashcard count: {count} (based on {word_count} words)")

        if count < 1 or count > 50:
            raise ValueError(f"Count must be between 1 and 50, got {count}")

        if difficulty not in ["easy", "medium", "hard"]:
            raise ValueError(
                f"Invalid difficulty: {difficulty}. Must be 'easy', 'medium', or 'hard'"
            )

        try:
            logger.info(
                f"Generating {count} {difficulty} flashcards "
                f"(TOON: {use_toon}, text: {len(text)} chars)"
            )

            # System prompt
            system_prompt = (
                "You are an expert educator who creates high-quality study flashcards. "
                "Generate clear, concise question-answer pairs."
            )

            # Use TOON format for massive token savings (40-50%)
            if use_toon:
                prompt = get_toon_flashcard_prompt(text, count, difficulty)
            else:
                # Fallback JSON (less efficient)
                prompt = self._get_json_prompt(text, count, difficulty)

            # Generate with direct Gemini API
            full_prompt = f"{system_prompt}\n\n{prompt}"
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=count * 80,
                ),
            )

            response_text = response.text.strip()
            # Estimate tokens used (Gemini API doesn't return usage in free tier)
            tokens_used = len(response_text) // 4  # Rough estimate

            # Parse based on format
            if use_toon:
                flashcards = TOONParser.parse_flashcards(response_text, difficulty)
                # Estimate savings
                json_sample = json.dumps(
                    [
                        {
                            "question": "What is the main topic discussed?",
                            "answer": "The text discusses various concepts and ideas.",
                            "difficulty": difficulty,
                        }
                    ]
                    * count
                )
                savings = TOONParser.estimate_token_savings(len(json_sample), len(response_text))
                tokens_saved = savings["tokens_saved"]
                logger.info(
                    f"✨ TOON saved ~{tokens_saved} tokens "
                    f"({savings['savings_percent']}% reduction)!"
                )
            else:
                flashcards = self._parse_json_flashcards(response_text, count, difficulty)
                tokens_saved = None

            logger.info(f"Generated {len(flashcards)} flashcards using {tokens_used} tokens")

            return {
                "flashcards": flashcards,
                "tokens_saved": tokens_saved,
            }

        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error generating flashcards: {str(e)}")
            raise Exception(f"Flashcard generation failed: {str(e)}")

    def _get_json_prompt(self, text: str, count: int, difficulty: str) -> str:
        """Generate JSON format prompt (fallback)"""
        guidelines = {
            "easy": "basic facts and definitions",
            "medium": "analysis and moderate complexity",
            "hard": "complex concepts and critical thinking",
        }

        return f"""Generate {count} flashcards ({difficulty}: {guidelines[difficulty]}).

Rules:
- Use substantive lecture content only; skip greetings, jokes, or logistics.
- Drop quiz/test dates or admin reminders unless they directly teach a concept.
- Ask clear, specific questions that require understanding, not rote recall.
- Provide concise answers that still capture the reasoning or formula involved.
- Keep every flashcard unique and tightly focused on the lesson material.

Return as JSON: [{{"question": "...", "answer": "...", "difficulty": "{difficulty}"}}]

Text:
{text}

JSON:"""

    def _parse_json_flashcards(
        self, response_text: str, expected_count: int, difficulty: str
    ) -> List[Flashcard]:
        """Parse flashcards from JSON response"""
        try:
            # Extract JSON from response
            json_match = re.search(r"\[\s*\{.*?\}\s*\]", response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
            else:
                json_str = response_text

            flashcards_data = json.loads(json_str)

            if not isinstance(flashcards_data, list):
                raise ValueError("Response is not a JSON array")

            flashcards = []
            for item in flashcards_data[:expected_count]:
                if not isinstance(item, dict):
                    continue

                question = item.get("question", "").strip()
                answer = item.get("answer", "").strip()

                if question and answer:
                    flashcards.append(
                        Flashcard(question=question, answer=answer, difficulty=difficulty)
                    )

            if not flashcards:
                raise ValueError("No valid flashcards found")

            return flashcards

        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {str(e)}")
            raise ValueError(f"Failed to parse JSON: {str(e)}")
        except Exception as e:
            logger.error(f"Parse error: {str(e)}")
            raise ValueError(f"Failed to parse flashcards: {str(e)}")
