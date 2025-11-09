# Lectura - Comprehensive Architecture Documentation

## Executive Summary

Lectura is a full-stack AI-powered lecture notes generator that transforms audio/text lectures into transcripts, summaries, flashcards, and multilingual translations. The system leverages Google Gemini AI via OpenRouter for processing and implements TOON format optimization to reduce token usage by 40-50%.

**Key Statistics:**
- Backend: Python 3.13, FastAPI, Uvicorn
- Frontend: React 18, TypeScript, Vite, Tailwind CSS
- Deployment: Docker & Docker Compose
- CI/CD: GitHub Actions
- Code Quality: Black, Flake8, MyPy, ESLint, Prettier

---

## 1. BACKEND ARCHITECTURE

### 1.1 Technology Stack

```
Core:
  - FastAPI 0.115.0+ (REST API framework)
  - Uvicorn 0.32.0+ (ASGI server)
  - Python 3.13 (runtime)
  - Pydantic 2.10.0+ (data validation)
  - Pydantic-Settings 2.6.0+ (configuration management)

AI/ML:
  - google-generativeai 0.8.0+ (Google Gemini direct API)
  - openai 1.54.0+ (OpenRouter compatibility layer)

Audio Processing:
  - pydub 0.25.1+ (audio format conversion)
  - mutagen 1.47.0+ (metadata extraction)
  - PyPDF2 3.0.0+ (PDF text extraction)

Utilities:
  - python-dotenv 1.0.1+ (environment configuration)
  - httpx 0.28.0+ (async HTTP client)

Development:
  - pytest 8.3.0+ (testing)
  - pytest-asyncio 0.24.0+ (async test support)
  - black 24.0.0+ (code formatter)
  - flake8 7.1.0+ (linter)
  - pylint 3.3.0+ (static analysis)
  - mypy 1.13.0+ (type checker)
  - pre-commit 4.0.0+ (git hooks)
```

### 1.2 Directory Structure

```
backend/
├── src/
│   ├── __init__.py                    # Package initialization
│   │
│   ├── main.py                         # FastAPI app entry point
│   │                                   # - Creates FastAPI instance
│   │                                   # - Configures CORS middleware
│   │                                   # - Registers all routers
│   │
│   ├── api/                           # API endpoints layer
│   │   ├── __init__.py
│   │   ├── health.py                  # GET /api/health
│   │   ├── transcribe.py              # POST /api/transcribe
│   │   ├── summarize.py               # POST /api/summarize
│   │   ├── flashcards.py              # POST /api/flashcards
│   │   └── translate.py               # POST /api/translate
│   │
│   ├── services/                      # Business logic layer
│   │   ├── __init__.py
│   │   ├── gemini.py                  # Gemini client wrapper (OpenRouter)
│   │   ├── transcriber.py             # Audio -> text transcription
│   │   ├── summarizer.py              # Text -> summary generation
│   │   ├── flashcards.py              # Text -> flashcard generation (with TOON)
│   │   ├── translator.py              # Text -> multilingual translation
│   │   └── toon.py                    # TOON format parser & utilities
│   │
│   ├── models/                        # Data models
│   │   ├── __init__.py
│   │   └── schemas.py                 # Pydantic request/response schemas
│   │
│   └── utils/                         # Utility functions
│       ├── __init__.py
│       ├── config.py                  # Settings management
│       ├── audio.py                   # Audio file validation & processing
│       └── logger.py                  # Logging configuration
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                    # Pytest configuration
│   ├── unit/
│   │   ├── __init__.py
│   │   └── test_*.py
│   ├── integration/
│   │   ├── __init__.py
│   │   └── test_api.py
│   └── fixtures/
│       └── sample_audio.mp3
│
├── .pre-commit-config.yaml            # Git pre-commit hooks
├── pyproject.toml                     # Project metadata & tool configuration
├── requirements.txt                   # Installed dependencies
├── requirements-dev.txt               # Development dependencies
├── .mypy_cache/                       # MyPy type checking cache
└── README.md
```

### 1.3 API Endpoints

#### Health Check
```
GET /api/health
Response:
{
  "status": "healthy"
}
```

#### Transcription
```
POST /api/transcribe
Content-Type: multipart/form-data

Parameters:
  - file: UploadFile (required) - Audio (mp3, wav, m4a, ogg, flac, aac) or Text (txt, pdf)
  - language: str (default: "en") - Language code

Response:
{
  "transcript": "string",          # Full transcribed text
  "duration": float,               # Audio duration in seconds
  "language": "string",            # Language of transcription
  "tokens_used": int               # Estimated tokens used
}

Max File Size: 500MB
Supported Audio: mp3, wav, m4a, ogg, flac, aac, wma
Supported Text: txt, pdf
```

