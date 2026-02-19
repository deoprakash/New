"""
Quick Start Script
Run this to execute the complete workflow
"""

import subprocess
import sys
from pathlib import Path

def main():
    print("="*70)
    print("  RIFT'26 - DevOps Lead Quick Start")
    print("="*70)
    print()
    
    # Check if virtual environment exists
    venv_path = Path("venv")
    if not venv_path.exists():
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"])
        print("[OK] Virtual environment created\n")
    
    # Determine pip path
    if sys.platform == "win32":
        pip_path = venv_path / "Scripts" / "pip.exe"
        python_path = venv_path / "Scripts" / "python.exe"
    else:
        pip_path = venv_path / "bin" / "pip"
        python_path = venv_path / "bin" / "python"
    
    # Install dependencies
    print("Installing dependencies...")
    subprocess.run([str(pip_path), "install", "-r", "requirements.txt", "-q"])
    print("[OK] Dependencies installed\n")
    
    # Run main script
    print("Running main workflow...\n")
    result = subprocess.run([str(python_path), "main.py"])
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(main())
