"""Audio transcription service using Google Gemini"""

import logging
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional

import google.generativeai as genai
from fastapi import UploadFile

from src.utils.audio import get_audio_duration, prepare_audio_for_transcription, validate_audio_file
from src.utils.config import settings

logger = logging.getLogger(__name__)


class Transcriber:
    """Audio transcription service using Google Gemini"""

    def __init__(self) -> None:
        """Initialize Gemini client"""
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not set in environment")

        # Configure Gemini API
        genai.configure(api_key=settings.gemini_api_key)
        # Use gemini-2.5-flash which supports audio
        self.model = genai.GenerativeModel("gemini-2.5-flash")
        logger.info("Initialized Transcriber with Google Gemini (gemini-2.5-flash)")

    async def transcribe(self, audio_file: UploadFile, language: str = "en") -> Dict[str, Any]:
        """
        Transcribe audio file to text using Gemini.

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

            # Transcribe using Gemini
            logger.info(f"Transcribing audio file with Gemini (language: {language})...")

            # Upload file to Gemini
            audio_file_gemini = genai.upload_file(temp_file_path)

            # Create prompt for transcription
            prompt = (
                "Please transcribe this audio file. Provide only the transcript text, nothing else."
            )
            if language and language != "auto" and language != "en":
                prompt = (
                    f"Please transcribe this audio file in {language}. "
                    "Provide only the transcript text, nothing else."
                )

            # Generate transcription
            response = self.model.generate_content([prompt, audio_file_gemini])
            transcript = response.text

            logger.info(
                f"Transcription complete: {len(transcript)} characters, {duration:.2f} seconds"
            )

            # Estimate tokens used
            estimated_tokens = int(duration * 100)

            # Clean up uploaded file from Gemini
            try:
                genai.delete_file(audio_file_gemini.name)
            except Exception as e:
                logger.warning(f"Could not delete Gemini file: {str(e)}")

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
        Transcribe audio file from file system path using Gemini.

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

            # Transcribe using Gemini
            logger.info(f"Transcribing audio file with Gemini: {file_path} (language: {language})")

            # Upload file to Gemini
            audio_file_gemini = genai.upload_file(file_path)

            # Create prompt for transcription
            prompt = (
                "Please transcribe this audio file. Provide only the transcript text, nothing else."
            )
            if language and language != "auto" and language != "en":
                prompt = (
                    f"Please transcribe this audio file in {language}. "
                    "Provide only the transcript text, nothing else."
                )

            # Generate transcription
            response = self.model.generate_content([prompt, audio_file_gemini])
            transcript = response.text

            logger.info(
                f"Transcription complete: {len(transcript)} characters, {duration:.2f} seconds"
            )

            # Estimate tokens used
            estimated_tokens = int(duration * 100)

            # Clean up uploaded file from Gemini
            try:
                genai.delete_file(audio_file_gemini.name)
            except Exception as e:
                logger.warning(f"Could not delete Gemini file: {str(e)}")

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

    def transcribe_with_chunking(
        self, file_path: str, language: str = "en", test_duration_seconds: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Transcribe audio/video file with automatic chunking for large files.
        Supports video files by extracting audio first.

        Args:
            file_path: Path to audio/video file
            language: Language code (default: 'en')
            test_duration_seconds: If set, only transcribe first N seconds (for testing)

        Returns:
            Dict with transcript, duration, language, tokens_used, and chunks_processed

        Raises:
            Exception: If transcription fails
        """
        import os

        temp_files_to_cleanup = []

        try:
            # Prepare file(s) for transcription (handles video, compression, chunking)
            logger.info(f"Preparing file for transcription: {file_path}")
            files_to_transcribe, is_temporary = prepare_audio_for_transcription(
                file_path, max_size_mb=24, test_duration_seconds=test_duration_seconds
            )

            if is_temporary:
                temp_files_to_cleanup = files_to_transcribe

            # Transcribe each chunk
            all_transcripts = []
            total_duration = 0.0
            total_tokens = 0

            for i, chunk_file in enumerate(files_to_transcribe):
                logger.info(f"Transcribing chunk {i+1}/{len(files_to_transcribe)}: {chunk_file}")

                # Get duration
                try:
                    duration = get_audio_duration(chunk_file)
                    total_duration += duration
                except Exception as e:
                    logger.warning(f"Could not get duration for chunk {i}: {str(e)}")
                    duration = 0.0

                # Transcribe chunk with Gemini
                audio_file_gemini = genai.upload_file(chunk_file)

                # Create prompt for transcription
                prompt = "Please transcribe this audio file. Provide only the transcript text, nothing else."  # noqa: E501
                if language and language != "auto" and language != "en":
                    prompt = (
                        f"Please transcribe this audio file in {language}. "
                        "Provide only the transcript text, nothing else."
                    )

                response = self.model.generate_content([prompt, audio_file_gemini])
                transcript = response.text
                all_transcripts.append(transcript)

                # Clean up uploaded file from Gemini
                try:
                    genai.delete_file(audio_file_gemini.name)
                except Exception as e:
                    logger.warning(f"Could not delete Gemini file: {str(e)}")

                # Estimate tokens
                chunk_tokens = int(duration * 100)
                total_tokens += chunk_tokens

                logger.info(f"Chunk {i+1} complete: {len(transcript)} characters, {duration:.2f}s")

            # Combine all transcripts
            combined_transcript = " ".join(all_transcripts)

            logger.info(
                f"Transcription complete: {len(combined_transcript)} characters total, "
                f"{total_duration:.2f}s, {len(files_to_transcribe)} chunk(s)"
            )

            return {
                "transcript": combined_transcript,
                "duration": total_duration,
                "language": language,
                "tokens_used": total_tokens,
                "chunks_processed": len(files_to_transcribe),
            }

        except Exception as e:
            logger.error(f"Error in chunked transcription: {str(e)}")
            raise Exception(f"Transcription failed: {str(e)}")

        finally:
            # Clean up temporary files
            for temp_file in temp_files_to_cleanup:
                try:
                    if os.path.exists(temp_file):
                        os.unlink(temp_file)
                        logger.debug(f"Deleted temporary file: {temp_file}")
                except Exception as e:
                    logger.warning(f"Could not delete temp file {temp_file}: {str(e)}")
