import pytest
from fastapi import status

def test_create_new_game_with_default_values(client):
    """
    Test creating a new game with only the required player_name parameter.
    Default values should be used for difficulty and galaxy_size.
    """
    response = client.post(
        "/new-game",
        json={"player_name": "TestPlayer"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "game_id" in data
    assert "message" in data
    assert "TestPlayer" in data["message"]
    assert "normal" in data["message"]  # Default difficulty
    assert "medium" in data["message"]  # Default galaxy size
    assert "initial_state" in data
    
    # Check player data
    player = data["initial_state"]["player"]
    assert player["name"] == "TestPlayer"
    assert "empire" in player
    assert "resources" in player
    
    # Check galaxy data
    galaxy = data["initial_state"]["galaxy"]
    assert galaxy["size"] == "medium"  # Default galaxy size
    assert "systems" in galaxy
    assert "explored" in galaxy
    
    # Check turn data
    assert data["initial_state"]["turn"] == 1

def test_create_new_game_with_custom_values(client):
    """
    Test creating a new game with custom values for all parameters.
    """
    response = client.post(
        "/new-game",
        json={
            "player_name": "CustomPlayer",
            "difficulty": "hard",
            "galaxy_size": "large"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "CustomPlayer" in data["message"]
    assert "hard" in data["message"]
    assert "large" in data["message"]
    assert data["initial_state"]["player"]["name"] == "CustomPlayer"
    assert data["initial_state"]["galaxy"]["size"] == "large"

def test_create_new_game_missing_player_name(client):
    """
    Test that creating a new game without a player_name returns a validation error.
    """
    response = client.post(
        "/new-game",
        json={}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert "detail" in data
    # Check that the error is about the missing player_name field
    assert any(error["loc"] == ["body", "player_name"] for error in data["detail"])