"""empty message

Revision ID: 70ec071af395
Revises: 0cd48fb556cf
Create Date: 2019-04-25 12:10:58.389103

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70ec071af395'
down_revision = '0cd48fb556cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('candidate', sa.Column('created_by', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'candidate', 'user', ['created_by'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'candidate', type_='foreignkey')
    op.drop_column('candidate', 'created_by')
    # ### end Alembic commands ###
