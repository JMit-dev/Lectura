"""Translation service using Gemini"""

import logging
from typing import Any, Dict, List

import google.generativeai as genai

from src.utils.config import settings

logger = logging.getLogger(__name__)


class Translator:
    """Translation service using Gemini"""

    def __init__(self) -> None:
        """Initialize translator with direct Gemini API"""
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not set in environment")

        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash-exp")
        logger.info("Initialized Translator with direct Gemini API")

    def translate(self, text: str, target_languages: List[str]) -> Dict[str, Any]:
        """
        Translate text to multiple languages using Gemini.

        Args:
            text: Text to translate
            target_languages: List of language codes to translate to

        Returns:
            Dict with 'translations' mapping language codes to translated text

        Raises:
            ValueError: If text is empty or target_languages is invalid
            Exception: If translation fails
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        if not target_languages:
            raise ValueError("At least one target language is required")

        if len(target_languages) > 20:
            raise ValueError("Maximum 20 target languages allowed")

        try:
            logger.info(
                f"Translating text ({len(text)} chars) to "
                f"{len(target_languages)} languages: {target_languages}"
            )

            translations = {}

            # Language code to full name mapping for better results
            language_names = {
                "en": "English",
                "es": "Spanish",
                "fr": "French",
                "de": "German",
                "pt": "Portuguese",
                "it": "Italian",
                "ja": "Japanese",
                "ko": "Korean",
                "zh": "Chinese (Simplified)",
                "zh-TW": "Chinese (Traditional)",
                "ar": "Arabic",
                "hi": "Hindi",
                "bn": "Bengali",
                "bg": "Bulgarian",
                "hr": "Croatian",
                "cs": "Czech",
                "da": "Danish",
                "nl": "Dutch",
                "et": "Estonian",
                "fa": "Farsi",
                "fi": "Finnish",
                "el": "Greek",
                "gu": "Gujarati",
                "he": "Hebrew",
                "hu": "Hungarian",
                "id": "Indonesian",
                "kn": "Kannada",
                "lv": "Latvian",
                "lt": "Lithuanian",
                "ml": "Malayalam",
                "mr": "Marathi",
                "no": "Norwegian",
                "pl": "Polish",
                "ro": "Romanian",
                "ru": "Russian",
                "sr": "Serbian",
                "sk": "Slovak",
                "sl": "Slovenian",
                "sw": "Swahili",
                "sv": "Swedish",
                "ta": "Tamil",
                "te": "Telugu",
                "th": "Thai",
                "tr": "Turkish",
                "uk": "Ukrainian",
                "ur": "Urdu",
                "vi": "Vietnamese",
            }

            # Translate to each language
            for lang_code in target_languages:
                # Skip English if it's in the list
                if lang_code == "en":
                    continue

                lang_name = language_names.get(lang_code, lang_code.upper())

                system_prompt = (
                    "You are a professional translator. "
                    "Translate the text accurately while preserving "
                    "the meaning, tone, and formatting."
                )

                preserve_marker_instruction = ""
                if "[[" in text and "]]" in text:
                    preserve_marker_instruction = (
                        " Keep any tokens surrounded by double square brackets exactly as they appear."
                    )

                prompt = (
                    f"Translate the following text to {lang_name}. "
                    f"Maintain any formatting (bullet points, paragraphs, etc.)."
                    f"{preserve_marker_instruction}\n\n"
                    f"{text}\n\n"
                    f"Translation:"
                )

                # Generate translation
                full_prompt = f"{system_prompt}\n\n{prompt}"
                response = self.model.generate_content(
                    full_prompt,
                    generation_config=genai.GenerationConfig(
                        temperature=0.3,
                        max_output_tokens=len(text.split()) * 3,
                    ),
                )

                translation = response.text.strip()
                translations[lang_code] = translation

                logger.info(
                    f"Translated to {lang_name} ({lang_code}): " f"{len(translation)} chars"
                )

            logger.info(f"Successfully translated to {len(translations)} languages")

            return {"translations": translations}

        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error translating text: {str(e)}")
            raise Exception(f"Translation failed: {str(e)}")
