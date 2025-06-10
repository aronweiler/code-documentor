#!/bin/bash

# Documentation Pipeline Installation Script for Mac/Linux
# This script sets up the Python virtual environment and installs dependencies

set -e  # Exit on any error

echo "🚀 Setting up Documentation Pipeline for Mac/Linux"
echo "=" * 50

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3 first."
    exit 1
fi

# Check if we're already in a virtual environment
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Already in virtual environment: $VIRTUAL_ENV"
else
    echo "🔧 Creating Python virtual environment..."
    python3 -m venv venv
    
    echo "🔧 Activating virtual environment..."
    source venv/bin/activate
    echo "✅ Virtual environment activated"
fi

# Upgrade pip to latest version
echo "🔧 Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies
echo "🔧 Installing Python dependencies from requirements.txt..."
pip install -r requirements.txt

# Run setup script
echo "🔧 Running setup script..."
python setup.py

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "To activate the virtual environment in future sessions:"
echo "  source venv/bin/activate"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your API keys"
echo "2. Test the configuration: python main.py validate-config"
echo "3. Analyze a repository: python main.py analyze /path/to/repo"
echo "4. Generate documentation: python main.py --repo-path /path/to/repo"
echo ""
echo "For help: python main.py --help"