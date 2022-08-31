from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class FormCriarConta(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 40)])
    confirmacao = PasswordField('Confirme a Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

class FormLogin(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    botao_submit_fazerlogin = SubmitField('Fazer Login')

class FormSolicitarVoucher(FlaskForm):
    solicitante = StringField('Nome do solicitante', validators=[DataRequired()])
    destinatario = StringField('Nome do destinatário do voucher', validators=[DataRequired()])
    validade = SelectField('Validade do Voucher', choices=[('2h'),('8h'),('30d')]) 
    botao_submit_solicitarvoucher = SubmitField('SolicitarVoucher')