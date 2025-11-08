# Lectura Scripts

Automation scripts for development and deployment.

## 📜 Available Scripts

### setup.sh

**Purpose:** Initial project setup for all team members

**Usage:**
```bash
./scripts/setup.sh
```

**What it does:**
1. ✅ Checks for Python 3.11+ (supports 3.11, 3.12, 3.13, or python3)
2. ✅ Checks for Node.js
3. ✅ Creates Python virtual environment
4. ✅ Installs backend dependencies
5. ✅ Installs development tools (Black, Flake8, pytest, etc.)
6. ✅ Creates `.env` file from template
7. ✅ Installs pre-commit hooks
8. ✅ Installs frontend dependencies

**Requirements:**
- Python 3.11+ installed
- Node.js 18+ installed
- Internet connection for package downloads

**After running:**
1. Add your `GEMINI_API_KEY` to `backend/.env`
2. Run `./scripts/dev.sh` to start development

---

### dev.sh

**Purpose:** Start both backend and frontend development servers

**Usage:**
```bash
./scripts/dev.sh
```

**What it does:**
1. ✅ Checks for `.env` file existence
2. ✅ Starts backend server on http://localhost:8000
3. ✅ Starts frontend server on http://localhost:5173
4. ✅ Runs both servers in background
5. ✅ Handles graceful shutdown with Ctrl+C

**Requirements:**
- Project must be set up (run `setup.sh` first)
- `GEMINI_API_KEY` must be in `backend/.env`

**Servers:**
- Backend: http://localhost:8000
- Backend API Docs: http://localhost:8000/docs
- Frontend: http://localhost:5173

**To stop:**
Press `Ctrl+C` - both servers will shut down gracefully

---

## 🛠️ Creating New Scripts

### Script Template

```bash
#!/bin/bash

# Script: script_name.sh
# Purpose: Brief description
# Usage: ./scripts/script_name.sh [args]

set -e  # Exit on error

echo "🎓 Script Name"
echo "=============="
echo ""

# Your script logic here

echo "✅ Done!"
```

### Best Practices

1. **Make executable:**
   ```bash
   chmod +x scripts/new_script.sh
   ```

2. **Use descriptive names:**
   - ✅ `setup.sh`
   - ✅ `dev.sh`
   - ✅ `test-all.sh`
   - ❌ `script1.sh`
   - ❌ `temp.sh`

3. **Add error handling:**
   ```bash
   set -e  # Exit on first error
   set -u  # Exit on undefined variable
   set -o pipefail  # Exit on pipe failure
   ```

4. **Provide feedback:**
   ```bash
   echo "✅ Success message"
   echo "⚠️  Warning message"
   echo "❌ Error message"
   ```

5. **Check prerequisites:**
   ```bash
   if ! command -v python3 &> /dev/null; then
       echo "❌ Python 3 not found"
       exit 1
   fi
   ```

---

## 🎯 Potential Additional Scripts

### test-all.sh
Run all tests (backend + frontend)

```bash
#!/bin/bash
set -e

echo "🧪 Running all tests..."

# Backend tests
cd backend
source venv/bin/activate
pytest --cov=src
cd ..

# Frontend tests (when added)
cd frontend
npm run test
cd ..

echo "✅ All tests passed!"
```

### lint-all.sh
Run all linters and formatters

```bash
#!/bin/bash
set -e

echo "🔍 Running linters..."

# Backend
cd backend
source venv/bin/activate
black --check src/
flake8 src/
mypy src/
cd ..

# Frontend
cd frontend
npm run lint
npm run type-check
cd ..

echo "✅ All linting passed!"
```

### deploy-backend.sh
Deploy backend to production

```bash
#!/bin/bash
set -e

echo "🚀 Deploying backend..."

# Build Docker image
docker build -t lectura-backend ./backend

# Tag for registry
docker tag lectura-backend registry.example.com/lectura-backend:latest

# Push to registry
docker push registry.example.com/lectura-backend:latest

echo "✅ Backend deployed!"
```

### deploy-frontend.sh
Deploy frontend to Vercel/Netlify

```bash
#!/bin/bash
set -e

echo "🚀 Deploying frontend..."

cd frontend

# Build production bundle
npm run build

# Deploy to Vercel
vercel --prod

cd ..

echo "✅ Frontend deployed!"
```

### clean.sh
Clean all build artifacts and caches

```bash
#!/bin/bash

echo "🧹 Cleaning project..."

# Backend
rm -rf backend/venv
rm -rf backend/.pytest_cache
rm -rf backend/.coverage
rm -rf backend/.mypy_cache
rm -rf backend/**/__pycache__

# Frontend
rm -rf frontend/node_modules
rm -rf frontend/dist
rm -rf frontend/.vite

echo "✅ Project cleaned!"
```

### backup.sh
Backup important files

```bash
#!/bin/bash

BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "💾 Creating backup..."

# Copy important files
cp -r backend/src "$BACKUP_DIR/"
cp -r frontend/src "$BACKUP_DIR/"
cp backend/.env "$BACKUP_DIR/" 2>/dev/null || true

# Create archive
tar -czf "${BACKUP_DIR}.tar.gz" "$BACKUP_DIR"
rm -rf "$BACKUP_DIR"

echo "✅ Backup created: ${BACKUP_DIR}.tar.gz"
```

---

## 🐛 Troubleshooting Scripts

### Common Issues

**Script won't run:**
```bash
# Make it executable
chmod +x scripts/script_name.sh
```

**Python not found:**
```bash
# Check Python installation
which python3
python3 --version

# Update setup.sh to use your Python version
```

**Node not found:**
```bash
# Install Node.js
# macOS: brew install node
# Ubuntu: sudo apt install nodejs npm
# Windows: Download from nodejs.org
```

**Port already in use:**
```bash
# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn src.main:app --port 8001
```

**Virtual environment activation fails:**
```bash
# Recreate virtual environment
rm -rf backend/venv
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 📚 Script Development Guidelines

### 1. Documentation
- Add comment header explaining purpose
- Document required arguments
- Include usage examples
- List prerequisites

### 2. Safety
- Use `set -e` to exit on errors
- Validate inputs
- Check for required files/directories
- Provide rollback if needed

### 3. User Experience
- Show progress messages
- Use emojis for visual feedback
- Provide helpful error messages
- Ask for confirmation on destructive actions

### 4. Portability
- Use POSIX-compatible syntax when possible
- Test on Linux and macOS
- Document OS-specific requirements
- Provide alternatives for Windows (PowerShell)

### 5. Maintenance
- Keep scripts simple and focused
- One script = one purpose
- Document why, not just what
- Version control all scripts

---

## 🔧 Environment Variables in Scripts

Scripts can access environment variables:

```bash
# Check if variable is set
if [ -z "$GEMINI_API_KEY" ]; then
    echo "❌ GEMINI_API_KEY not set"
    exit 1
fi

# Use variable
echo "Using API key: ${GEMINI_API_KEY:0:10}..."
```

Load from .env file:

```bash
# Load environment variables
if [ -f backend/.env ]; then
    export $(cat backend/.env | xargs)
fi
```

---

## 🤝 Contributing Scripts

When adding a new script:

1. **Create the script** in `scripts/` directory
2. **Make it executable** with `chmod +x`
3. **Test thoroughly** on clean environment
4. **Document it** in this README
5. **Add to git** and commit
6. **Update main README** if user-facing

---

## 📖 Resources

- [Bash Scripting Guide](https://www.gnu.org/software/bash/manual/)
- [ShellCheck](https://www.shellcheck.net/) - Script linter
- [Bash Best Practices](https://bertvv.github.io/cheat-sheets/Bash.html)
