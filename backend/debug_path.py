import os
import sys

print("Current working directory:", os.getcwd())
print("Python path:", sys.path)

# Try to import the app module
try:
    import app
    print("Successfully imported app module")
    try:
        from app import main
        print("Successfully imported app.main module")
    except ImportError as e:
        print(f"Failed to import app.main: {e}")
except ImportError as e:
    print(f"Failed to import app module: {e}")

# List all files in the current directory
print("\nFiles in current directory:")
for item in os.listdir('.'):
    print(f"  {item}")

# List all files in the app directory if it exists
app_dir = os.path.join('.', 'app')
if os.path.exists(app_dir):
    print(f"\nFiles in {app_dir} directory:")
    for item in os.listdir(app_dir):
        print(f"  {item}")