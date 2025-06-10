# Documentation Pipeline Installation Script for Windows
# This script sets up the Python virtual environment and installs dependencies

# Set error action preference to stop on errors
$ErrorActionPreference = "Stop"

Write-Host "Setting up Documentation Pipeline for Windows" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Python is required but not found. Please install Python first." -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Check if we're already in a virtual environment
if ($env:VIRTUAL_ENV) {
    Write-Host "Already in virtual environment: $env:VIRTUAL_ENV" -ForegroundColor Green
    $venvPython = "python"
    $venvPip = "pip"
} else {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Cyan
    
    # Create virtual environment
    python -m venv venv
    
    # Build paths to virtual environment executables
    $currentDir = Get-Location
    $venvPython = Join-Path $currentDir "venv\Scripts\python.exe"
    $venvPip = Join-Path $currentDir "venv\Scripts\pip.exe"
    
    # Check if virtual environment was created successfully
    if (-not (Test-Path $venvPython)) {
        Write-Host "Virtual environment creation failed - python.exe not found at $venvPython" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "Virtual environment created successfully" -ForegroundColor Green
    Write-Host "Using virtual environment for remaining commands..." -ForegroundColor Cyan
}

# Upgrade pip to latest version
Write-Host "Upgrading pip..." -ForegroundColor Cyan
try {
    & "$venvPython" -m pip install --upgrade pip
    Write-Host "Pip upgraded successfully" -ForegroundColor Green
} catch {
    Write-Host "Failed to upgrade pip: $_" -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Cyan

if (-not (Test-Path "requirements.txt")) {
    Write-Host "requirements.txt not found, skipping dependency installation" -ForegroundColor Yellow
} else {
    try {
        & "$venvPip" install -r requirements.txt
        Write-Host "Dependencies installed successfully" -ForegroundColor Green
    } catch {
        Write-Host "Failed to install dependencies: $_" -ForegroundColor Red
        Write-Host "Please check your Python environment and requirements.txt file" -ForegroundColor Yellow
        exit 1
    }
}

# Create .env file if it doesn't exist
Write-Host "Setting up environment configuration..." -ForegroundColor Cyan

if (Test-Path ".env") {
    Write-Host ".env file already exists" -ForegroundColor Green
} elseif (Test-Path ".env.example") {
    try {
        Copy-Item ".env.example" ".env"
        Write-Host "Created .env file from template" -ForegroundColor Green
        Write-Host "Please edit .env and add your API keys" -ForegroundColor Yellow
    } catch {
        Write-Host "Failed to create .env file: $_" -ForegroundColor Red
    }
} else {
    Write-Host ".env.example not found - you'll need to create .env manually" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Installation completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "To activate the virtual environment in future sessions:" -ForegroundColor Yellow
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "  (You may need to run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser)" -ForegroundColor Gray
Write-Host ""
Write-Host "Or use the virtual environment directly:" -ForegroundColor Yellow
Write-Host "  .\venv\Scripts\python.exe your_script.py" -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Edit .env file and add your API keys" -ForegroundColor White
Write-Host "2. Test the configuration: .\venv\Scripts\python.exe main.py validate-config" -ForegroundColor White
Write-Host "3. Analyze a repository: .\venv\Scripts\python.exe main.py analyze C:\path\to\repo" -ForegroundColor White
Write-Host "4. Generate documentation: .\venv\Scripts\python.exe main.py --repo-path C:\path\to\repo" -ForegroundColor White
Write-Host ""
Write-Host "For help: .\venv\Scripts\python.exe main.py --help" -ForegroundColor White