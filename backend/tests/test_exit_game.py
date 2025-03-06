import pytest
from fastapi import status

def test_exit_game_with_save(client):
    """
    Test exiting the game with saving.
    The endpoint should return a success message and save information.
    """
    response = client.post(
        "/exit",
        json={"save_before_exit": True}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "message" in data
    assert "saved" in data
    assert data["saved"] is True
    assert "save_id" in data
    assert data["save_id"] is not None
    assert "auto-exit" in data["save_id"]

def test_exit_game_with_custom_save_name(client):
    """
    Test exiting the game with a custom save name.
    The endpoint should return a success message and save information with the custom name.
    """
    custom_save_name = "My Custom Save"
    response = client.post(
        "/exit",
        json={"save_before_exit": True, "save_name": custom_save_name}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "message" in data
    assert custom_save_name in data["message"]
    assert "saved" in data
    assert data["saved"] is True
    assert "save_id" in data
    assert "my-custom-save" in data["save_id"]

def test_exit_game_without_save(client):
    """
    Test exiting the game without saving.
    The endpoint should return a success message without save information.
    """
    response = client.post(
        "/exit",
        json={"save_before_exit": False}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "message" in data
    assert "without saving" in data["message"]
    assert "saved" in data
    assert data["saved"] is False
    assert "save_id" not in data

def test_exit_game_default_behavior(client):
    """
    Test exiting the game with default parameters.
    By default, the game should be saved before exit.
    """
    response = client.post(
        "/exit",
        json={}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "message" in data
    assert "saved" in data
    assert data["saved"] is True
    assert "save_id" in data