#### Summarization
```
POST /api/summarize
Content-Type: application/json

Request:
{
  "text": "string",      # Text to summarize (required)
  "format": "string"    # Format (deprecated, ignored)
}

Response:
{
  "summary": "string",           # Generated summary
  "original_length": int,        # Original text word count
  "summary_length": int          # Summary word count
}

Features:
  - Adaptive target length (600-4000 words based on input)
  - Markdown-formatted output
  - Filters filler content
  - Markdown structure: ## headings, bullets, bold
```

#### Flashcard Generation
```
POST /api/flashcards
Content-Type: application/json

Request:
{
  "text": "string",                # Source text (required)
  "count": int | null,           # Number of cards (1-50, auto-calculated if null)
  "difficulty": "easy|medium|hard"  # Difficulty level (default: "medium")
}

Response:
{
  "flashcards": [
    {
      "question": "string",
      "answer": "string",
      "difficulty": "string"
    }
  ],
  "tokens_saved": int | null    # Token savings from TOON format
}

Features:
  - TOON format optimization (40-50% token savings)
  - Auto-count: ~1 card per 100 words
  - Three difficulty levels
  - Quality prompts with deduplication
```

#### Translation
```
POST /api/translate
Content-Type: application/json

Request:
{
  "text": "string",                    # Text to translate
  "target_languages": ["string", ...] # Language codes (max 20)
}

Response:
{
  "translations": {
    "es": "Spanish translation",
    "fr": "French translation",
    "de": "German translation",
    ...
  }
}

Supported: 50+ languages (ar, bg, bn, zh, cs, da, nl, et, fa, fi, fr, de, el, gu, he, hi, hu, id, it, ja, kn, ko, lv, lt, ml, mr, no, pl, pt, ro, ru, sr, sk, sl, es, sw, sv, ta, te, th, tr, uk, ur, vi, etc.)
```

### 1.4 Service Layer Architecture

#### GeminiClient (gemini.py)
Wrapper around OpenRouter API using OpenAI SDK for compatibility.

```python
class GeminiClient:
  def __init__()               # Initialize with OpenRouter API key
  def generate_text()          # Core text generation method
  def transcribe_audio()       # Placeholder (uses Transcriber instead)
  async def test_connection()  # Verify API connectivity
```

**Key Points:**
- Uses OpenRouter as the Gemini API gateway
- Model: google/gemini-2.0-flash-exp:free
- Supports prompt caching (>1024 tokens auto-cached)
- Returns tokens_used for cost tracking

#### Transcriber (transcriber.py)
Direct Google Gemini API integration for audio processing.

```python
class Transcriber:
  def __init__()                    # Initialize with Gemini API key
  async def transcribe()            # Process UploadFile
  def transcribe_file_path()        # Process local file path
```

**Key Features:**
- Uses google.generativeai library (direct Gemini)
- Model: gemini-2.5-flash (supports audio)
- Auto-detects audio duration
- Temp file cleanup
- Supports 60+ languages

**Workflow:**
1. Save uploaded file to temp location
2. Validate audio format
3. Get audio duration
4. Upload to Gemini
5. Generate transcription with language-specific prompt
6. Delete from Gemini and cleanup temp file

#### Summarizer (summarizer.py)
High-quality lecture note generation using Gemini.

```python
class Summarizer:
  def __init__()         # Initialize with Gemini API
  def summarize()        # Process text to summary
```

**Key Features:**
- Adaptive target length (600-4000 words)
- Markdown formatting with structure
- Filters admin chatter and filler
- System prompt: "meticulous university note-taker"
- Uses ## headings, bullets, bold for key concepts

**Algorithm:**
1. Calculate word count and char count
2. Adaptive target = max(600, min(4000, max(chars/30, words*0.2)))
3. Multi-part prompt with 6 rules
4. Generate with temperature 0.25
5. Return summary and metrics

#### FlashcardGenerator (flashcards.py)
Study material generation with TOON optimization.

```python
class FlashcardGenerator:
  def __init__()                           # Initialize with Gemini
  def generate_flashcards()                # Main generation method
  def _get_json_prompt()                   # Fallback JSON format
  def _parse_json_flashcards()             # Parse JSON responses
```

