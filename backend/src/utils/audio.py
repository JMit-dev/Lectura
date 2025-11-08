"""Audio processing utilities"""

import logging
import os
from pathlib import Path
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

# Try to import pydub, but make it optional
try:
    from pydub import AudioSegment  # type: ignore[import-untyped]

    PYDUB_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    PYDUB_AVAILABLE = False
    logger.warning("pydub not available - some audio features will be limited")

# Supported audio formats
SUPPORTED_FORMATS = {
    "mp3": "mp3",
    "wav": "wav",
    "m4a": "mp4",  # pydub uses 'mp4' for m4a files
    "ogg": "ogg",
    "flac": "flac",
    "aac": "aac",
    "wma": "wma",
}


def validate_audio_file(file_path: str) -> Tuple[bool, Optional[str]]:
    """
    Validate audio file format and size.

    Args:
        file_path: Path to audio file

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            return False, f"File not found: {file_path}"

        # Check file extension
        file_ext = Path(file_path).suffix.lower().lstrip(".")
        if file_ext not in SUPPORTED_FORMATS:
            return (
                False,
                f"Unsupported format: {file_ext}. "
                f"Supported: {', '.join(SUPPORTED_FORMATS.keys())}",
            )

        # Check file size (max 25MB for Whisper API)
        file_size = os.path.getsize(file_path)
        max_size = 25 * 1024 * 1024  # 25MB in bytes
        if file_size > max_size:
            return False, f"File too large: {file_size} bytes (max: {max_size})"

        logger.info(f"Audio file validated: {file_path} ({file_size} bytes)")
        return True, None

    except Exception as e:
        logger.error(f"Error validating audio file: {str(e)}")
        return False, str(e)


def get_audio_duration(file_path: str) -> float:
    """
    Get duration of audio file in seconds.

    Args:
        file_path: Path to audio file

    Returns:
        Duration in seconds (0.0 if pydub not available)

    Raises:
        Exception: If unable to read audio file
    """
    if not PYDUB_AVAILABLE:
        logger.warning("pydub not available, returning 0.0 for duration")
        return 0.0

    try:
        file_ext = Path(file_path).suffix.lower().lstrip(".")
        format_name = SUPPORTED_FORMATS.get(file_ext, file_ext)

        audio = AudioSegment.from_file(file_path, format=format_name)
        duration = len(audio) / 1000.0  # Convert milliseconds to seconds

        logger.info(f"Audio duration: {duration:.2f} seconds")
        return duration

    except Exception as e:
        logger.error(f"Error getting audio duration: {str(e)}")
        raise


def convert_audio_format(input_path: str, output_path: str, target_format: str = "mp3") -> bool:
    """
    Convert audio file to different format.

    Args:
        input_path: Input audio file path
        output_path: Output audio file path
        target_format: Target format (default: 'mp3')

    Returns:
        True if conversion successful, False otherwise
    """
    if not PYDUB_AVAILABLE:
        logger.error("pydub not available, cannot convert audio format")
        return False

    try:
        file_ext = Path(input_path).suffix.lower().lstrip(".")
        format_name = SUPPORTED_FORMATS.get(file_ext, file_ext)

        audio = AudioSegment.from_file(input_path, format=format_name)
        audio.export(output_path, format=target_format)

        logger.info(f"Converted {input_path} to {output_path} ({target_format})")
        return True

    except Exception as e:
        logger.error(f"Error converting audio format: {str(e)}")
        return False


def compress_audio(input_path: str, output_path: str, bitrate: str = "64k") -> bool:
    """
    Compress audio file to reduce size.

    Args:
        input_path: Input audio file path
        output_path: Output audio file path
        bitrate: Target bitrate (default: '64k')

    Returns:
        True if compression successful, False otherwise
    """
    if not PYDUB_AVAILABLE:
        logger.error("pydub not available, cannot compress audio")
        return False

    try:
        file_ext = Path(input_path).suffix.lower().lstrip(".")
        format_name = SUPPORTED_FORMATS.get(file_ext, file_ext)

        audio = AudioSegment.from_file(input_path, format=format_name)

        # Export with lower bitrate for compression
        audio.export(output_path, format="mp3", bitrate=bitrate)

        original_size = os.path.getsize(input_path)
        compressed_size = os.path.getsize(output_path)
        savings = ((original_size - compressed_size) / original_size) * 100

        logger.info(
            f"Compressed audio: {original_size} -> {compressed_size} bytes "
            f"({savings:.1f}% reduction)"
        )
        return True

    except Exception as e:
        logger.error(f"Error compressing audio: {str(e)}")
        return False
