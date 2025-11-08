"""Audio processing utilities"""

import logging
import os
import tempfile
from pathlib import Path
from typing import List, Optional, Tuple

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

# Supported video formats
SUPPORTED_VIDEO_FORMATS = {
    "mp4": "mp4",
    "webm": "webm",
    "avi": "avi",
    "mov": "mov",
    "mkv": "mkv",
    "flv": "flv",
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


def is_video_file(file_path: str) -> bool:
    """
    Check if file is a video file.

    Args:
        file_path: Path to file

    Returns:
        True if video file, False otherwise
    """
    file_ext = Path(file_path).suffix.lower().lstrip(".")
    return file_ext in SUPPORTED_VIDEO_FORMATS


def extract_audio_from_video(video_path: str, output_path: Optional[str] = None) -> str:
    """
    Extract audio from video file.

    Args:
        video_path: Path to video file
        output_path: Output path for audio (optional, will create temp file if not provided)

    Returns:
        Path to extracted audio file

    Raises:
        Exception: If extraction fails
    """
    if not PYDUB_AVAILABLE:
        raise Exception("pydub not available - cannot extract audio from video")

    try:
        # Validate video file exists
        if not os.path.exists(video_path):
            raise ValueError(f"Video file not found: {video_path}")

        file_ext = Path(video_path).suffix.lower().lstrip(".")
        if file_ext not in SUPPORTED_VIDEO_FORMATS:
            raise ValueError(f"Unsupported video format: {file_ext}")

        # Create output path if not provided
        if output_path is None:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            output_path = temp_file.name
            temp_file.close()

        logger.info(f"Extracting audio from video: {video_path}")

        # Load video and extract audio
        video = AudioSegment.from_file(video_path, format=SUPPORTED_VIDEO_FORMATS[file_ext])
        video.export(output_path, format="mp3")

        file_size = os.path.getsize(output_path)
        logger.info(f"Audio extracted to: {output_path} ({file_size} bytes)")

        return output_path

    except Exception as e:
        logger.error(f"Error extracting audio from video: {str(e)}")
        raise


def extract_audio_segment(
    input_path: str,
    output_path: str,
    start_seconds: float = 0,
    duration_seconds: Optional[float] = None,
) -> bool:
    """
    Extract a segment from audio/video file (useful for testing with shorter clips).

    Args:
        input_path: Input audio/video file path
        output_path: Output audio file path
        start_seconds: Start time in seconds (default: 0)
        duration_seconds: Duration in seconds (None = until end)

    Returns:
        True if extraction successful, False otherwise
    """
    if not PYDUB_AVAILABLE:
        logger.error("pydub not available, cannot extract audio segment")
        return False

    try:
        # Determine format
        file_ext = Path(input_path).suffix.lower().lstrip(".")
        if file_ext in SUPPORTED_VIDEO_FORMATS:
            format_name = SUPPORTED_VIDEO_FORMATS[file_ext]
        else:
            format_name = SUPPORTED_FORMATS.get(file_ext, file_ext)

        # Load audio
        audio = AudioSegment.from_file(input_path, format=format_name)

        # Convert to milliseconds
        start_ms = int(start_seconds * 1000)
        end_ms = int((start_seconds + duration_seconds) * 1000) if duration_seconds else len(audio)

        # Extract segment
        segment = audio[start_ms:end_ms]

        # Export
        segment.export(output_path, format="mp3")

        segment_duration = len(segment) / 1000.0
        logger.info(f"Extracted {segment_duration:.2f}s segment from {input_path} to {output_path}")

        return True

    except Exception as e:
        logger.error(f"Error extracting audio segment: {str(e)}")
        return False


def split_audio_into_chunks(
    input_path: str, max_chunk_size_mb: float = 20, output_dir: Optional[str] = None
) -> List[str]:
    """
    Split audio file into chunks that fit within size limit.

    Args:
        input_path: Input audio file path
        max_chunk_size_mb: Maximum chunk size in MB (default: 20)
        output_dir: Output directory for chunks (optional, creates temp dir if not provided)

    Returns:
        List of paths to chunk files

    Raises:
        Exception: If splitting fails
    """
    if not PYDUB_AVAILABLE:
        raise Exception("pydub not available - cannot split audio")

    try:
        # Load audio
        file_ext = Path(input_path).suffix.lower().lstrip(".")
        format_name = SUPPORTED_FORMATS.get(file_ext, file_ext)
        audio = AudioSegment.from_file(input_path, format=format_name)

        # Create output directory
        if output_dir is None:
            output_dir = tempfile.mkdtemp()
        else:
            os.makedirs(output_dir, exist_ok=True)

        # Calculate chunk duration based on file size
        total_duration_ms = len(audio)
        file_size_mb = os.path.getsize(input_path) / (1024 * 1024)

        # Estimate chunk duration to achieve target size
        chunk_duration_ms = int((max_chunk_size_mb / file_size_mb) * total_duration_ms)

        # Split into chunks
        chunks = []
        chunk_num = 0
        for start_ms in range(0, total_duration_ms, chunk_duration_ms):
            end_ms = min(start_ms + chunk_duration_ms, total_duration_ms)
            chunk = audio[start_ms:end_ms]

            # Export chunk
            chunk_path = os.path.join(
                output_dir, f"{Path(input_path).stem}_chunk_{chunk_num:03d}.mp3"
            )
            chunk.export(chunk_path, format="mp3", bitrate="48k")

            chunk_size_mb = os.path.getsize(chunk_path) / (1024 * 1024)
            logger.info(
                f"Created chunk {chunk_num}: {chunk_path} "
                f"({chunk_size_mb:.2f}MB, {len(chunk)/1000:.1f}s)"
            )

            chunks.append(chunk_path)
            chunk_num += 1

        logger.info(f"Split audio into {len(chunks)} chunks in {output_dir}")
        return chunks

    except Exception as e:
        logger.error(f"Error splitting audio into chunks: {str(e)}")
        raise


def prepare_audio_for_transcription(
    input_path: str, max_size_mb: float = 24, test_duration_seconds: Optional[float] = None
) -> Tuple[List[str], bool]:
    """
    Prepare audio/video file for transcription by handling video extraction,
    compression, and chunking as needed.

    Args:
        input_path: Input audio/video file path
        max_size_mb: Maximum size per file in MB (default: 24)
        test_duration_seconds: If set, only process first N seconds (for testing)

    Returns:
        Tuple of (list of file paths ready for transcription, is_temporary)
        is_temporary indicates if files should be cleaned up after use

    Raises:
        Exception: If preparation fails
    """
    temp_files_created = False
    files_to_transcribe = []

    try:
        working_file = input_path

        # Extract audio from video if needed
        if is_video_file(input_path):
            logger.info("Video file detected, extracting audio...")
            working_file = extract_audio_from_video(input_path)
            temp_files_created = True

        # Extract test segment if requested
        if test_duration_seconds:
            logger.info(f"Extracting {test_duration_seconds}s test segment...")
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            temp_file.close()
            if extract_audio_segment(working_file, temp_file.name, 0, test_duration_seconds):
                working_file = temp_file.name
                temp_files_created = True
            else:
                raise Exception("Failed to extract test segment")

        # Check file size
        file_size_mb = os.path.getsize(working_file) / (1024 * 1024)
        logger.info(f"Working file size: {file_size_mb:.2f}MB")

        if file_size_mb <= max_size_mb:
            # File is small enough, use as-is
            files_to_transcribe = [working_file]
        else:
            # Try compression first
            logger.info("File too large, attempting compression...")
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            temp_file.close()

            if compress_audio(working_file, temp_file.name, bitrate="48k"):
                compressed_size_mb = os.path.getsize(temp_file.name) / (1024 * 1024)
                logger.info(f"Compressed to {compressed_size_mb:.2f}MB")

                if compressed_size_mb <= max_size_mb:
                    files_to_transcribe = [temp_file.name]
                    temp_files_created = True
                else:
                    # Still too large, need to chunk
                    logger.info("Still too large after compression, splitting into chunks...")
                    chunks = split_audio_into_chunks(temp_file.name, max_chunk_size_mb=max_size_mb)
                    files_to_transcribe = chunks
                    temp_files_created = True
            else:
                # Compression failed, try chunking original
                logger.info("Compression failed, splitting into chunks...")
                chunks = split_audio_into_chunks(working_file, max_chunk_size_mb=max_size_mb)
                files_to_transcribe = chunks
                temp_files_created = True

        logger.info(
            f"Prepared {len(files_to_transcribe)} file(s) for transcription "
            f"(temporary: {temp_files_created})"
        )
        return files_to_transcribe, temp_files_created

    except Exception as e:
        logger.error(f"Error preparing audio for transcription: {str(e)}")
        raise