**TOON Format Benefits:**
```
JSON (150 tokens):
[
  {"question": "What is Python?", "answer": "A programming language", "difficulty": "easy"}
]

TOON (80 tokens - 47% savings):
Q: What is Python?
A: A programming language
D: easy
```

**Generation Process:**
1. Auto-calculate count: max(5, min(50, words/100))
2. Choose TOON format (default) for token efficiency
3. Generate with prompt requesting TOON output
4. Parse response with regex patterns
5. Calculate token savings vs JSON equivalent
6. Return flashcards list + savings metric

#### Translator (translator.py)
Multilingual content generation.

```python
class Translator:
  def __init__()           # Initialize with Gemini
  def translate()          # Translate to multiple languages
```

**Features:**
- Parallel language processing
- 50+ language support
- Preserves special markers in translation (for tracking)
- Temperature: 0.3 (more deterministic)
- Max tokens: len(text.split()) * 3

### 1.5 Data Models (schemas.py)

```python
# Responses
TranscribeResponse
├── transcript: str
├── duration: float
├── language: str
└── tokens_used: int

SummarizeRequest
├── text: str
└── format: Optional[str]

SummarizeResponse
├── summary: str
├── original_length: int
└── summary_length: int

Flashcard
├── question: str
├── answer: str
└── difficulty: str

FlashcardRequest
├── text: str
├── count: Optional[int] (1-50)
└── difficulty: str (easy|medium|hard)

FlashcardResponse
├── flashcards: List[Flashcard]
└── tokens_saved: Optional[int]

TranslateRequest
├── text: str
└── target_languages: List[str]

TranslateResponse
└── translations: Dict[str, str]
```

### 1.6 Configuration (config.py)

```python
class Settings (Pydantic BaseSettings):
  # OpenRouter/Gemini API
  openrouter_api_key: str = ""
  openrouter_base_url: str = "https://openrouter.ai/api/v1"
  gemini_model: str = "google/gemini-2.0-flash-exp:free"

  # Google Gemini API (direct)
  gemini_api_key: str = ""

  # Application
  environment: str = "development"
  log_level: str = "INFO"
  cors_origins: str = "http://localhost:5173"
  max_file_size: int = 524288000  # 500MB
```

Loaded from: `.env` file with fallback to env vars

### 1.7 Audio Processing (audio.py)

Utilities for validating and processing audio files:

```python
SUPPORTED_FORMATS = {
  "mp3": "mp3",
  "wav": "wav",
  "m4a": "mp4",
  "ogg": "ogg",
  "flac": "flac",
  "aac": "aac",
  "wma": "wma",
}

def validate_audio_file(file_path: str) -> Tuple[bool, Optional[str]]
  # Checks existence and format

def get_audio_duration(file_path: str) -> float
  # Uses multiple strategies:
  # 1. pydub (most formats)
  # 2. mutagen (mp3, m4a, flac)
  # 3. wave module (wav)
  # Fallback: 0.0
```

### 1.8 TOON Format (toon.py)

Custom optimized format for token efficiency.

```
Format Specification:
Q: Question text here
A: Answer text here
D: difficulty_level

(Blank line separates cards)
```

**Parser Features:**
```python
class TOONParser:
  @staticmethod
  def parse_flashcards()         # TOON -> Flashcard objects

  @staticmethod
  def flashcards_to_toon()       # Flashcard objects -> TOON

  @staticmethod
  def estimate_token_savings()   # Compare JSON vs TOON

def get_toon_flashcard_prompt()  # Generate TOON request prompt
```

**Token Savings Calculation:**
- JSON tokens: json_length / 4
- TOON tokens: toon_length / 4
- Savings: json_tokens - toon_tokens
- Typical: 40-50% reduction

---

## 2. FRONTEND ARCHITECTURE

### 2.1 Technology Stack

```
Core:
  - React 18.2.0 (UI framework)
  - TypeScript 5.2.2 (type safety)
  - Vite 5.0.8+ (build tool)

Styling:
  - Tailwind CSS 3.3.6 (utility CSS)
  - PostCSS 8.4.32 (CSS processor)
  - Autoprefixer 10.4.16 (vendor prefixes)

HTTP & API:
  - Axios 1.6.2+ (HTTP client)
  - (No state management: local hooks)

UI Libraries:
  - lucide-react 0.294.0+ (icons)
  - marked 17.0.0+ (Markdown parsing)
  - html2pdf.js 0.12.1+ (PDF generation)
  - pptxgenjs 4.0.1+ (PowerPoint generation)

Development:
  - @vitejs/plugin-react 4.2.1+ (React plugin)
  - ESLint 8.55.0+ (linter)
  - Prettier 3.1.1+ (formatter)
  - TypeScript compiler (type checking)
```

