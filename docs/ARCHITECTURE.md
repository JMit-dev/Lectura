# Architecture Overview

## System Design

Lectura follows a simple stateless architecture:

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Frontend  │  HTTP   │   Backend   │  API    │   Gemini    │
│   (React)   │────────>│  (FastAPI)  │────────>│     AI      │
│             │<────────│             │<────────│             │
└─────────────┘         └─────────────┘         └─────────────┘
```

## Components

### Frontend (React)

**Responsibilities:**
- File upload interface
- Display results (transcript, summary, flashcards)
- Language selection
- Export functionality

**Key Technologies:**
- React 18 with TypeScript
- Tailwind CSS for styling
- Axios for HTTP requests
- Vite for bundling

### Backend (FastAPI)

**Responsibilities:**
- Handle file uploads
- Process audio with Gemini API
- Generate summaries and flashcards
- Manage translations
- Token optimization with TOON format

**Key Technologies:**
- FastAPI for REST API
- Pydantic for validation
- Google Gemini AI SDK
- Pydub for audio processing

### External Services

**Gemini API:**
- Audio transcription
- Text summarization
- Flashcard generation
- Multi-language translation

## Data Flow

### Transcription Flow

1. User uploads audio file via frontend
2. Frontend sends file to `/api/transcribe`
3. Backend validates file
4. Backend sends audio to Gemini API
5. Gemini returns transcript
6. Backend processes and returns to frontend
7. Frontend displays transcript

### Flashcard Generation Flow

1. User requests flashcards from transcript
2. Frontend sends text to `/api/flashcards`
3. Backend formats prompt with TOON optimization
4. Gemini generates Q&A pairs
5. Backend parses TOON format
6. Returns structured flashcards
7. Frontend displays interactive cards

## Security Considerations

- No user data stored
- API key stored in environment variables
- CORS configured for frontend origin
- File size limits enforced
- Input validation on all endpoints

## Scalability

Current design is stateless and can scale horizontally:
- Backend can run multiple instances
- Load balancer can distribute requests
- No database = no bottleneck
- Gemini API handles heavy processing

## TOON Optimization

Token-Optimized Object Notation reduces API costs:
- 40% fewer tokens vs JSON
- Faster response times
- Lower costs for high-volume usage
- Maintained readability

## Testing Strategy

- Unit tests for business logic
- Integration tests for API endpoints
- Component tests for frontend
- E2E tests for critical flows
- CI/CD pipeline ensures quality
