#!/bin/bash

echo "🎓 Lectura Setup Script"
echo "======================="
echo ""

# Check Python version
if ! command -v python3.11 &> /dev/null; then
    echo "❌ Python 3.11 is required but not found"
    exit 1
fi
echo "✅ Python 3.11 found"

# Check Node.js version
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not found"
    exit 1
fi
echo "✅ Node.js found ($(node --version))"

# Backend setup
echo ""
echo "📦 Setting up backend..."
cd backend

# Create virtual environment
python3.11 -m venv venv
echo "✅ Virtual environment created"

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
echo "✅ Backend dependencies installed"

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  Created .env file - Please add your GEMINI_API_KEY"
fi

# Install pre-commit hooks
pre-commit install
echo "✅ Pre-commit hooks installed"

cd ..

# Frontend setup
echo ""
echo "📦 Setting up frontend..."
cd frontend

# Install dependencies
npm install
echo "✅ Frontend dependencies installed"

cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Add your GEMINI_API_KEY to backend/.env"
echo "2. Run './scripts/dev.sh' to start development servers"
echo "   OR"
echo "   Run 'docker-compose up' to use Docker"
