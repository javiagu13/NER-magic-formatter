import subprocess
import os

def create_executable():
    # Define the name of the Python script to be converted to an executable
    script_name = 'app.py'
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller.__main__
    except ImportError:
        print("PyInstaller is not installed. Installing now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Run PyInstaller
    try:
        subprocess.run(['pyinstaller', '--onefile', '--noconsole', script_name], check=True)
        print(f"Executable for {script_name} created successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create executable: {e}")

    # Clean up the build directories created by PyInstaller
    for folder in ['build', '__pycache__']:
        if os.path.exists(folder):
            import shutil
            shutil.rmtree(folder)

    # Optionally, remove the spec file if you don't need it
    spec_file = script_name.replace('.py', '.spec')
    if os.path.exists(spec_file):
        os.remove(spec_file)

if __name__ == "__main__":
    create_executable()
