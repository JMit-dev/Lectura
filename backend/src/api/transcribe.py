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
    file: UploadFile = File(..., description="Audio, video, or text file to process"),
    language: str = Form("en", description="Language code (e.g., 'en', 'es', 'fr')"),
) -> TranscribeResponse:
    """
    Process audio, video, or text file to extract text transcript.

    **Supported formats:**
    - Audio: mp3, wav, m4a, ogg, flac, aac
    - Video: mp4, webm, mov, avi, mkv
    - Text: txt, pdf

    **Max file size:** 200MB

    **Languages:** en, es, fr, de, it, pt, nl, pl, ru, zh, ja, ko, and more

    Args:
        file: Audio, video, or text file to process
        language: Language code (default: 'en', use 'auto' for auto-detection)

    Returns:
        TranscribeResponse with transcript, duration, language, and tokens_used

    Raises:
        HTTPException: If processing fails
    """
    try:
        # Validate file size
        if file.size and file.size > settings.max_file_size:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Max size: {settings.max_file_size} bytes",
            )

        # Validate file type (accept audio, video, and text)
        if file.content_type and not (
            file.content_type.startswith("audio/")
            or file.content_type.startswith("video/")
            or file.content_type.startswith("text/")
            or file.content_type == "application/pdf"
        ):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type: {file.content_type}. "
                "Must be audio, video, or text file.",
            )

        logger.info(
            f"Processing file: {file.filename} "
            f"(type: {file.content_type}, size: {file.size}, language: {language})"
        )

        # Handle text files directly
        if file.content_type and (
            file.content_type.startswith("text/") or file.content_type == "application/pdf"
        ):
            content = await file.read()
            if file.content_type == "application/pdf":
                # For PDF, try to extract text
                try:
                    from io import BytesIO

                    import PyPDF2

                    pdf_reader = PyPDF2.PdfReader(BytesIO(content))
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text()
                    transcript = text.strip()
                except Exception as e:
                    logger.warning(f"PDF extraction failed, using raw content: {e}")
                    transcript = content.decode("utf-8", errors="ignore")
            else:
                # Plain text file
                transcript = content.decode("utf-8", errors="ignore")

            result = {
                "transcript": transcript,
                "duration": 0.0,
                "language": language,
                "tokens_used": 0,
            }
        else:
            # Initialize transcriber and transcribe audio/video
            transcriber = Transcriber()
            result = await transcriber.transcribe(file, language=language)

        logger.info(f"Processing successful: {len(result['transcript'])} characters")

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
