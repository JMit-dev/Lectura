"""Transcription API endpoint"""

import logging

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from src.models.schemas import TranscribeResponse
from src.services.transcriber import Transcriber
from src.utils.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/transcribe", response_model=TranscribeResponse)
async def transcribe_audio(
    file: UploadFile = File(..., description="Audio file to transcribe"),
    language: str = Form("en", description="Language code (e.g., 'en', 'es', 'fr')"),
) -> TranscribeResponse:
    """
    Transcribe audio file to text using Whisper.

    **Supported formats:** mp3, wav, m4a, ogg, flac, aac, wma

    **Max file size:** 25MB

    **Languages:** en, es, fr, de, it, pt, nl, pl, ru, zh, ja, ko, and more

    Args:
        file: Audio file to transcribe
        language: Language code (default: 'en', use 'auto' for auto-detection)

    Returns:
        TranscribeResponse with transcript, duration, language, and tokens_used

    Raises:
        HTTPException: If transcription fails
    """
    try:
        # Validate file size
        if file.size and file.size > settings.max_file_size:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Max size: {settings.max_file_size} bytes",
            )

        # Validate file type
        if file.content_type and not file.content_type.startswith("audio/"):
            raise HTTPException(status_code=400, detail=f"Invalid file type: {file.content_type}")

        logger.info(
            f"Transcribing audio file: {file.filename} "
            f"(size: {file.size}, language: {language})"
        )

        # Initialize transcriber and transcribe
        transcriber = Transcriber()
        result = await transcriber.transcribe(file, language=language)

        logger.info(f"Transcription successful: {len(result['transcript'])} characters")

        return TranscribeResponse(
            transcript=result["transcript"],
            duration=result["duration"],
            language=result["language"],
            tokens_used=result["tokens_used"],
        )

    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Transcription error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
