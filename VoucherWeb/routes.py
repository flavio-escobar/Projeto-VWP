from flask import render_template, redirect, url_for, flash, request
from VoucherWeb import app, database, bcrypt
from VoucherWeb.forms import FormCriarConta, FormLogin, FormSolicitarVoucher
from VoucherWeb.models import Usuario, Voucher
import datetime

lista_usuarios = ['flavio', 'escobar']

@app.route('/', methods=['GET', 'POST'])
def home():
    form_solicitarvoucher = FormSolicitarVoucher()
    if form_solicitarvoucher.validate_on_submit and 'botao_submit_solicitarvoucher' in request.form:
        #verificar se o solicitante ja pediu voucher na data corrente
        date = datetime.date.today()
        query = Voucher.query.filter_by(data_uso = date).all()
        if form_solicitarvoucher.solicitante.data in query.solicitante:
            flash("Você já solicitou um voucher hoje",'alert-danger')
        else:
            #consultar o Bd atras de um voucher não usado
            query = session.query(database.Voucher).filter_by(usado = False).first()
            if query:
                #escrever nesse BD o nome e cpf_mat do solicitante e data da solicitação,marcar voucher como usado=True
                voucher = Voucher(cod_voucher=query.cod_voucher, usado = True, solicitante = form_solicitarvoucher.solicitante.data, cpf_mat = form_solicitarvoucher.cpf_mat.data, data_uso = date)
                database.session.add(voucher)
                #committar o bd
                database.session.commit()
                #Entregar o voucher pro cliente
                flash("Este é o seu Voucher: {}".format(query.cod_voucher),'alert-success')
            else:
                flash("Não há vouchers disponivel. Favor contatar o setor de I.T.",'alert-danger')
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
        #Adicionar condições de autenticação para acesso as areas restritas do sistema
        flash("Bem-Vindo {}".format(form_login.username.data), 'alert-success')
        return redirect(url_for('home'))
        #fez login com sucesso
    return render_template('login.html', form_login=form_login)

@app.route('/criar_conta', methods=['GET', 'POST'])
def criar_conta():
    #Instacia as informações do formulario de criar conta
    form_criarconta = FormCriarConta()
    #Verifica a validação dos dados do formulario e vê se houve submissão pormeio do clique no botão_submit
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        #recebe a informação da senha criptografada do sistema
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
        #Instacia as informações de usuario a serem salvas
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)
        #adiciona a instancia usuario ao banco
        database.session.add(usuario)
        #"comita" as informações efetivando as alterações do BD
        database.session.commit()
        #Retorna mensagem de sucesso para a criação da conta
        flash("Conta Criada com Sucesso para: {}".format(form_criarconta.username.data),'alert-success')
        return redirect(url_for('home'))
        #Criou Conta com sucesso
    return render_template('criar_conta.html', form_criarconta=form_criarconta)