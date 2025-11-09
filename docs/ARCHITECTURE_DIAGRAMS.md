# Lectura Architecture Diagrams

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      User Browser                            │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              React 18 Frontend (Vite)                  │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────────┤ │
│  │  │ Audio Upload │  │  ResultTabs  │  │ Export Options │ │
│  │  │  (Drag/Drop) │  │ (Transcript  │  │ (TXT/PDF/PPTX) │ │
│  │  │              │  │  Summary     │  │                │ │
│  │  │              │  │  Flashcards) │  │ Language       │ │
│  │  └──────┬───────┘  └──────┬───────┘  │ Selector       │ │
│  │         │                 │          └────────────────┤ │
│  │         └─────────┬───────┘                            │ │
│  │              Hooks Layer                               │ │
│  │  ┌─────────────┬──────────────┬──────────────────────┐ │
│  │  │useTranscribe│useSummarize  │useFlashcards        │ │
│  │  │useTranslate │(with cache)  │(with cache)         │ │
│  │  └─────────────┴──────────────┴──────────────────────┘ │
│  │                      │                                  │
│  │                   Axios Client                          │
│  │            (VITE_API_URL config)                        │
│  └────────────┬────────────────────────────────────────────┘
│               │ HTTP/JSON
│               │
└───────────────┼──────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────┐
│                   Docker Container                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │          Python FastAPI Backend (Uvicorn)            │  │
│  │  ┌──────────────────────────────────────────────────┤  │
│  │  │                 API Layer                         │  │
│  │  │  GET  /api/health                                │  │
│  │  │  POST /api/transcribe    (multipart/form-data)  │  │
│  │  │  POST /api/summarize     (JSON)                 │  │
│  │  │  POST /api/flashcards    (JSON)                 │  │
│  │  │  POST /api/translate     (JSON)                 │  │
│  │  └──────┬───────────────────────────────────────────┘  │
│  │         │                                              │
│  │  ┌──────▼──────────────────────────────────────────┐  │
│  │  │           Services Layer                        │  │
│  │  │  ┌─────────────┐      ┌──────────────────────┐ │  │
│  │  │  │Transcriber  │      │Summarizer            │ │  │
│  │  │  │ (Gemini API)│      │(Gemini 2.0-flash)   │ │  │
│  │  │  │             │      │ • Markdown output    │ │  │
│  │  │  │ • mp3,wav   │      │ • Adaptive length    │ │  │
│  │  │  │ • m4a,flac  │      │ • Filter filler      │ │  │
│  │  │  └─────┬───────┘      └──────────────────────┘ │  │
│  │  │        │                      │                │  │
│  │  │  ┌─────▼─────────┐    ┌───────▼────────────┐  │  │
│  │  │  │ Audio Utils   │    │FlashcardGenerator  │  │  │
│  │  │  │ • Validate    │    │ • TOON format      │  │  │
│  │  │  │ • Get Duration│    │ • 40-50% savings   │  │  │
│  │  │  │ • Cleanup     │    │ • Auto-count cards │  │  │
│  │  │  └───────────────┘    └───────┬────────────┘  │  │
│  │  │                                │               │  │
│  │  │                        ┌───────▼────────────┐  │  │
│  │  │                        │TOON Parser         │  │  │
│  │  │                        │ • Parse flashcards │  │  │
│  │  │                        │ • Token estimation │  │  │
│  │  │                        └────────────────────┘  │  │
│  │  │                                                 │  │
│  │  │  ┌──────────────────────────────────────────┐  │  │
│  │  │  │Translator (Gemini 2.0-flash)            │  │  │
│  │  │  │ • 50+ languages                         │  │  │
│  │  │  │ • Parallel processing                   │  │  │
│  │  │  │ • Preserve markers                      │  │  │
│  │  │  └──────────────────────────────────────────┘  │  │
│  │  └─────────────┬──────────────────────────────────┘  │
│  │                │                                     │
│  │  ┌─────────────▼──────────────────────────────────┐  │
│  │  │         Configuration & Utils                 │  │
│  │  │  • Settings (from .env)                      │  │
│  │  │  • Logging                                   │  │
│  │  │  • Error handling                            │  │
│  │  │  • CORS middleware                           │  │
│  │  └──────────────────────────────────────────────┘  │
│  └──────────────────┬─────────────────────────────────┘
│                     │ HTTP/REST
└─────────────────────┼──────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│         Google Gemini API (via Direct Connection)           │
│                                                              │
│  • gemini-2.5-flash (audio transcription)                   │
│  • gemini-2.0-flash-exp (text processing)                   │
│  • File upload API (for audio)                              │
│  • Prompt caching (>1024 tokens)                            │
└─────────────────────────────────────────────────────────────┘
```

## Request/Response Flow: Complete Workflow

```
┌──────────────────┐
│  User Actions    │
└────────┬─────────┘
         │
         ├─── 1. Upload Audio File ──────────┐
         │                                    │
         │  ┌────────────────────────────────▼─────────────────┐
         │  │ Frontend: AudioUploader Component                 │
         │  │ • Validate file type (mp3, wav, m4a, etc.)      │
         │  │ • Validate file size (<500MB)                   │
         │  │ • Show drag-drop interface                       │
         │  │ • Display upload progress                        │
         │  └────────────┬──────────────────────────────────────┘
         │               │
         │               ▼
         │  ┌────────────────────────────────────────────────┐
         │  │ useTranscribe Hook                              │
         │  │ • api.transcribeAudio(file, progressCallback) │
         │  │ • Track upload & processing separately        │
         │  └────────────┬───────────────────────────────────┘
         │               │
         │               ▼
         │  ┌────────────────────────────────────────────────┐
         │  │ POST /api/transcribe                            │
         │  │ • Content-Type: multipart/form-data            │
         │  │ • Params: file, language                       │
         │  └────────────┬───────────────────────────────────┘
         │               │
         │               ▼
         │  ┌────────────────────────────────────────────────┐
         │  │ Backend: transcribe() Endpoint                  │
         │  │ • Validate file size & type                    │
         │  │ • Save to temp file                            │
         │  │ • Check if text or audio                       │
         │  │  - If text: extract/parse content              │
         │  │  - If audio: continue...                       │
         │  └────────────┬───────────────────────────────────┘
         │               │
         │               ▼
         │  ┌────────────────────────────────────────────────┐
         │  │ Transcriber Service                             │
         │  │ • Validate audio format                        │
         │  │ • Get audio duration (pydub/mutagen/wave)     │
         │  │ • Upload to Gemini API                         │
         │  │ • Call Gemini with transcription prompt        │
         │  │ • Delete from Gemini                           │
         │  │ • Cleanup temp file                            │
         │  └────────────┬───────────────────────────────────┘
         │               │
         │               ▼
         │  ┌────────────────────────────────────────────────┐
         │  │ Google Gemini (gemini-2.5-flash)               │
         │  │ • Input: Audio file                            │
         │  │ • Output: Full transcript                      │
         │  └────────────┬───────────────────────────────────┘
         │               │
         │               ▼
         │  ┌────────────────────────────────────────────────┐
         │  │ TranscribeResponse                              │
         │  │ {                                               │
         │  │   "transcript": "...",   (full text)           │
         │  │   "duration": 305.5,     (seconds)             │
         │  │   "language": "en",      (detected)            │
         │  │   "tokens_used": 1234    (estimated)           │
         │  │ }                                               │
         │  └────────────┬───────────────────────────────────┘
         │               │
         │               ▼
         │  ┌────────────────────────────────────────────────┐
         │  │ Frontend: Display in TranscriptView             │
         │  │ • Show full transcript                         │
         │  │ • Copy to clipboard button                     │
         │  │ • Download as text                             │
         │  │ • Word/char count                              │
         │  └────────────────────────────────────────────────┘
         │
         ├─── 2. Generate Summary ────────────┐
         │                                    │
         │  ┌────────────────────────────────▼─────────────────┐
         │  │ Frontend: Summary Settings Panel                  │
         │  │ • Click "Generate Summary"                       │
         │  │ • handleGenerateSummary() in Home                │
         │  └────────────┬──────────────────────────────────────┘
         │               │
         │               ▼
         │  ┌────────────────────────────────────────────────┐
         │  │ useSummarize Hook                               │
         │  │ • Check cache (first 100 chars + format)       │
         │  │ • api.summarizeText(transcript)                │
         │  └────────────┬───────────────────────────────────┘
         │               │
         │               ▼
         │  ┌────────────────────────────────────────────────┐
         │  │ POST /api/summarize [JSON]                      │
         │  │ {                                               │
         │  │   "text": "full transcript...",                │
         │  │   "format": null                               │
         │  │ }                                               │
         │  └────────────┬───────────────────────────────────┘
         │               │
         │               ▼
         │  ┌────────────────────────────────────────────────┐
         │  │ Summarizer Service                              │
         │  │ • Calculate adaptive target:                   │
         │  │   max(600, min(4000, max(chars/30, words*0.2)))│
         │  │ • Create system & user prompts                 │
         │  │ • Call Gemini with temperature=0.25            │
         │  │ • Generate Markdown summary                    │
         │  │ • Return summary + metrics                     │
         │  └────────────┬───────────────────────────────────┘
         │               │
         │               ▼
         │  ┌────────────────────────────────────────────────┐
         │  │ Google Gemini (gemini-2.0-flash-exp)           │
         │  │ • Input: Full transcript                       │
         │  │ • Prompt: Markdown notes instructions          │
         │  │ • Output: Detailed summary                     │
         │  │ • Filtering: No admin chatter                  │
         │  └────────────┬───────────────────────────────────┘
         │               │
         │               ▼
         │  ┌────────────────────────────────────────────────┐
         │  │ SummarizeResponse                               │
         │  │ {                                               │
         │  │   "summary": "## Overview\n...",   (Markdown) │
         │  │   "original_length": 5000,         (words)    │
         │  │   "summary_length": 1000           (words)    │
         │  │ }                                               │
         │  └────────────┬───────────────────────────────────┘
         │               │
         │               ├─ If languages selected (not 'en'):
         │               │     ▼
         │               │  api.translateText(summary, langs)
         │               │     │
         │               │     ▼ [See Translation Flow]
         │               │     │
         │               │     ▼
         │               │  setSummaryTranslations(langs)
         │               │
         │               ▼
         │  ┌────────────────────────────────────────────────┐
         │  │ Frontend: Display in SummaryView                │
         │  │ • Markdown rendering                           │
         │  │ • Language switcher (if translated)            │
         │  │ • Copy button                                  │
         │  │ • Download options:                            │
         │  │   - Plain text (.txt)                          │
         │  │   - PDF (html2pdf)                             │
         │  │   - PowerPoint (pptxgenjs)                     │
         │  └────────────────────────────────────────────────┘
         │
         ├─── 3. Generate Flashcards ────────┐
         │                                    │
         │  ┌────────────────────────────────▼─────────────────┐
         │  │ Frontend: Flashcard Settings Panel                │
         │  │ • Select difficulty (easy/medium/hard)           │
         │  │ • Click "Generate Flashcards"                    │
         │  └────────────┬──────────────────────────────────────┘
         │               │
         │               ▼
         │  ┌────────────────────────────────────────────────┐
         │  │ useFlashcards Hook                              │
         │  │ • api.generateFlashcards(transcript, difficulty)│
         │  └────────────┬───────────────────────────────────┘
         │               │
         │               ▼
         │  ┌────────────────────────────────────────────────┐
         │  │ POST /api/flashcards [JSON]                     │
         │  │ {                                               │
         │  │   "text": "full transcript...",                │
         │  │   "count": null,              (auto-calculate) │
         │  │   "difficulty": "medium"                       │
         │  │ }                                               │
         │  └────────────┬───────────────────────────────────┘
         │               │
         │               ▼
         │  ┌────────────────────────────────────────────────┐
         │  │ FlashcardGenerator Service                      │
         │  │ • Auto-count: max(5, min(50, words/100))      │
         │  │ • Use TOON format (not JSON)                   │
         │  │ • Create prompt requesting TOON output         │
         │  │ • Call Gemini                                  │
         │  │ • Parse TOON format (regex):                   │
         │  │   Q: Question\nA: Answer\nD: difficulty       │
         │  │ • Calculate token savings vs JSON             │
         │  │ • Return flashcards + savings info             │
         │  └────────────┬───────────────────────────────────┘
         │               │
         │               ▼
         │  ┌────────────────────────────────────────────────┐
         │  │ Google Gemini (gemini-2.0-flash-exp)           │
         │  │ • Input: Transcript + TOON format request     │
         │  │ • Output: TOON-formatted flashcards            │
         │  │ • Efficiency: 40-50% token savings vs JSON    │
         │  └────────────┬───────────────────────────────────┘
         │               │
         │               ▼
         │  ┌────────────────────────────────────────────────┐
         │  │ FlashcardResponse                               │
         │  │ {                                               │
         │  │   "flashcards": [                              │
         │  │     {                                          │
         │  │       "question": "...",                       │
         │  │       "answer": "...",                         │
         │  │       "difficulty": "medium"                   │
         │  │     },                                         │
         │  │     ...                                        │
         │  │   ],                                           │
         │  │   "tokens_saved": 234           (estimation)  │
         │  │ }                                               │
         │  └────────────┬───────────────────────────────────┘
         │               │
         │               ├─ If languages selected (not 'en'):
         │               │     ▼
         │               │  buildFlashcardPayload(cards)
         │               │  with markers: [[CARD_0_QUESTION]]
         │               │     │
         │               │     ▼
         │               │  api.translateText(payload, langs)
         │               │     │
         │               │     ▼ [See Translation Flow]
         │               │     │
         │               │     ▼
         │               │  parseFlashcardTranslation()
         │               │  setFlashcardTranslations(langs)
         │               │
         │               ▼
         │  ┌────────────────────────────────────────────────┐
         │  │ Frontend: Display in FlashcardsView              │
         │  │ • 3D flip animation                            │
         │  │ • Navigation (arrows, space)                   │
         │  │ • Language switcher (if translated)            │
         │  │ • Shuffle button                               │
         │  │ • Progress indicator (e.g., 3/10)             │
         │  │ • Difficulty badge                             │
         │  └────────────────────────────────────────────────┘
         │
         └─── 4. Translate Content ──────────┐
                                             │
            ┌────────────────────────────────▼──────────┐
            │ Frontend: LanguageSelector Component      │
            │ • Checkboxes for 50+ languages            │
            │ • Updates selectedLanguages state         │
            │ • Triggers translations on content gen    │
            └────────────┬───────────────────────────────┘
                         │
                         ▼
            ┌──────────────────────────────────────────┐
            │ useTranslate Hook                         │
            │ • api.translateText(content, langs)      │
            └────────────┬───────────────────────────────┘
                         │
                         ▼
            ┌──────────────────────────────────────────┐
            │ POST /api/translate [JSON]                │
            │ {                                         │
            │   "text": "...",                         │
            │   "target_languages": ["es", "fr", ...]  │
            │ }                                         │
            └────────────┬───────────────────────────────┘
                         │
                         ▼
            ┌──────────────────────────────────────────┐
            │ Translator Service                        │
            │ • For each language:                     │
            │   - Create system prompt                 │
            │   - Create user prompt with lang name   │
            │   - Call Gemini                         │
            │   - Store translation                   │
            │ • Return dict: {lang: translation}      │
            └────────────┬───────────────────────────────┘
                         │
                         ▼
            ┌──────────────────────────────────────────┐
            │ Google Gemini (gemini-2.0-flash-exp)     │
            │ • Parallel calls (not sequential)        │
            │ • Temperature: 0.3 (deterministic)       │
            │ • Preserves markers in flashcard trans   │
            └────────────┬───────────────────────────────┘
                         │
                         ▼
            ┌──────────────────────────────────────────┐
            │ TranslateResponse                         │
            │ {                                         │
            │   "translations": {                      │
            │     "es": "Spanish translation...",      │
            │     "fr": "French translation...",       │
            │     "de": "German translation...",       │
            │     ...                                  │
            │   }                                       │
            │ }                                         │
            └────────────┬───────────────────────────────┘
                         │
                         ▼
            ┌──────────────────────────────────────────┐
            │ Frontend: Language Switcher               │
            │ • SummaryView or FlashcardsView          │
            │ • Dropdown to select displayed language  │
            │ • Render appropriate translation         │
            └──────────────────────────────────────────┘
