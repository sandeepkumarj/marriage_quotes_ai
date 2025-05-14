"""
Setup script to install dependencies for the Marriage Quotes AI project.
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install the required dependencies."""
    print("Installing dependencies...")
    
    # Install PyTorch first
    print("\n=== Installing PyTorch ===")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "torch"])
        print("PyTorch installed successfully!")
    except subprocess.CalledProcessError:
        print("Failed to install PyTorch. Please install it manually.")
        return False
    
    # Install other dependencies
    print("\n=== Installing other dependencies ===")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("All dependencies installed successfully!")
    except subprocess.CalledProcessError:
        print("Failed to install some dependencies. Please check the error messages.")
        return False
    
    return True

def create_directories():
    """Create necessary directories."""
    print("\n=== Creating directories ===")
    os.makedirs("output", exist_ok=True)
    print("Created 'output' directory")

def main():
    """Main function to set up the project."""
    print("=== Marriage Quotes AI Setup ===")
    
    # Install dependencies
    if not install_dependencies():
        print("\nSetup failed. Please fix the issues and try again.")
        return
    
    # Create directories
    create_directories()
    
    print("\n=== Setup completed successfully! ===")
    print("\nYou can now run the application:")
    print("1. To test email functionality: python test_email.py")
    print("2. To test Instagram posting: python test_instagram.py")
    print("3. To run the scheduler: python main.py")
    print("4. To run once immediately: python main.py --run-now")

if __name__ == "__main__":
    main()
