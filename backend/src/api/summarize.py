"""Summarization API endpoint"""

import logging

from fastapi import APIRouter, HTTPException

from src.models.schemas import SummarizeRequest, SummarizeResponse
from src.services.summarizer import Summarizer

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/summarize", response_model=SummarizeResponse)
async def summarize_text(request: SummarizeRequest) -> SummarizeResponse:
    """
    Summarize text using Gemini AI.

    **Formats:**
    - `bullet_points`: Returns summary as bullet points
    - `paragraph`: Returns summary as a flowing paragraph

    **Max length:** Defaults to 500 words

    Args:
        request: SummarizeRequest with text and format

    Returns:
        SummarizeResponse with summary, original_length, and summary_length

    Raises:
        HTTPException: If summarization fails
    """
    try:
        logger.info(f"Summarizing text: {len(request.text)} characters, format: {request.format}")

        # Initialize summarizer and summarize
        summarizer = Summarizer()
        result = summarizer.summarize(text=request.text, format=request.format)

        logger.info(
            f"Summarization successful: {result['original_length']} -> "
            f"{result['summary_length']} words"
        )

        return SummarizeResponse(
            summary=result["summary"],
            original_length=result["original_length"],
            summary_length=result["summary_length"],
        )

    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Summarization error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Summarization failed: {str(e)}")
