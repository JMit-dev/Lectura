# 🧪 Lectura API Usage Examples

## Base URL
```
http://localhost:8000
```

## Available Endpoints

### 1. Health Check
```bash
curl http://localhost:8000/api/health
```

**Response:**
```json
{"status": "healthy"}
```

---

### 2. Summarize Text

**Endpoint:** `POST /api/summarize`

**Example:**
```bash
curl -X POST http://localhost:8000/api/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Python is a high-level, interpreted programming language. It emphasizes code readability and simplicity. Python supports multiple programming paradigms including procedural, object-oriented, and functional programming. It has a large standard library and active community.",
    "format": "bullet_points"
  }'
```

**Response:**
```json
{
  "summary": "• Python is a high-level, interpreted language\n• Emphasizes code readability and simplicity\n• Supports multiple programming paradigms\n• Has extensive standard library and community",
  "original_length": 45,
  "summary_length": 25
}
```

**Formats:** `bullet_points` or `paragraph`

---

### 3. Generate Flashcards (with TOON format!)

**Endpoint:** `POST /api/flashcards`

**Example:**
```bash
curl -X POST http://localhost:8000/api/flashcards \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Photosynthesis is the process by which plants use sunlight, water, and carbon dioxide to create oxygen and energy in the form of sugar. This process occurs in the chloroplasts of plant cells. The light-dependent reactions occur in the thylakoid membranes, while the Calvin cycle occurs in the stroma.",
    "count": 5,
    "difficulty": "medium"
  }'
```

**Response:**
```json
{
  "flashcards": [
    {
      "question": "What is photosynthesis?",
      "answer": "The process by which plants use sunlight, water, and CO2 to create oxygen and sugar",
      "difficulty": "medium"
    },
    {
      "question": "Where does photosynthesis occur in plant cells?",
      "answer": "In the chloroplasts",
      "difficulty": "medium"
    }
  ],
  "tokens_saved": 124
}
```

**Difficulty:** `easy`, `medium`, or `hard`

---

### 4. Transcribe Audio

**Endpoint:** `POST /api/transcribe`

**Example (with audio file):**
```bash
curl -X POST http://localhost:8000/api/transcribe \
  -F "file=@/path/to/your/lecture.mp3" \
  -F "language=en"
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

**Supported formats:** mp3, wav, m4a, ogg, flac
**Supported languages:** en, es, fr, de, it, pt, zh, ja, ko, etc.

---

## 🔥 Full Workflow Example

### Step 1: Transcribe Audio
```bash
# Transcribe a lecture
curl -X POST http://localhost:8000/api/transcribe \
  -F "file=@lecture.mp3" \
  -F "language=en" \
  > transcript.json

# Extract just the transcript text
cat transcript.json | jq -r '.transcript' > transcript.txt
```

### Step 2: Summarize the Transcript
```bash
# Read transcript and summarize
TRANSCRIPT=$(cat transcript.txt)
curl -X POST http://localhost:8000/api/summarize \
  -H "Content-Type: application/json" \
  -d "{
    \"text\": \"$TRANSCRIPT\",
    \"format\": \"bullet_points\"
  }" > summary.json
```

### Step 3: Generate Flashcards
```bash
# Generate flashcards from transcript
curl -X POST http://localhost:8000/api/flashcards \
  -H "Content-Type: application/json" \
  -d "{
    \"text\": \"$TRANSCRIPT\",
    \"count\": 10,
    \"difficulty\": \"medium\"
  }" > flashcards.json
```

### Step 4: View Results
```bash
# Pretty print the flashcards
cat flashcards.json | jq '.flashcards[]'
```

---

## 🐍 Python Example

```python
import requests

# Base URL
BASE_URL = "http://localhost:8000"

# 1. Transcribe audio
with open("lecture.mp3", "rb") as audio_file:
    response = requests.post(
        f"{BASE_URL}/api/transcribe",
        files={"file": audio_file},
        data={"language": "en"}
    )
    transcript = response.json()["transcript"]
    print(f"Transcript: {transcript[:100]}...")

# 2. Summarize
response = requests.post(
    f"{BASE_URL}/api/summarize",
    json={
        "text": transcript,
        "format": "bullet_points"
    }
)
summary = response.json()["summary"]
print(f"\nSummary:\n{summary}")

# 3. Generate flashcards
response = requests.post(
    f"{BASE_URL}/api/flashcards",
    json={
        "text": transcript,
        "count": 10,
        "difficulty": "medium"
    }
)
flashcards = response.json()["flashcards"]
print(f"\nGenerated {len(flashcards)} flashcards!")

for i, card in enumerate(flashcards, 1):
    print(f"\n{i}. Q: {card['question']}")
    print(f"   A: {card['answer']}")
```

---

## 🌐 JavaScript/TypeScript Example (for Frontend)

```javascript
const BASE_URL = 'http://localhost:8000';

// Transcribe audio
async function transcribeAudio(audioFile) {
  const formData = new FormData();
  formData.append('file', audioFile);
  formData.append('language', 'en');

  const response = await fetch(`${BASE_URL}/api/transcribe`, {
    method: 'POST',
    body: formData,
  });

  return await response.json();
}

// Summarize text
async function summarizeText(text, format = 'bullet_points') {
  const response = await fetch(`${BASE_URL}/api/summarize`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, format }),
  });

  return await response.json();
}

// Generate flashcards
async function generateFlashcards(text, count = 10, difficulty = 'medium') {
  const response = await fetch(`${BASE_URL}/api/flashcards`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, count, difficulty }),
  });

  return await response.json();
}

// Usage
const audioFile = document.querySelector('#audio-input').files[0];
const result = await transcribeAudio(audioFile);
console.log('Transcript:', result.transcript);

const summary = await summarizeText(result.transcript);
console.log('Summary:', summary.summary);

const flashcards = await generateFlashcards(result.transcript, 10, 'medium');
console.log('Flashcards:', flashcards);
```

---

## 🧪 Testing Tips

### 1. Use Swagger UI (Easiest!)
Go to http://localhost:8000/docs and click "Try it out" on any endpoint.

### 2. Use Postman
Import the OpenAPI spec from http://localhost:8000/openapi.json

### 3. Sample Text for Testing
```
"Artificial intelligence (AI) is intelligence demonstrated by machines,
in contrast to natural intelligence displayed by animals including humans.
AI research has been defined as the field of study of intelligent agents,
which refers to any system that perceives its environment and takes actions
that maximize its chance of achieving its goals."
```

---

## ⚠️ Common Issues

### CORS Error
If you're calling from a different origin, make sure the frontend is running on `http://localhost:5173` or update CORS settings in `backend/src/main.py`.

### File Too Large
Max file size is 25MB. Compress or trim longer audio files.

### Invalid Format
Use supported audio formats: mp3, wav, m4a, ogg, flac

---

## 💰 Token Savings with TOON

Notice the `tokens_saved` field in flashcard responses! This shows how much you're saving vs standard JSON format.

Example:
```json
{
  "flashcards": [...],
  "tokens_saved": 234  // 47% reduction! 🎉
}
```

---

## 📊 Monitoring Usage

Check the logs to see token usage:
```bash
# In backend directory
tail -f logs/app.log
```

Or check the terminal where uvicorn is running to see real-time logs with token counts!
