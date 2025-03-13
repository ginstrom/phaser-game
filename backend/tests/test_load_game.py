import pytest
from fastapi import status

def test_list_saved_games(client):
    """
    Test listing all saved games.
    The endpoint should return a list of saved games.
    """
    # First create a game to ensure there's at least one to list
    client.post(
        "/api/v1/games/new",
        json={
            "player_name": "TestPlayer",
            "difficulty": "normal",
            "galaxy_size": "medium"
        }
    )
    
    response = client.get("/api/v1/games/saved")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "game_id" in data[0]
    assert "player_name" in data[0]
    
    # Check the structure of the first saved game
    first_game = data[0]
    assert "game_id" in first_game  # API returns game_id
    assert "player_name" in first_game
    assert "empire_name" in first_game
    assert "turn" in first_game
    assert "save_date" in first_game

def test_load_existing_game(client):
    """
    Test loading an existing game by ID.
    The endpoint should return the game state for the specified game ID.
    """
    # First, create a new game to get a valid game ID
    new_game_response = client.post(
        "/api/v1/games/new",
        json={
            "player_name": "LoadGameTest",
            "difficulty": "normal",
            "galaxy_size": "medium"
        }
    )
    assert new_game_response.status_code == 200
    new_game_data = new_game_response.json()
    assert "id" in new_game_data
    valid_game_id = new_game_data["id"]

    # Now try to load the game with the valid ID
    response = client.post(f"/api/v1/games/load?game_id={valid_game_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["game_id"] == valid_game_id
    assert "game_state" in data
    assert "empires" in data

def test_load_nonexistent_game(client):
    """
    Test loading a game with a non-existent ID.
    The endpoint should return a 404 error.
    """
    response = client.post(
        "/load-game",
        json={"game_id": "non-existent-id"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()

def test_load_game_missing_id(client):
    """
    Test loading a game without providing a game ID.
    The endpoint should return a validation error.
    """
    response = client.post("/api/v1/games/load")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY