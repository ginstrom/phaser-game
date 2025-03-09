#!/usr/bin/env python3
import os
import sys
import importlib.util

# Print current environment
print(f"Current working directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

# List directories
print("\nDirectories:")
print(f"Current directory contents: {os.listdir('.')}")
if os.path.exists('./app'):
    print(f"./app directory contents: {os.listdir('./app')}")
if os.path.exists('./tests'):
    print(f"./tests directory contents: {os.listdir('./tests')}")

# Try different import approaches
print("\nTrying imports:")

# Approach 1: Direct import
try:
    import app.main
    print("✅ Successfully imported 'app.main' directly")
except ImportError as e:
    print(f"❌ Failed to import 'app.main' directly: {e}")

# Approach 2: Import from file path
try:
    app_path = os.path.join(os.getcwd(), 'app', 'main.py')
    if os.path.exists(app_path):
        print(f"File exists at {app_path}")
        spec = importlib.util.spec_from_file_location("app.main", app_path)
        app_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(app_module)
        print("✅ Successfully imported 'app.main' from file path")
        print(f"Module attributes: {dir(app_module)}")
    else:
        print(f"❌ File does not exist at {app_path}")
except Exception as e:
    print(f"❌ Failed to import 'app.main' from file path: {e}")

# Approach 3: Modify sys.path and try again
sys.path.insert(0, os.path.join(os.getcwd(), 'app'))
print(f"\nUpdated Python path: {sys.path}")

try:
    import main
    print("✅ Successfully imported 'main' after path update")
except ImportError as e:
    print(f"❌ Failed to import 'main' after path update: {e}")