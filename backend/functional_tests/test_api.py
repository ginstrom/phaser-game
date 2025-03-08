import requests

def test_api_available():
    """
    Functional test to verify that the API is available.
    The test sends an HTTP GET request to the API's root endpoint ("/")
    and asserts that the returned status code is 200.
    Adjust the URL if your server runs on a different host or port.
    """
    url = "http://localhost:8000/"
    response = requests.get(url)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
