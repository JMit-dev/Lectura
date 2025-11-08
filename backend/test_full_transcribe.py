#!/usr/bin/env python3
"""Test full transcription to find the output source"""

import os
import sys

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

os.environ["TQDM_DISABLE"] = "1"

import logging  # noqa: E402

# Disable all genai logging
logging.getLogger("google.generativeai").setLevel(logging.CRITICAL)
logging.getLogger("google.ai.generativelanguage").setLevel(logging.CRITICAL)

from src.services.transcriber import Transcriber  # noqa: E402

print("Looking for test file in data/...")
data_dir = os.path.join(os.path.dirname(__file__), "..", "data")

# Find first audio file
test_file = None
for filename in os.listdir(data_dir):
    if filename.endswith((".mp3", ".wav", ".m4a")):
        test_file = os.path.join(data_dir, filename)
        break

if not test_file:
    print("ERROR: No audio files found in data/")
    sys.exit(1)

print(f"Found test file: {test_file}")

print("\n" + "=" * 80)
print("FULL TRANSCRIPTION - WATCH FOR ANY OUTPUT:")
print("=" * 80 + "\n")

transcriber = Transcriber()
result = transcriber.transcribe_file_path(test_file, language="en")

print("\n" + "=" * 80)
print("TRANSCRIPTION COMPLETE")
print("=" * 80)
print(f"Transcript length: {len(result['transcript'])} characters")
print(f"Duration: {result['duration']:.2f} seconds")
print(f"Tokens used: {result['tokens_used']}")
print(f"\nFirst 200 chars: {result['transcript'][:200]}...")
