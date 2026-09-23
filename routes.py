from flask import render_template
from datetime import datetime
from forms import FormularioAluno
from models import User, Role
import requests


def registrar_rotas(app):

    usuarios = {
        'jhonatan': {
            'prontuario': 'PT3026931',
            'nome': 'Jhonatan Mendes Morão'
        }
    }

    @app.route('/', methods=['GET', 'POST'])
    def index():

        form = FormularioAluno()
        usuarios_banco = User.query.all()

        if form.validate_on_submit():

            usuario = form.usuario.data.strip().lower()
            enviar_email = form.enviar_email.data

            dados_usuario = usuarios.get(usuario)

            if dados_usuario:

                prontuario = dados_usuario['prontuario']
                nome = dados_usuario['nome']

                # Se não marcar o checkbox, não envia e-mail
                if not enviar_email:
                    return render_template(
                        'index.html',
                        form=form,
                        nome=nome,
                        mensagem='Usuário localizado com sucesso. E-mail não enviado.',
                        users=usuarios_banco,
                        current_time=datetime.utcnow()
                    )

                flasky_admin = app.config.get('FLASKY_ADMIN', '')

                destinatarios = [
                    email.strip()
                    for email in flasky_admin.split(',')
                    if email.strip()
                ]

                mailgun_api_key = app.config.get('MAILGUN_API_KEY')
                mailgun_domain = app.config.get('MAILGUN_DOMAIN')
                mailgun_base_url = app.config.get('MAILGUN_BASE_URL')

                if not mailgun_api_key:
                    return 'ERRO: MAILGUN_API_KEY não configurada.'

                if not mailgun_domain:
                    return 'ERRO: MAILGUN_DOMAIN não configurada.'

                if not mailgun_base_url:
                    return 'ERRO: MAILGUN_BASE_URL não configurada.'

                if not destinatarios:
                    return 'ERRO: FLASKY_ADMIN não configurada.'

                url = (
                    f'{mailgun_base_url}/v3/'
                    f'{mailgun_domain}/messages'
                )

                remetente = (
                    'Formulário Flask '
                    f'<postmaster@{mailgun_domain}>'
                )

                assunto = 'Novo cadastro realizado'

                mensagem = (
                    'Novo cadastro realizado!\n\n'
                    f'Prontuário: {prontuario}\n'
                    f'Nome: {nome}\n'
                    f'Usuário: {usuario}'
                )

                dados = {
                    'from': remetente,
                    'to': destinatarios,
                    'subject': assunto,
                    'text': mensagem
                }

                try:
                    resposta = requests.post(
                        url,
                        auth=('api', mailgun_api_key),
                        data=dados,
                        timeout=30
                    )

                    if resposta.status_code == 200:
                        return render_template(
                            'index.html',
                            form=form,
                            nome=nome,
                            mensagem='E-mail enviado para o Administrador do sistema, notificando o cadastro de um novo usuário.',
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

            else:
                return render_template(
                    'index.html',
                    form=form,
                    erro=f'O usuário "{usuario}" não foi encontrado.',
                    users=usuarios_banco,
                    current_time=datetime.utcnow()
                )

        return render_template(
            'index.html',
            form=form,
            users=usuarios_banco,
            current_time=datetime.utcnow()
        )