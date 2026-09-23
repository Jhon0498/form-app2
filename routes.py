from flask import render_template
from datetime import datetime
from forms import FormularioAluno
from models import User
import requests


def registrar_rotas(app):

    # Rota principal do sistema
    # Aceita requisições GET e POST
    @app.route('/', methods=['GET', 'POST'])
    def index():

        # Cria uma instância do formulário
        form = FormularioAluno()

        # Busca todos os usuários cadastrados no banco de dados
        # Esses usuários serão enviados para o template
        usuarios_banco = User.query.all()

        # Verifica se o formulário foi enviado e preenchido corretamente
        if form.validate_on_submit():

            # Pega o nome de usuário digitado no formulário
            # strip() remove espaços antes e depois
            # lower() transforma o texto em letras minúsculas
            usuario = form.usuario.data.strip().lower()

            # Verifica se o usuário marcou a opção de enviar e-mail
            enviar_email = form.enviar_email.data

            # Procura o usuário no banco de dados pelo username
            # first() retorna o primeiro usuário encontrado
            # Se não encontrar, retorna None
            dados_usuario = User.query.filter_by(
                username=usuario
            ).first()

            # Verifica se o usuário foi encontrado
            if dados_usuario:

                # Pega o prontuário cadastrado no banco de dados
                prontuario = dados_usuario.prontuario

                # Pega o nome cadastrado no banco de dados
                nome = dados_usuario.name

                # Se o usuário não marcou o checkbox,
                # apenas mostra o nome e não envia o e-mail
                if not enviar_email:
                    return render_template(
                        'index.html',
                        form=form,
                        nome=nome,
                        mensagem='Usuário localizado com sucesso. E-mail não enviado.',
                        users=usuarios_banco,
                        current_time=datetime.utcnow()
                    )

                # Recupera os e-mails dos administradores
                # definidos na variável FLASKY_ADMIN do arquivo .env
                flasky_admin = app.config.get('FLASKY_ADMIN', '')

                # Converte os e-mails separados por vírgula
                # em uma lista e remove espaços desnecessários
                destinatarios = [
                    email.strip()
                    for email in flasky_admin.split(',')
                    if email.strip()
                ]

                # Recupera as configurações do Mailgun
                mailgun_api_key = app.config.get('MAILGUN_API_KEY')
                mailgun_domain = app.config.get('MAILGUN_DOMAIN')
                mailgun_base_url = app.config.get('MAILGUN_BASE_URL')

                # Verifica se a chave da API do Mailgun foi configurada
                if not mailgun_api_key:
                    return 'ERRO: MAILGUN_API_KEY não configurada.'

                # Verifica se o domínio do Mailgun foi configurado
                if not mailgun_domain:
                    return 'ERRO: MAILGUN_DOMAIN não configurada.'

                # Verifica se a URL do Mailgun foi configurada
                if not mailgun_base_url:
                    return 'ERRO: MAILGUN_BASE_URL não configurada.'

                # Verifica se existe pelo menos um destinatário
                if not destinatarios:
                    return 'ERRO: FLASKY_ADMIN não configurada.'

                # Monta a URL utilizada para enviar o e-mail
                url = (
                    f'{mailgun_base_url}/v3/'
                    f'{mailgun_domain}/messages'
                )

                # Define o endereço que aparecerá como remetente
                remetente = (
                    'Formulário Flask '
                    f'<postmaster@{mailgun_domain}>'
                )

                # Define o assunto do e-mail
                assunto = 'Novo cadastro realizado'

                # Monta o conteúdo do e-mail
                # Os dados são obtidos diretamente do banco de dados
                mensagem = (
                    'Novo cadastro realizado!\n\n'
                    f'Prontuário: {prontuario}\n'
                    f'Nome: {nome}\n'
                    f'Usuário: {usuario}'
                )

                # Organiza os dados que serão enviados para o Mailgun
                dados = {
                    'from': remetente,
                    'to': destinatarios,
                    'subject': assunto,
                    'text': mensagem
                }

                try:

                    # Faz a requisição para a API do Mailgun
                    # utilizando a chave da API para autenticação
                    resposta = requests.post(
                        url,
                        auth=('api', mailgun_api_key),
                        data=dados,
                        timeout=30
                    )

                    # Código 200 significa que o Mailgun aceitou o envio
                    if resposta.status_code == 200:

                        # Mostra a página novamente
                        # informando que o e-mail foi enviado
                        return render_template(
                            'index.html',
                            form=form,
                            nome=nome,
                            mensagem='E-mail enviado para o Administrador do sistema, notificando o cadastro de um novo usuário.',
                            users=usuarios_banco,
                            current_time=datetime.utcnow()
                        )

                    else:

                        # Se o Mailgun retornar outro código,
                        # mostra o código e a resposta recebida
                        erro_mailgun = (
                            '<h2>Erro ao enviar o e-mail</h2>'
                            '<p>Código do Mailgun: '
                            f'{resposta.status_code}</p>'
                            '<p>Resposta:</p>'
                            f'<pre>{resposta.text}</pre>'
                        )

                        return erro_mailgun

                except requests.exceptions.RequestException as erro:

                    # Trata erros de conexão com a API do Mailgun
                    erro_conexao = (
                        '<h2>Erro ao conectar com o Mailgun</h2>'
                        f'<p>{erro}</p>'
                    )

                    return erro_conexao

            else:

                # Caso o username digitado não exista no banco,
                # mostra uma mensagem de erro para o usuário
                return render_template(
                    'index.html',
                    form=form,
                    erro=f'O usuário "{usuario}" não foi encontrado.',
                    users=usuarios_banco,
                    current_time=datetime.utcnow()
                )

        # Exibe a página normalmente quando o formulário
        # ainda não foi enviado
        return render_template(
            'index.html',
            form=form,
            users=usuarios_banco,
            current_time=datetime.utcnow()
        )
