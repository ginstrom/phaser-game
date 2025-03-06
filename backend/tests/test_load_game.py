import pytest
from fastapi import status

def test_list_saved_games(client):
    """
    Test listing all saved games.
    The endpoint should return a list of saved games.
    """
    response = client.get("/saved-games")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    
    # Check the structure of the first saved game
    first_game = data[0]
    assert "game_id" in first_game
    assert "player_name" in first_game
    assert "empire_name" in first_game
    assert "turn" in first_game
    assert "save_date" in first_game

def test_load_existing_game(client):
    """
    Test loading an existing game by ID.
    The endpoint should return the game state for the specified game ID.
    """
    # First, get a list of saved games to find a valid game ID
    saved_games_response = client.get("/saved-games")
    saved_games = saved_games_response.json()
    valid_game_id = saved_games[0]["game_id"]
    
    # Now try to load the game with the valid ID
    response = client.post(
        "/load-game",
        json={"game_id": valid_game_id}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["game_id"] == valid_game_id
    assert "message" in data
    assert "Game loaded successfully" in data["message"]
    assert "game_state" in data
    
    # Check the structure of the game state
    game_state = data["game_state"]
    assert "player" in game_state
    assert "galaxy" in game_state
    assert "turn" in game_state

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
    response = client.post(
        "/load-game",
        json={}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert "detail" in data
    # Check that the error is about the missing game_id field
    assert any(error["loc"] == ["body", "game_id"] for error in data["detail"])
