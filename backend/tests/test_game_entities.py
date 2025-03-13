import pytest
from sqlalchemy.orm import Session
from app.database.models import (
    Game as GameDB,
    PlayerResources as PlayerResourcesDB,
    Galaxy as GalaxyDB,
    Empire
)
from app.config import Difficulty, GalaxySize

@pytest.fixture
def test_game(db_session, sample_player):
    # Create test game in database
    game = GameDB(
        player_name=sample_player["name"],
        difficulty=Difficulty.NORMAL,
        galaxy_size=GalaxySize.SMALL
    )
    
    resources = PlayerResourcesDB(
        game=game,
        **sample_player["resources"]
    )
    
    galaxy = GalaxyDB(
        game=game,
        size=GalaxySize.SMALL
    )
    
    # Create player empire
    empire = Empire(
        game=game,
        name=f"{sample_player['name']}'s Empire",
        is_player=True,
        color="#00FF00"
    )
    
    db_session.add(game)
    db_session.add(resources)
    db_session.add(galaxy)
    db_session.add(empire)
    db_session.commit()
    
    # Update game with player empire
    game.player_empire_id = empire.id
    db_session.commit()
    
    return game 