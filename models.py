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
        nullable=False
    )

    # Liga o usuário à tabela de funções
    role_id = db.Column(
        db.Integer,
        db.ForeignKey('roles.id')
    )

    # Representação do objeto
    def __repr__(self):
        return f'<User {self.username}>'