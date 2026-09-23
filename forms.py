from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class FormularioAluno(FlaskForm):

    # Usuário
    usuario = StringField(
        'Qual é o seu nome?:',
        validators=[DataRequired()]
    )
    # Checkbox para escolher se deseja enviar e-mail
    enviar_email = BooleanField(
        'Deseja enviar e-mail para flaskaulasweb@zohomail.com?'
)
    # botão que envia o formulário
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):

    usuario = StringField(
        validators=[DataRequired()],
        render_kw={
            'placeholder': 'Usuário ou e-mail'
        }
    )

    senha = PasswordField(
        'Informe a sua senha',
        validators=[DataRequired()],
        render_kw={
            'placeholder': 'Informe a sua senha',
        }
    )

    submit = SubmitField('Enviar')