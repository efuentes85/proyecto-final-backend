"""empty message

Revision ID: b933ecc400dd
Revises: 478c899cd9c8
Create Date: 2020-01-14 00:19:04.871107

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b933ecc400dd'
down_revision = '478c899cd9c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('registro', sa.Column('date', sa.DATETIME(), nullable=False))
    op.drop_constraint('registro_ibfk_2', 'registro', type_='foreignkey')
    op.drop_constraint('registro_ibfk_1', 'registro', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('registro_ibfk_1', 'registro', 'postulacion', ['postulacion_ID'], ['ID'])
    op.create_foreign_key('registro_ibfk_2', 'registro', 'user', ['user_ID'], ['ID'])
    op.drop_column('registro', 'date')
    # ### end Alembic commands ###
