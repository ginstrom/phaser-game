def test_root_endpoint(client):
    """
    Test the root endpoint of the API.
    It should return a welcome message, version, and documentation URL.
    """
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Welcome to the 4X Space Empire API" in data["message"]
    assert "version" in data
    assert "documentation" in data
    assert data["documentation"] == "/docs"