### 2.2 Directory Structure

```
frontend/
├── src/
│   ├── main.tsx                       # React entry point
│   ├── App.tsx                        # Root component (just renders Home)
│   ├── vite-env.d.ts                  # Vite type definitions
│   │
│   ├── pages/
│   │   └── Home.tsx                   # Main application page
│   │                                  # - Orchestrates all features
│   │                                  # - Manages file upload workflow
│   │                                  # - Handles state coordination
│   │
│   ├── components/
│   │   ├── AudioUploader.tsx          # File upload with drag-drop
│   │   ├── ResultsDisplay.tsx         # Tabbed results container
│   │   ├── TranscriptView.tsx         # Display raw transcript
│   │   ├── SummaryView.tsx            # Display summary + downloads
│   │   ├── FlashcardsView.tsx         # Flashcard flip animation
│   │   ├── LanguageSelector.tsx       # Translation language picker
│   │   ├── TranslationsView.tsx       # Translation display
│   │   ├── ErrorMessage.tsx           # Error display component
│   │   └── LoadingSpinner.tsx         # Loading indicator
│   │
│   ├── hooks/
│   │   ├── useTranscribe.ts           # File upload + transcription
│   │   ├── useSummarize.ts            # Summary generation + caching
│   │   ├── useFlashcards.ts           # Flashcard generation
│   │   └── useTranslate.ts            # Translation service
│   │
│   ├── lib/
│   │   └── api.ts                     # Axios API client + methods
│   │
│   ├── types/
│   │   ├── api.ts                     # TypeScript API interfaces
│   │   └── html2pdf.d.ts              # html2pdf type definitions
│   │
│   ├── constants/
│   │   └── languages.ts               # 50+ supported languages
│   │
│   └── index.css                      # Global styles
│
├── public/
│
├── postcss.config.js                  # PostCSS configuration
├── tailwind.config.js                 # Tailwind CSS configuration
├── vite.config.ts                     # Vite build configuration
├── tsconfig.json                      # TypeScript configuration
├── tsconfig.node.json                 # TS config for Vite/tools
├── .eslintrc.json                     # ESLint configuration
├── package.json                       # Dependencies & scripts
├── package-lock.json                  # Lock file
└── README.md
```

### 2.3 Component Hierarchy

```
App
  └── Home
      ├── AudioUploader
      ├── LanguageSelector
      ├── [Workflow sidebar]
      ├── [Summary settings]
      ├── [Flashcard settings]
      ├── [Translation languages]
      └── ResultsDisplay
          ├── TranscriptView
          ├── SummaryView (with translations)
          └── FlashcardsView (with translations)
```

### 2.4 Core Components

#### AudioUploader (AudioUploader.tsx)
File upload interface with drag-and-drop.

**Props:**
```typescript
interface AudioUploaderProps {
  onFileSelected: (file: File) => void     // Called on file selection
  onClear?: () => void                     // Clear UI
  isUploading?: boolean                    # Show upload progress
  isProcessing?: boolean                   # Show processing indicator
  uploadProgress?: number                  # Upload % (0-100)
  error?: string | null                    # Error message
  acceptedTypes?: string[]                 # Accepted MIME types
  maxFileSizeMb?: number                   # Max file size in MB
}
```

**Features:**
- Drag-and-drop interface
- File validation (type, size)
- Upload progress bar
- Processing indicator
- File preview (audio player)
- Error display
- Clear/reset button

**Validation:**
- Audio: mp3, wav, m4a, aac, ogg, flac
- Text: txt, pdf
- Default max: 500MB
- Custom size/type support

#### ResultsDisplay (ResultsDisplay.tsx)
Tabbed interface for viewing results.

**Props:**
```typescript
interface ResultsDisplayProps {
  transcript: ReactNode          # Transcript tab content
  summary: ReactNode             # Summary tab content
  flashcards: ReactNode          # Flashcards tab content
  activeTab?: ResultsTab         # Current tab
  onTabChange?: (tab: ResultsTab) => void
}
```

**Features:**
- Three tabs: Transcript, Summary, Flashcards
- Smooth tab switching
- Clean UI with background styling
- Internal tab state management

#### TranscriptView (TranscriptView.tsx)
Display raw transcript with copy/download.

