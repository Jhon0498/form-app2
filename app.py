import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from dotenv import load_dotenv


# Carrega as variáveis do arquivo .env
load_dotenv()


# Cria a aplicação Flask
app = Flask(__name__)


# Define a chave secreta usada para proteger sessões e formulários
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


# Obtém a chave da API do Mailgun através do arquivo .env
app.config['MAILGUN_API_KEY'] = os.environ.get('MAILGUN_API_KEY')


# Obtém o domínio configurado no Mailgun
app.config['MAILGUN_DOMAIN'] = os.environ.get('MAILGUN_DOMAIN')


# Obtém a URL base da API do Mailgun
# Caso não esteja no .env, utiliza a URL padrão
app.config['MAILGUN_BASE_URL'] = os.environ.get(
    'MAILGUN_BASE_URL',
    'https://api.mailgun.net'
)


# Obtém o e-mail que receberá as mensagens
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')


# Inicializa o Bootstrap na aplicação
bootstrap = Bootstrap(app)


# Inicializa o Flask-Moment na aplicação
moment = Moment(app)

# Importa a função responsável por registrar as rotas
from routes import registrar_rotas

# Registra as rotas na aplicação
registrar_rotas(app)


# Verifica se o arquivo está sendo executado diretamente
if __name__ == '__main__':

    # Inicia o servidor Flask em modo debug
    app.run(debug=True)