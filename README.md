# Sistema de Cadastro e Notificação por E-mail

Aplicação web desenvolvida em Flask para cadastro de usuários e envio de e-mails.

## Sobre o projeto

O projeto permite realizar o cadastro de usuários através de um formulário web.

Após o cadastro, o sistema pode enviar um e-mail utilizando a API do Mailgun.

Também possui uma área para consultar o histórico dos e-mails enviados.

## Funcionalidades

- Cadastro de usuários
- Cadastro do nome e prontuário
- Prontuário padrão `PT3026931`
- Opção de enviar e-mail após o cadastro
- Envio de e-mail utilizando o Mailgun
- Registro dos e-mails enviados no banco de dados
- Consulta do histórico de e-mails enviados
- Banco de dados SQLite
- Sistema de migrations com Flask-Migrate

## Tecnologias utilizadas

- Python
- Flask
- Flask-WTF
- Flask-Bootstrap
- Flask-Moment
- Flask-SQLAlchemy
- Flask-Migrate
- SQLite
- Mailgun API
- HTML
- Jinja2

## Estrutura do projeto

```text
form-app2/
│
├── migrations/
│   └── versions/
│
├── static/
│
├── templates/
│   ├── base.html
│   ├── index.html
│   └── emails_enviados.html
│
├── app.py
├── forms.py
├── models.py
├── routes.py
├── requirements.txt
├── usuarios.db
└── README.md
```

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/Jhon0498/form-app2.git
```

### 2. Entrar na pasta

```bash
cd form-app2
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar as variáveis de ambiente

O projeto utiliza variáveis de ambiente para as configurações do Mailgun.

Exemplo:

```text
SECRET_KEY=
MAILGUN_API_KEY=
MAILGUN_DOMAIN=
MAILGUN_BASE_URL=https://api.mailgun.net
FLASKY_ADMIN=
```

As informações da API do Mailgun não devem ser colocadas diretamente no código ou publicadas no GitHub.

### 5. Executar as migrations

```bash
flask db upgrade
```

### 6. Executar a aplicação

```bash
python app.py
```

Depois, acesse:

```text
http://127.0.0.1:5000
```

## Banco de dados

O projeto utiliza SQLite para armazenar os dados dos usuários e o histórico dos e-mails enviados.

A tabela de usuários armazena informações como:

- Usuário
- Nome
- Prontuário
- Função

A tabela de e-mails enviados armazena:

- Data do envio
- Usuário
- Nome
- Prontuário
- Destinatário
- Assunto
- Status

## Envio de e-mails

O envio dos e-mails é realizado através da API do Mailgun.

O sistema utiliza as configurações definidas nas variáveis de ambiente:

```text
MAILGUN_API_KEY
MAILGUN_DOMAIN
MAILGUN_BASE_URL
FLASKY_ADMIN
```

Quando o envio é realizado com sucesso, o sistema registra o envio no histórico.

## Histórico de e-mails

A aplicação possui uma página chamada **E-mails Enviados**.

Nessa página é possível consultar os e-mails que foram enviados pelo sistema, incluindo a data, usuário, destinatário, assunto e status.

## Autor

Jhonatan Mendes Morão

Projeto desenvolvido para fins acadêmicos.
