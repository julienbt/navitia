"""Add language column for Asgard

Revision ID: 7a77ccf8f94e
Revises: 9c9e9706c049
Create Date: 2021-11-15 16:45:46.699720

"""

# revision identifiers, used by Alembic.
revision = '7a77ccf8f94e'
down_revision = '9c9e9706c049'

from alembic import op
import sqlalchemy as sa
from navitiacommon import default_values


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'instance',
        sa.Column(
            'asgard_language',
            sa.Text(),
            nullable=False,
            server_default='{}'.format(default_values.asgard_language),
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('instance', 'asgard_language')
    # ### end Alembic commands ###
