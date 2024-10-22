"""Add file_name to profile_picture

Revision ID: 58f70f60108a
Revises: e96f0673a8c6
Create Date: 2024-10-05 20:48:35.741676

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '58f70f60108a'
down_revision: Union[str, None] = 'e96f0673a8c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('profile_picture', sa.Column('file_name', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('profile_picture', 'file_name')
    # ### end Alembic commands ###