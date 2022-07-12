#Projeto Voucher WebPage
from flask import Flask, render_template, url_for, request, flash, redirect
from forms import FormLogin, FormCriarConta, FormSolicitarVoucher
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

lista_usuarios = ['admin', 'usuario']

app.config['SECRET_KEY'] = '8b7250cf7c5dc00f81c393043ae04db7e19d08a376b835b0f5a2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///voucher.db'

database = SQLAlchemy(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    form_solicitarvoucher = FormSolicitarVoucher()
    if form_solicitarvoucher.validate_on_submit and 'botao_submit_solicitarvoucher' in request.form:
        flash("Este é o seu Voucher: {}".format('AASD$@!#'),'alert-success')
        return redirect(url_for('home'))
    return render_template('home.html', form_solicitarvoucher=form_solicitarvoucher)

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/usuarios')
def usuarios():
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    if form_login.validate_on_submit() and 'botao_submit_fazerlogin' in request.form:
        flash("Bem-Vindo {}".format(form_login.username.data), 'alert-success')
        return redirect(url_for('home'))
        #fez login com sucesso
    return render_template('login.html', form_login=form_login)

@app.route('/criar_conta', methods=['GET', 'POST'])
def criar_conta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        flash("Conta Criada com Sucesso para: {}".format(form_criarconta.username.data),'alert-success')
        return redirect(url_for('home'))
        #Criou Conta com sucesso
    return render_template('criar_conta.html', form_criarconta=form_criarconta)

if __name__ == '__main__':
    app.run(debug=True)