```

## Data Structure Flowchart: Flashcard Translation

```
Original Flashcards:
┌─────────────────────────────┐
│ Flashcard 1                  │
│ Q: What is Python?          │
│ A: A programming language   │
│ D: easy                      │
└─────────────────────────────┘
┌─────────────────────────────┐
│ Flashcard 2                  │
│ Q: What is OOP?             │
│ A: Object-oriented program  │
│ D: medium                    │
└─────────────────────────────┘

           │
           ▼

buildFlashcardPayload():
┌──────────────────────────────────────────────┐
│ [[CARD_0_QUESTION]] What is Python?          │
│ [[CARD_0_ANSWER]] A programming language    │
│                                              │
│ [[CARD_1_QUESTION]] What is OOP?            │
│ [[CARD_1_ANSWER]] Object-oriented program   │
└──────────────────────────────────────────────┘

           │
           ▼ POST /api/translate

Gemini Translation (Spanish):
┌──────────────────────────────────────────────┐
│ [[CARD_0_QUESTION]] ¿Qué es Python?         │
│ [[CARD_0_ANSWER]] Un lenguaje de programación│
│                                              │
│ [[CARD_1_QUESTION]] ¿Qué es POO?            │
│ [[CARD_1_ANSWER]] Programación orientada... │
└──────────────────────────────────────────────┘

           │
           ▼

