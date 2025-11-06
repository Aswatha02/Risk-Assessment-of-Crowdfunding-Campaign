#!/usr/bin/env python
"""
Setup script for CrowdRisk project
Automates installation and initial setup
"""

import os
import sys
import subprocess
import platform

def print_header(message):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {message}")
    print("=" * 60 + "\n")

def run_command(command, cwd=None):
    """Run a shell command"""
    try:
        print(f"Running: {command}")
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print_header("Checking Python Version")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def check_node():
    """Check if Node.js is installed"""
    print_header("Checking Node.js")
    try:
        result = subprocess.run(
            ["node", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ Node.js {result.stdout.strip()} detected")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Node.js not found. Please install Node.js 16+")
        return False

def install_python_dependencies():
    """Install Python dependencies"""
    print_header("Installing Python Dependencies")
    return run_command(f"{sys.executable} -m pip install -r requirements.txt")

def install_frontend_dependencies():
    """Install frontend dependencies"""
    print_header("Installing Frontend Dependencies")
    frontend_dir = os.path.join(os.getcwd(), "frontend")
    return run_command("npm install", cwd=frontend_dir)

def create_directories():
    """Create necessary directories"""
    print_header("Creating Directories")
    dirs = [
        "data/processed",
        "trained_models",
        "logs"
    ]
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"✅ Created: {dir_path}")
    return True

def copy_env_file():
    """Copy .env.example to .env if not exists"""
    print_header("Setting Up Environment File")
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            import shutil
            shutil.copy(".env.example", ".env")
            print("✅ Created .env file from .env.example")
        else:
            print("⚠️  .env.example not found")
    else:
        print("✅ .env file already exists")
    return True

def train_models():
    """Train ML models"""
    print_header("Training Machine Learning Models")
    print("This may take several minutes...")
    
    backend_dir = os.path.join(os.getcwd(), "backend", "app")
    return run_command(f"{sys.executable} train.py", cwd=backend_dir)

def main():
    """Main setup function"""
    print("\n" + "🎯" * 30)
    print("  CrowdRisk - Automated Setup")
    print("🎯" * 30)
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    if not check_node():
        sys.exit(1)
    
    # Setup steps
    steps = [
        ("Creating directories", create_directories),
        ("Setting up environment", copy_env_file),
        ("Installing Python dependencies", install_python_dependencies),
        ("Installing frontend dependencies", install_frontend_dependencies),
    ]
    
    for step_name, step_func in steps:
        if not step_func():
            print(f"\n❌ Setup failed at: {step_name}")
            sys.exit(1)
    
    # Ask about model training
    print_header("Model Training")
    print("Do you want to train the ML models now?")
    print("(This requires the Kickstarter dataset in data/raw/)")
    response = input("Train models? (y/n): ").strip().lower()
    
    if response == 'y':
        if not train_models():
            print("\n⚠️  Model training failed. You can train later with:")
            print("   cd backend/app && python train.py")
    
    # Success message
    print_header("Setup Complete! 🎉")
    print("Next steps:")
    print("\n1. Start the backend:")
    print("   cd backend/app")
    print("   python main.py")
    print("\n2. Start the frontend (in a new terminal):")
    print("   cd frontend")
    print("   npm run dev")
    print("\n3. Access the application:")
    print("   Frontend: http://localhost:3000")
    print("   API Docs: http://localhost:8000/docs")
    print("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
    main()
