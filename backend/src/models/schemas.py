"""Pydantic models for request/response validation"""

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class TranscribeResponse(BaseModel):
    """Response model for transcription"""

    transcript: str
    duration: float
    language: str
    tokens_used: int


class SummarizeRequest(BaseModel):
    """Request model for summarization"""

    text: str
    format: str = Field(default="bullet_points", pattern="^(bullet_points|paragraph)$")


class SummarizeResponse(BaseModel):
    """Response model for summarization"""

    summary: str
    original_length: int
    summary_length: int


class FlashcardRequest(BaseModel):
    """Request model for flashcard generation"""

    text: str
    count: int = Field(default=10, ge=1, le=50)
    difficulty: str = Field(default="medium", pattern="^(easy|medium|hard)$")


class Flashcard(BaseModel):
    """Individual flashcard model"""

    question: str
    answer: str
    difficulty: str


class FlashcardResponse(BaseModel):
    """Response model for flashcards"""

    flashcards: List[Flashcard]
    tokens_saved: Optional[int] = None


class TranslateRequest(BaseModel):
    """Request model for translation"""

    text: str
    target_languages: List[str]


class TranslateResponse(BaseModel):
    """Response model for translation"""

    translations: Dict[str, str]
