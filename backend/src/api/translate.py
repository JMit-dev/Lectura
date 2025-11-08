"""Translation API endpoint"""

import logging

from fastapi import APIRouter, HTTPException

from src.models.schemas import TranslateRequest, TranslateResponse
from src.services.translator import Translator

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/translate", response_model=TranslateResponse)
async def translate_text(request: TranslateRequest) -> TranslateResponse:
    """
    Translate text to multiple languages.

    Args:
        request: Translation request with text and target languages

    Returns:
        TranslateResponse with translations for each language

    Raises:
        HTTPException: If translation fails
    """
    try:
        translator = Translator()
        result = translator.translate(text=request.text, target_languages=request.target_languages)

        return TranslateResponse(translations=result["translations"])

    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")
