"""Add player empire foreign key

Revision ID: 370ec9c71774
Revises: 8a45fd57e4fa
Create Date: 2025-03-11 11:29:35.786973

"""
from typing import Sequence, Union
import uuid

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = '370ec9c71774'
down_revision: Union[str, None] = '8a45fd57e4fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create a new table with the desired schema
    with op.batch_alter_table('games', schema=None) as batch_op:
        batch_op.add_column(sa.Column('player_empire_id', sa.String(), nullable=True))
    
    # Create a new empire for each existing game and set it as the player's empire
    connection = op.get_bind()
    games = connection.execute(text("SELECT id, empire_name FROM games")).fetchall()
    
    for game in games:
        empire_id = str(uuid.uuid4())
        empire_name = game[1] if game[1] else 'Human Empire'
        
        # Insert new empire
        connection.execute(
            text("INSERT INTO empires (id, game_id, name, is_player, color) VALUES (:id, :game_id, :name, :is_player, :color)"),
            {"id": empire_id, "game_id": game[0], "name": empire_name, "is_player": True, "color": '#0000FF'}
        )
        
        # Update game with new empire id
        connection.execute(
            text("UPDATE games SET player_empire_id = :empire_id WHERE id = :game_id"),
            {"empire_id": empire_id, "game_id": game[0]}
        )
    
    # Add foreign key and remove old column in batch mode
    with op.batch_alter_table('games', schema=None) as batch_op:
        batch_op.create_foreign_key('fk_games_player_empire_id_empires', 'empires',
                                  ['player_empire_id'], ['id'])
        batch_op.drop_column('empire_name')


def downgrade() -> None:
    # Add back the empire_name column and remove foreign key in batch mode
    with op.batch_alter_table('games', schema=None) as batch_op:
        batch_op.add_column(sa.Column('empire_name', sa.String(), nullable=True))
        batch_op.drop_constraint('fk_games_player_empire_id_empires', type_='foreignkey')
    
    # Copy empire names back from the empires table
    connection = op.get_bind()
    connection.execute(
        text("""
            UPDATE games
            SET empire_name = (
                SELECT name 
                FROM empires 
                WHERE games.player_empire_id = empires.id
            )
        """)
    )
    
    # Remove the player_empire_id column in batch mode
    with op.batch_alter_table('games', schema=None) as batch_op:
        batch_op.drop_column('player_empire_id')
