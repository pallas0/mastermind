"""hm ok let's get you working

Revision ID: fe178721d835
Revises: 5c7f0257c136
Create Date: 2023-11-10 15:30:20.218712

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe178721d835'
down_revision = '5c7f0257c136'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('BestScores',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('player_name', sa.String(length=80), nullable=True),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('BestScores')
    # ### end Alembic commands ###