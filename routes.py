from flask import render_template
from datetime import datetime
from forms import FormularioAluno
import requests


def registrar_rotas(app):

    # Usuários cadastrados temporariamente
    usuarios = {
        'jhonatan': {
            'prontuario': 'PT3026931',
            'nome': 'Jhonatan Mendes Morão'
        }
    }

    # Rota principal
    @app.route('/', methods=['GET', 'POST'])
    def index():

        # Cria o formulário
        form = FormularioAluno()

        # Verifica se o formulário foi enviado
        if form.validate_on_submit():

            # Pega o usuário digitado
            usuario = form.usuario.data.strip().lower()

            # Procura o usuário cadastrado
            dados_usuario = usuarios.get(usuario)

            # Verifica se o usuário existe
            if dados_usuario:

                # Pega os dados do usuário
                prontuario = dados_usuario['prontuario']
                nome = dados_usuario['nome']

                # Pega o e-mail do administrador
                flasky_admin = app.config.get(
                    'FLASKY_ADMIN',
                    ''
                )

                # Cria a lista de destinatários
                destinatarios = [
                    email.strip()
                    for email in flasky_admin.split(',')
                    if email.strip()
                ]

                # Pega a chave do Mailgun
                mailgun_api_key = app.config.get(
                    'MAILGUN_API_KEY'
                )

                # Pega o domínio do Mailgun
                mailgun_domain = app.config.get(
                    'MAILGUN_DOMAIN'
                )

                # Pega a URL base do Mailgun
                mailgun_base_url = app.config.get(
                    'MAILGUN_BASE_URL'
                )

                # Verifica se a chave foi configurada
                if not mailgun_api_key:
                    return (
                        'ERRO: MAILGUN_API_KEY '
                        'não configurada.'
                    )

                # Verifica se o domínio foi configurado
                if not mailgun_domain:
                    return (
                        'ERRO: MAILGUN_DOMAIN '
                        'não configurada.'
                    )

                # Verifica se a URL foi configurada
                if not mailgun_base_url:
                    return (
                        'ERRO: MAILGUN_BASE_URL '
                        'não configurada.'
                    )

                # Verifica se existe destinatário
                if not destinatarios:
                    return (
                        'ERRO: FLASKY_ADMIN '
                        'não configurada.'
                    )

                # Monta a URL para envio do e-mail
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

                # Monta a mensagem
                mensagem = (
                    'Novo cadastro realizado!\n\n'
                    f'Prontuário: {prontuario}\n'
                    f'Nome: {nome}\n'
                    f'Usuário: {usuario}'
                )

                # Dados enviados para o Mailgun
                dados = {
                    'from': remetente,
                    'to': destinatarios,
                    'subject': assunto,
                    'text': mensagem
                }

                try:

                    # Envia o e-mail
                    resposta = requests.post(
                        url,
                        auth=('api', mailgun_api_key),
                        data=dados,
                        timeout=30
                    )

                    # Verifica se o envio funcionou
                    if resposta.status_code == 200:

                        return render_template(
                            'index.html',
                            form=form,
                            nome=nome,
                            mensagem=(
                                'E-mail enviado '
                                'com sucesso!'
                            ),
                            current_time=datetime.utcnow()
                        )

                    # Caso o Mailgun retorne erro
                    else:

                        erro_mailgun = (
                            '<h2>Erro ao enviar o e-mail</h2>'
                            '<p>Código do Mailgun: '
                            f'{resposta.status_code}</p>'
                            '<p>Resposta:</p>'
                            f'<pre>{resposta.text}</pre>'
                        )

                        return erro_mailgun

                # Caso ocorra erro de conexão
                except requests.exceptions.RequestException as erro:

                    erro_conexao = (
                        '<h2>Erro ao conectar '
                        'com o Mailgun</h2>'
                        f'<p>{erro}</p>'
                    )

                    return erro_conexao

            # Caso o usuário não seja encontrado
            else:

                return render_template(
                    'index.html',
                    form=form,
                    erro=(
                        f'O usuário "{usuario}" '
                        'não foi encontrado.'
                    ),
                    current_time=datetime.utcnow()
                )

        # Carrega a página inicialmente
        return render_template(
            'index.html',
            form=form,
            current_time=datetime.utcnow()
        )