"""Add perks column to empires

Revision ID: add_perks_column
Revises: 370ec9c71774
Create Date: 2025-03-11 11:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = 'add_perks_column'
down_revision: Union[str, None] = '370ec9c71774'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add perks column with default value in batch mode
    with op.batch_alter_table('empires', schema=None) as batch_op:
        batch_op.add_column(sa.Column('perks', sa.JSON(), nullable=True))
    
    # Set default perks for all existing empires
    connection = op.get_bind()
    connection.execute(
        text("""
            UPDATE empires 
            SET perks = :default_perks
            WHERE perks IS NULL
        """),
        {"default_perks": '{"research_efficiency": 1.0, "combat_efficiency": 1.0, "economic_efficiency": 1.0, "diplomatic_influence": 1.0}'}
    )


def downgrade() -> None:
    # Remove perks column in batch mode
    with op.batch_alter_table('empires', schema=None) as batch_op:
        batch_op.drop_column('perks') 