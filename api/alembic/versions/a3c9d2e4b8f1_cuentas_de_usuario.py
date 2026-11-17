"""cuentas de usuario para auth JWT

Revision ID: a3c9d2e4b8f1
Revises: f85f1e7f6b42
Create Date: 2026-11-17 09:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'a3c9d2e4b8f1'
down_revision: Union[str, Sequence[str], None] = 'f85f1e7f6b42'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('cuenta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('usuario', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('nombre', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('rol', sa.Enum('OPERARIO', 'MANTENIMIENTO', 'ENCARGADO', 'CONSULTA', name='rol'), nullable=False),
    sa.Column('password_hash', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('activa', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cuenta_usuario'), 'cuenta', ['usuario'], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_cuenta_usuario'), table_name='cuenta')
    op.drop_table('cuenta')
    sa.Enum(name='rol').drop(op.get_bind(), checkfirst=True)
