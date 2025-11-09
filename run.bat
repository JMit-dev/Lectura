@echo off
setlocal enabledelayedexpansion

REM ===========================================================================
REM LECTURA LAUNCHER - Windows Batch Version
REM ===========================================================================

REM Get script directory
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM Config file
set "CONFIG_FILE=lectura.conf"

echo.
echo ===============================================================
echo.
echo                  🎓 LECTURA LAUNCHER 🎓
echo         AI-Powered Lecture Intelligence Platform
echo.
echo ===============================================================
echo.

REM Check if config file exists
if not exist "%CONFIG_FILE%" (
    echo [ERROR] Configuration file '%CONFIG_FILE%' not found!
    echo Please create %CONFIG_FILE% with your API keys.
    echo You can use lectura.conf.example as a template.
    exit /b 1
)

REM Load configuration
echo [1/7] Loading configuration from %CONFIG_FILE%...
for /f "usebackq tokens=1,* delims==" %%a in ("%CONFIG_FILE%") do (
    set "line=%%a"
    set "value=%%b"
    REM Skip comments and empty lines
    if not "!line:~0,1!"=="#" if not "!line!"=="" (
        set "%%a=%%b"
    )
)

REM Validate required configuration
if "%GEMINI_API_KEY%"=="your_gemini_api_key_here" (
    echo [ERROR] GEMINI_API_KEY not configured!
    echo Please edit %CONFIG_FILE% and add your Gemini API key.
    echo Get your API key from: https://makersuite.google.com/app/apikey
    exit /b 1
)
if "%GEMINI_API_KEY%"=="" (
    echo [ERROR] GEMINI_API_KEY not configured!
    echo Please edit %CONFIG_FILE% and add your Gemini API key.
    echo Get your API key from: https://makersuite.google.com/app/apikey
    exit /b 1
)

REM Set defaults if not configured
if "%BACKEND_PORT%"=="" set "BACKEND_PORT=8000"
if "%FRONTEND_PORT%"=="" set "FRONTEND_PORT=5173"
if "%FRONTEND_URL%"=="" set "FRONTEND_URL=http://localhost:%FRONTEND_PORT%"

echo [✓] Configuration loaded successfully
echo.

REM Check for Python
echo [2/7] Checking Python installation...
where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 3 is not installed or not in PATH!
    echo Please install Python 3.11 or higher.
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version 2^>^&1') do set "PYTHON_VERSION=%%i"
echo [✓] Found %PYTHON_VERSION%
echo.

REM Check for Node.js
echo [3/7] Checking Node.js installation...
where node >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed or not in PATH!
    echo Please install Node.js 18 or higher.
    exit /b 1
)
for /f "tokens=*" %%i in ('node --version') do set "NODE_VERSION=%%i"
echo [✓] Found Node.js %NODE_VERSION%
echo.

REM Setup backend
echo [4/7] Setting up backend...
cd backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo   Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install/upgrade backend dependencies
echo   Installing backend dependencies...
python -m pip install -q --upgrade pip
pip install -q -e .[dev]

echo [✓] Backend setup complete
echo.

REM Setup frontend
echo [5/7] Setting up frontend...
cd ..\frontend

REM Install frontend dependencies if node_modules doesn't exist
if not exist "node_modules" (
    echo   Installing frontend dependencies...
    call npm install
) else (
    echo   Dependencies already installed
)

echo [✓] Frontend setup complete
echo.

REM Create backend .env file
cd "%SCRIPT_DIR%\backend"
(
    echo GEMINI_API_KEY=%GEMINI_API_KEY%
    echo ENVIRONMENT=%ENVIRONMENT%
    echo LOG_LEVEL=%LOG_LEVEL%
    echo CORS_ORIGINS=%CORS_ORIGINS%
    echo MAX_FILE_SIZE=%MAX_FILE_SIZE%
) > .env

REM Start services
echo [6/7] Starting services...

REM Start backend
echo   Starting backend on port %BACKEND_PORT%...
call venv\Scripts\activate.bat
start /b cmd /c "uvicorn src.main:app --host 0.0.0.0 --port %BACKEND_PORT% --reload > %TEMP%\lectura-backend.log 2>&1"
timeout /t 2 /nobreak >nul

echo [✓] Backend started

REM Start frontend
cd "%SCRIPT_DIR%\frontend"
echo   Starting frontend on port %FRONTEND_PORT%...
start /b cmd /c "npm run dev -- --host --port %FRONTEND_PORT% > %TEMP%\lectura-frontend.log 2>&1"
timeout /t 3 /nobreak >nul

echo [✓] Frontend started
echo.

REM Open browser
echo [7/7] Opening browser...
timeout /t 2 /nobreak >nul
start "" "%FRONTEND_URL%"

echo.
echo ===============================================================
echo.
echo              ✨ LECTURA IS NOW RUNNING! ✨
echo.
echo ===============================================================
echo.
echo 📱 Frontend:  %FRONTEND_URL%
echo 🔧 Backend:   http://localhost:%BACKEND_PORT%
echo 📚 API Docs:  http://localhost:%BACKEND_PORT%/docs
echo.
echo 📋 Logs:
echo    Backend:  %TEMP%\lectura-backend.log
echo    Frontend: %TEMP%\lectura-frontend.log
echo.
echo Press Ctrl+C to stop all services
echo.

REM Keep window open
pause

REM Note: On Windows, services will continue running in background
REM Use Task Manager to stop uvicorn and node processes if needed
