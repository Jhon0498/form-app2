import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv


# Carrega as variáveis do arquivo .env
load_dotenv()


# Cria a aplicação Flask
app = Flask(__name__)


# Chave usada nas sessões e formulários
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


# Configuração do banco SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'sqlite:////home/Jhonatan1701/usuarios.db'
)

# Desativa o rastreamento de modificações
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Chave da API do Mailgun
app.config['MAILGUN_API_KEY'] = os.environ.get(
    'MAILGUN_API_KEY'
)

# Domínio do Mailgun
app.config['MAILGUN_DOMAIN'] = os.environ.get(
    'MAILGUN_DOMAIN'
)

# URL da API do Mailgun
app.config['MAILGUN_BASE_URL'] = os.environ.get(
    'MAILGUN_BASE_URL',
    'https://api.mailgun.net'
)

# E-mail do administrador
app.config['FLASKY_ADMIN'] = os.environ.get(
    'FLASKY_ADMIN'
)


# Inicializa o banco de dados
db = SQLAlchemy(app)


# Inicializa as migrations
migrate = Migrate(app, db)


# Inicializa o Bootstrap
bootstrap = Bootstrap(app)


# Inicializa o Flask-Moment
moment = Moment(app)


# Importa os modelos
from models import Role, User


# Importa e registra as rotas
from routes import registrar_rotas

registrar_rotas(app)


# Executa a aplicação localmente
if __name__ == '__main__':
    app.run(debug=True)