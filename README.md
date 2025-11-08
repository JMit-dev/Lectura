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
│   ├── src/          # Source code
│   ├── tests/        # Tests
│   └── README.md     # 👈 Backend setup guide
│
├── frontend/         # React TypeScript frontend
│   ├── src/          # Source code
│   └── README.md     # 👈 Frontend setup guide
│
├── docs/             # Documentation
│   ├── API.md        # API reference
│   ├── ARCHITECTURE.md  # System design
│   └── README.md     # 👈 Documentation index
│
├── scripts/          # Automation scripts
│   ├── setup.sh      # Initial setup
│   ├── dev.sh        # Development servers
│   └── README.md     # 👈 Scripts guide
│
├── .github/          # CI/CD workflows
└── CLAUDE.md         # Hackathon technical plan
```

**📖 Detailed Documentation:**
- [Backend README](./backend/README.md) - Backend setup, API development, testing
- [Frontend README](./frontend/README.md) - Frontend setup, components, hooks
- [Documentation Guide](./docs/README.md) - Documentation standards and index
- [Scripts Guide](./scripts/README.md) - Automation tools and utilities
- [Hackathon Plan](./CLAUDE.md) - Complete technical design and timeline

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

## 🤖 Working with AI Agents

This project is fully documented for AI coding assistants (Claude, GPT, Cursor, etc.):

### For AI Agents to Understand the Project:

1. **Start here:** Read this `README.md` for project overview
2. **Backend work:** Read [`backend/README.md`](./backend/README.md) for:
   - File structure and what goes where
   - API endpoints to implement
   - Service layer patterns
   - Testing requirements
3. **Frontend work:** Read [`frontend/README.md`](./frontend/README.md) for:
   - Component structure
   - React hooks to create
   - API integration patterns
   - Styling with Tailwind
4. **Documentation:** Check [`docs/README.md`](./docs/README.md) for:
   - API specifications
   - Architecture decisions
   - Code documentation standards
5. **Automation:** See [`scripts/README.md`](./scripts/README.md) for:
   - Available scripts
   - How to run tests
   - Development workflows

### AI Agent Quick Commands:

```bash
# Setup everything
./scripts/setup.sh

# Start development
./scripts/dev.sh

# Run tests
cd backend && pytest
cd frontend && npm test

# Check code quality
cd backend && black src/ && flake8 src/
cd frontend && npm run lint
```

### Context for AI Assistants:

Each directory has a README with:
- ✅ Clear file structure
- ✅ What each file/directory is for
- ✅ TODO markers for unfinished work
- ✅ Code examples and patterns
- ✅ Testing instructions
- ✅ Priority order of tasks

This makes it easy for AI agents to:
- Understand the codebase quickly
- Know where to add new code
- Follow existing patterns
- Write appropriate tests
- Maintain code quality

## 🙏 Acknowledgments

- Powered by Google Gemini AI
- TOON format for token optimization
- Designed for accessibility and student success
