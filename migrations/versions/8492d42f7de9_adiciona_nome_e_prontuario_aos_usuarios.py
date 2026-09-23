"""Adiciona nome e prontuario aos usuarios

Revision ID: 8492d42f7de9
Revises: 93a8f82c7bfa
Create Date: 2026-09-23
"""

from alembic import op
import sqlalchemy as sa


# Identificação desta migration
revision = '8492d42f7de9'

# Migration anterior
down_revision = '93a8f82c7bfa'

branch_labels = None
depends_on = None


def upgrade():

    # Adiciona a coluna name permitindo valores vazios
    # temporariamente, pois os usuários já existem no banco
    op.add_column(
        'users',
        sa.Column(
            'name',
            sa.String(length=128),
            nullable=True
        )
    )

    # Adiciona a coluna prontuario permitindo valores vazios
    # temporariamente, pois os usuários já existem no banco
    op.add_column(
        'users',
        sa.Column(
            'prontuario',
            sa.String(length=64),
            nullable=True
        )
    )


def downgrade():

    # Remove a coluna prontuario
    op.drop_column(
        'users',
        'prontuario'
    )

    # Remove a coluna name
    op.drop_column(
        'users',
        'name'
    )