from datetime import datetime
from app import db


class Role(db.Model):

    # Nome da tabela no banco
    __tablename__ = 'roles'

    # Identificador da função
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # Nome da função
    name = db.Column(
        db.String(64),
        unique=True,
        index=True,
        nullable=False
    )

    # Relacionamento entre Role e User
    users = db.relationship(
        'User',
        backref='role',
        lazy='dynamic'
    )

    # Representação do objeto
    def __repr__(self):
        return f'<Role {self.name}>'


class User(db.Model):

    # Nome da tabela no banco
    __tablename__ = 'users'

    # Identificador do usuário
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # Nome de usuário usado no formulário
    username = db.Column(
        db.String(64),
        unique=True,
        index=True,
        nullable=False
    )

    # Nome completo do usuário
    name = db.Column(
        db.String(128),
        nullable=False
    )

    # Número do prontuário
    prontuario = db.Column(
        db.String(64),
        unique=True,
        nullable=True
    )

    # Liga o usuário à tabela de funções
    role_id = db.Column(
        db.Integer,
        db.ForeignKey('roles.id')
    )

    # Representação do objeto
    def __repr__(self):
        return f'<User {self.username}>'


class EmailEnviado(db.Model):

    # Nome da tabela no banco
    __tablename__ = 'emails_enviados'

    # Identificador do e-mail
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # Data e hora em que o e-mail foi enviado
    data_envio = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    # Usuário utilizado no cadastro
    username = db.Column(
        db.String(64),
        nullable=False
    )

    # Nome completo do usuário
    nome = db.Column(
        db.String(128),
        nullable=False
    )

    # Número do prontuário
    prontuario = db.Column(
        db.String(64),
        nullable=True
    )

    # E-mail que recebeu a mensagem
    destinatario = db.Column(
        db.Text,
        nullable=False
    )

    # Assunto do e-mail
    assunto = db.Column(
        db.String(255),
        nullable=False
    )

    # Status do envio
    status = db.Column(
        db.String(50),
        nullable=False
    )

    # Representação do objeto
    def __repr__(self):
        return f'<EmailEnviado {self.id}>'