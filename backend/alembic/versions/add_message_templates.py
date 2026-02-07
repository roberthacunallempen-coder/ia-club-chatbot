"""add message templates table

Revision ID: add_message_templates
Revises: 
Create Date: 2026-01-12

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_message_templates'
down_revision = None  # Update this if you have previous migrations
branch_labels = None
depends_on = None


def upgrade():
    # Create message_templates table
    op.create_table(
        'message_templates',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('messages', sa.JSON(), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('trigger_keywords', sa.JSON(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index(op.f('ix_message_templates_id'), 'message_templates', ['id'], unique=False)
    op.create_index(op.f('ix_message_templates_name'), 'message_templates', ['name'], unique=True)
    op.create_index(op.f('ix_message_templates_category'), 'message_templates', ['category'], unique=False)


def downgrade():
    # Drop indexes
    op.drop_index(op.f('ix_message_templates_category'), table_name='message_templates')
    op.drop_index(op.f('ix_message_templates_name'), table_name='message_templates')
    op.drop_index(op.f('ix_message_templates_id'), table_name='message_templates')
    
    # Drop table
    op.drop_table('message_templates')