parseFlashcardTranslation():
┌─────────────────────────────┐
│ Flashcard 1 (Spanish)        │
│ Q: ¿Qué es Python?          │
│ A: Un lenguaje de prog...   │
│ D: easy                      │
└─────────────────────────────┘
┌─────────────────────────────┐
│ Flashcard 2 (Spanish)        │
│ Q: ¿Qué es POO?             │
│ A: Programación orientada... │
│ D: medium                    │
└─────────────────────────────┘
```

## Component State Management (Home.tsx)

```
Home Component State:
┌──────────────────────────────────────┐
│ transcribe Hook                      │
├──────────────────────────────────────┤
│ • data: TranscribeResponse | null    │
│ • isLoading: boolean                 │
│ • isUploadingFile: boolean           │
│ • uploadProgress: number (0-100)     │
│ • error: string | null               │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│ summarize Hook                       │
├──────────────────────────────────────┤
│ • data: SummarizeResponse | null     │
│ • isLoading: boolean                 │
│ • error: string | null               │
│ • cache: Map<string, Response>       │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│ flashcards Hook                      │
├──────────────────────────────────────┤
│ • data: FlashcardResponse | null     │
│ • isLoading: boolean                 │
│ • error: string | null               │
│ • cache: Map<string, Response>       │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│ translate Hook                       │
├──────────────────────────────────────┤
│ • data: TranslateResponse | null     │
│ • isLoading: boolean                 │
│ • error: string | null               │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│ Local State (useState)                │
├──────────────────────────────────────┤
│ • selectedLanguages: string[]        │
│ • flashcardDifficulty: Difficulty   │
│ • summaryTranslations: Record       │
│ • flashcardTranslations: Record     │
│ • isSummaryGenerating: boolean      │
│ • isFlashcardsGenerating: boolean   │
└──────────────────────────────────────┘
```

## TOON Format Optimization

```
Original JSON Flashcards (150 tokens):
┌───────────────────────────────────────────┐
│ [                                         │
│   {                                       │
│     "question": "What is Python?",       │
│     "answer": "A programming language", │
│     "difficulty": "easy"                 │
│   },                                     │
│   {                                       │
│     "question": "What is OOP?",         │
│     "answer": "Object Oriented Prog",   │
│     "difficulty": "medium"              │
│   }                                      │
│ ]                                        │
└───────────────────────────────────────────┘
        ≈150 tokens / 4 = 37.5 tokens

                    ↓

