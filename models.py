from app import db


# Modelo da tabela de funções
class Role(db.Model):

    # Nome da tabela no banco
    __tablename__ = 'roles'

    # Identificador da função
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # Nome da função
    # Exemplo: Administrator ou User
    name = db.Column(
        db.String(64),
        unique=True,
        index=True,
        nullable=False
    )

    # Relacionamento entre Role e User
    # Uma função pode possuir vários usuários
    users = db.relationship(
        'User',
        backref='role',
        lazy='dynamic'
    )

    # Forma como o objeto será mostrado no terminal
    def __repr__(self):
        return f'<Role {self.name}>'


# Modelo da tabela de usuários
class User(db.Model):

    # Nome da tabela no banco
    __tablename__ = 'users'

    # Identificador do usuário
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # Nome do usuário
    username = db.Column(
        db.String(64),
        unique=True,
        index=True,
        nullable=False
    )

    # Chave estrangeira que liga o usuário à função
    role_id = db.Column(
        db.Integer,
        db.ForeignKey('roles.id')
    )

    # Forma como o objeto será mostrado no terminal
    def __repr__(self):
        return f'<User {self.username}>'