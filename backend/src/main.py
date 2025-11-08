"""FastAPI application entry point"""

from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import flashcards, health, summarize, transcribe

app = FastAPI(
    title="Lectura API", description="AI-powered lecture notes generator", version="0.1.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(transcribe.router, prefix="/api", tags=["transcription"])
app.include_router(summarize.router, prefix="/api", tags=["summarization"])
app.include_router(flashcards.router, prefix="/api", tags=["flashcards"])


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint"""
    return {"message": "Lectura API", "version": "0.1.0", "docs": "/docs"}