**Features:**
- Copy to clipboard
- Download as text
- Word/char count
- Search/scroll support

#### SummaryView (SummaryView.tsx)
Display summary with multiple export formats.

**Features:**
- Multi-language switching
- Character count badge
- Copy to clipboard
- Download options:
  - Plain text (.txt)
  - PDF with Markdown styling
  - PowerPoint presentation (.pptx)
- Markdown rendering
- Scrollable content area

**Export Algorithm (PPTX):**
1. Parse Markdown headings (## becomes slides)
2. Split long sections into multiple slides (6 bullets per slide)
3. Normalize bullet text (removes markdown symbols)
4. Create presentation with consistent styling
5. Download via pptxgenjs

#### FlashcardsView (FlashcardsView.tsx)
Interactive flashcard flipper with navigation.

**Props:**
```typescript
interface FlashcardsViewProps {
  flashcards?: Flashcard[]                    # Cards to display
  isLoading?: boolean                         # Show loading
  translations?: Record<string, Flashcard[]>  # Language translations
  selectedLanguages?: string[]                # Available languages
}
```

**Features:**
- 3D flip animation (CSS perspective)
- Arrow key navigation (left/right)
- Spacebar to flip
- Shuffle button
- Language switcher
- Progress indicator (e.g., "3/10")
- Difficulty badge
- Smooth transitions

**Keyboard Shortcuts:**
- Left Arrow: Previous card
- Right Arrow: Next card
- Space: Flip card

#### LanguageSelector (LanguageSelector.tsx)
Multi-select for translation languages.

**Features:**
- 50+ language options
- Multi-select checkboxes
- Organized by region
- Default: English only
- Real-time state updates

### 2.5 Custom Hooks

#### useTranscribe (useTranscribe.ts)
Manages audio transcription state and progress.

```typescript
interface UseTranscribeReturn {
  data: TranscribeResponse | null
  isLoading: boolean
  isUploadingFile: boolean
  isProcessing: boolean          // isLoading && !isUploadingFile
  error: string | null
  uploadProgress: number         // 0-100
  transcribe: (file: File) => Promise<TranscribeResponse>
  reset: () => void
}
```

**Behavior:**
- Tracks upload progress separately from processing
- Calls transcribeAudio with progress callback
- Parses Axios errors to user-friendly messages
- Manages loading states independently

#### useSummarize (useSummarize.ts)
Handles summarization with local caching.

```typescript
interface UseSummarizeReturn {
  data: SummarizeResponse | null
  isLoading: boolean
  error: string | null
  summarize: (
    payload: SummarizeRequest,
    options?: { force?: boolean }
  ) => Promise<SummarizeResponse>
  reset: () => void
}
```

**Features:**
- Client-side caching (same text + format = cached)
- Force refresh option
- Error handling
- Clean state reset

#### useFlashcards (useFlashcards.ts)
Flashcard generation with state management.

Similar structure to useSummarize with caching.

#### useTranslate (useTranslate.ts)
Translation service hook.

```typescript
interface UseTranslateReturn {
  data: TranslateResponse | null
  isLoading: boolean
  error: string | null
  translate: (payload: TranslateRequest) => Promise<TranslateResponse>
  reset: () => void
}
```

### 2.6 API Client (lib/api.ts)

Axios-based HTTP client with typed methods.

```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' }
})

// API Methods
export const transcribeAudio(file, onUploadProgress)    // FormData upload
export const summarizeText(payload)                     // JSON POST
export const generateFlashcards(payload)                // JSON POST
export const translateText(payload)                     // JSON POST
export const healthCheck()                              // GET health
```

**Features:**
- Typed request/response
- Upload progress callbacks
- Error handling in hooks
- VITE_API_URL environment variable support

### 2.7 Type Definitions (types/api.ts)

```typescript
// Responses
interface TranscribeResponse {
  transcript: string
  duration: number
  language: string
  tokens_used: number
}

interface SummarizeRequest {
  text: string
  format?: string
}

interface SummarizeResponse {
  summary: string
  original_length: number
  summary_length: number
}

interface Flashcard {
  question: string
  answer: string
  difficulty: string
}

interface FlashcardRequest {
  text: string
  count?: number | null
  difficulty?: 'easy' | 'medium' | 'hard'
}

interface FlashcardResponse {
  flashcards: Flashcard[]
  tokens_saved?: number
}

interface TranslateRequest {
  text: string
  target_languages: string[]
}

interface TranslateResponse {
  translations: Record<string, string>
}
```

### 2.8 Constants (constants/languages.ts)

50+ supported languages with codes and labels:

```typescript
const supportedLanguages = [
  { code: 'en', label: 'English' },
  { code: 'ar', label: 'Arabic' },
  { code: 'bn', label: 'Bengali' },
  { code: 'zh', label: 'Chinese (Simplified)' },
  // ... 46 more languages
  { code: 'vi', label: 'Vietnamese' }
]
```

### 2.9 Styling

**Tailwind Configuration:**
- Base colors: Indigo-600 for primary actions
- Spacing: Consistent padding/margins (4px, 8px, 16px, 32px)
- Responsive: Mobile-first design
- Dark mode: Not enabled (light only)

**Component Patterns:**
- Rounded corners: `rounded-2xl`, `rounded-full`
- Shadows: `shadow-sm`, `shadow-lg`, `shadow-xl`
- Transitions: `transition`, `transition-all`
- Hover states: `hover:bg-indigo-500`, `hover:text-indigo-600`
- Disabled states: `disabled:bg-gray-200`, `disabled:cursor-not-allowed`

---

## 3. SYSTEM INTEGRATION

### 3.1 Request/Response Flow

#### Upload & Transcription Flow
```
User selects audio file
  ↓
AudioUploader validates file
  ↓
useTranscribe.transcribe(file)
  ↓
api.transcribeAudio(file, onUploadProgress)
  ↓
POST /api/transcribe [multipart/form-data]
  ↓
transcribe.py validates & saves temp file
  ↓
Transcriber.transcribe() calls Gemini API
  ↓
Gemini processes audio → returns transcript
  ↓
TranscribeResponse (transcript, duration, language, tokens_used)
  ↓
Frontend displays in TranscriptView tab
```

#### Summary Generation with Translation Flow
```
User clicks "Generate Summary"
  ↓
handleGenerateSummary() in Home.tsx
  ↓
useSummarize.summarize(transcript)
  ↓
POST /api/summarize [JSON]
  ↓
Summarizer.summarize() → Gemini API
  ↓
SummarizeResponse
  ↓
If languages selected:
  ↓
useTranslate.translate(summary, languages)
  ↓
POST /api/translate [JSON]
  ↓
Translator.translate() → parallel Gemini calls
  ↓
TranslateResponse (translations)
  ↓
Frontend displays summary + translations in SummaryView
```

#### Flashcard Generation with Translation Flow
```
User clicks "Generate Flashcards"
  ↓
handleGenerateFlashcards() in Home.tsx
  ↓
useFlashcards.generateFlashcards(transcript, difficulty)
  ↓
POST /api/flashcards [JSON]
  ↓
FlashcardGenerator.generate_flashcards() → Gemini (TOON format)
  ↓
FlashcardResponse (flashcards, tokens_saved)
  ↓
If languages selected:
  ↓
Build flashcard payload with markers: [[CARD_0_QUESTION]], [[CARD_0_ANSWER]]
  ↓
useTranslate.translate(payload, languages)
  ↓
Translator translates entire payload
  ↓
parseFlashcardTranslation() parses markers back to Flashcard objects
  ↓
Frontend displays with language switcher in FlashcardsView
```

### 3.2 Data Flow Architecture

```
                    FRONTEND (React)
                          ↓
                      Home.tsx
                    ↙    ↓    ↘
            AudioUploader  Settings  ResultsDisplay
                    ↓                      ↓
            useTranscribe          TranscriptView
            useSummarize           SummaryView
            useFlashcards          FlashcardsView
            useTranslate
                    ↓
                api.ts (Axios)
                    ↓
                HTTP/JSON
                    ↓
          BACKEND (FastAPI)
                    ↓
            main.py (routers)
                    ↓
        ↙      ↓      ↓       ↘
    health   transcribe  summarize  flashcards  translate
        ↓      ↓      ↓       ↘        ↓
      [APIs]        [Services]
        ↓           ↓
    Transcriber  Summarizer
    Flashcards   Translator
    Transcriber
        ↓
    Google Gemini API
```

### 3.3 Error Handling

**Frontend:**
- Axios errors → hook state errors
- User-friendly messages via ErrorMessage component
- Fallback messages: "Unable to [action]"

**Backend:**
- ValueError → 400 Bad Request
- Exception → 500 Internal Server Error
- All errors logged with context
- Proper cleanup (temp files, Gemini uploads)

### 3.4 Caching & Optimization

**Frontend:**
- useSummarize: In-memory cache (key: first 100 chars + format)
- useFlashcards: In-memory cache (key: text + difficulty)
- Component memoization via useMemo hooks
- Upload progress tracking

**Backend:**
- Gemini prompt caching: Auto-caches >1024 tokens
- TOON format: 40-50% token reduction vs JSON
- Temp file cleanup: Automatic on completion/error
- Connection pooling: Uvicorn handles HTTP/2

---

## 4. DEPLOYMENT & DEVOPS

### 4.1 Docker Configuration

#### Backend Dockerfile
```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Frontend Dockerfile
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]
```

### 4.2 Docker Compose

```yaml
services:
  backend:
    build: ./backend
    ports: ["8000:8000"]
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - ENVIRONMENT=development
      - LOG_LEVEL=INFO
      - CORS_ORIGINS=http://localhost:5173
    volumes:
      - ./backend:/app
    command: uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build: ./frontend
    ports: ["5173:5173"]
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: npm run dev -- --host
    depends_on:
      - backend
```

**Usage:**
```bash
docker-compose up
# Backend: http://localhost:8000
# Frontend: http://localhost:5173
# API Docs: http://localhost:8000/docs
```

### 4.3 GitHub Actions CI/CD

#### Backend CI (ci-backend.yml)
```yaml
name: Backend CI
on:
  push:
    branches: [main, develop]
    paths: ['backend/**', '.github/workflows/ci-backend.yml']
  pull_request:
    paths: ['backend/**']

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.13'
          cache: 'pip'
      - run: cd backend && pip install -e '.[dev]'
      - run: cd backend && flake8 src/ --max-line-length=100
      - run: cd backend && black src/
      - run: cd backend && mypy src/ --ignore-missing-imports
      - run: cd backend && pytest --cov=src --cov-report=xml
      - uses: codecov/codecov-action@v3
        with:
          file: ./backend/coverage.xml
          flags: backend
```

**Checks:**
1. Flake8 linting (100 char limit)
2. Black formatting
3. MyPy type checking
4. Pytest with coverage
5. CodeCov upload

### 4.4 Code Quality Tools

**Black:**
```toml
[tool.black]
line-length = 100
target-version = ['py312']
```

**MyPy:**
```toml
[tool.mypy]
python_version = "3.13"
warn_return_any = true
disallow_untyped_defs = true
```

**Pytest:**
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=src --cov-report=term-missing"
```

**Pre-commit:**
```yaml
repos:
  - repo: https://github.com/psf/black
    hooks:
      - id: black
  - repo: https://github.com/PyCQA/flake8
    hooks:
      - id: flake8
```

---

## 5. KEY ARCHITECTURAL DECISIONS

### 5.1 Why Direct Gemini API for Transcription?

**Decision:** Use `google-generativeai` directly instead of OpenRouter

**Rationale:**
- Audio processing requires Gemini's multimodal capabilities
- OpenRouter doesn't support audio transcription
- Direct API provides best latency
- google-generativeai handles file uploads properly

### 5.2 Why TOON Format for Flashcards?

**Decision:** Custom TOON format instead of JSON

**Benefits:**
- 40-50% token reduction vs JSON
- Simpler parsing without external libs
- Human-readable
- Easier prompt engineering
- Significant cost savings at scale

**Trade-off:** Custom parser required (mitigated by simple regex)

### 5.3 Why Client-Side Translation Markers?

**Decision:** Use `[[CARD_0_QUESTION]]` markers for flashcard translation

**Rationale:**
- Keeps translation context together
- Preserves flashcard structure
- Allows accurate post-parsing
- Works across languages

### 5.4 Why No Complex State Management?

**Decision:** Use React hooks (useState, useCallback) instead of Redux/Zustand

**Rationale:**
- Application scope: Single page
- Limited state complexity
- Easy debugging
- Lower bundle size
- Sufficient for feature requirements

### 5.5 Why Adaptive Summary Length?

**Decision:** Dynamically adjust target length based on input

**Algorithm:**
```
adaptive_target = max(600, min(4000, max(chars/30, words*0.2)))
```

**Rationale:**
- Short lectures (5min): ~600 word summary
- Medium lectures (30min): ~1500 word summary
- Long lectures (90min): ~4000 word summary
- Proportional: 20-30% of original length
- Fits most lecture patterns

---

## 6. DEPLOYMENT READINESS

### 6.1 Environment Variables

**Required (.env or system env):**
```bash
GEMINI_API_KEY=<your-key>
OPENROUTER_API_KEY=<optional-for-text-generation>
```

**Optional:**
```bash
ENVIRONMENT=development|production
LOG_LEVEL=DEBUG|INFO|WARNING|ERROR
CORS_ORIGINS=http://localhost:5173
MAX_FILE_SIZE=524288000
BACKEND_PORT=8000
FRONTEND_PORT=5173
```

### 6.2 Secrets Management

**Current:** .env file (development only)

**For Production:**
- GitHub Secrets for CI/CD
- Environment-specific secrets
- Rotate API keys regularly
- Never commit secrets

### 6.3 Monitoring & Logging

**Backend:**
- Structured logging with timestamps
- Log levels: DEBUG, INFO, WARNING, ERROR
- Formatted: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`

**Metrics to Track:**
- API response times
- Token usage (cost tracking)
- Error rates by endpoint
- File sizes processed
- Language distribution

---

## 7. DEVELOPMENT WORKFLOW

### 7.1 Local Setup

```bash
# Backend
cd backend
python3.13 -m venv venv
source venv/bin/activate
pip install -e '.[dev]'
cp .env.example .env
pre-commit install
uvicorn src.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

### 7.2 Testing

```bash
# Backend tests
cd backend
pytest                    # Run all tests
pytest --cov             # With coverage
pytest -v                # Verbose

# Frontend tests
cd frontend
npm run test             # If configured
```

### 7.3 Code Quality Checks

```bash
# Backend
cd backend
black src/               # Format
flake8 src/              # Lint
mypy src/                # Type check
pre-commit run --all-files  # All hooks

# Frontend
cd frontend
npm run lint             # ESLint
npm run type-check       # TypeScript
```

---

## 8. PERFORMANCE CONSIDERATIONS

### 8.1 Backend Optimizations

- **Async/Await:** FastAPI + Uvicorn for concurrent requests
- **TOON Format:** 40-50% token reduction
- **Prompt Caching:** Gemini auto-caches >1024 tokens
- **Connection Pooling:** Handled by httpx/Uvicorn
- **Temp File Cleanup:** Automatic on completion/error

### 8.2 Frontend Optimizations

- **Code Splitting:** Vite bundles efficiently
- **Lazy Loading:** Components load on demand
- **Memoization:** useMemo for expensive computations
- **Local Caching:** Summarize/Flashcard hooks cache results
- **CSS:** Tailwind purges unused styles

### 8.3 API Performance

- **Transcription:** Depends on audio length (typically 10-30s)
- **Summarization:** Depends on text length (typically 5-15s)
- **Flashcards:** ~5-10s for 10-20 cards
- **Translation:** ~3-5s per language

**Typical Full Workflow:**
1. Upload 60min audio: 30s
2. Transcription: 30s
3. Summary: 10s
4. 10 flashcards: 8s
5. 3 translations (summary + flashcards): 20s
Total: ~98 seconds

---

## 9. SCALABILITY & FUTURE ENHANCEMENTS

### 9.1 Scaling Considerations

**Current Bottlenecks:**
- Gemini API rate limits
- File upload size limits (500MB)
- Single-threaded audio processing

**Scaling Options:**
1. Queue system (Celery/RabbitMQ) for long jobs
2. Distributed audio processing
3. Caching layer (Redis) for popular lectures
4. CDN for frontend assets
5. Load balancing for backend

### 9.2 Potential Features

- Batch processing (multiple files)
- Video lecture support (extract audio)
- Custom prompts per feature
- Export to Anki format
- Collaboration/sharing
- User accounts + persistence
- API rate limiting
- Advanced analytics

---

## 10. ARCHITECTURE SUMMARY TABLE

| Component | Technology | Purpose | Key Files |
|-----------|-----------|---------|-----------|
| **Backend** | FastAPI | REST API | main.py, api/*.py |
| **AI** | Gemini 2.0 | Content generation | services/*.py |
| **Database** | None | Stateless design | - |
| **Frontend** | React 18 | UI/UX | src/pages/Home.tsx |
| **HTTP** | Axios | API calls | src/lib/api.ts |
| **Styling** | Tailwind | CSS framework | tailwind.config.js |
| **Build** | Vite | Frontend bundler | vite.config.ts |
| **Deployment** | Docker | Containerization | docker-compose.yml |
| **CI/CD** | GitHub Actions | Testing/QA | .github/workflows/ |
| **Type Safety** | TypeScript/MyPy | Type checking | tsconfig.json, pyproject.toml |
