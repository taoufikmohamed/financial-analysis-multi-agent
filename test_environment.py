# test_environment.py
import sys
import os

def test_python_environment():
    """Check Python environment"""
    print("\n" + "="*60)
    print("🐍 PYTHON ENVIRONMENT CHECK")
    print("="*60)
    
    print(f"\nPython version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Current working directory: {os.getcwd()}")
    
    print("\n📂 Python path:")
    for i, path in enumerate(sys.path):
        print(f"  {i}: {path}")
    
    print("\n📦 Installed packages (try to import common ones):")
    packages_to_check = ['pytest', 'asyncio', 'dotenv']
    for package in packages_to_check:
        try:
            if package == 'dotenv':
                from dotenv import load_dotenv
                print(f"  ✅ python-dotenv is installed")
            else:
                __import__(package)
                print(f"  ✅ {package} is installed")
        except ImportError:
            print(f"  ❌ {package} is NOT installed")
    
    print("\n" + "="*60)