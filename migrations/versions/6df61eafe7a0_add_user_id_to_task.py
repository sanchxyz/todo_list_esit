"""Add user_id to Task

Revision ID: 6df61eafe7a0
Revises: 5ab8b615b0d2
Create Date: 2025-01-22 14:49:56.630508

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6df61eafe7a0'
down_revision = '5ab8b615b0d2'
branch_labels = None
depends_on = None

def upgrade():
    # Crear una tabla temporal con la nueva estructura
    op.create_table(
        'task_new',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('completed', sa.Boolean(), default=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE')
    )

    # Copiar datos de la tabla original a la nueva
    op.execute('''
        INSERT INTO task_new (id, title, completed)
        SELECT id, title, completed FROM task
    ''')

    # Eliminar la tabla original
    op.drop_table('task')

    # Renombrar la tabla nueva a la original
    op.rename_table('task_new', 'task')


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###