TOON Format (80 tokens - 47% savings):
┌───────────────────────────────────────────┐
│ Q: What is Python?                       │
│ A: A programming language                │
│ D: easy                                  │
│                                          │
│ Q: What is OOP?                         │
│ A: Object Oriented Programming          │
│ D: medium                                │
└───────────────────────────────────────────┘
        ≈80 tokens / 4 = 20 tokens

Token Savings: 37.5 - 20 = 17.5 tokens (47% reduction)
```

## Error Handling Flow

```
User Action (e.g., Upload File)
        │
        ▼
Frontend Validation
  ├─ File type check
  ├─ File size check
  └─ Throw ValueError if invalid
        │
        ├─ INVALID → Show local error
        │
        ├─ VALID ↓
        │
        ▼
Axios Request
        │
        ├─ Network error → Catch in hook
        │                  → Parse Axios error
        │                  → Set error state
        │                  → Show ErrorMessage
        │
        ├─ Timeout → Same as above
        │
        └─ Response received ↓
                    │
                    ▼
            Response Status
                    │
        ┌───────────┼───────────┐
        │           │           │
    2xx OK      4xx Error   5xx Error
        │           │           │
        ▼           ▼           ▼
    Parse      Get detail  "500: Server error"
    Response   from API    in state.error
        │           │           │
        ✓       SetError    Show message
                Parse/Show

