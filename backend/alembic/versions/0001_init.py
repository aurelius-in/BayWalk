from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_init'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'projects',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('targets', sa.JSON(), nullable=False),
        sa.Column('scene_ref', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_table(
        'runs',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('project_id', sa.String(), index=True),
        sa.Column('kind', sa.String(), nullable=False),
        sa.Column('state', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_table(
        'artifacts',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('project_id', sa.String(), index=True),
        sa.Column('kind', sa.String(), nullable=False),
        sa.Column('path', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

def downgrade() -> None:
    op.drop_table('artifacts')
    op.drop_table('runs')
    op.drop_table('projects')
