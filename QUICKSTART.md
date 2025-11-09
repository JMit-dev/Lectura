# 🚀 Lectura Quick Start Guide

Get Lectura up and running in under 2 minutes!

## Prerequisites

- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **Gemini API Key** - [Get yours free](https://makersuite.google.com/app/apikey)

## Installation & Running

### Step 1: Get Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the key

### Step 2: Configure Lectura

1. Open `lectura.conf` in your text editor
2. Replace `your_gemini_api_key_here` with your actual API key:
   ```bash
   GEMINI_API_KEY=AIza...your_actual_key_here
   ```
3. Save the file

### Step 3: Run Lectura

Simply run:

```bash
./run.sh
```

That's it! The script will:
- ✅ Install all dependencies (backend & frontend)
- ✅ Start both servers
- ✅ Automatically open your browser to the app

## What the Run Script Does

1. **Validates** your configuration and API key
2. **Checks** for Python and Node.js
3. **Sets up** the backend (creates venv, installs dependencies)
4. **Sets up** the frontend (installs npm packages)
5. **Starts** the backend API server
6. **Starts** the frontend web app
7. **Opens** your browser to `http://localhost:5173`

## Accessing Lectura

- **Web App**: http://localhost:5173
- **API Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Logs

If something goes wrong, check the logs:
- Backend: `/tmp/lectura-backend.log`
- Frontend: `/tmp/lectura-frontend.log`

## Stopping Lectura

Press `Ctrl+C` in the terminal where you ran `./run.sh`

The script will gracefully shut down both services.

## Troubleshooting

### "Permission denied" error
```bash
chmod +x run.sh
./run.sh
```

### Backend won't start
1. Check `/tmp/lectura-backend.log`
2. Verify your `GEMINI_API_KEY` is correct in `lectura.conf`

### Frontend won't start
1. Check `/tmp/lectura-frontend.log`
2. Make sure port 5173 isn't already in use

### Port already in use
Edit `lectura.conf` and change the ports:
```bash
BACKEND_PORT=8001
FRONTEND_PORT=5174
```

## Manual Setup (Alternative)

If you prefer to set up manually:

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e '.[dev]'
cp .env.example .env
# Edit .env with your API key
uvicorn src.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Next Steps

1. Upload an audio file (lecture, podcast, etc.)
2. Get instant transcription
3. Generate AI summaries
4. Create study flashcards
5. Translate to 60+ languages!

Enjoy using Lectura! 🎓
