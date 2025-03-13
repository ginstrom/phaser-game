import pytest
from sqlalchemy.orm import Session
from typing import Dict

from app.services.empire_service import (
    create_player_empire,
    create_computer_empire,
    initialize_game_empires,
    get_empire,
    get_empires
)
from app.models.empire import EmpireDB, EmpireResponse
from app.utils.config_loader import config
from app.database.models import Game

@pytest.fixture
def test_game(db_session: Session) -> Game:
    """Create a test game in the database."""
    game = Game(
        player_name="TestPlayer",
        difficulty="normal",
        galaxy_size="medium"
    )
    db_session.add(game)
    db_session.commit()
    return game

@pytest.fixture
def test_game_id(test_game: Game) -> str:
    return test_game.id

@pytest.fixture
def test_player_name() -> str:
    return "TestPlayer"

@pytest.fixture
def test_perks() -> Dict:
    return {
        "research_efficiency": 1.0,
        "combat_efficiency": 1.0,
        "economic_efficiency": 1.0,
        "diplomatic_influence": 1.0
    }

def test_create_player_empire(db_session: Session, test_game_id: str, test_player_name: str, test_perks: Dict):
    """Test creating a player empire with default settings."""
    empire_response = create_player_empire(
        db=db_session,
        game_id=test_game_id,
        name=f"{test_player_name}'s Empire",
        perks=test_perks
    )

    assert empire_response is not None
    # Query the database to check game_id
    empire_db = db_session.query(EmpireDB).filter(EmpireDB.id == empire_response.id).first()
    assert empire_db.game_id == test_game_id
    
    # Check other properties from the response
    assert empire_response.name == f"{test_player_name}'s Empire"
    assert empire_response.is_player is True
    assert empire_response.color == "#00FF00"  # Default player color
    assert empire_response.credits == 1000  # Default normal difficulty
    assert empire_response.research_points == 50  # Default normal difficulty
    assert empire_response.perks.model_dump() == test_perks

def test_create_player_empire_with_difficulty(db_session: Session, test_game_id: str, test_player_name: str):
    """Test creating a player empire with different difficulty settings."""
    difficulties = ["easy", "normal", "hard"]
    expected_credits = {"easy": 2000, "normal": 1000, "hard": 500}
    expected_research = {"easy": 100, "normal": 50, "hard": 25}
    
    for difficulty in difficulties:
        empire = create_player_empire(
            db=db_session,
            game_id=test_game_id,
            name=f"{test_player_name}'s Empire",
            difficulty=difficulty
        )
        
        assert empire.credits == expected_credits[difficulty]
        assert empire.research_points == expected_research[difficulty]

def test_create_computer_empire(db_session: Session, test_game_id: str):
    """Test creating a computer-controlled empire."""
    empire_response = create_computer_empire(db=db_session, game_id=test_game_id)

    assert empire_response is not None
    # Query the database to check game_id
    empire_db = db_session.query(EmpireDB).filter(EmpireDB.id == empire_response.id).first()
    assert empire_db.game_id == test_game_id
    
    # Check other properties from the response
    assert empire_response.is_player is False
    assert empire_response.name != ""  # Should have a generated name
    assert empire_response.color != ""  # Should have a color from archetype
    
    # Verify the empire has valid perks from an archetype
    archetypes = config.get_config_section("empire_archetypes")
    archetype_found = False
    for archetype in archetypes:
        if empire_response.perks.model_dump() == archetype.perks.model_dump():
            archetype_found = True
            break
    assert archetype_found

def test_create_computer_empire_hard_difficulty(db_session: Session, test_game_id: str):
    """Test creating a computer empire on hard difficulty with bonuses."""
    empire = create_computer_empire(db=db_session, game_id=test_game_id, difficulty="hard")
    
    starting_resources = config.get_config_section("defaults", "starting_resources")
    normal_resources = starting_resources["normal"]
    assert empire.credits == int(normal_resources.credits * 1.5)
    assert empire.research_points == int(normal_resources.research_points * 1.5)

def test_initialize_game_empires(db_session: Session, test_game_id: str, test_player_name: str):
    """Test initializing all empires for a new game."""
    num_computer_empires = 3
    empires = initialize_game_empires(
        db=db_session,
        game_id=test_game_id,
        player_name=test_player_name,
        num_computer_empires=num_computer_empires
    )
    
    assert len(empires) == num_computer_empires + 1  # +1 for player empire
    
    # Verify player empire
    player_empires = [e for e in empires if e.is_player]
    assert len(player_empires) == 1
    assert player_empires[0].name == f"{test_player_name}'s Empire"
    
    # Verify computer empires
    computer_empires = [e for e in empires if not e.is_player]
    assert len(computer_empires) == num_computer_empires
    
    # Verify all empires have unique names and colors
    names = [e.name for e in empires]
    colors = [e.color for e in empires]
    assert len(set(names)) == len(names)  # All names should be unique
    assert len(set(colors)) == len(colors)  # All colors should be unique

def test_initialize_game_empires_validation(db_session: Session, test_game_id: str, test_player_name: str):
    """Test validation of number of computer empires."""
    game_settings = config.get_config_section("game_settings")
    min_empires = game_settings.min_computer_empires
    max_empires = game_settings.max_computer_empires
    
    # Test minimum boundary
    with pytest.raises(ValueError):
        initialize_game_empires(
            db=db_session,
            game_id=test_game_id,
            player_name=test_player_name,
            num_computer_empires=min_empires - 1
        )
    
    # Test maximum boundary
    with pytest.raises(ValueError):
        initialize_game_empires(
            db=db_session,
            game_id=test_game_id,
            player_name=test_player_name,
            num_computer_empires=max_empires + 1
        )

def test_get_empire(db_session: Session, test_game_id: str, test_player_name: str):
    """Test retrieving a specific empire."""
    # Create an empire first
    created_empire = create_player_empire(
        db=db_session,
        game_id=test_game_id,
        name=f"{test_player_name}'s Empire"
    )
    
    # Retrieve the empire
    retrieved_empire = get_empire(db_session, test_game_id, created_empire.id)
    
    assert retrieved_empire is not None
    assert retrieved_empire.id == created_empire.id
    assert retrieved_empire.name == created_empire.name

def test_get_empires(db_session: Session, test_game_id: str, test_player_name: str):
    """Test retrieving all empires for a game."""
    # Initialize game with empires
    num_computer_empires = 3
    created_empires = initialize_game_empires(
        db=db_session,
        game_id=test_game_id,
        player_name=test_player_name,
        num_computer_empires=num_computer_empires
    )
    
    # Retrieve all empires
    retrieved_empires = get_empires(db_session, test_game_id)
    
    assert len(retrieved_empires) == len(created_empires)
    assert all(isinstance(empire, EmpireResponse) for empire in retrieved_empires)
    
    # Verify we have the correct number of player and computer empires
    player_empires = [e for e in retrieved_empires if e.is_player]
    computer_empires = [e for e in retrieved_empires if not e.is_player]
    assert len(player_empires) == 1
    assert len(computer_empires) == num_computer_empires 