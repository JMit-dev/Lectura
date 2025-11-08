"""Flashcard generation service using Gemini"""

import json
import logging
import re
from typing import Dict, List

from src.models.schemas import Flashcard
from src.services.gemini import GeminiClient

logger = logging.getLogger(__name__)


class FlashcardGenerator:
    """Flashcard generation service using Gemini"""

    def __init__(self) -> None:
        """Initialize flashcard generator with Gemini client"""
        self.gemini_client = GeminiClient()
        logger.info("Initialized FlashcardGenerator with Gemini")

    def generate_flashcards(
        self, text: str, count: int = 10, difficulty: str = "medium"
    ) -> Dict[str, any]:
        """
        Generate flashcards from text using Gemini.

        Args:
            text: Source text to generate flashcards from
            count: Number of flashcards to generate (1-50)
            difficulty: Difficulty level ('easy', 'medium', 'hard')

        Returns:
            Dict with 'flashcards' list and optional 'tokens_saved'

        Raises:
            ValueError: If text is empty, count invalid, or difficulty invalid
            Exception: If flashcard generation fails
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        if count < 1 or count > 50:
            raise ValueError(f"Count must be between 1 and 50, got {count}")

        if difficulty not in ["easy", "medium", "hard"]:
            raise ValueError(
                f"Invalid difficulty: {difficulty}. Must be 'easy', 'medium', or 'hard'"
            )

        try:
            logger.info(f"Generating {count} {difficulty} flashcards from {len(text)} characters")

            # Create prompt for flashcard generation
            system_prompt = (
                "You are an expert educator who creates high-quality study flashcards. "
                "Generate clear, concise question-answer pairs that help students "
                "learn effectively."
            )

            difficulty_guidelines = {
                "easy": "Focus on basic facts, definitions, and simple concepts.",
                "medium": "Include some analysis, comparisons, and moderate complexity.",
                "hard": "Include complex concepts, critical thinking, and deep understanding.",
            }

            prompt = f"""Generate exactly {count} flashcards from the following text.

Difficulty level: {difficulty} - {difficulty_guidelines[difficulty]}

Return the flashcards as a JSON array with this exact format:
[
  {{
    "question": "Clear, specific question",
    "answer": "Concise, accurate answer",
    "difficulty": "{difficulty}"
  }}
]

Rules:
- Questions should be clear and specific
- Answers should be concise but complete
- Cover different aspects of the content
- Avoid yes/no questions
- Make sure all {count} flashcards are unique and valuable

Text:
{text}

JSON output:"""

            # Generate flashcards using Gemini
            result = self.gemini_client.generate_text(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.7,  # Some creativity but focused
                max_tokens=count * 100,  # Rough estimate per flashcard
            )

            flashcards_text = result["text"].strip()
            tokens_used = result["tokens_used"]

            # Parse JSON response
            flashcards = self._parse_flashcards_response(flashcards_text, count, difficulty)

            logger.info(f"Generated {len(flashcards)} flashcards using {tokens_used} tokens")

            return {
                "flashcards": flashcards,
                "tokens_saved": None,  # TODO: Implement TOON format for token savings
            }

        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error generating flashcards: {str(e)}")
            raise Exception(f"Flashcard generation failed: {str(e)}")

    def _parse_flashcards_response(
        self, response_text: str, expected_count: int, difficulty: str
    ) -> List[Flashcard]:
        """
        Parse flashcards from Gemini response.

        Args:
            response_text: Raw response from Gemini
            expected_count: Expected number of flashcards
            difficulty: Difficulty level

        Returns:
            List of Flashcard objects

        Raises:
            ValueError: If parsing fails or format is invalid
        """
        try:
            # Try to extract JSON from response
            # Sometimes the model adds markdown code blocks
            json_match = re.search(r"\[\s*\{.*?\}\s*\]", response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
            else:
                json_str = response_text

            # Parse JSON
            flashcards_data = json.loads(json_str)

            if not isinstance(flashcards_data, list):
                raise ValueError("Response is not a JSON array")

            flashcards = []
            for item in flashcards_data[:expected_count]:  # Limit to expected count
                if not isinstance(item, dict):
                    logger.warning(f"Skipping invalid flashcard item: {item}")
                    continue

                question = item.get("question", "").strip()
                answer = item.get("answer", "").strip()

                if not question or not answer:
                    logger.warning("Skipping flashcard with empty question or answer")
                    continue

                flashcards.append(
                    Flashcard(question=question, answer=answer, difficulty=difficulty)
                )

            if not flashcards:
                raise ValueError("No valid flashcards found in response")

            logger.debug(f"Parsed {len(flashcards)} flashcards successfully")
            return flashcards

        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {str(e)}\nResponse: {response_text}")
            raise ValueError(f"Failed to parse flashcards response: {str(e)}")
        except Exception as e:
            logger.error(f"Error parsing flashcards: {str(e)}")
            raise ValueError(f"Failed to parse flashcards: {str(e)}")
