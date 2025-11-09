#!/usr/bin/env python3
"""Test script to see what genai.upload_file() outputs"""

import os
import sys

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

# Set environment variables
os.environ["TQDM_DISABLE"] = "1"

import logging  # noqa: E402

import google.generativeai as genai  # noqa: E402

from src.utils.config import settings  # noqa: E402

# Disable logging
logging.getLogger("google.generativeai").setLevel(logging.CRITICAL)
logging.getLogger("google.ai.generativelanguage").setLevel(logging.CRITICAL)

print("Configuring Gemini...")
genai.configure(api_key=settings.gemini_api_key)

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
file_size = os.path.getsize(test_file) / (1024 * 1024)
print(f"File size: {file_size:.2f} MB")

print("\n" + "=" * 80)
print("UPLOADING FILE - WATCH FOR ANY OUTPUT:")
print("=" * 80 + "\n")

# This is where the output happens
uploaded_file = genai.upload_file(test_file)

print("\n" + "=" * 80)
print("UPLOAD COMPLETE")
print("=" * 80)
print(f"Uploaded file name: {uploaded_file.name}")
print(f"Uploaded file URI: {uploaded_file.uri}")
