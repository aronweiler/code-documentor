#!/bin/bash

# Documentation Pipeline Installation Script for Mac/Linux
# This script sets up the Python virtual environment and installs dependencies

set -e  # Exit on any error

echo "🚀 Setting up Documentation Pipeline for Mac/Linux"
echo "=================================================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3 first."
    exit 1
fi

python_version=$(python3 --version)
echo "✅ Found Python: $python_version"

# Check if we're already in a virtual environment
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Already in virtual environment: $VIRTUAL_ENV"
    venv_python="python"
    venv_pip="pip"
else
    echo "🔧 Creating Python virtual environment..."
    python3 -m venv venv
    
    # Check if virtual environment was created successfully
    if [[ ! -f "venv/bin/python" ]]; then
        echo "❌ Virtual environment creation failed - python not found in venv/bin/"
        exit 1
    fi
    
    echo "✅ Virtual environment created successfully"
    echo "🔧 Using virtual environment for remaining commands..."
    venv_python="./venv/bin/python"
    venv_pip="./venv/bin/pip"
fi

# Upgrade pip to latest version
echo "🔧 Upgrading pip..."
if ! $venv_python -m pip install --upgrade pip; then
    echo "❌ Failed to upgrade pip"
    exit 1
fi
echo "✅ Pip upgraded successfully"

# Install dependencies
echo "🔧 Installing Python dependencies..."
if [[ ! -f "requirements.txt" ]]; then
    echo "⚠️  requirements.txt not found, skipping dependency installation"
else
    if ! $venv_pip install -r requirements.txt; then
        echo "❌ Failed to install dependencies"
        echo "   Please check your Python environment and requirements.txt file"
        exit 1
    fi
    echo "✅ Dependencies installed successfully"
fi

# Create .env file if it doesn't exist
echo "🔧 Setting up environment configuration..."
if [[ -f ".env" ]]; then
    echo "✅ .env file already exists"
elif [[ -f ".env.example" ]]; then
    if cp ".env.example" ".env"; then
        echo "✅ Created .env file from template"
        echo "⚠️  Please edit .env and add your API keys"
    else
        echo "❌ Failed to create .env file"
    fi
else
    echo "⚠️  .env.example not found - you'll need to create .env manually"
fi

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "To activate the virtual environment in future sessions:"
echo "  source venv/bin/activate"
echo ""
echo "Or use the virtual environment directly:"
echo "  ./venv/bin/python your_script.py"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your API keys"
echo "2. Test the configuration: ./venv/bin/python main.py validate-config"
echo "3. Analyze a repository: ./venv/bin/python main.py analyze /path/to/repo"
echo "4. Generate documentation: ./venv/bin/python main.py --repo-path /path/to/repo"
echo ""
echo "For help: ./venv/bin/python main.py --help"