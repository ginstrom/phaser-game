import pytest
from app.services.game_service import create_new_game, get_game
from app.database.models import Game, Galaxy, StarSystem, Planet
from app.models.game import GameCreate

class TestGameCreation:
    def test_create_new_game(self, db_session):
        """Test the game creation service."""
        game = create_new_game(
            db_session,
            player_name="TestPlayer",
            difficulty="normal",
            galaxy_size="medium"
        )
        
        # Verify game creation
        assert game.player_name == "TestPlayer"
        assert game.difficulty == "normal"
        assert game.galaxy_size == "medium"
        
        # Verify player resources through the game state
        game_dict = game.to_dict()
        assert game_dict["player"]["resources"]["mineral"] == 500  # Starting resources
        assert game_dict["player"]["resources"]["energy"] == 200
        assert game_dict["player"]["resources"]["credits"] == 1000

    def test_galaxy_generation(self, db_session):
        """Test galaxy generation logic."""
        game = create_new_game(
            db_session,
            player_name="TestPlayer",
            difficulty="normal",
            galaxy_size="medium"
        )
        
        game_dict = game.to_dict()
        # Verify star systems were generated
        assert len(game_dict["galaxy"]["systems"]) > 0
        
        # Check that systems have valid positions
        for system in game_dict["galaxy"]["systems"]:
            assert 0 <= system["position_x"] <= 1
            assert 0 <= system["position_y"] <= 1
            assert system["name"] is not None
            
            # Verify planets were generated
            assert len(system["planets"]) > 0
            for planet in system["planets"]:
                assert planet["name"] is not None
                assert planet["type"] in ["terrestrial", "gas_giant", "ice_giant", "rocky", "volcanic", "oceanic", "jungle", "desert", "arctic"]
                assert 1 <= planet["size"] <= 10
                
                # Verify planet resources
                assert "resources" in planet
                assert planet["resources"]["organic"] >= 0
                assert planet["resources"]["mineral"] >= 0
                assert planet["resources"]["energy"] >= 0
                assert planet["resources"]["exotics"] >= 0

class TestGameLoading:
    def test_load_existing_game(self, db_session):
        """Test loading an existing game."""
        # First create a game
        original_game = create_new_game(
            db_session,
            player_name="TestPlayer",
            difficulty="normal",
            galaxy_size="medium"
        )
        game_id = original_game.id
        
        # Then load it
        loaded_game = get_game(db_session, game_id)
        
        assert loaded_game is not None
        assert loaded_game.id == game_id
        assert loaded_game.player_name == "TestPlayer"
        assert loaded_game.difficulty == "normal"
        assert loaded_game.galaxy_size == "medium"

    def test_load_nonexistent_game(self, db_session):
        """Test loading a game that doesn't exist."""
        loaded_game = get_game(db_session, "nonexistent-id")
        assert loaded_game is None

class TestGameMechanics:
    def test_system_discovery(self, db_session):
        """Test system discovery mechanics."""
        game = create_new_game(
            db_session,
            player_name="TestPlayer",
            difficulty="normal",
            galaxy_size="medium"
        )
        
        game_dict = game.to_dict()
        # Get a system that isn't the starting system
        unexplored_system = next(
            system for system in game_dict["galaxy"]["systems"]
            if not system["explored"]
        )
        
        # Initially should be unexplored
        assert not unexplored_system["explored"]
        assert unexplored_system["discovery_level"] == 0

    def test_planet_colonization(self, db_session):
        """Test planet colonization mechanics."""
        game = create_new_game(
            db_session,
            player_name="TestPlayer",
            difficulty="normal",
            galaxy_size="medium"
        )
        
        game_dict = game.to_dict()
        # Find a suitable planet to colonize
        planet = next(
            planet for system in game_dict["galaxy"]["systems"]
            for planet in system["planets"]
            if planet["type"] in ["terrestrial", "oceanic", "jungle"]
            and not planet["colonized"]
        )
        
        # Initially should not be colonized
        assert not planet["colonized"]
        assert planet["owner"] is None 