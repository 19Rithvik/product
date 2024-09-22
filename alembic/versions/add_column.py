import sqlalchemy as sa
from alembic import op 

def upgrade():
    op.add_column('products',sa.Column('category',sa.String,nullable = True))


def downgrade():
    op.drop_column('products','category')