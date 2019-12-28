"""empty message

Revision ID: 6194106093ea
Revises: f4585e832e60
Create Date: 2019-12-28 19:27:38.816748

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6194106093ea'
down_revision = 'f4585e832e60'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Favoritos',
    sa.Column('user_ID', sa.Integer(), nullable=False),
    sa.Column('games_ID', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['games_ID'], ['games.ID'], ),
    sa.ForeignKeyConstraint(['user_ID'], ['user.ID'], ),
    sa.PrimaryKeyConstraint('user_ID', 'games_ID')
    )
    op.create_table('team',
    sa.Column('ID', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.Column('tag', sa.String(length=30), nullable=True),
    sa.Column('owner_ID', sa.Integer(), nullable=True),
    sa.Column('game_ID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['game_ID'], ['games.ID'], ),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_table('User_Team',
    sa.Column('user_ID', sa.Integer(), nullable=False),
    sa.Column('team_ID', sa.Integer(), nullable=False),
    sa.Column('isMember', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['team_ID'], ['team.ID'], ),
    sa.ForeignKeyConstraint(['user_ID'], ['user.ID'], ),
    sa.PrimaryKeyConstraint('user_ID', 'team_ID')
    )
    op.create_table('postulacion',
    sa.Column('ID', sa.Integer(), nullable=False),
    sa.Column('start_date', sa.DATETIME(), nullable=True),
    sa.Column('end_date', sa.DATETIME(), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.Column('team_ID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['team_ID'], ['team.ID'], ),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_table('Registro',
    sa.Column('user_ID', sa.Integer(), nullable=False),
    sa.Column('postulacion_ID', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['postulacion_ID'], ['postulacion.ID'], ),
    sa.ForeignKeyConstraint(['user_ID'], ['user.ID'], ),
    sa.PrimaryKeyConstraint('user_ID', 'postulacion_ID')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Registro')
    op.drop_table('postulacion')
    op.drop_table('User_Team')
    op.drop_table('team')
    op.drop_table('Favoritos')
    # ### end Alembic commands ###
