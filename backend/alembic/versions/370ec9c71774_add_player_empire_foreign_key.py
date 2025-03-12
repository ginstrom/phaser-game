"""Add player empire foreign key

Revision ID: 370ec9c71774
Revises: 8a45fd57e4fa
Create Date: 2025-03-11 11:29:35.786973

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '370ec9c71774'
down_revision: Union[str, None] = '8a45fd57e4fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add player_empire_id column
    op.add_column('games', sa.Column('player_empire_id', sa.String(), nullable=True))
    
    # Create a new empire for each existing game and set it as the player's empire
    op.execute("""
        WITH new_empires AS (
            INSERT INTO empires (id, game_id, name, is_player, color)
            SELECT 
                gen_random_uuid()::text, 
                games.id, 
                COALESCE(games.empire_name, 'Human Empire'), 
                true, 
                '#0000FF'
            FROM games
            RETURNING id, game_id
        )
        UPDATE games
        SET player_empire_id = new_empires.id
        FROM new_empires
        WHERE games.id = new_empires.game_id
    """)
    
    # Create the foreign key constraint
    op.create_foreign_key('fk_games_player_empire_id_empires', 'games', 'empires',
                         ['player_empire_id'], ['id'])
    
    # Remove the old empire_name column
    op.drop_column('games', 'empire_name')


def downgrade() -> None:
    # Add back the empire_name column
    op.add_column('games', sa.Column('empire_name', sa.String(), nullable=True))
    
    # Copy empire names back from the empires table
    op.execute("""
        UPDATE games
        SET empire_name = empires.name
        FROM empires
        WHERE games.player_empire_id = empires.id
    """)
    
    # Remove the player_empire_id foreign key and column
    op.drop_constraint('fk_games_player_empire_id_empires', 'games', type_='foreignkey')
    op.drop_column('games', 'player_empire_id')
