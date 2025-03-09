import os
import sys

print(f"Current working directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

# Try different import approaches
print("\nTrying imports:")

try:
    import main
    print("✅ Successfully imported 'main'")
except ImportError as e:
    print(f"❌ Failed to import 'main': {e}")

try:
    import app.main
    print("✅ Successfully imported 'app.main'")
except ImportError as e:
    print(f"❌ Failed to import 'app.main': {e}")

try:
    from app import main
    print("✅ Successfully imported 'from app import main'")
except ImportError as e:
    print(f"❌ Failed to import 'from app import main': {e}")

# Add parent directory to path and try again
parent_dir = os.path.dirname(os.getcwd())
sys.path.insert(0, parent_dir)
print(f"\nAdded parent directory to path: {parent_dir}")
print(f"Updated Python path: {sys.path}")

try:
    import app.main
    print("✅ Successfully imported 'app.main' after path update")
except ImportError as e:
    print(f"❌ Failed to import 'app.main' after path update: {e}")