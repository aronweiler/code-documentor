#!/usr/bin/env python3
"""
Setup script for the Documentation Pipeline
"""

import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False


def main():
    """Main setup function."""
    print("🚀 Setting up Documentation Pipeline")
    print("=" * 50)
    
    # Check if we're in a virtual environment
    if sys.prefix == sys.base_prefix:
        print("⚠️  Warning: You're not in a virtual environment.")
        print("   It's recommended to create one first:")
        print("   python -m venv venv")
        print("   venv\\Scripts\\activate  # On Windows")
        print("   source venv/bin/activate  # On Unix/Mac")
        print()
        
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return
    
    # Install requirements
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        print("❌ Failed to install dependencies. Please check your Python environment.")
        return
    
    # Create .env file if it doesn't exist
    env_file = Path(".env")
    if not env_file.exists():
        env_example = Path(".env.example")
        if env_example.exists():
            env_file.write_text(env_example.read_text())
            print("✅ Created .env file from template")
            print("⚠️  Please edit .env and add your API keys")
        else:
            print("❌ .env.example not found")
    else:
        print("✅ .env file already exists")
    
    print()
    print("🎉 Setup completed!")
    print()
    print("Next steps:")
    print("1. Edit .env file and add your API keys")
    print("2. Test the configuration: python main.py validate-config")
    print("3. Analyze a repository: python main.py analyze /path/to/repo")
    print("4. Generate documentation: python main.py --repo-path /path/to/repo")
    print()
    print("For help: python main.py --help")


if __name__ == "__main__":
    main()
