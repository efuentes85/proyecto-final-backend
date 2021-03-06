"""empty message

Revision ID: 35789a00d428
Revises: 
Create Date: 2020-01-15 22:18:02.077617

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35789a00d428'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('games',
    sa.Column('ID', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('logo', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_table('user',
    sa.Column('ID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=True),
    sa.Column('last_name', sa.String(length=100), nullable=True),
    sa.Column('password', sa.String(length=256), nullable=False),
    sa.Column('role', sa.Integer(), nullable=True),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.Column('image', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('ID'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_user_ID'), 'user', ['ID'], unique=False)
    op.create_table('favoritos',
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
    sa.Column('logo', sa.String(length=200), nullable=True),
    sa.Column('tag', sa.String(length=30), nullable=True),
    sa.Column('owner_ID', sa.Integer(), nullable=True),
    sa.Column('game_ID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['game_ID'], ['games.ID'], ),
    sa.PrimaryKeyConstraint('ID')
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
    op.create_table('user_team',
    sa.Column('user_ID', sa.Integer(), nullable=False),
    sa.Column('team_ID', sa.Integer(), nullable=False),
    sa.Column('isMember', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['team_ID'], ['team.ID'], ),
    sa.ForeignKeyConstraint(['user_ID'], ['user.ID'], ),
    sa.PrimaryKeyConstraint('user_ID', 'team_ID')
    )
    op.create_table('registro',
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
    op.drop_table('registro')
    op.drop_table('user_team')
    op.drop_table('postulacion')
    op.drop_table('team')
    op.drop_table('favoritos')
    op.drop_index(op.f('ix_user_ID'), table_name='user')
    op.drop_table('user')
    op.drop_table('games')
    # ### end Alembic commands ###
