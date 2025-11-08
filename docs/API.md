# API Documentation

## Base URL

Development: `http://localhost:8000`

## Endpoints

### Health Check

**GET** `/api/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy"
}
```

---

### Transcribe Audio

**POST** `/api/transcribe`

Transcribe audio file to text.

**Request:**
- Content-Type: `multipart/form-data`
- Body:
  - `file`: Audio file (mp3, wav, etc.)
  - `language`: Language code (default: "en")

**Response:**
```json
{
  "transcript": "Today we'll discuss Python programming...",
  "duration": 305.5,
  "language": "en",
  "tokens_used": 1234
}
```

---

### Summarize Text

**POST** `/api/summarize`

Generate summary from text.

**Request:**
```json
{
  "text": "Long transcript here...",
  "format": "bullet_points"
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

---

### Generate Flashcards

**POST** `/api/flashcards`

Create study flashcards from text.

**Request:**
```json
{
  "text": "Transcript or summary...",
  "count": 10,
  "difficulty": "medium"
}
```

**Response:**
```json
{
  "flashcards": [
    {
      "question": "What is polymorphism?",
      "answer": "The ability of objects to take multiple forms",
      "difficulty": "medium"
    }
  ],
  "tokens_saved": 234
}
```

---

### Translate Text

**POST** `/api/translate`

Translate text to multiple languages.

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

## Error Responses

All endpoints may return error responses:

**400 Bad Request:**
```json
{
  "detail": "Error message"
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Internal server error"
}
```

## Rate Limits

No rate limits in development. Production limits TBD.
