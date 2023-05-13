"""add_campos_user_table

Revision ID: fbae2326d8bf
Revises: 86beea6dab18
Create Date: 2023-05-12 21:43:42.875325

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbae2326d8bf'
down_revision = '86beea6dab18'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column(
        'lastname', sa.String(length=255), nullable=True, server_default=''))
    op.add_column('users', sa.Column(
        'document', sa.String(length=255), nullable=True, server_default=''))
    op.add_column('users', sa.Column('phone_number',
                  sa.String(length=255), nullable=True, server_default=''))
    op.add_column('users', sa.Column(
        'pwd', sa.String(length=255), nullable=True, server_default=''))
    op.add_column('users', sa.Column(
        'activated', sa.Boolean(), nullable=True, server_default='true'))
    op.alter_column('users', 'email',
                    existing_type=sa.VARCHAR(length=120),
                    nullable=True)
    op.alter_column('users', 'name',
                    existing_type=sa.VARCHAR(length=50),
                    nullable=True)

    op.create_unique_constraint(None, 'users', ['email'])
    alter_columns()


def alter_columns():

    op.alter_column('users', 'lastname', nullable=False)
    op.alter_column('users', 'document', nullable=False)
    op.alter_column('users', 'phone_number', nullable=False)
    op.alter_column('users', 'pwd', nullable=False)
    op.alter_column('users', 'activated', nullable=False)
    op.alter_column('users', 'email', nullable=False)
    op.alter_column('users', 'name', nullable=False)


def downgrade():
    op.alter_column('users', 'name',
                    existing_type=sa.VARCHAR(length=50),
                    nullable=True)
    op.alter_column('users', 'email',
                    existing_type=sa.VARCHAR(length=120),
                    nullable=True)
    op.drop_column('users', 'activated')
    op.drop_column('users', 'pwd')
    op.drop_column('users', 'phone_number')
    op.drop_column('users', 'document')
    op.drop_column('users', 'lastname')
    op.drop_constraint('users_email_key', 'users', type_='unique')
