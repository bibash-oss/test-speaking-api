"""create questions table

Revision ID: b91f0c43a7e2
Revises: 599f0b628212
Create Date: 2026-11-03 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'b91f0c43a7e2'
down_revision = '599f0b628212'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'questions',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('question_type', sa.String(length=50), nullable=False),
        sa.Column('difficulty', sa.String(length=50), nullable=False),
        sa.Column('content', postgresql.JSONB(astext_type=sa.Text()).with_variant(sa.JSON(), 'sqlite'), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('duration', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(length=36), nullable=True),
        sa.Column('updated_by', sa.String(length=36), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('questions', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_questions_question_type'), ['question_type'], unique=False)
        batch_op.create_index(batch_op.f('ix_questions_difficulty'), ['difficulty'], unique=False)
        batch_op.create_index(batch_op.f('ix_questions_is_active'), ['is_active'], unique=False)


def downgrade():
    with op.batch_alter_table('questions', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_questions_is_active'))
        batch_op.drop_index(batch_op.f('ix_questions_difficulty'))
        batch_op.drop_index(batch_op.f('ix_questions_question_type'))

    op.drop_table('questions')

