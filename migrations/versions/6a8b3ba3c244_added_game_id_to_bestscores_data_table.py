"""Added game_id to BestScores data table

Revision ID: 6a8b3ba3c244
Revises: fe178721d835
Create Date: 2023-11-10 20:22:53.491813

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a8b3ba3c244'
down_revision = 'fe178721d835'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('BestScores', schema=None) as batch_op:
        batch_op.add_column(sa.Column('game_id', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('BestScores', schema=None) as batch_op:
        batch_op.drop_column('game_id')

    # ### end Alembic commands ###
