#!/usr/bin/env python3
"""Test script to see what audio processing outputs"""

import os
import sys

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from src.utils.audio import get_audio_duration, validate_audio_file  # noqa: E402

print("Looking for test file in data/...")
data_dir = os.path.join(os.path.dirname(__file__), "..", "data")

# Find first audio file
test_file = None
for filename in os.listdir(data_dir):
    if filename.endswith((".mp3", ".wav", ".m4a", ".flac")):
        test_file = os.path.join(data_dir, filename)
        break

if not test_file:
    print("ERROR: No audio files found in data/")
    sys.exit(1)

print(f"Found test file: {test_file}")

print("\n" + "=" * 80)
print("VALIDATING AUDIO - WATCH FOR ANY OUTPUT:")
print("=" * 80 + "\n")

is_valid, error_msg = validate_audio_file(test_file)
print(f"Valid: {is_valid}, Error: {error_msg}")

print("\n" + "=" * 80)
print("GETTING AUDIO DURATION - WATCH FOR ANY OUTPUT:")
print("=" * 80 + "\n")

duration = get_audio_duration(test_file)
print(f"Duration: {duration:.2f} seconds")

print("\n" + "=" * 80)
print("COMPLETE")
print("=" * 80)
