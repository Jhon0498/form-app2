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

    @app.route('/', methods=['GET', 'POST'])
    def index():

        # Cria o formulário
        form = FormularioAluno()

        # Se o usuário clicou em Submit
        # E o campo foi preenchido corretamente
        if form.validate_on_submit():

            # Pega o usuário informado no formulário
            usuario = form.usuario.data.strip().lower()

            # Procura o usuário cadastrado
            dados_usuario = usuarios.get(usuario)

            # Verifica se o usuário existe
            if dados_usuario:

                # Pega o prontuário do usuário cadastrado
                prontuario = dados_usuario['prontuario']

                # Pega o nome do usuário cadastrado
                nome = dados_usuario['nome']

                # Pega o e-mail que receberá a mensagem
                destinatario = app.config['FLASKY_ADMIN'].split(',')

                # Pega a chave do Mailgun
                mailgun_api_key = app.config['MAILGUN_API_KEY']

                # Pega o domínio do Mailgun
                mailgun_domain = app.config['MAILGUN_DOMAIN']

                # Pega a URL base do Mailgun
                mailgun_base_url = app.config['MAILGUN_BASE_URL']

                # Verifica se as configurações existem
                if not mailgun_api_key:
                    return 'ERRO: MAILGUN_API_KEY não configurada.'

                if not mailgun_domain:
                    return 'ERRO: MAILGUN_DOMAIN não configurada.'

                if not destinatario:
                    return 'ERRO: FLASKY_ADMIN não configurada.'

                # Monta o endereço da API do Mailgun
                url = (
                    f'{mailgun_base_url}/v3/'
                    f'{mailgun_domain}/messages'
                )

                # E-mail utilizado como remetente
                remetente = (
                    f'Formulário Flask '
                    f'<postmaster@{mailgun_domain}>'
                )

                # Assunto do e-mail
                assunto = 'Novo cadastro realizado'

                # Conteúdo do e-mail
                mensagem = f
Novo cadastro realizado!

Prontuário: {prontuario}
Nome: {nome}
Usuário: {usuario}


                # Dados enviados para o Mailgun
                dados = {
                    'from': remetente,
                    'to': destinatario,
                    'subject': assunto,
                    'text': mensagem
                }

                try:

                    # Envia o e-mail através do Mailgun
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
                            mensagem='E-mail enviado com sucesso!',
                            current_time=datetime.utcnow()
                        )

                    else:

                        # Mostra o erro retornado pelo Mailgun
                        return f
                        <h2>Erro ao enviar o e-mail</h2>

                        <p>
                            Código do Mailgun:
                            {resposta.status_code}
                        </p>

                        <p>Resposta:</p>

                        <pre>{resposta.text}</pre>


                except requests.exceptions.RequestException as erro:

                    # Mostra erro de conexão
                    return f
                    <h2>Erro ao conectar com o Mailgun</h2>

                    <p>{erro}</p>


            else:

                # Usuário não encontrado
                return render_template(
                    'index.html',
                    form=form,
                    erro=f'O usuário "{usuario}" não foi encontrado.',
                    current_time=datetime.utcnow()
                )

        # Quando a pessoa entra pela primeira vez,
        # ainda não existe nenhum dado preenchido
        return render_template(
            'index.html',
            form=form,
            current_time=datetime.utcnow()
        )