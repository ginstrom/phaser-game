import pytest
from sqlalchemy.orm import Session
from app.database.models import Game, Galaxy, StarSystem, Planet, Empire, PlanetResources, PlayerResources
from datetime import datetime

class TestGameModel:
    def test_game_creation(self, db_session: Session):
        """Test creating a new game record."""
        game = Game(
            player_name="TestPlayer",
            difficulty="normal",
            galaxy_size="medium"
        )
        db_session.add(game)
        db_session.commit()
        
        assert game.id is not None
        assert game.created_at is not None
        assert game.turn == 1
        assert game.player_name == "TestPlayer"

    def test_game_relationships(self, db_session: Session):
        """Test game relationships with other models."""
        game = Game(
            player_name="TestPlayer",
            difficulty="normal",
            galaxy_size="medium"
        )
        
        # Create related entities
        galaxy = Galaxy(game=game, size="medium")
        empire = Empire(game=game, name="Test Empire", is_player=True, color="#FF0000")
        player_resources = PlayerResources(game=game)
        
        # Add all entities to session
        db_session.add(game)
        db_session.add(galaxy)
        db_session.add(empire)
        db_session.add(player_resources)
        db_session.commit()
        
        # Refresh the game object to ensure relationships are loaded
        db_session.refresh(game)
        
        assert game.galaxy == galaxy
        assert len(game.empires) == 1
        assert game.empires[0] == empire
        assert game.player_resources == player_resources

class TestGalaxyModel:
    def test_galaxy_creation(self, db_session: Session):
        """Test creating a new galaxy."""
        game = Game(
            player_name="TestPlayer",
            difficulty="normal",
            galaxy_size="medium"
        )
        galaxy = Galaxy(game=game, size="medium")
        db_session.add_all([game, galaxy])
        db_session.commit()
        
        assert galaxy.id is not None
        assert galaxy.size == "medium"
        assert galaxy.explored_count == 0

    def test_galaxy_systems(self, db_session: Session):
        """Test galaxy relationship with star systems."""
        game = Game(
            player_name="TestPlayer",
            difficulty="normal",
            galaxy_size="medium"
        )
        galaxy = Galaxy(game=game, size="medium")
        system = StarSystem(
            galaxy=galaxy,
            name="Test System",
            position_x=0.5,
            position_y=0.5
        )
        db_session.add_all([game, galaxy, system])
        db_session.commit()
        
        assert len(galaxy.systems) == 1
        assert galaxy.systems[0] == system

class TestStarSystemModel:
    def test_star_system_creation(self, db_session: Session):
        """Test creating a new star system."""
        game = Game(
            player_name="TestPlayer",
            difficulty="normal",
            galaxy_size="medium"
        )
        galaxy = Galaxy(game=game, size="medium")
        system = StarSystem(
            galaxy=galaxy,
            name="Test System",
            position_x=0.5,
            position_y=0.5
        )
        db_session.add_all([game, galaxy, system])
        db_session.commit()
        
        assert system.id is not None
        assert system.name == "Test System"
        assert system.position_x == 0.5
        assert system.position_y == 0.5
        assert not system.explored
        assert system.discovery_level == 0

class TestPlanetModel:
    def test_planet_creation(self, db_session: Session):
        """Test creating a new planet."""
        game = Game(
            player_name="TestPlayer",
            difficulty="normal",
            galaxy_size="medium"
        )
        galaxy = Galaxy(game=game, size="medium")
        system = StarSystem(
            galaxy=galaxy,
            name="Test System",
            position_x=0.5,
            position_y=0.5
        )
        planet = Planet(
            system=system,
            name="Test Planet",
            type="terrestrial",
            size=5
        )
        db_session.add_all([game, galaxy, system, planet])
        db_session.commit()
        
        assert planet.id is not None
        assert planet.name == "Test Planet"
        assert planet.type == "terrestrial"
        assert planet.size == 5
        assert not planet.colonized
        assert planet.empire_id is None

    def test_planet_resources(self, db_session: Session):
        """Test planet relationship with resources."""
        game = Game(
            player_name="TestPlayer",
            difficulty="normal",
            galaxy_size="medium"
        )
        galaxy = Galaxy(game=game, size="medium")
        system = StarSystem(
            galaxy=galaxy,
            name="Test System",
            position_x=0.5,
            position_y=0.5
        )
        planet = Planet(
            system=system,
            name="Test Planet",
            type="terrestrial",
            size=5
        )
        resources = PlanetResources(
            planet=planet,
            organic=100,
            mineral=200,
            energy=150,
            exotics=50
        )
        db_session.add_all([game, galaxy, system, planet, resources])
        db_session.commit()
        
        assert planet.resources == resources
        assert planet.resources.organic == 100
        assert planet.resources.mineral == 200 