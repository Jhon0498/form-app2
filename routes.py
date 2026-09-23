from flask import render_template
from datetime import datetime
from forms import FormularioAluno
from models import User
from app import db
import requests


def registrar_rotas(app):

    # Rota principal do sistema
    # Aceita requisições GET e POST
    @app.route('/', methods=['GET', 'POST'])
    def index():

        # Cria uma instância do formulário
        form = FormularioAluno()

        # Busca todos os usuários cadastrados no banco
        usuarios_banco = User.query.all()

        # Verifica se o formulário foi enviado corretamente
        if form.validate_on_submit():

            # Pega o nome digitado no formulário
            nome = form.usuario.data.strip()

            # Pega o prontuário digitado no formulário
            prontuario = form.prontuario.data.strip()

            # Verifica se o checkbox foi marcado
            enviar_email = form.enviar_email.data

            # Cria um username a partir do nome
            username = nome.lower().replace(' ', '')

            # Verifica se o usuário já existe
            usuario_existente = User.query.filter(
                (User.username.ilike(username)) |
                (User.name.ilike(nome))
            ).first()

            # Se o usuário já existir
            if usuario_existente:

                return render_template(
                    'index.html',
                    form=form,
                    nome=usuario_existente.name,
                    mensagem='Este usuário já está cadastrado.',
                    users=usuarios_banco,
                    current_time=datetime.utcnow()
                )

            # Cria um novo usuário
            novo_usuario = User(
                username=username,
                name=nome,
                prontuario=prontuario
            )

            # Adiciona o usuário à sessão do banco
            db.session.add(novo_usuario)

            # Salva o usuário no banco de dados
            db.session.commit()

            # Atualiza a relação de usuários
            usuarios_banco = User.query.all()

            # Se não marcou o checkbox,
            # apenas mostra o usuário cadastrado
            if not enviar_email:

                return render_template(
                    'index.html',
                    form=form,
                    nome=nome,
                    mensagem='Usuário cadastrado com sucesso. E-mail não enviado.',
                    users=usuarios_banco,
                    current_time=datetime.utcnow()
                )

            # Recupera os e-mails dos administradores
            flasky_admin = app.config.get(
                'FLASKY_ADMIN',
                ''
            )

            # Transforma os e-mails separados por vírgula
            # em uma lista
            destinatarios = [
                email.strip()
                for email in flasky_admin.split(',')
                if email.strip()
            ]

            # Recupera as configurações do Mailgun
            mailgun_api_key = app.config.get(
                'MAILGUN_API_KEY'
            )

            mailgun_domain = app.config.get(
                'MAILGUN_DOMAIN'
            )

            mailgun_base_url = app.config.get(
                'MAILGUN_BASE_URL'
            )

            # Verifica se a chave da API existe
            if not mailgun_api_key:
                return 'ERRO: MAILGUN_API_KEY não configurada.'

            # Verifica se o domínio existe
            if not mailgun_domain:
                return 'ERRO: MAILGUN_DOMAIN não configurada.'

            # Verifica se a URL do Mailgun existe
            if not mailgun_base_url:
                return 'ERRO: MAILGUN_BASE_URL não configurada.'

            # Verifica se existe destinatário
            if not destinatarios:
                return 'ERRO: FLASKY_ADMIN não configurada.'

            # Monta a URL da API do Mailgun
            url = (
                f'{mailgun_base_url}/v3/'
                f'{mailgun_domain}/messages'
            )

            # Define o remetente
            remetente = (
                'Formulário Flask '
                f'<postmaster@{mailgun_domain}>'
            )

            # Define o assunto
            assunto = 'Novo cadastro realizado'

            # Monta o conteúdo do e-mail
            mensagem_email = (
                'Novo cadastro realizado!\n\n'
                f'Prontuário: {prontuario}\n'
                f'Nome: {nome}\n'
                f'Usuário: {username}'
            )

            # Dados enviados para o Mailgun
            dados = {
                'from': remetente,
                'to': destinatarios,
                'subject': assunto,
                'text': mensagem_email
            }

            try:

                # Envia o e-mail pelo Mailgun
                resposta = requests.post(
                    url,
                    auth=('api', mailgun_api_key),
                    data=dados,
                    timeout=30
                )

                # Verifica se o Mailgun aceitou o envio
                if resposta.status_code == 200:

                    return render_template(
                        'index.html',
                        form=form,
                        nome=nome,
                        mensagem='Usuário cadastrado e e-mail enviado com sucesso.',
                        users=usuarios_banco,
                        current_time=datetime.utcnow()
                    )

                else:

                    erro_mailgun = (
                        '<h2>Erro ao enviar o e-mail</h2>'
                        '<p>Código do Mailgun: '
                        f'{resposta.status_code}</p>'
                        '<p>Resposta:</p>'
                        f'<pre>{resposta.text}</pre>'
                    )

                    return erro_mailgun

            except requests.exceptions.RequestException as erro:

                erro_conexao = (
                    '<h2>Erro ao conectar com o Mailgun</h2>'
                    f'<p>{erro}</p>'
                )

                return erro_conexao

        # Exibe a página normalmente
        return render_template(
            'index.html',
            form=form,
            users=usuarios_banco,
            current_time=datetime.utcnow()
        )