Example: Transcription 400 Error
┌────────────────────────────────────────┐
│ HTTP 400 - Bad Request                 │
│ {                                      │
│   "detail": "File too large. Max size: │
│   524288000 bytes"                     │
│ }                                      │
└────────────────────────────────────────┘
        │
        ▼
Hook: parseError()
        │
        ▼
Extract detail field
        │
        ▼
setError(message)
        │
        ▼
<ErrorMessage message={error} />
        │
        ▼
User sees friendly message
```

## Deployment Architecture

```
┌─────────────────────────────────────────┐
│         GitHub Repository               │
│  ┌─────────────────────────────────────┤
│  │ Branches:                            │
│  │ • main (production)                  │
│  │ • develop (staging)                  │
│  │                                      │
│  │ On push/PR:                          │
│  │ • GitHub Actions triggers            │
│  │ • CI workflows run                   │
│  │   - Backend: lint, test, type-check  │
│  │   - Frontend: lint, build            │
│  │ • Results: Pass/Fail                 │
│  └──────────┬──────────────────────────┘
│             │
│             ▼
├─────────────────────────────────────┐
│ Docker Build & Push                 │
│ ├─ Backend Dockerfile               │
│ │  ├─ FROM python:3.13-slim         │
│ │  ├─ COPY requirements.txt          │
│ │  ├─ pip install                    │
│ │  ├─ COPY app code                  │
│ │  ├─ EXPOSE 8000                    │
│ │  └─ CMD uvicorn                    │
│ │                                    │
│ ├─ Frontend Dockerfile               │
│ │  ├─ FROM node:18-alpine            │
│ │  ├─ npm ci                         │
│ │  ├─ npm run build                  │
│ │  ├─ EXPOSE 5173                    │
│ │  └─ CMD npm run dev                │
│ │                                    │
│ └─ Push to registry                  │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│ Docker Compose (Local Dev)          │
│ ├─ Backend service                  │
│ │  ├─ Build from ./backend          │
│ │  ├─ Expose port 8000              │
│ │  ├─ Env: GEMINI_API_KEY, etc.    │
│ │  ├─ Volume: ./backend:/app        │
│ │  └─ CMD: uvicorn --reload         │
│ │                                    │
│ ├─ Frontend service                 │
│ │  ├─ Build from ./frontend         │
│ │  ├─ Expose port 5173              │
│ │  ├─ Volume: ./frontend:/app       │
│ │  └─ CMD: npm run dev              │
│ │                                    │
│ └─ depends_on: backend              │
│    (frontend waits for backend)      │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│ Production Deployment               │
│ (Railway, Fly.io, or Render)        │
│ ├─ Backend                          │
│ │  ├─ Container from registry       │
│ │  ├─ Environment secrets injected   │
│ │  ├─ Health check: /api/health     │
│ │  ├─ Auto-restart on failure       │
│ │  └─ Scale: Multiple instances     │
│ │                                    │
│ ├─ Frontend                         │
│ │  ├─ Static build output           │
│ │  ├─ Deployed to CDN (Vercel)     │
│ │  ├─ Points to backend API         │
│ │  └─ Auto-deploy on push           │
│ │                                    │
│ └─ Database                         │
│    (None - stateless design)         │
└─────────────────────────────────────┘
```

## Database Schema (N/A - Stateless)

```
Lectura is designed as a STATELESS application:

✓ No user accounts
✓ No persistent storage
✓ No database
✓ No session tracking
✓ No authentication required

Benefits:
• Simple deployment
• Horizontal scalability
• No data privacy concerns
• Reduced operational complexity
• Pay-per-use API model

Trade-offs:
• Users can't save history
• File upload happens every time
• No account customization
• No collaborative features

Future enhancement (if needed):
If user accounts added:
┌────────────────────────────────┐
│ PostgreSQL Database            │
│ ├─ users table                 │
│ ├─ lectures table              │
│ ├─ transcriptions table        │
│ ├─ generated_summaries table   │
│ ├─ flashcards table            │
│ └─ api_usage table             │
└────────────────────────────────┘
```
