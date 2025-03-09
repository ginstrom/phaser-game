import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_get_settings(client):
    """
    Test getting the current game settings.
    The endpoint should return the default settings.
    """
    response = client.get("/settings")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "message" in data
    assert "Settings retrieved successfully" in data["message"]
    assert "settings" in data
    
    # Check that all expected settings are present with their default values
    settings = data["settings"]
    assert settings["audio_volume"] == 100
    assert settings["music_volume"] == 100
    assert settings["sfx_volume"] == 100
    assert settings["fullscreen"] is False
    assert settings["resolution"] == "1920x1080"
    assert settings["language"] == "en"
    assert settings["auto_save"] is True
    assert settings["auto_save_interval"] == 5
    assert settings["ui_scale"] == 1.0
    assert settings["show_tutorials"] is True

@pytest.mark.asyncio
async def test_update_settings_all_fields(client):
    """
    Test updating all game settings.
    The endpoint should return the updated settings.
    """
    new_settings = {
        "audio_volume": 80,
        "music_volume": 70,
        "sfx_volume": 90,
        "fullscreen": True,
        "resolution": "2560x1440",
        "language": "fr",
        "auto_save": False,
        "auto_save_interval": 10,
        "ui_scale": 1.2,
        "show_tutorials": False
    }
    
    response = client.post(
        "/settings",
        json={"settings": new_settings}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "message" in data
    assert "Settings updated successfully" in data["message"]
    assert "settings" in data
    
    # Check that all settings were updated correctly
    updated_settings = data["settings"]
    for key, value in new_settings.items():
        assert updated_settings[key] == value

@pytest.mark.asyncio
async def test_update_settings_partial(client):
    """
    Test updating only some of the game settings.
    The endpoint should return all settings with only the specified ones updated.
    """
    partial_settings = {
        "audio_volume": 50,
        "fullscreen": True
    }
    
    response = client.post(
        "/settings",
        json={"settings": partial_settings}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    updated_settings = data["settings"]
    
    # Check that the specified settings were updated
    assert updated_settings["audio_volume"] == 50
    assert updated_settings["fullscreen"] is True
    
    # Check that other settings remain at their default values
    assert updated_settings["music_volume"] == 100
    assert updated_settings["sfx_volume"] == 100
    assert updated_settings["resolution"] == "1920x1080"
    assert updated_settings["language"] == "en"
    assert updated_settings["auto_save"] is True
    assert updated_settings["auto_save_interval"] == 5
    assert updated_settings["ui_scale"] == 1.0
    assert updated_settings["show_tutorials"] is True

@pytest.mark.asyncio
async def test_update_settings_invalid_field(client):
    """
    Test updating settings with an invalid field.
    The endpoint should return a 400 error.
    """
    invalid_settings = {
        "invalid_setting": "value"
    }
    
    response = client.post(
        "/settings",
        json={"settings": invalid_settings}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert "detail" in data
    assert "Invalid setting" in data["detail"]

@pytest.mark.asyncio
async def test_reset_settings(client):
    """
    Test resetting game settings to default values.
    The endpoint should return the default settings.
    """
    # First, update some settings
    client.post(
        "/settings",
        json={"settings": {"audio_volume": 50, "fullscreen": True}}
    )
    
    # Then reset the settings
    response = client.get("/settings/reset")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "message" in data
    assert "Settings reset to defaults" in data["message"]
    assert "settings" in data
    
    # Check that all settings are back to their default values
    settings = data["settings"]
    assert settings["audio_volume"] == 100
    assert settings["music_volume"] == 100
    assert settings["sfx_volume"] == 100
    assert settings["fullscreen"] is False
    assert settings["resolution"] == "1920x1080"
    assert settings["language"] == "en"
    assert settings["auto_save"] is True
    assert settings["auto_save_interval"] == 5
    assert settings["ui_scale"] == 1.0
    assert settings["show_tutorials"] is True