# Lectura

AI-powered lecture notes generator that transforms audio recordings into comprehensive study materials.

## Features

- **Audio Transcription**: Upload lecture recordings and get accurate transcripts
- **Smart Summaries**: Generate concise summaries with adaptive length
- **Interactive Flashcards**: Extract key concepts as Q&A pairs for active recall
- **Multi-language Translation**: Translate content into 50+ languages
- **Export Options**: Download as PDF, PowerPoint, or plain text

## Quick Start

### Prerequisites

- Python 3.13+
- Node.js 18+
- Gemini API key

### Backend Setup

```bash
cd backend
python3.13 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e '.[dev]'

# Create .env file with your API key
echo "GEMINI_API_KEY=your_api_key_here" > .env

# Run the server
uvicorn src.main:app --reload
```

Backend will be available at `http://localhost:8000`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at `http://localhost:5173`

## Usage

1. Open the frontend at `http://localhost:5173`
2. Upload an audio file (MP3, WAV, M4A, OGG, or FLAC)
3. Wait for transcription to complete
4. View transcript, generate summary, or create flashcards
5. Translate to other languages if needed
6. Export your study materials

## Technology Stack

**Backend**: Python 3.13, FastAPI, Gemini AI, OpenRouter
**Frontend**: React 18, TypeScript, Vite, Tailwind CSS

## Documentation

Complete technical documentation is available in the `/docs` folder:

- [Documentation Index](./docs/README.md) - Start here
- [Architecture Overview](./docs/ARCHITECTURE_INDEX.md) - System navigation
- [API Reference](./docs/API.md) - REST API documentation
- [Project Description](./docs/PROJECT_DESCRIPTION.md) - Project overview

## License

GPL 3.0
