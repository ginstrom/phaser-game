import os
import sys
from fastapi.testclient import TestClient

# Add the current directory to sys.path
sys.path.insert(0, os.getcwd())

# Import the app
from app.main import app
from app.database.config import get_db, Base

# Create a test client
client = TestClient(app)

def test_root():
    """Test the root endpoint."""
    response = client.get("/")
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Welcome to the 4X Space Empire API"
    print("Test passed!")

if __name__ == "__main__":
    # Run the test directly
    print("Running test_root...")
    test_root()
    print("All tests passed!")