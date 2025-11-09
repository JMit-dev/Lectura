# ===========================================================================
# LECTURA LAUNCHER - Windows PowerShell Version
# ===========================================================================

# Enable strict mode
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Colors
$Red = "Red"
$Green = "Green"
$Yellow = "Yellow"
$Blue = "Cyan"
$White = "White"

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# Config file
$ConfigFile = "lectura.conf"

Write-Host ""
Write-Host "===============================================================" -ForegroundColor $Blue
Write-Host ""
Write-Host "                  🎓 LECTURA LAUNCHER 🎓" -ForegroundColor $Blue
Write-Host "         AI-Powered Lecture Intelligence Platform" -ForegroundColor $Blue
Write-Host ""
Write-Host "===============================================================" -ForegroundColor $Blue
Write-Host ""

# Check if config file exists
if (-not (Test-Path $ConfigFile)) {
    Write-Host "[ERROR] Configuration file '$ConfigFile' not found!" -ForegroundColor $Red
    Write-Host "Please create $ConfigFile with your API keys." -ForegroundColor $Yellow
    Write-Host "You can use lectura.conf.example as a template." -ForegroundColor $Yellow
    exit 1
}

# Load configuration
Write-Host "[1/7] Loading configuration from $ConfigFile..." -ForegroundColor $Blue
$config = @{}
Get-Content $ConfigFile | ForEach-Object {
    $line = $_.Trim()
    # Skip comments and empty lines
    if ($line -and -not $line.StartsWith("#")) {
        $parts = $line -split "=", 2
        if ($parts.Length -eq 2) {
            $key = $parts[0].Trim()
            $value = $parts[1].Trim()
            $config[$key] = $value
            Set-Variable -Name $key -Value $value -Scope Script
        }
    }
}

# Validate required configuration
if (-not $config["GEMINI_API_KEY"] -or $config["GEMINI_API_KEY"] -eq "your_gemini_api_key_here") {
    Write-Host "[ERROR] GEMINI_API_KEY not configured!" -ForegroundColor $Red
    Write-Host "Please edit $ConfigFile and add your Gemini API key." -ForegroundColor $Yellow
    Write-Host "Get your API key from: https://makersuite.google.com/app/apikey" -ForegroundColor $Yellow
    exit 1
}

# Set defaults if not configured
if (-not $config["BACKEND_PORT"]) { $config["BACKEND_PORT"] = "8000" }
if (-not $config["FRONTEND_PORT"]) { $config["FRONTEND_PORT"] = "5173" }
if (-not $config["FRONTEND_URL"]) { $config["FRONTEND_URL"] = "http://localhost:$($config['FRONTEND_PORT'])" }

Write-Host "[✓] Configuration loaded successfully" -ForegroundColor $Green
Write-Host ""

# Check for Python
Write-Host "[2/7] Checking Python installation..." -ForegroundColor $Blue
try {
    $pythonVersion = & python --version 2>&1
    Write-Host "[✓] Found $pythonVersion" -ForegroundColor $Green
} catch {
    Write-Host "[ERROR] Python 3 is not installed or not in PATH!" -ForegroundColor $Red
    Write-Host "Please install Python 3.11 or higher." -ForegroundColor $Yellow
    exit 1
}
Write-Host ""

# Check for Node.js
Write-Host "[3/7] Checking Node.js installation..." -ForegroundColor $Blue
try {
    $nodeVersion = & node --version 2>&1
    Write-Host "[✓] Found Node.js $nodeVersion" -ForegroundColor $Green
} catch {
    Write-Host "[ERROR] Node.js is not installed or not in PATH!" -ForegroundColor $Red
    Write-Host "Please install Node.js 18 or higher." -ForegroundColor $Yellow
    exit 1
}
Write-Host ""

# Setup backend
Write-Host "[4/7] Setting up backend..." -ForegroundColor $Blue
Set-Location backend

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "  Creating virtual environment..."
    & python -m venv venv
}

# Activate virtual environment
& .\venv\Scripts\Activate.ps1

# Install/upgrade backend dependencies
Write-Host "  Installing backend dependencies..."
& python -m pip install -q --upgrade pip | Out-Null
& pip install -q -e .[dev] | Out-Null

Write-Host "[✓] Backend setup complete" -ForegroundColor $Green
Write-Host ""

# Setup frontend
Write-Host "[5/7] Setting up frontend..." -ForegroundColor $Blue
Set-Location ..\frontend

# Install frontend dependencies if node_modules doesn't exist
if (-not (Test-Path "node_modules")) {
    Write-Host "  Installing frontend dependencies..."
    & npm install
} else {
    Write-Host "  Dependencies already installed"
}

Write-Host "[✓] Frontend setup complete" -ForegroundColor $Green
Write-Host ""

