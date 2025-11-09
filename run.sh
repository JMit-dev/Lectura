#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Config file
CONFIG_FILE="lectura.conf"

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                           ║${NC}"
echo -e "${BLUE}║                  🎓 LECTURA LAUNCHER 🎓                   ║${NC}"
echo -e "${BLUE}║         AI-Powered Lecture Intelligence Platform          ║${NC}"
echo -e "${BLUE}║                                                           ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if config file exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${RED}ERROR: Configuration file '$CONFIG_FILE' not found!${NC}"
    echo -e "${YELLOW}Please create $CONFIG_FILE with your API keys.${NC}"
    echo -e "${YELLOW}You can use lectura.conf as a template.${NC}"
    exit 1
fi

# Load configuration
echo -e "${BLUE}[1/7]${NC} Loading configuration from $CONFIG_FILE..."
set -a
source "$CONFIG_FILE"
set +a

# Validate required configuration
if [ "$GEMINI_API_KEY" = "your_gemini_api_key_here" ] || [ -z "$GEMINI_API_KEY" ]; then
    echo -e "${RED}ERROR: GEMINI_API_KEY not configured!${NC}"
    echo -e "${YELLOW}Please edit $CONFIG_FILE and add your Gemini API key.${NC}"
    echo -e "${YELLOW}Get your API key from: https://makersuite.google.com/app/apikey${NC}"
    exit 1
fi

# Set defaults if not configured
BACKEND_PORT="${BACKEND_PORT:-8000}"
FRONTEND_PORT="${FRONTEND_PORT:-5173}"
FRONTEND_URL="${FRONTEND_URL:-http://localhost:$FRONTEND_PORT}"

echo -e "${GREEN}✓${NC} Configuration loaded successfully"
echo ""

# Check for Python
echo -e "${BLUE}[2/7]${NC} Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python 3 is not installed!${NC}"
    echo -e "${YELLOW}Please install Python 3.11 or higher.${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✓${NC} Found $PYTHON_VERSION"
echo ""

# Check for Node.js
echo -e "${BLUE}[3/7]${NC} Checking Node.js installation..."
if ! command -v node &> /dev/null; then
    echo -e "${RED}ERROR: Node.js is not installed!${NC}"
    echo -e "${YELLOW}Please install Node.js 18 or higher.${NC}"
    exit 1
fi
NODE_VERSION=$(node --version)
echo -e "${GREEN}✓${NC} Found Node.js $NODE_VERSION"
echo ""

# Setup backend
echo -e "${BLUE}[4/7]${NC} Setting up backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "  Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/upgrade backend dependencies
echo "  Installing backend dependencies..."
pip install -q --upgrade pip
pip install -q -e '.[dev]'

echo -e "${GREEN}✓${NC} Backend setup complete"
echo ""

# Setup frontend
echo -e "${BLUE}[5/7]${NC} Setting up frontend..."
cd ../frontend

# Install frontend dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "  Installing frontend dependencies..."
    npm install
else
    echo "  Dependencies already installed"
fi

echo -e "${GREEN}✓${NC} Frontend setup complete"
echo ""

# Create backend .env file
cd "$SCRIPT_DIR/backend"
cat > .env << EOF
GEMINI_API_KEY=$GEMINI_API_KEY
ENVIRONMENT=$ENVIRONMENT
LOG_LEVEL=$LOG_LEVEL
CORS_ORIGINS=$CORS_ORIGINS
MAX_FILE_SIZE=$MAX_FILE_SIZE
EOF

# Start services
echo -e "${BLUE}[6/7]${NC} Starting services..."

# Start backend
echo "  Starting backend on port $BACKEND_PORT..."
source venv/bin/activate
uvicorn src.main:app --host 0.0.0.0 --port "$BACKEND_PORT" --reload > /tmp/lectura-backend.log 2>&1 &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 2

# Check if backend is running
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo -e "${RED}ERROR: Backend failed to start!${NC}"
    echo -e "${YELLOW}Check logs at /tmp/lectura-backend.log${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} Backend started (PID: $BACKEND_PID)"

# Start frontend
cd "$SCRIPT_DIR/frontend"
echo "  Starting frontend on port $FRONTEND_PORT..."
npm run dev -- --host --port "$FRONTEND_PORT" > /tmp/lectura-frontend.log 2>&1 &
FRONTEND_PID=$!

# Wait for frontend to start
sleep 3

# Check if frontend is running
if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo -e "${RED}ERROR: Frontend failed to start!${NC}"
    echo -e "${YELLOW}Check logs at /tmp/lectura-frontend.log${NC}"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo -e "${GREEN}✓${NC} Frontend started (PID: $FRONTEND_PID)"
echo ""

# Open browser
echo -e "${BLUE}[7/7]${NC} Opening browser..."
sleep 2

# Detect OS and open browser
if command -v xdg-open &> /dev/null; then
    # Linux
    xdg-open "$FRONTEND_URL" &>/dev/null &
elif command -v open &> /dev/null; then
    # macOS
    open "$FRONTEND_URL" &>/dev/null &
elif command -v start &> /dev/null; then
    # Windows (Git Bash)
    start "$FRONTEND_URL" &>/dev/null &
else
    echo -e "${YELLOW}Could not automatically open browser.${NC}"
    echo -e "${YELLOW}Please open manually: $FRONTEND_URL${NC}"
fi

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                           ║${NC}"
echo -e "${GREEN}║              ✨ LECTURA IS NOW RUNNING! ✨               ║${NC}"
echo -e "${GREEN}║                                                           ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📱 Frontend:${NC}  $FRONTEND_URL"
echo -e "${BLUE}🔧 Backend:${NC}   http://localhost:$BACKEND_PORT"
echo -e "${BLUE}📚 API Docs:${NC}  http://localhost:$BACKEND_PORT/docs"
echo ""
echo -e "${BLUE}📋 Logs:${NC}"
echo -e "   Backend:  /tmp/lectura-backend.log"
echo -e "   Frontend: /tmp/lectura-frontend.log"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop all services${NC}"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}Shutting down services...${NC}"

    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        echo -e "${GREEN}✓${NC} Backend stopped"
    fi

    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        echo -e "${GREEN}✓${NC} Frontend stopped"
    fi

    echo -e "${GREEN}Goodbye! 👋${NC}"
    exit 0
}

# Trap Ctrl+C and call cleanup
trap cleanup INT TERM

# Wait for processes
wait
