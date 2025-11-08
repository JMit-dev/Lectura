"""Audio transcription service using Whisper via OpenRouter"""

import logging
import tempfile
from pathlib import Path
from typing import Any, Dict

from fastapi import UploadFile
from openai import OpenAI

from src.utils.audio import get_audio_duration, validate_audio_file
from src.utils.config import settings

logger = logging.getLogger(__name__)


class Transcriber:
    """Audio transcription service using Whisper via OpenRouter"""

    def __init__(self) -> None:
        """Initialize Whisper client via OpenRouter"""
        if not settings.openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY not set in environment")

        # OpenRouter supports OpenAI's Whisper API
        self.client = OpenAI(
            base_url=settings.openrouter_base_url,
            api_key=settings.openrouter_api_key,
        )
        self.whisper_model = "whisper-1"  # OpenAI Whisper model
        logger.info("Initialized Transcriber with Whisper via OpenRouter")

    async def transcribe(self, audio_file: UploadFile, language: str = "en") -> Dict[str, Any]:
        """
        Transcribe audio file to text.

        Args:
            audio_file: Uploaded audio file
            language: Language code (default: 'en')

        Returns:
            Dict with transcript, duration, language, and tokens_used

        Raises:
            ValueError: If audio file is invalid
            Exception: If transcription fails
        """
        temp_file_path = None

        try:
            # Save uploaded file to temporary location
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=Path(audio_file.filename or "audio.mp3").suffix
            ) as temp_file:
                content = await audio_file.read()
                temp_file.write(content)
                temp_file_path = temp_file.name

            logger.info(f"Saved uploaded file to: {temp_file_path}")

            # Validate audio file
            is_valid, error_msg = validate_audio_file(temp_file_path)
            if not is_valid:
                raise ValueError(f"Invalid audio file: {error_msg}")

            # Get audio duration
            try:
                duration = get_audio_duration(temp_file_path)
            except Exception as e:
                logger.warning(f"Could not get audio duration: {str(e)}")
                duration = 0.0

            # Transcribe using Whisper
            logger.info(f"Transcribing audio file (language: {language})...")

            with open(temp_file_path, "rb") as audio:
                # Build transcription parameters
                transcribe_params: Dict[str, Any] = {
                    "model": self.whisper_model,
                    "file": audio,
                    "response_format": "json",
                }

                # Only add language if not auto-detect
                if language and language != "auto":
                    transcribe_params["language"] = language

                response = self.client.audio.transcriptions.create(**transcribe_params)

            transcript = response.text
            logger.info(
                f"Transcription complete: {len(transcript)} characters, " f"{duration:.2f} seconds"
            )

            # Estimate tokens used (Whisper pricing is per second, but we'll estimate)
            # Whisper uses ~0.006 USD per second, approximating to token count
            estimated_tokens = int(duration * 100)  # Rough estimate

            return {
                "transcript": transcript,
                "duration": duration,
                "language": language,
                "tokens_used": estimated_tokens,
            }

        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error transcribing audio: {str(e)}")
            raise Exception(f"Transcription failed: {str(e)}")

        finally:
            # Clean up temporary file
            if temp_file_path:
                try:
                    Path(temp_file_path).unlink()
                    logger.debug(f"Deleted temporary file: {temp_file_path}")
                except Exception as e:
                    logger.warning(f"Could not delete temp file: {str(e)}")

    def transcribe_file_path(self, file_path: str, language: str = "en") -> Dict[str, Any]:
        """
        Transcribe audio file from file system path.

        Args:
            file_path: Path to audio file
            language: Language code (default: 'en')

        Returns:
            Dict with transcript, duration, language, and tokens_used

        Raises:
            ValueError: If audio file is invalid
            Exception: If transcription fails
        """
        try:
            # Validate audio file
            is_valid, error_msg = validate_audio_file(file_path)
            if not is_valid:
                raise ValueError(f"Invalid audio file: {error_msg}")

            # Get audio duration
            try:
                duration = get_audio_duration(file_path)
            except Exception as e:
                logger.warning(f"Could not get audio duration: {str(e)}")
                duration = 0.0

            # Transcribe using Whisper
            logger.info(f"Transcribing audio file: {file_path} (language: {language})")

            with open(file_path, "rb") as audio:
                # Build transcription parameters
                transcribe_params: Dict[str, Any] = {
                    "model": self.whisper_model,
                    "file": audio,
                    "response_format": "json",
                }

                # Only add language if not auto-detect
                if language and language != "auto":
                    transcribe_params["language"] = language

                response = self.client.audio.transcriptions.create(**transcribe_params)

            transcript = response.text
            logger.info(
                f"Transcription complete: {len(transcript)} characters, " f"{duration:.2f} seconds"
            )

            # Estimate tokens used
            estimated_tokens = int(duration * 100)

            return {
                "transcript": transcript,
                "duration": duration,
                "language": language,
                "tokens_used": estimated_tokens,
            }

        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error transcribing audio: {str(e)}")
            raise Exception(f"Transcription failed: {str(e)}")