# Create backend .env file
Set-Location "$ScriptDir\backend"
$envContent = @"
GEMINI_API_KEY=$($config['GEMINI_API_KEY'])
ENVIRONMENT=$($config['ENVIRONMENT'])
LOG_LEVEL=$($config['LOG_LEVEL'])
CORS_ORIGINS=$($config['CORS_ORIGINS'])
MAX_FILE_SIZE=$($config['MAX_FILE_SIZE'])
"@
$envContent | Out-File -FilePath ".env" -Encoding UTF8

# Start services
Write-Host "[6/7] Starting services..." -ForegroundColor $Blue

# Start backend
Write-Host "  Starting backend on port $($config['BACKEND_PORT'])..."
& .\venv\Scripts\Activate.ps1
$backendLog = "$env:TEMP\lectura-backend.log"
$backendProcess = Start-Process -FilePath "uvicorn" -ArgumentList "src.main:app", "--host", "0.0.0.0", "--port", "$($config['BACKEND_PORT'])", "--reload" -RedirectStandardOutput $backendLog -RedirectStandardError $backendLog -PassThru -NoNewWindow

Start-Sleep -Seconds 2

# Check if backend is running
if ($backendProcess.HasExited) {
    Write-Host "[ERROR] Backend failed to start!" -ForegroundColor $Red
    Write-Host "Check logs at $backendLog" -ForegroundColor $Yellow
    exit 1
}

Write-Host "[✓] Backend started (PID: $($backendProcess.Id))" -ForegroundColor $Green

# Start frontend
Set-Location "$ScriptDir\frontend"
Write-Host "  Starting frontend on port $($config['FRONTEND_PORT'])..."
$frontendLog = "$env:TEMP\lectura-frontend.log"
$frontendProcess = Start-Process -FilePath "npm" -ArgumentList "run", "dev", "--", "--host", "--port", "$($config['FRONTEND_PORT'])" -RedirectStandardOutput $frontendLog -RedirectStandardError $frontendLog -PassThru -NoNewWindow

Start-Sleep -Seconds 3

# Check if frontend is running
if ($frontendProcess.HasExited) {
    Write-Host "[ERROR] Frontend failed to start!" -ForegroundColor $Red
    Write-Host "Check logs at $frontendLog" -ForegroundColor $Yellow
    Stop-Process -Id $backendProcess.Id -Force -ErrorAction SilentlyContinue
    exit 1
}

Write-Host "[✓] Frontend started (PID: $($frontendProcess.Id))" -ForegroundColor $Green
Write-Host ""

# Open browser
Write-Host "[7/7] Opening browser..." -ForegroundColor $Blue
Start-Sleep -Seconds 2
Start-Process $config['FRONTEND_URL']

Write-Host ""
Write-Host "===============================================================" -ForegroundColor $Green
Write-Host ""
Write-Host "              ✨ LECTURA IS NOW RUNNING! ✨" -ForegroundColor $Green
Write-Host ""
Write-Host "===============================================================" -ForegroundColor $Green
Write-Host ""
Write-Host "📱 Frontend:  $($config['FRONTEND_URL'])" -ForegroundColor $Blue
Write-Host "🔧 Backend:   http://localhost:$($config['BACKEND_PORT'])" -ForegroundColor $Blue
Write-Host "📚 API Docs:  http://localhost:$($config['BACKEND_PORT'])/docs" -ForegroundColor $Blue
Write-Host ""
Write-Host "📋 Logs:" -ForegroundColor $Blue
Write-Host "   Backend:  $backendLog"
Write-Host "   Frontend: $frontendLog"
Write-Host ""
Write-Host "Press Ctrl+C to stop all services" -ForegroundColor $Yellow
Write-Host ""

# Function to cleanup on exit
function Cleanup {
    Write-Host ""
    Write-Host "Shutting down services..." -ForegroundColor $Yellow

    if ($backendProcess -and -not $backendProcess.HasExited) {
        Stop-Process -Id $backendProcess.Id -Force -ErrorAction SilentlyContinue
        Write-Host "[✓] Backend stopped" -ForegroundColor $Green
    }

    if ($frontendProcess -and -not $frontendProcess.HasExited) {
        Stop-Process -Id $frontendProcess.Id -Force -ErrorAction SilentlyContinue
        Write-Host "[✓] Frontend stopped" -ForegroundColor $Green
    }

    Write-Host "Goodbye! 👋" -ForegroundColor $Green
    exit 0
}

# Register cleanup on Ctrl+C
try {
    # Wait for user to press Ctrl+C
    while ($true) {
        Start-Sleep -Seconds 1

        # Check if processes are still running
        if ($backendProcess.HasExited -or $frontendProcess.HasExited) {
            Write-Host ""
            Write-Host "[ERROR] One or more services stopped unexpectedly!" -ForegroundColor $Red
            Write-Host "Check the log files for details." -ForegroundColor $Yellow
            Cleanup
        }
    }
} finally {
    Cleanup
}
