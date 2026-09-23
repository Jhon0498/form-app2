from flask import render_template, request
from datetime import datetime
from forms import FormularioAluno
from models import User, Role
from app import db
import requests


def registrar_rotas(app):

    # Rota principal do sistema
    # Aceita requisições GET e POST
    @app.route('/', methods=['GET', 'POST'])
    def index():

        # Cria uma instância do formulário
        form = FormularioAluno()

        # Diagnóstico temporário
        print('MÉTODO:', request.method)
        print('DADOS:', request.form)

        # Busca todos os usuários cadastrados no banco
        usuarios_banco = User.query.all()

        # Verifica se o formulário foi enviado
        if request.method == 'POST':

            # Pega os dados digitados no formulário
            username = (
                form.usuario.data.strip()
                if form.usuario.data
                else ''
            )

            nome = (
                form.nome.data.strip()
                if form.nome.data
                else ''
            )

            prontuario = (
                form.prontuario.data.strip()
                if form.prontuario.data
                else ''
            )

            # Verifica se os campos foram preenchidos
            if not username or not nome or not prontuario:

                return render_template(
                    'index.html',
                    form=form,
                    nome=nome,
                    mensagem='Preencha todos os campos.',
                    users=usuarios_banco,
                    current_time=datetime.utcnow()
                )

            # Verifica se o checkbox foi marcado
            enviar_email = form.enviar_email.data

            # Verifica se o usuário já existe
            usuario_existente = User.query.filter(
                (User.username.ilike(username)) |
                (User.prontuario.ilike(prontuario))
            ).first()

            # Se o usuário já existir
            if usuario_existente:

                return render_template(
                    'index.html',
                    form=form,
                    nome=usuario_existente.name,
                    mensagem='Este usuário ou prontuário já está cadastrado.',
                    users=usuarios_banco,
                    current_time=datetime.utcnow()
                )

            # Busca a função User
            funcao_user = Role.query.filter_by(
                name='User'
            ).first()

            # Cria um novo usuário com a função User
            novo_usuario = User(
                username=username,
                name=nome,
                prontuario=prontuario,
                role=funcao_user
            )

            try:

                # Adiciona o usuário à sessão do banco
                db.session.add(novo_usuario)

                # Salva o usuário no banco de dados
                db.session.commit()

                # Diagnóstico temporário
                print(
                    'USUÁRIO SALVO:',
                    novo_usuario.id,
                    novo_usuario.username,
                    novo_usuario.name,
                    novo_usuario.prontuario
                )

            except Exception as erro:

                # Desfaz a operação caso ocorra algum erro
                db.session.rollback()

                # Mostra o erro no log
                print('ERRO AO SALVAR USUÁRIO:', erro)

                return render_template(
                    'index.html',
                    form=form,
                    nome=nome,
                    mensagem='Erro ao cadastrar o usuário.',
                    users=usuarios_banco,
                    current_time=datetime.utcnow()
                )

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
                'Cadastro de Alunos '
                f'<postmaster@{mailgun_domain}>'
            )

            # Define o assunto
            assunto = 'Novo cadastro realizado'

            # Monta o conteúdo do e-mail
            mensagem_email = (
                'Novo cadastro realizado!\n\n'
                f'Usuário: {username}\n'
                f'Nome do aluno: {nome}\n'
                f'Prontuário: {prontuario}'
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

                    # Mostra o erro retornado pelo Mailgun
                    erro_mailgun = (
                        '<h2>Erro ao enviar o e-mail</h2>'
                        '<p>Código do Mailgun: '
                        f'{resposta.status_code}</p>'
                        '<p>Resposta:</p>'
                        f'<pre>{resposta.text}</pre>'
                    )

                    return erro_mailgun

            except requests.exceptions.RequestException as erro:

                # Trata erros de conexão com o Mailgun
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