# 🎓 LECTURA - COMPLETE HACKATHON TECHNICAL DESIGN (REVISED)

**Team of 3 | 48 Hours | AI Lecture Notes Generator**

**NO USER ACCOUNTS - Just Gemini API + Frontend/CLI**

---

## 📋 TABLE OF CONTENTS

1. [Project Overview](#project-overview)
2. [Tech Stack](#tech-stack)
3. [Project Structure](#project-structure)
4. [Team Roles & Task Breakdown](#team-roles--task-breakdown)
5. [Development Timeline](#development-timeline)
6. [Setup Instructions](#setup-instructions)
7. [Core Features Implementation](#core-features-implementation)
8. [DevOps & CI/CD](#devops--cicd)
9. [Testing Strategy](#testing-strategy)
10. [Demo Preparation](#demo-preparation)

---

## PROJECT OVERVIEW

### Product Vision
**Lectura** transforms lecture recordings into accessible study materials using AI. Upload audio → get transcripts, summaries, flashcards, and translations in 60+ languages.

### Target Tracks
- ✅ **Reach Capital**: AI for learning (lecture comprehension)
- ✅ **Student Experience**: Helps students study more effectively
- ✅ **EquiTech**: Accessibility features (translation, disabilities support)
- ❌ **Auth0**: NOT using (no user accounts needed)

### Core Value Proposition
**Problem:** Students struggle to keep up with lectures, miss classes, or English isn't their first language.

**Solution:** AI generates comprehensive study materials from any lecture recording with accessibility features built-in.

### Architecture
**Simple stateless design:**
- Frontend uploads audio file
- Backend processes with Gemini API
- Returns results immediately
- No database, no users, no auth

---

## TECH STACK

### Backend (Python API)
```yaml
Core:
  - Python 3.11+
  - FastAPI (REST API)
  - Uvicorn (ASGI server)
  - Pydantic (data validation)

AI/ML:
  - google-generativeai (Gemini API)
  - pydub (audio processing)

Utilities:
  - python-dotenv (config)
  - httpx (async HTTP)

Format Optimization:
  - TOON format (via subprocess to CLI)
```

### Frontend (React Web App)
```yaml
Framework:
  - React 18 + TypeScript
  - Vite (build tool)

UI:
  - Tailwind CSS
  - shadcn/ui components
  - lucide-react (icons)

HTTP:
  - Axios or fetch

State:
  - React hooks (useState, useEffect)
  - No complex state management needed
```

### DevOps
```yaml
Version Control:
  - Git + GitHub

CI/CD:
  - GitHub Actions

Code Quality:
  - Black (formatter)
  - Flake8 (linter)
  - Pylint (static analysis)
  - mypy (type checking)
  - pytest (testing)
  - pre-commit hooks
  - ESLint + Prettier (frontend)

Containerization:
  - Docker
  - Docker Compose

Deployment (Optional):
  - Backend: Railway/Fly.io/Render
  - Frontend: Vercel/Netlify
```

---

## PROJECT STRUCTURE

```
lectura/
├── .github/
│   └── workflows/
│       ├── ci-backend.yml            # Backend tests
│       ├── ci-frontend.yml           # Frontend tests
│       └── deploy.yml                # Optional deployment
│
├── backend/
│   ├── src/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI app entry
│   │   │
│   │   ├── api/                      # API routes
│   │   │   ├── __init__.py
│   │   │   ├── health.py             # Health check
│   │   │   ├── transcribe.py         # POST /api/transcribe
│   │   │   ├── summarize.py          # POST /api/summarize
│   │   │   ├── flashcards.py         # POST /api/flashcards
│   │   │   └── translate.py          # POST /api/translate
│   │   │
│   │   ├── services/                 # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── gemini.py             # Gemini API client
│   │   │   ├── transcriber.py        # Audio → text
│   │   │   ├── summarizer.py         # Text → summary
│   │   │   ├── flashcards.py         # Text → flashcards
│   │   │   ├── translator.py         # Text → translations
│   │   │   └── toon.py               # TOON format helper
│   │   │
│   │   ├── models/                   # Data models
│   │   │   ├── __init__.py
│   │   │   └── schemas.py            # Pydantic request/response models
│   │   │
│   │   └── utils/                    # Helpers
│   │       ├── __init__.py
│   │       ├── audio.py              # Audio processing
│   │       ├── config.py             # Settings
│   │       └── logger.py             # Logging
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── unit/
│   │   │   ├── test_gemini.py
│   │   │   ├── test_transcriber.py
│   │   │   └── test_flashcards.py
│   │   ├── integration/
│   │   │   └── test_api.py
│   │   └── fixtures/
│   │       └── sample_audio.mp3
│   │
│   ├── .env.example
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── Dockerfile
│   └── pyproject.toml
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AudioUploader.tsx     # File upload component
│   │   │   ├── ResultsDisplay.tsx    # Show results
│   │   │   ├── TranscriptView.tsx    # Display transcript
│   │   │   ├── FlashcardsView.tsx    # Display flashcards
│   │   │   ├── SummaryView.tsx       # Display summary
│   │   │   └── LanguageSelector.tsx  # Translation options
│   │   │
│   │   ├── pages/
│   │   │   └── Home.tsx              # Main page
│   │   │
│   │   ├── hooks/
│   │   │   ├── useTranscribe.ts      # API call hook
│   │   │   └── useFlashcards.ts      # API call hook
│   │   │
│   │   ├── types/
│   │   │   └── api.ts                # TypeScript types
│   │   │
│   │   ├── lib/
│   │   │   └── api.ts                # API client
│   │   │
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   │
│   ├── public/
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── .eslintrc.json
│   └── .prettierrc
│
├── docs/
│   ├── API.md                        # API documentation
│   ├── ARCHITECTURE.md               # System design
│   └── DEPLOYMENT.md                 # How to deploy
│
├── scripts/
│   ├── setup.sh                      # Initial setup
│   └── dev.sh                        # Run dev servers
│
├── docker-compose.yml                # Run entire stack
├── .gitignore
├── README.md
└── LICENSE
```

---

## TEAM ROLES & TASK BREAKDOWN

### 👤 **Person 1: AI/Backend Lead** (50% of work)

**Focus:** Gemini integration, FastAPI endpoints, AI features

#### Day 1 (Hours 0-12):

**Setup (Hours 0-2):**
- [ ] Create `backend/` structure
- [ ] Install dependencies (FastAPI, Gemini SDK, etc.)
- [ ] Set up `.env` with `GEMINI_API_KEY`
- [ ] Create `main.py` with basic FastAPI app
- [ ] Test Gemini API connection

**Core Services (Hours 2-8):**
- [ ] Implement `services/gemini.py` - Gemini client wrapper
- [ ] Implement `services/transcriber.py` - Audio → text
- [ ] Implement `services/summarizer.py` - Text → summary
- [ ] Test with sample audio files
- [ ] Prompt engineering for quality

**API Endpoints (Hours 8-12):**
- [ ] Create `api/transcribe.py` - POST endpoint
- [ ] Create `api/summarize.py` - POST endpoint
- [ ] Test endpoints with curl/Postman
- [ ] Add error handling

#### Day 1 (Hours 12-24):

**Advanced Features (Hours 12-18):**
- [ ] Implement `services/flashcards.py` - Generate Q&A
- [ ] Implement `services/translator.py` - Multi-language
- [ ] Create corresponding API endpoints
- [ ] Integrate TOON format for token efficiency

**Optimization (Hours 18-24):**
- [ ] Add request validation (Pydantic models)
- [ ] Add CORS middleware for frontend
- [ ] Implement file upload handling
- [ ] Audio format conversion (if needed)
- [ ] Write unit tests for services

#### Day 2 (Hours 24-36):

**Polish & Testing (Hours 24-30):**
- [ ] Integration tests for all endpoints
- [ ] Error handling improvements
- [ ] Add health check endpoint
- [ ] Performance optimization
- [ ] Add logging

**TOON Integration (Hours 30-36):**
- [ ] Benchmark token usage (JSON vs TOON)
- [ ] Document token savings
- [ ] Create comparison charts
- [ ] Optimize prompts further

#### Day 2 (Hours 36-48):

**Final Push:**
- [ ] Bug fixes from frontend integration
- [ ] API documentation
- [ ] Demo preparation
- [ ] Deploy backend (Railway/Fly.io)

**Key Files:**
```python
backend/src/main.py
backend/src/api/transcribe.py
backend/src/api/flashcards.py
backend/src/services/gemini.py
backend/src/services/transcriber.py
backend/src/services/flashcards.py
backend/tests/integration/test_api.py
```

---

### 👤 **Person 2: Frontend Lead** (35% of work)

**Focus:** React UI, file upload, results display

#### Day 1 (Hours 0-12):

**Setup (Hours 0-3):**
- [ ] Create React app with Vite + TypeScript
- [ ] Install Tailwind CSS + shadcn/ui
- [ ] Set up project structure
- [ ] Create basic layout
- [ ] Test dev server running

**Core Components (Hours 3-9):**
- [ ] Build `AudioUploader.tsx` - Drag & drop file upload
- [ ] Build `ResultsDisplay.tsx` - Tabbed results view
- [ ] Build `TranscriptView.tsx` - Show transcript
- [ ] Style with Tailwind
- [ ] Add loading states

**API Integration (Hours 9-12):**
- [ ] Create `lib/api.ts` - API client
- [ ] Implement file upload to backend
- [ ] Display transcription results
- [ ] Add error handling

#### Day 1 (Hours 12-24):

**Feature Components (Hours 12-18):**
- [ ] Build `FlashcardsView.tsx` - Card flip animation
- [ ] Build `SummaryView.tsx` - Formatted summary
- [ ] Build `LanguageSelector.tsx` - Multi-language options
- [ ] Add progress indicators

**Polish UI (Hours 18-24):**
- [ ] Make it responsive (mobile-friendly)
- [ ] Add animations/transitions
- [ ] Improve UX (copy buttons, download, etc.)
- [ ] Test on different screen sizes

#### Day 2 (Hours 24-36):

**Advanced Features (Hours 24-30):**
- [ ] Add export functionality (download as PDF/Markdown)
- [ ] Add "Try with sample" demo feature
- [ ] Implement batch processing UI (if time)
- [ ] Add accessibility features (ARIA labels, keyboard nav)

**Testing & Polish (Hours 30-36):**
- [ ] Cross-browser testing
- [ ] Fix bugs
- [ ] Optimize bundle size
- [ ] Add loading skeletons

#### Day 2 (Hours 36-48):

**Deployment & Demo:**
- [ ] Deploy to Vercel/Netlify
- [ ] Test production build
- [ ] Create demo video/GIF
- [ ] Final polish

**Key Files:**
```typescript
frontend/src/components/AudioUploader.tsx
frontend/src/components/FlashcardsView.tsx
frontend/src/lib/api.ts
frontend/src/App.tsx
```

---

### 👤 **Person 3: DevOps/Testing/Integration** (15% of work)

**Focus:** CI/CD, testing, documentation, integration support

#### Day 1 (Hours 0-12):

**DevOps Setup (Hours 0-4):**
- [ ] Set up GitHub repo
- [ ] Create `.gitignore` files
- [ ] Set up GitHub Actions workflows
- [ ] Configure pre-commit hooks (backend)
- [ ] Set up ESLint/Prettier (frontend)

**Testing Infrastructure (Hours 4-8):**
- [ ] Set up pytest for backend
- [ ] Create test fixtures
- [ ] Set up Vitest for frontend
- [ ] Write initial tests
- [ ] Configure code coverage

**Documentation (Hours 8-12):**
- [ ] Write comprehensive README
- [ ] Create API documentation
- [ ] Document setup instructions
- [ ] Create architecture diagram

#### Day 1 (Hours 12-24):

**Testing (Hours 12-18):**
- [ ] Write unit tests for backend services
- [ ] Write integration tests for API
- [ ] Write component tests for frontend
- [ ] Ensure >70% code coverage

**CI/CD (Hours 18-24):**
- [ ] Backend CI running (lint, test, type-check)
- [ ] Frontend CI running (lint, test, build)
- [ ] Docker setup for easy deployment
- [ ] Docker Compose for local dev

#### Day 2 (Hours 24-36):

**Integration Support (Hours 24-30):**
- [ ] Help connect frontend ↔ backend
- [ ] Debug CORS issues
- [ ] Test full flow end-to-end
- [ ] Performance testing

**Demo Materials (Hours 30-36):**
- [ ] Create demo script
- [ ] Record demo video
- [ ] Create pitch deck slides
- [ ] Prepare token savings charts

#### Day 2 (Hours 36-48):

**Final Push:**
- [ ] Bug triage and fixes
- [ ] Final testing
- [ ] Demo rehearsal
- [ ] Backup plans ready

**Key Files:**
```yaml
.github/workflows/ci-backend.yml
.github/workflows/ci-frontend.yml
docker-compose.yml
README.md
docs/API.md
```

---

## DEVELOPMENT TIMELINE

### 🕐 **HOUR 0-4: Foundation**

**All Team - Kickoff Meeting (30 min):**
- [ ] Review plan
- [ ] Assign tasks
- [ ] Set up communication (Discord/Slack)
- [ ] Create GitHub repo

**Person 1 (Backend):**
- [ ] FastAPI app running
- [ ] Gemini API connected
- [ ] First transcription working

**Person 2 (Frontend):**
- [ ] React app running
- [ ] Basic UI layout
- [ ] File upload component

**Person 3 (DevOps):**
- [ ] GitHub Actions configured
- [ ] Pre-commit hooks installed
- [ ] README started

**Milestone:** Both servers running, can transcribe test audio

---

### 🕐 **HOUR 4-12: Core Features**

**Person 1:**
- [ ] Transcription API endpoint working
- [ ] Summarization API endpoint working
- [ ] Both tested with Postman

**Person 2:**
- [ ] Frontend can upload file
- [ ] Frontend displays transcript
- [ ] Frontend displays summary
- [ ] Nice loading states

**Person 3:**
- [ ] Tests written for backend
- [ ] CI passing
- [ ] Docker Compose working

**Milestone:** End-to-end flow works (upload → transcribe → display)

---

### 🕐 **HOUR 12-24: Feature Complete**

**Person 1:**
- [ ] Flashcards generation working
- [ ] Translation working (3+ languages)
- [ ] TOON integration complete
- [ ] All endpoints tested

**Person 2:**
- [ ] Flashcards UI with flip animation
- [ ] Translation selector working
- [ ] Export functionality
- [ ] Responsive design done

**Person 3:**
- [ ] Full test coverage
- [ ] All linting passing
- [ ] Documentation complete
- [ ] API docs generated

**Milestone:** All features working, polished UI

---

### 🕐 **HOUR 24-36: Polish & Optimization**

**Person 1:**
- [ ] Token usage benchmarks
- [ ] Performance optimization
- [ ] Error handling polished
- [ ] Backend deployed

**Person 2:**
- [ ] UI animations smooth
- [ ] Accessibility features
- [ ] Cross-browser tested
- [ ] Frontend deployed

**Person 3:**
- [ ] Demo script finalized
- [ ] Demo video recorded
- [ ] Pitch deck ready
- [ ] Architecture diagram complete

**Milestone:** Production deployed, demo ready

---

### 🕐 **HOUR 36-48: Demo Preparation**

**All Team:**
- [ ] Practice pitch 5+ times
- [ ] Test deployed app thoroughly
- [ ] Prepare for technical questions
- [ ] Backup demo video ready

**Final Checklist:**
- [ ] Live demo URL works
- [ ] GitHub repo polished
- [ ] README has screenshots
- [ ] Can explain token savings
- [ ] Can explain accessibility features
- [ ] Judges can try it themselves

---

## CORE FEATURES IMPLEMENTATION

### Backend API Endpoints

#### 1. POST `/api/transcribe`

**Request:**
```json
{
  "audio": "<base64-encoded-audio-file>",
  "language": "en"
}
```

**Response:**
```json
{
  "transcript": "Today we'll discuss Python programming...",
  "duration": 305.5,
  "language": "en",
  "tokens_used": 1234
}
```

**Implementation:**
```python
# backend/src/api/transcribe.py
from fastapi import APIRouter, UploadFile, File
from src.services.transcriber import Transcriber
from src.models.schemas import TranscribeResponse

router = APIRouter()

@router.post("/transcribe", response_model=TranscribeResponse)
async def transcribe_audio(
    file: UploadFile = File(...),
    language: str = "en"
):
    transcriber = Transcriber()
    result = await transcriber.transcribe(file, language)
    return result
```

#### 2. POST `/api/summarize`

**Request:**
```json
{
  "text": "Long transcript here...",
  "format": "bullet_points"  // or "paragraph"
}
```

**Response:**
```json
{
  "summary": "Key points:\n- Topic 1\n- Topic 2...",
  "original_length": 5000,
  "summary_length": 500
}
```

#### 3. POST `/api/flashcards`

**Request:**
```json
{
  "text": "Transcript or summary...",
  "count": 10,
  "difficulty": "medium"
}
```

**Response (using TOON for efficiency):**
```json
{
  "flashcards": [
    {
      "question": "What is polymorphism?",
      "answer": "The ability of objects to take multiple forms",
      "difficulty": "medium"
    }
  ],
  "tokens_saved": 234  // vs JSON format
}
```

#### 4. POST `/api/translate`

**Request:**
```json
{
  "text": "English text...",
  "target_languages": ["es", "fr", "zh"]
}
```

**Response:**
```json
{
  "translations": {
    "es": "Texto en español...",
    "fr": "Texte en français...",
    "zh": "中文文本..."
  }
}
```

---

### Frontend Components

#### AudioUploader Component

```typescript
// frontend/src/components/AudioUploader.tsx
import { useState } from 'react'
import { Upload } from 'lucide-react'

export function AudioUploader({ onUpload }: { onUpload: (file: File) => void }) {
  const [dragActive, setDragActive] = useState(false)

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setDragActive(false)

    const file = e.dataTransfer.files[0]
    if (file && file.type.startsWith('audio/')) {
      onUpload(file)
    }
  }

  return (
    <div
      className={`border-2 border-dashed rounded-lg p-12 text-center ${
        dragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300'
      }`}
      onDragOver={(e) => { e.preventDefault(); setDragActive(true) }}
      onDragLeave={() => setDragActive(false)}
      onDrop={handleDrop}
    >
      <Upload className="mx-auto h-12 w-12 text-gray-400" />
      <p className="mt-2 text-sm text-gray-600">
        Drag and drop audio file or click to browse
      </p>
      <input
        type="file"
        accept="audio/*"
        className="hidden"
        onChange={(e) => e.target.files?.[0] && onUpload(e.target.files[0])}
      />
    </div>
  )
}
```

#### FlashcardsView Component

```typescript
// frontend/src/components/FlashcardsView.tsx
import { useState } from 'react'

interface Flashcard {
  question: string
  answer: string
  difficulty: string
}

export function FlashcardsView({ cards }: { cards: Flashcard[] }) {
  const [currentIndex, setCurrentIndex] = useState(0)
  const [flipped, setFlipped] = useState(false)

  const card = cards[currentIndex]

  return (
    <div className="max-w-2xl mx-auto">
      <div
        className="bg-white rounded-lg shadow-lg p-8 min-h-[300px] cursor-pointer"
        onClick={() => setFlipped(!flipped)}
      >
        <div className="text-center">
          {!flipped ? (
            <>
              <p className="text-sm text-gray-500 mb-4">Question</p>
              <p className="text-xl">{card.question}</p>
            </>
          ) : (
            <>
              <p className="text-sm text-gray-500 mb-4">Answer</p>
              <p className="text-xl">{card.answer}</p>
            </>
          )}
        </div>
      </div>

      <div className="flex justify-between mt-4">
        <button
          onClick={() => setCurrentIndex(Math.max(0, currentIndex - 1))}
          disabled={currentIndex === 0}
        >
          Previous
        </button>
        <span>{currentIndex + 1} / {cards.length}</span>
        <button
          onClick={() => setCurrentIndex(Math.min(cards.length - 1, currentIndex + 1))}
          disabled={currentIndex === cards.length - 1}
        >
          Next
        </button>
      </div>
    </div>
  )
}
```

---

## DEVOPS & CI/CD

### GitHub Actions - Backend CI

```yaml
# .github/workflows/ci-backend.yml
name: Backend CI

on:
  push:
    branches: [main, develop]
    paths:
      - 'backend/**'
  pull_request:
    paths:
      - 'backend/**'

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'
          cache-dependency-path: backend/requirements.txt

      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Lint with flake8
        run: |
          cd backend
          flake8 src/ --max-line-length=100

      - name: Format check with black
        run: |
          cd backend
          black --check src/

      - name: Type check with mypy
        run: |
          cd backend
          mypy src/

      - name: Test with pytest
        run: |
          cd backend
          pytest --cov=src --cov-report=xml --cov-report=term

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./backend/coverage.xml
          flags: backend
```

### GitHub Actions - Frontend CI

```yaml
# .github/workflows/ci-frontend.yml
name: Frontend CI

on:
  push:
    branches: [main, develop]
    paths:
      - 'frontend/**'
  pull_request:
    paths:
      - 'frontend/**'

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - name: Install dependencies
        run: |
          cd frontend
          npm ci

      - name: Lint
        run: |
          cd frontend
          npm run lint

      - name: Type check
        run: |
          cd frontend
          npm run type-check

      - name: Test
        run: |
          cd frontend
          npm run test

      - name: Build
        run: |
          cd frontend
          npm run build
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    volumes:
      - ./backend:/app
    command: uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: npm run dev -- --host
    depends_on:
      - backend
```

### Backend Dockerfile

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Dockerfile

```dockerfile
# frontend/Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]
```

---

## TESTING STRATEGY

### Backend Tests

```python
# backend/tests/unit/test_transcriber.py
import pytest
from src.services.transcriber import Transcriber

@pytest.mark.asyncio
async def test_transcribe_audio():
    """Test basic transcription"""
    transcriber = Transcriber()

    # Use fixture audio file
    with open("tests/fixtures/sample_audio.mp3", "rb") as f:
        result = await transcriber.transcribe(f, language="en")

    assert result["transcript"]
    assert len(result["transcript"]) > 0
    assert result["language"] == "en"

@pytest.mark.asyncio
async def test_transcribe_invalid_format():
    """Test error handling for invalid audio"""
    transcriber = Transcriber()

    with pytest.raises(ValueError):
        await transcriber.transcribe(None, language="en")
```

```python
# backend/tests/integration/test_api.py
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_check():
    """Test health endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_transcribe_endpoint():
    """Test transcription endpoint"""
    with open("tests/fixtures/sample_audio.mp3", "rb") as f:
        response = client.post(
            "/api/transcribe",
            files={"file": ("test.mp3", f, "audio/mpeg")},
            data={"language": "en"}
        )

    assert response.status_code == 200
    data = response.json()
    assert "transcript" in data
    assert "duration" in data
```

### Frontend Tests

```typescript
// frontend/src/components/__tests__/AudioUploader.test.tsx
import { render, screen, fireEvent } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import { AudioUploader } from '../AudioUploader'

describe('AudioUploader', () => {
  it('renders upload area', () => {
    render(<AudioUploader onUpload={vi.fn()} />)
    expect(screen.getByText(/drag and drop/i)).toBeInTheDocument()
  })

  it('calls onUpload when file is selected', () => {
    const mockOnUpload = vi.fn()
    render(<AudioUploader onUpload={mockOnUpload} />)

    const file = new File(['audio'], 'test.mp3', { type: 'audio/mp3' })
    const input = screen.getByLabelText(/upload/i)

    fireEvent.change(input, { target: { files: [file] } })

    expect(mockOnUpload).toHaveBeenCalledWith(file)
  })
})
```

---

## DEMO PREPARATION

### Demo Script (3 minutes)

**Introduction (30 seconds):**
> "Hi, we're Team Lectura. Students struggle to keep up with lectures—they miss classes, English isn't their first language, or they just need better study materials. We built Lectura to solve this using AI."

**Live Demo (2 minutes):**
1. **Upload audio** (5-10 second sample lecture clip)
   - "I'm uploading a lecture about Python programming..."

2. **Show transcription** (appears in ~3 seconds)
   - "Gemini transcribes it accurately in seconds..."

3. **Show summary** (click tab)
   - "Generates a concise summary of key points..."

4. **Show flashcards** (flip through 2-3)
   - "Creates interactive flashcards for studying..."

5. **Show translation** (select Spanish)
   - "Translates to 60+ languages for accessibility..."

**Technical Highlight (30 seconds):**
> "We optimized token usage with TOON format, reducing API costs by 40% compared to standard JSON. This makes it sustainable to process thousands of lectures."

**Closing:**
> "Lectura makes education more accessible. Try it yourself at [URL]."

### Backup Plans

1. **Video demo** - Pre-recorded walkthrough if internet fails
2. **Local demo** - Docker Compose running on laptop
3. **Screenshots** - High-quality images of each feature
4. **Deployed app** - Multiple team members have the URL

### Pitch Deck Slides

1. **Title slide** - Team name, project name, tagline
2. **Problem** - Students struggle with lectures
3. **Solution** - AI-powered study materials
4. **Demo** - Live or video
5. **Technology** - Gemini API, TOON optimization, React
6. **Impact** - Accessibility (60+ languages), token savings (40%)
7. **Try it** - QR code + URL

---

## SETUP INSTRUCTIONS

### Initial Setup (All Team Members)

```bash
# Clone repo
git clone https://github.com/your-team/lectura.git
cd lectura

# Backend setup
cd backend
python3.11 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Create .env file
cp .env.example .env
# Add your GEMINI_API_KEY to .env

# Install pre-commit hooks
pre-commit install

# Run backend
uvicorn src.main:app --reload

# In new terminal - Frontend setup
cd frontend
npm install

# Run frontend
npm run dev

# Or use Docker Compose (easiest)
docker-compose up
```

### Environment Variables

```bash
# backend/.env.example
GEMINI_API_KEY=your_gemini_api_key_here
ENVIRONMENT=development
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:5173
MAX_FILE_SIZE=10485760  # 10MB
```

---

## FINAL CHECKLIST

### 4 Hours Before Submission

- [ ] All features working end-to-end
- [ ] Both servers deployed and accessible
- [ ] GitHub repo is public and polished
- [ ] README has clear instructions and screenshots
- [ ] Demo video recorded and uploaded
- [ ] Pitch deck finalized
- [ ] Team has practiced pitch 5+ times

### 1 Hour Before Demo

- [ ] Test deployed app on fresh browser
- [ ] Confirm internet connection
- [ ] Have backup demo video ready
- [ ] All team members know their speaking parts
- [ ] Laptop charged, backup laptop ready

---

## SUCCESS METRICS

**What judges will evaluate:**

1. **Technical Implementation** (40%)
   - Clean code architecture
   - Proper error handling
   - Tests and CI/CD
   - Token optimization (TOON)

2. **User Experience** (30%)
   - Intuitive interface
   - Fast response times
   - Mobile-friendly
   - Accessibility features

3. **Innovation** (20%)
   - Novel use of Gemini API
   - TOON format optimization
   - Multi-language support

4. **Presentation** (10%)
   - Clear problem/solution
   - Confident delivery
   - Working demo

**Our advantages:**
✅ Solves real student problem
✅ Beautiful, polished UI
✅ Technical depth (TOON optimization)
✅ Accessibility focus (translations)
✅ Actually works (deployed + demo)

---

## COPY THIS TO CLAUDE CODE

**To get started immediately in Claude Code terminal:**

```bash
# Create project structure
mkdir -p lectura/{backend/{src/{api,services,models,utils},tests/{unit,integration,fixtures}},frontend/src/{components,pages,hooks,types,lib},.github/workflows,docs,scripts}

# Initialize backend
cd lectura/backend
python3.11 -m venv venv
source venv/bin/activate

# Create requirements files
cat > requirements.txt << EOF
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
google-generativeai==0.3.0
python-multipart==0.0.6
pydub==0.25.1
python-dotenv==1.0.0
httpx==0.25.2
EOF

cat > requirements-dev.txt << EOF
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
httpx==0.25.2
black==23.12.0
flake8==6.1.0
pylint==3.0.3
mypy==1.7.1
pre-commit==3.6.0
EOF

pip install -r requirements.txt
pip install -r requirements-dev.txt

# Initialize frontend
cd ../frontend
npm create vite@latest . -- --template react-ts
npm install
npm install -D tailwindcss postcss autoprefixer
npm install axios lucide-react

# Initialize git
cd ..
git init
echo "Tell me what file to create next and I'll generate the complete code!"
```

**READY TO BUILD. LET'S WIN THIS HACKATHON! 🚀**
