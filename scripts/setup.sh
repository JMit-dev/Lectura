#!/bin/bash

echo "🎓 Lectura Setup Script"
echo "======================="
echo ""

# Check Python version
PYTHON_CMD=""
if command -v python3.13 &> /dev/null; then
    PYTHON_CMD="python3.13"
    echo "✅ Python 3.13 found"
elif command -v python3.12 &> /dev/null; then
    PYTHON_CMD="python3.12"
    echo "✅ Python 3.12 found"
elif command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
    echo "✅ Python 3.11 found"
elif command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    PYTHON_CMD="python3"
    echo "✅ Python $PYTHON_VERSION found"
else
    echo "❌ Python 3.11+ is required but not found"
    exit 1
fi

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
$PYTHON_CMD -m venv venv
echo "✅ Virtual environment created"

# Activate virtual environment
source venv/bin/activate

# Install dependencies (runtime + dev tooling)
pip install -e '.[dev]'
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
