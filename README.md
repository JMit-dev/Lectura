# 🎓 Lectura - AI Lecture Notes Generator

Transform lecture recordings into accessible study materials using AI. Upload audio → get transcripts, summaries, flashcards, and translations in 60+ languages.

## 🚀 Features

- **Audio Transcription**: Convert lecture recordings to text using Gemini AI
- **Smart Summaries**: Generate concise summaries of key points
- **Flashcards**: Automatically create study flashcards
- **Multi-language Support**: Translate content to 60+ languages
- **TOON Format Optimization**: Reduced API costs by 40%

## 🛠️ Tech Stack

### Backend
- Python 3.11+
- FastAPI
- Google Gemini API
- Uvicorn

### Frontend
- React 18 + TypeScript
- Vite
- Tailwind CSS
- Axios

### DevOps
- Docker & Docker Compose
- GitHub Actions (CI/CD)
- Pre-commit hooks

## 📦 Installation

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker (optional)
- Gemini API Key

### Quick Start with Docker

```bash
# Clone the repository
git clone https://github.com/your-team/lectura.git
cd lectura

# Set up environment variables
cp backend/.env.example backend/.env
# Add your GEMINI_API_KEY to backend/.env

# Run with Docker Compose
docker-compose up
```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Manual Setup

#### Backend Setup

```bash
cd backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Set up environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Install pre-commit hooks
pre-commit install

# Run the server
uvicorn src.main:app --reload
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest --cov=src
```

### Frontend Tests

```bash
cd frontend
npm run test
```

## 📚 API Documentation

Once the backend is running, visit http://localhost:8000/docs for interactive API documentation.

### Key Endpoints

- `POST /api/transcribe` - Transcribe audio to text
- `POST /api/summarize` - Generate summary
- `POST /api/flashcards` - Create flashcards
- `POST /api/translate` - Translate to multiple languages

## 🎯 Project Structure

```
lectura/
├── backend/          # Python FastAPI backend
│   ├── src/
│   │   ├── api/      # API routes
│   │   ├── services/ # Business logic
│   │   ├── models/   # Data models
│   │   └── utils/    # Utilities
│   └── tests/        # Tests
├── frontend/         # React frontend
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── hooks/
│       └── lib/
└── docs/            # Documentation
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

MIT License - see LICENSE file for details

## 👥 Team

Built for [Hackathon Name] by Team Lectura

## 🙏 Acknowledgments

- Powered by Google Gemini AI
- TOON format for token optimization
- Designed for accessibility and student success
