"""
Build script for Shreelock Video Player
Creates standalone executable with PyInstaller
"""

import subprocess
import sys
import os

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("PyInstaller is already installed")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build_simple_app():
    """Build simple portable application"""
    print("Building simple portable application...")
    
    # PyInstaller command for simple portable app
    cmd = [
        "pyinstaller",
        "--onefile",                    # Create single executable file
        "--windowed",                   # Hide console window
        "--name=ShreelockVideoPlayer",  # Executable name
        "main.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("\n✅ Build successful!")
        print("📁 Executable location: dist/ShreelockVideoPlayer.exe")
        print("📦 Single file - ready to distribute!")
        print("💡 Users can:")
        print("   • Double-click to run immediately")
        print("   • No installation required")
        print("   • Create shortcuts manually if needed")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure VLC is installed on your system")
        print("2. Check that all dependencies are installed")
        print("3. Try running: pip install --upgrade pyinstaller")

def main():
    """Main build function"""
    print("🔨 Shreelock Video Player - Build Script")
    print("=" * 40)
    print("Building recommended portable application...")
    
    try:
        install_pyinstaller()
        build_simple_app()
            
    except KeyboardInterrupt:
        print("\n❌ Build cancelled by user")
    except Exception as e:
        print(f"❌ Build failed: {e}")

if __name__ == "__main__":
    main()