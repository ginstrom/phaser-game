from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_app_works():
    """Test that the app is working."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data 