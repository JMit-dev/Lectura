# Lectura Backend

FastAPI backend for the Lectura AI lecture notes generator.

## 📁 Project Structure

```
backend/
├── src/
│   ├── api/              # API route handlers
│   │   ├── health.py     # Health check endpoint
│   │   ├── transcribe.py # Audio transcription (TODO)
│   │   ├── summarize.py  # Text summarization (TODO)
│   │   ├── flashcards.py # Flashcard generation (TODO)
│   │   └── translate.py  # Translation (TODO)
│   │
│   ├── services/         # Business logic
│   │   ├── gemini.py     # Gemini API client (TODO)
│   │   ├── transcriber.py # Audio → text service (TODO)
│   │   ├── summarizer.py  # Text → summary service (TODO)
│   │   ├── flashcards.py  # Text → flashcards service (TODO)
│   │   ├── translator.py  # Translation service (TODO)
│   │   └── toon.py        # TOON format helper (TODO)
│   │
│   ├── models/           # Data models
│   │   └── schemas.py    # Pydantic request/response models
│   │
│   ├── utils/            # Utility functions
│   │   ├── config.py     # Settings and configuration
│   │   ├── logger.py     # Logging setup
│   │   └── audio.py      # Audio processing (TODO)
│   │
│   └── main.py           # FastAPI application entry point
│
├── tests/
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   │   └── test_api.py   # API endpoint tests
│   ├── fixtures/         # Test data
│   └── conftest.py       # Pytest configuration
│
├── requirements.txt      # Production dependencies
├── requirements-dev.txt  # Development dependencies
├── pyproject.toml        # Python tooling configuration
├── .env.example          # Environment variables template
└── Dockerfile            # Docker configuration
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+ (tested with 3.13)
- Gemini API key

### Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
# For production/runtime tooling only
pip install -e .

# For full dev tooling (linters, tests, hooks)
pip install -e .[dev]

# Set up environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Install pre-commit hooks
pre-commit install
```

### Run Development Server

```bash
source venv/bin/activate
uvicorn src.main:app --reload
```

Server runs on http://localhost:8000
- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/api/health

## 🧪 Testing

```bash
# Run all tests with coverage
pytest --cov=src

# Run specific test file
pytest tests/integration/test_api.py

# Run with verbose output
pytest -v
```

## 🔍 Code Quality

```bash
# Format code with Black
black src/

# Lint with Flake8
flake8 src/

# Type check with mypy
mypy src/

# Run all checks
pre-commit run --all-files
```

## 📝 API Endpoints

### Health Check
```http
GET /api/health
```
Returns: `{"status": "healthy"}`

### Transcribe Audio (TODO)
```http
POST /api/transcribe
Content-Type: multipart/form-data

file: <audio-file>
language: "en"
```

### Summarize Text (TODO)
```http
POST /api/summarize
Content-Type: application/json

{
  "text": "Long transcript...",
  "format": "bullet_points"
}
```

### Generate Flashcards (TODO)
```http
POST /api/flashcards
Content-Type: application/json

{
  "text": "Content to study...",
  "count": 10,
  "difficulty": "medium"
}
```

### Translate (TODO)
```http
POST /api/translate
Content-Type: application/json

{
  "text": "Text to translate...",
  "target_languages": ["es", "fr", "zh"]
}
```

## 🛠️ Development Tasks

### Person 1 (AI/Backend Lead) - Priority Order

1. **Implement Gemini Client** (`src/services/gemini.py`)
   - Create Gemini API wrapper
   - Handle authentication
   - Error handling

2. **Audio Transcription**
   - Service: `src/services/transcriber.py`
   - API: `src/api/transcribe.py`
   - Test with sample audio files

3. **Text Summarization**
   - Service: `src/services/summarizer.py`
   - API: `src/api/summarize.py`
   - Prompt engineering for quality

4. **Flashcard Generation**
   - Service: `src/services/flashcards.py`
   - API: `src/api/flashcards.py`
   - TOON format integration

5. **Translation**
   - Service: `src/services/translator.py`
   - API: `src/api/translate.py`
   - Support 60+ languages

6. **TOON Optimization**
   - Implement: `src/services/toon.py`
   - Token usage benchmarks
   - Documentation

## 📦 Dependencies

### Core
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation
- `google-generativeai` - Gemini API
- `python-multipart` - File uploads
- `pydub` - Audio processing
- `httpx` - HTTP client

### Development
- `pytest` - Testing framework
- `pytest-asyncio` - Async test support
- `pytest-cov` - Coverage reporting
- `black` - Code formatter
- `flake8` - Linter
- `mypy` - Type checker
- `pre-commit` - Git hooks

## 🔧 Configuration

Environment variables in `.env`:

```bash
GEMINI_API_KEY=your_key_here
ENVIRONMENT=development
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:5173
MAX_FILE_SIZE=10485760  # 10MB
```

## 🐛 Debugging

```bash
# Run with debug logging
LOG_LEVEL=DEBUG uvicorn src.main:app --reload

# Run with specific host/port
uvicorn src.main:app --host 0.0.0.0 --port 8080
```

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Gemini API Docs](https://ai.google.dev/docs)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Project Architecture](../docs/ARCHITECTURE.md)
- [API Documentation](../docs/API.md)
