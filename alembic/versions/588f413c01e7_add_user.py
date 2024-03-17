"""Add User

Revision ID: 588f413c01e7
Revises: 
Create Date: 2024-03-16 20:28:09.408724

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '588f413c01e7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('status', postgresql.ENUM('ALIVE', 'DEAD', 'FINISHED', name='status_enum'), nullable=False),
    sa.Column('status_updated_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('msg_num', sa.Integer(), nullable=False),
    sa.Column('msg_sent_at', sa.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###