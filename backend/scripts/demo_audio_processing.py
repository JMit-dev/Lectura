#!/usr/bin/env python3
"""
Demo script for audio/video processing (without API calls).

Tests:
- Video to audio extraction
- Audio segmentation (for testing with N minutes)
- Audio chunking for large files
- Compression

Usage:
    python scripts/demo_audio_processing.py --test-duration 600
"""

import argparse
import logging
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.audio import (  # noqa: F401, E402
    extract_audio_from_video,
    extract_audio_segment,
    get_audio_duration,
    is_video_file,
    prepare_audio_for_transcription,
    split_audio_into_chunks,
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def test_audio_processing(file_path: str, test_duration_seconds: float = None):
    """
    Test audio/video processing without making API calls.

    Args:
        file_path: Path to audio/video file
        test_duration_seconds: If set, only process first N seconds
    """
    logger.info("=" * 80)
    logger.info(f"Testing audio processing: {file_path}")
    logger.info(
        f"Test duration: {test_duration_seconds}s" if test_duration_seconds else "Full file"
    )
    logger.info("=" * 80)

    try:
        # Check if it's a video file
        is_video = is_video_file(file_path)
        logger.info(f"File type: {'VIDEO' if is_video else 'AUDIO'}")

        # Get original duration
        if not is_video:
            try:
                duration = get_audio_duration(file_path)
                logger.info(f"Original duration: {duration:.2f}s ({duration/60:.2f} minutes)")
            except Exception as e:
                logger.warning(f"Could not get duration: {e}")

        # Test prepare_audio_for_transcription
        logger.info("\n--- Testing prepare_audio_for_transcription ---")
        files, is_temp = prepare_audio_for_transcription(
            file_path, max_size_mb=24, test_duration_seconds=test_duration_seconds
        )

        logger.info(f"Prepared {len(files)} file(s) for processing:")
        for i, f in enumerate(files):
            size_mb = Path(f).stat().st_size / (1024 * 1024)
            try:
                dur = get_audio_duration(f)
                logger.info(f"  File {i+1}: {size_mb:.2f}MB, {dur:.2f}s ({dur/60:.2f} min)")
            except Exception as e:
                logger.info(f"  File {i+1}: {size_mb:.2f}MB (duration unknown: {e})")

        logger.info(f"Temporary files: {is_temp}")

        if test_duration_seconds:
            logger.info(f"\n✅ Successfully extracted {test_duration_seconds}s segment!")
        else:
            logger.info("\n✅ Successfully prepared full file!")

        # Cleanup temp files
        if is_temp:
            import os

            for f in files:
                try:
                    os.unlink(f)
                    logger.debug(f"Cleaned up: {f}")
                except Exception:
                    pass

        return True

    except Exception as e:
        logger.error(f"Processing failed: {str(e)}", exc_info=True)
        return False


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Test audio/video processing without API calls",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Path to audio/video file (if not provided, will test with data folder files)",
    )
    parser.add_argument(
        "--test-duration",
        type=float,
        help="Only process first N seconds (for testing). Example: 600 for 10 minutes",
    )
    parser.add_argument("--all", action="store_true", help="Test all files in data folder")

    args = parser.parse_args()

    # Find data directory
    data_dir = Path(__file__).parent.parent / "data"

    if args.file:
        # Test single file
        result = test_audio_processing(args.file, args.test_duration)
        sys.exit(0 if result else 1)

    elif args.all:
        # Test all files in data folder
        if not data_dir.exists():
            logger.error(f"Data directory not found: {data_dir}")
            sys.exit(1)

        # Find all audio/video files
        audio_exts = [".mp3", ".wav", ".m4a", ".ogg", ".flac", ".aac"]
        video_exts = [".mp4", ".webm", ".avi", ".mov", ".mkv", ".flv"]
        all_exts = audio_exts + video_exts

        files = []
        for ext in all_exts:
            files.extend(data_dir.glob(f"*{ext}"))

        if not files:
            logger.error(f"No audio/video files found in {data_dir}")
            sys.exit(1)

        logger.info(f"Found {len(files)} files to test\n")

        all_passed = True
        for file_path in files:
            result = test_audio_processing(str(file_path), args.test_duration)
            all_passed = all_passed and result
            print("\n")

        sys.exit(0 if all_passed else 1)

    else:
        # Test one file from data folder as default
        if not data_dir.exists():
            logger.error(f"Data directory not found: {data_dir}")
            logger.info("Please specify a file with --file or use --all to test all files")
            sys.exit(1)

        # Find first mp3 or mp4 file
        test_file = None
        for ext in [".mp3", ".mp4"]:
            files = list(data_dir.glob(f"*{ext}"))
            if files:
                test_file = files[0]
                break

        if not test_file:
            logger.error(f"No MP3 or MP4 files found in {data_dir}")
            sys.exit(1)

        logger.info(f"Testing with file: {test_file}\n")
        result = test_audio_processing(str(test_file), args.test_duration)
        sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
