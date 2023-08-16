"""add address fields to User table

Revision ID: 96ce8d4eeea8
Revises: fbae2326d8bf
Create Date: 2023-08-15 20:39:00.507490

"""
from alembic import op
import sqlalchemy as sa


revision = '96ce8d4eeea8'
down_revision = 'fbae2326d8bf'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('address', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('number', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('zip_code', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('neighborhood', sa.String(length=255), nullable=True))


def downgrade():
    op.drop_column('users', 'neighborhood')
    op.drop_column('users', 'zip_code')
    op.drop_column('users', 'number')
    op.drop_column('users', 'address')
