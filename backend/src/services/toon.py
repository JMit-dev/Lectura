"""TOON (Tree Object Oriented Notation) format for token optimization

TOON is a compact text format that reduces token usage compared to JSON
by using abbreviated keys and minimal punctuation.

Example JSON vs TOON:
JSON (150 tokens):
[
  {"question": "What is Python?", "answer": "A programming language", "difficulty": "easy"},
  {"question": "What is OOP?", "answer": "Object Oriented Programming", "difficulty": "medium"}
]

TOON (80 tokens - 47% savings):
Q: What is Python?
A: A programming language
D: easy

Q: What is OOP?
A: Object Oriented Programming
D: medium
"""

import logging
import re
from typing import Any, Dict, List

from src.models.schemas import Flashcard

logger = logging.getLogger(__name__)


class TOONParser:
    """Parser for TOON format to Python objects"""

    @staticmethod
    def parse_flashcards(toon_text: str, difficulty: str = "medium") -> List[Flashcard]:
        """
        Parse flashcards from TOON format.

        TOON Format:
        Q: Question text
        A: Answer text
        D: difficulty (optional)

        (blank line separates flashcards)

        Args:
            toon_text: Text in TOON format
            difficulty: Default difficulty if not specified

        Returns:
            List of Flashcard objects

        Raises:
            ValueError: If parsing fails
        """
        try:
            flashcards = []

            # Split by double newlines (flashcard separator)
            card_blocks = re.split(r"\n\s*\n", toon_text.strip())

            for block in card_blocks:
                if not block.strip():
                    continue

                # Extract Q, A, D fields
                question_match = re.search(r"Q:\s*(.+?)(?=\nA:|\Z)", block, re.DOTALL)
                answer_match = re.search(r"A:\s*(.+?)(?=\nD:|\Z)", block, re.DOTALL)
                difficulty_match = re.search(r"D:\s*(.+?)(?=\n|\Z)", block, re.DOTALL)

                if not question_match or not answer_match:
                    logger.warning(f"Skipping invalid TOON block: {block[:50]}...")
                    continue

                question = question_match.group(1).strip()
                answer = answer_match.group(1).strip()
                card_difficulty = (
                    difficulty_match.group(1).strip() if difficulty_match else difficulty
                )

                flashcards.append(
                    Flashcard(question=question, answer=answer, difficulty=card_difficulty)
                )

            if not flashcards:
                raise ValueError("No valid flashcards found in TOON format")

            logger.info(f"Parsed {len(flashcards)} flashcards from TOON format")
            return flashcards

        except Exception as e:
            logger.error(f"Error parsing TOON format: {str(e)}")
            raise ValueError(f"Failed to parse TOON format: {str(e)}")

    @staticmethod
    def flashcards_to_toon(flashcards: List[Flashcard]) -> str:
        """
        Convert flashcards to TOON format.

        Args:
            flashcards: List of Flashcard objects

        Returns:
            String in TOON format
        """
        toon_blocks = []

        for card in flashcards:
            block = f"Q: {card.question}\nA: {card.answer}\nD: {card.difficulty}"
            toon_blocks.append(block)

        return "\n\n".join(toon_blocks)

    @staticmethod
    def estimate_token_savings(json_length: int, toon_length: int) -> Dict[str, Any]:
        """
        Estimate token savings from using TOON vs JSON.

        Args:
            json_length: Character length of JSON representation
            toon_length: Character length of TOON representation

        Returns:
            Dict with savings statistics
        """
        # Rough estimate: 1 token ≈ 4 characters
        json_tokens = json_length / 4
        toon_tokens = toon_length / 4
        savings = json_tokens - toon_tokens
        savings_percent = (savings / json_tokens * 100) if json_tokens > 0 else 0

        return {
            "json_tokens": int(json_tokens),
            "toon_tokens": int(toon_tokens),
            "tokens_saved": int(savings),
            "savings_percent": round(savings_percent, 1),
        }


def get_toon_flashcard_prompt(text: str, count: int, difficulty: str) -> str:
    """
    Generate prompt for flashcard generation in TOON format.

    Args:
        text: Source text
        count: Number of flashcards
        difficulty: Difficulty level

    Returns:
        Formatted prompt requesting TOON output
    """
    difficulty_guidelines = {
        "easy": "Focus on basic facts, definitions, and simple concepts.",
        "medium": "Include some analysis, comparisons, and moderate complexity.",
        "hard": "Include complex concepts, critical thinking, and deep understanding.",
    }

    prompt = f"""Generate exactly {count} flashcards from the following text.

Difficulty level: {difficulty} - {difficulty_guidelines[difficulty]}

Use TOON format (more efficient than JSON):

Q: Question text here
A: Answer text here
D: {difficulty}

(separate each flashcard with a blank line)

Rules:
- Questions should be clear and specific
- Answers should be concise but complete
- Cover different aspects of the content
- Avoid yes/no questions
- Make sure all {count} flashcards are unique and valuable

Text:
{text}

TOON output:"""

    return prompt
