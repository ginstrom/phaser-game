import pytest
from fastapi import status

def test_create_new_game_with_default_values(client):
    """
    Test creating a new game with only the required player_name parameter.
    Default values should be used for difficulty and galaxy_size.
    """
    response = client.post(
        "/api/v1/games/new",
        json={"player_name": "TestPlayer"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["game_id"]
    assert data["message"]
    assert data["initial_state"]

def test_create_new_game_with_custom_values(client):
    """
    Test creating a new game with custom values for all parameters.
    """
    response = client.post(
        "/api/v1/games/new",
        json={
            "player_name": "CustomPlayer",
            "difficulty": "hard",
            "galaxy_size": "large"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["game_id"]
    assert data["message"]
    assert data["initial_state"]
    assert data["initial_state"]["difficulty"] == "hard"
    assert data["initial_state"]["galaxy_size"] == "large"

def test_create_new_game_missing_player_name(client):
    """
    Test that creating a new game without a player_name returns a validation error.
    """
    response = client.post(
        "/api/v1/games/new",
        json={}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY