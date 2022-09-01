from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from VoucherWeb.models import Usuario

class FormCriarConta(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 40)])
    confirmacao = PasswordField('Confirme a Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    #Utilizando o metodo da classe FlaskForm (validade_on_submit), ele, por padrão, valida qualquer condição que comece com declaração "validade_". Por isso criei um def começando com esse nome
    #para que eu possa criar uma validação para o campo email no formulario, porque ele é unico na estrutura do bd e se não tiver essa validação no formulario, o sistema ira apresentar um erro
    #na hora de inserir um cadastro com o email igual a algum que ja tenha no bd. Como não é interessante o sistema apresentar um erro, fiz aqui um validador para tratamento de exceção.
    def validate_email(self, email):
        # o email sozinho corresponde ao campo no formulario, para pegar o valor do campo do formulario é preciso colocar email.data
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Email já cadastrado. Cadastra-se com outro e-mail ou faça login para continuar')

    def validate_username(self, username):
        usuario = Usuario.query.filter_by(username=username.data).first()
        if usuario:
            raise ValidationError('Username já cadastrado. Cadastra-se com outro username.')        


class FormLogin(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    botao_submit_fazerlogin = SubmitField('Fazer Login')

class FormSolicitarVoucher(FlaskForm):
    solicitante = StringField('Nome do solicitante', validators=[DataRequired()])
    cpf_mat = StringField('Digite o CPF ou Matricula (Somente Numeros)', validators=[DataRequired(), Length(6, 11)]) 
    botao_submit_solicitarvoucher = SubmitField('SolicitarVoucher')