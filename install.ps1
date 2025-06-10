# Documentation Pipeline Installation Script for Windows
# This script sets up the Python virtual environment and installs dependencies

# Set error action preference to stop on errors
$ErrorActionPreference = "Stop"

Write-Host "🚀 Setting up Documentation Pipeline for Windows" -ForegroundColor Green
Write-Host ("=" * 50) -ForegroundColor Green

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Found Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is required but not found. Please install Python first." -ForegroundColor Red
    Write-Host "   Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Check if we're already in a virtual environment
if ($env:VIRTUAL_ENV) {
    Write-Host "✅ Already in virtual environment: $env:VIRTUAL_ENV" -ForegroundColor Green
} else {
    Write-Host "🔧 Creating Python virtual environment..." -ForegroundColor Cyan
    python -m venv venv
    
    Write-Host "🔧 Activating virtual environment..." -ForegroundColor Cyan
    & ".\venv\Scripts\Activate.ps1"
    Write-Host "✅ Virtual environment activated" -ForegroundColor Green
}

# Upgrade pip to latest version
Write-Host "🔧 Upgrading pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip

# Install dependencies
Write-Host "🔧 Installing Python dependencies from requirements.txt..." -ForegroundColor Cyan
pip install -r requirements.txt

# Run setup script
Write-Host "🔧 Running setup script..." -ForegroundColor Cyan
python setup.py

Write-Host ""
Write-Host "🎉 Installation completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "To activate the virtual environment in future sessions:" -ForegroundColor Yellow
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Edit .env file and add your API keys" -ForegroundColor White
Write-Host "2. Test the configuration: python main.py validate-config" -ForegroundColor White
Write-Host "3. Analyze a repository: python main.py analyze C:\path\to\repo" -ForegroundColor White
Write-Host "4. Generate documentation: python main.py --repo-path C:\path\to\repo" -ForegroundColor White
Write-Host ""
Write-Host "For help: python main.py --help" -ForegroundColor White