#!/usr/bin/env python3
"""
Test script for transcribing audio/video files with chunking support.

Usage:
    python test_transcription.py [--test-duration SECONDS]

Examples:
    # Test with 10 minutes (600 seconds) of a video
    python test_transcription.py --test-duration 600

    # Transcribe full file
    python test_transcription.py
"""

import argparse
import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.transcriber import Transcriber  # noqa: E402

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def test_transcription(file_path: str, test_duration_seconds: float = None, language: str = "en"):
    """
    Test transcription of audio/video file.

    Args:
        file_path: Path to audio/video file
        test_duration_seconds: If set, only process first N seconds
        language: Language code
    """
    logger.info("=" * 80)
    logger.info(f"Testing transcription: {file_path}")
    logger.info(
        f"Test duration: {test_duration_seconds}s" if test_duration_seconds else "Full file"
    )
    logger.info("=" * 80)

    try:
        # Initialize transcriber
        transcriber = Transcriber()

        # Transcribe with chunking
        result = transcriber.transcribe_with_chunking(
            file_path=file_path, language=language, test_duration_seconds=test_duration_seconds
        )

        # Display results
        logger.info("\n" + "=" * 80)
        logger.info("TRANSCRIPTION RESULTS")
        logger.info("=" * 80)
        logger.info(
            f"Duration: {result['duration']:.2f} seconds ({result['duration']/60:.2f} minutes)"
        )
        logger.info(f"Language: {result['language']}")
        logger.info(f"Tokens used: {result['tokens_used']}")
        logger.info(f"Chunks processed: {result.get('chunks_processed', 1)}")
        logger.info(f"Transcript length: {len(result['transcript'])} characters")
        logger.info("\n--- TRANSCRIPT ---")
        logger.info(
            result["transcript"][:500] + "..."
            if len(result["transcript"]) > 500
            else result["transcript"]
        )
        logger.info("=" * 80)

        return result

    except Exception as e:
        logger.error(f"Transcription failed: {str(e)}", exc_info=True)
        return None


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Test transcription with audio/video files",
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
    parser.add_argument("--language", type=str, default="en", help="Language code (default: en)")
    parser.add_argument("--all", action="store_true", help="Test all files in data folder")

    args = parser.parse_args()

    # Find data directory
    data_dir = Path(__file__).parent.parent / "data"

    if args.file:
        # Test single file
        test_transcription(args.file, args.test_duration, args.language)

    elif args.all:
        # Test all files in data folder
        if not data_dir.exists():
            logger.error(f"Data directory not found: {data_dir}")
            return

        # Find all audio/video files
        audio_exts = [".mp3", ".wav", ".m4a", ".ogg", ".flac", ".aac"]
        video_exts = [".mp4", ".webm", ".avi", ".mov", ".mkv", ".flv"]
        all_exts = audio_exts + video_exts

        files = []
        for ext in all_exts:
            files.extend(data_dir.glob(f"*{ext}"))

        if not files:
            logger.error(f"No audio/video files found in {data_dir}")
            return

        logger.info(f"Found {len(files)} files to test")

        for file_path in files:
            test_transcription(str(file_path), args.test_duration, args.language)
            print("\n")

    else:
        # Test one MP3 file from data folder as default
        if not data_dir.exists():
            logger.error(f"Data directory not found: {data_dir}")
            logger.info("Please specify a file with --file or use --all to test all files")
            return

        # Find first mp3 file
        mp3_files = list(data_dir.glob("*.mp3"))
        if not mp3_files:
            logger.error(f"No MP3 files found in {data_dir}")
            return

        test_file = mp3_files[0]
        logger.info(f"Testing with first MP3 file found: {test_file}")
        test_transcription(str(test_file), args.test_duration, args.language)


if __name__ == "__main__":
    main()
