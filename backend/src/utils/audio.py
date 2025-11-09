"""Audio-only processing utilities."""

import contextlib
import logging
import os
import wave
from pathlib import Path
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

try:
    from pydub import AudioSegment  # type: ignore[import-untyped]

    PYDUB_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    PYDUB_AVAILABLE = False
    logger.warning("pydub not available - some audio features will be limited")

try:
    from mutagen import File as MutagenFile  # type: ignore[import-untyped]
    from mutagen.flac import FLAC  # type: ignore[import-untyped]
    from mutagen.mp3 import MP3  # type: ignore[import-untyped]
    from mutagen.mp4 import MP4  # type: ignore[import-untyped]

    MUTAGEN_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    MUTAGEN_AVAILABLE = False
    MutagenFile = None  # type: ignore[assignment]
    logger.warning("mutagen not available - some duration features will be limited")

# Audio formats we explicitly allow
SUPPORTED_FORMATS = {
    "mp3": "mp3",
    "wav": "wav",
    "m4a": "mp4",
    "ogg": "ogg",
    "flac": "flac",
    "aac": "aac",
    "wma": "wma",
}


def validate_audio_file(file_path: str) -> Tuple[bool, Optional[str]]:
    """
    Validate that the given file exists and is one of our supported audio formats.
    """
    try:
        if not os.path.exists(file_path):
            return False, f"File not found: {file_path}"

        file_ext = Path(file_path).suffix.lower().lstrip(".")
        if file_ext not in SUPPORTED_FORMATS:
            return (
                False,
                f"Unsupported format: {file_ext}. "
                f"Supported: {', '.join(sorted(SUPPORTED_FORMATS.keys()))}",
            )

        logger.info("Audio file validated: %s (%s)", file_path, file_ext)
        return True, None
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.error("Error validating audio file: %s", exc)
        return False, str(exc)


def _duration_from_pydub(file_path: str, file_ext: str) -> Optional[float]:
    if not PYDUB_AVAILABLE:
        return None
    try:
        format_name = SUPPORTED_FORMATS.get(file_ext, file_ext)
        audio = AudioSegment.from_file(file_path, format=format_name)
        return len(audio) / 1000.0
    except Exception as exc:  # pragma: no cover - best-effort fallback
        logger.warning("pydub failed to read duration: %s", exc)
        return None


def _duration_from_mutagen(file_path: str, file_ext: str) -> Optional[float]:
    if not MUTAGEN_AVAILABLE or MutagenFile is None:
        return None
    try:
        if file_ext == "mp3":
            return float(MP3(file_path).info.length)  # type: ignore[arg-type,attr-defined]
        if file_ext in {"m4a", "mp4", "m4b"}:
            return float(MP4(file_path).info.length)  # type: ignore[arg-type,attr-defined]
        if file_ext == "flac":
            return float(FLAC(file_path).info.length)  # type: ignore[arg-type,attr-defined]

        metadata = MutagenFile(file_path)
        if metadata and metadata.info and metadata.info.length:
            return float(metadata.info.length)
    except Exception as exc:  # pragma: no cover - best-effort fallback
        logger.warning("mutagen failed to read duration: %s", exc)
    return None


def _duration_from_wave(file_path: str, file_ext: str) -> Optional[float]:
    if file_ext not in {"wav", "wave"}:
        return None
    try:
        with contextlib.closing(wave.open(file_path, "rb")) as wav_file:
            frames = wav_file.getnframes()
            rate = wav_file.getframerate() or 1
            return frames / float(rate)
    except Exception as exc:  # pragma: no cover - best-effort fallback
        logger.warning("wave module failed to read duration: %s", exc)
        return None


def get_audio_duration(file_path: str) -> float:
    """
    Attempt to determine the duration of an audio file using pure-Python libraries only.
    Returns 0.0 if every strategy fails.
    """
    file_ext = Path(file_path).suffix.lower().lstrip(".")

    for strategy in (
        _duration_from_pydub,
        _duration_from_mutagen,
        _duration_from_wave,
    ):
        duration = strategy(file_path, file_ext)
        if duration and duration > 0:
            logger.info("Audio duration resolved via %s: %.2fs", strategy.__name__, duration)
            return float(duration)

    logger.warning("Unable to determine audio duration, defaulting to 0.0 seconds")
    return 0.0
