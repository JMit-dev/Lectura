"""Flashcards API endpoint"""

import logging

from fastapi import APIRouter, HTTPException

from src.models.schemas import FlashcardRequest, FlashcardResponse
from src.services.flashcards import FlashcardGenerator

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/flashcards", response_model=FlashcardResponse)
async def generate_flashcards(request: FlashcardRequest) -> FlashcardResponse:
    """
    Generate study flashcards from text using Gemini AI.

    **Difficulty levels:**
    - `easy`: Basic facts, definitions, simple concepts
    - `medium`: Analysis, comparisons, moderate complexity
    - `hard`: Complex concepts, critical thinking, deep understanding

    **Count:** 1-50 flashcards

    Args:
        request: FlashcardRequest with text, count, and difficulty

    Returns:
        FlashcardResponse with list of flashcards and token savings info

    Raises:
        HTTPException: If flashcard generation fails
    """
    try:
        logger.info(
            f"Generating flashcards: {len(request.text)} characters, "
            f"count={request.count}, difficulty={request.difficulty}"
        )

        # Initialize generator and generate flashcards
        generator = FlashcardGenerator()
        result = generator.generate_flashcards(
            text=request.text, count=request.count, difficulty=request.difficulty
        )

        logger.info(f"Generated {len(result['flashcards'])} flashcards successfully")

        return FlashcardResponse(
            flashcards=result["flashcards"], tokens_saved=result.get("tokens_saved")
        )

    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Flashcard generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Flashcard generation failed: {str(e)}")
