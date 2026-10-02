"""
Migration para criar a tabela de e-mails enviados.
"""

from alembic import op
import sqlalchemy as sa


# Identificação da migration
revision = '4a43fa1978b0'

# Migration anterior
down_revision = '8492d42f7de9'

# Dependências
branch_labels = None

# Dependências adicionais
depends_on = None


def upgrade():

    # Cria a tabela de e-mails enviados
    op.create_table(
        'emails_enviados',

        # Identificador do e-mail
        sa.Column(
            'id',
            sa.Integer(),
            nullable=False
        ),

        # Data e hora do envio
        sa.Column(
            'data_envio',
            sa.DateTime(),
            nullable=False
        ),

        # Usuário utilizado no cadastro
        sa.Column(
            'username',
            sa.String(length=64),
            nullable=False
        ),

        # Nome completo do usuário
        sa.Column(
            'nome',
            sa.String(length=128),
            nullable=False
        ),

        # Número do prontuário
        sa.Column(
            'prontuario',
            sa.String(length=64),
            nullable=True
        ),

        # E-mail que recebeu a mensagem
        sa.Column(
            'destinatario',
            sa.Text(),
            nullable=False
        ),

        # Assunto do e-mail
        sa.Column(
            'assunto',
            sa.String(length=255),
            nullable=False
        ),

        # Status do envio
        sa.Column(
            'status',
            sa.String(length=50),
            nullable=False
        ),

        # Chave primária
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():

    # Remove somente a tabela de e-mails enviados
    op.drop_table('emails_enviados')
