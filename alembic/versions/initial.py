from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'products',
        sa.Column('id',sa.Integer(),primary_key = True),
        sa.Column('name',sa.String(),nullable =False),
        sa.Column('price',sa.Float(),nullable=False),
        sa.Column('quantity',sa.Integer(),nullable=False),
        sa.Column('description',sa.String(),nullable=False),
    )

def downgrade():
    op.drop_table('products')