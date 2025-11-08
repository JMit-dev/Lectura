#!/bin/bash

echo "🎓 Starting Lectura Development Servers"
echo "======================================="
echo ""

# Check if .env exists
if [ ! -f backend/.env ]; then
    echo "❌ backend/.env not found. Please run ./scripts/setup.sh first"
    exit 1
fi

# Start backend in background
echo "🚀 Starting backend server..."
cd backend
source venv/bin/activate
uvicorn src.main:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

# Give backend time to start
sleep 2

# Start frontend in background
echo "🚀 Starting frontend server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Both servers started!"
echo ""
echo "📍 Access the application:"
echo "   Frontend: http://localhost:5173"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"

# Handle Ctrl+C
trap "echo ''; echo '🛑 Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT

# Wait for background processes
wait
