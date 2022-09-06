from flask import render_template, redirect, url_for, flash, request
from VoucherWeb import app, database, bcrypt
from VoucherWeb.forms import FormCriarConta, FormLogin, FormSolicitarVoucher
from VoucherWeb.models import Usuario, Voucher
from flask_login import login_user, logout_user, current_user, login_required
import datetime


lista_usuarios = ['flavio', 'escobar']

#Pega a data corrente
data = (str(datetime.date.today()))

#Verifica se o usuario quer ser espertão e pegar mais de voucher por dia
def espertao(esperto):
    #pega uma lista de vouchers usados
    usado = Voucher.query.filter_by(data_uso=data).all()
    #Percorre a lista de vouchers usados e ve se tem algum espertão nessa lista
    for i in range(len(usado)):
        if usado[i].solicitante == esperto:
            #flash("usado:{}".format(usado[i].solicitante),'alert-danger')
            #flash("esperto:{}".format(esperto),'alert-danger')
            return True
    return False      

def valida_cpf(cpf):
    #try: 
        #  Verifica se o CPF tem todos os números iguais, ex: 111.111.111-11
        #  Esses CPFs são considerados inválidos mas passam na validação dos dígitos
        #  Antigo código para referência: if all(cpf[i] == cpf[i+1] for i in range (0, len(cpf)-1))
        if int(cpf) and len(set(cpf)) != 1:  
            flash("teste1 - é inteiro e os digitos são diferentes",'alter-success')
            num = 11
            ver_cpf[0]
            d1 = 0
            d2 = 0
            for i in range(9):
                ver_cpf.append(cpf[:i:])
                flash(ver_cpf,'alert-success')

            for i in ver_cpf:
                num = num - 1
                d1 += (int(i)*num) #soma os resultados entre os 9pri digitos e o fatorial de 10

            num = 11
            d1 = 11 - (d1 % 11) #objetivo é pegar o resto da divisão
            
            if d1 > 9:
                d1 = 0

            
            flash(ver_cpf[0],'alter-success')
            ver_cpf.append(int(d1))
            
            flash("teste3 - primeiro if",'alter-success')
            

            for i in ver_cpf:
                num = num - 1
                d2 += (int(i)*num)
            flash("teste4 - segundo for",'alter-success')

            d2 = 11 - (d2 % 11)

            if d2 > 9:
                d2 = 0
            ver_cpf.append(d2)
            flash("teste5 - segundo if",'alter-success')
            
            if cpf == ver_cpf:
                flash("teste6 - cpf valido",'alter-success')
                return True
        else:
            flash("Teste 7 - nao inteiro ou os digitos sao iguais")
            return False
    #except:
        flash('O CPF informado não é valido. Digite somente numeros.','alter-danger')
        return False

#o @ é um decorator, serve para atribuir outras caracteristicas para as mesmas funções
@app.route('/', methods=['GET', 'POST'])
def home():
    form_solicitarvoucher = FormSolicitarVoucher()
    if form_solicitarvoucher.validate_on_submit and 'botao_submit_solicitarvoucher' in request.form:
        #verificar se o solicitante ja pediu voucher na data corrente
        if espertao(form_solicitarvoucher.solicitante.data):
            flash("Só é possivel solicitar um Voucher por dia. Você já solicitou um voucher hoje.",'alert-danger')
        elif not valida_cpf(form_solicitarvoucher.cpf.data):
            flash("CPF inválido. Digite um CPF válido para continuar.",'alert-danger')
        else:
            #consultar o Bd atras de um voucher não usado
            nao_usado = Voucher.query.filter_by(data_uso = '').first()
            if nao_usado:
                #escrever nesse BD o nome e cpf_mat do solicitante e data da solicitação,marcar voucher como usado=True
                voucher = Voucher(cod_voucher=nao_usado.cod_voucher, usado = True, solicitante = form_solicitarvoucher.solicitante.data, cpf = form_solicitarvoucher.cpf.data, data_uso = data)
                database.session.delete(nao_usado)
                database.session.commit()
                database.session.add(voucher)
                #committar o bd
                database.session.commit()
                #Entregar o voucher pro cliente
                flash("Este é o seu Voucher: {}".format(voucher.cod_voucher),'alert-success')
            else:
                flash("Não há vouchers disponivel. Favor contatar o setor de I.T.",'alert-danger')
        return redirect(url_for('home'))
    return render_template('home.html', form_solicitarvoucher=form_solicitarvoucher)

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/usuarios')
@login_required
def usuarios():
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    if form_login.validate_on_submit() and 'botao_submit_fazerlogin' in request.form:
        #intancia um usuario no formato do da tabela do BD filtrando pelo username
        usuario = Usuario.query.filter_by(username=form_login.username.data).first()
        #verifica se o username e a senha encriptada estão preenchidas, pois se estiverem é pq há um username no bd
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            #efetiva a sessão do login do usuario
            login_user(usuario)
            #mostra uma caixa de mensagem com uma alerta de sucesso no login
            flash("Bem-Vindo {}".format(form_login.username.data), 'alert-success')
            #pega o indicador de uma pagina que o usuario estava tentando acessar e que precisa de login feito pra ter acesso
            # e depois do login feito redireciona para a pagina que estava tentando ser acessada anteriomente
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
            #fez login com sucesso
        else:
            flash("Falha no login. Username ou senha incorretos", 'alert-danger')
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

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout Feito com Sucesso', 'alert-success')
    return redirect(url_for('home'))

@app.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html')

@app.route('/admin')
@login_required
def admin():
    lista_voucher = Voucher.query.all()
    tam_lista = (int(len(lista_voucher)))
    return render_template('admin.html', tam_lista=tam_lista, lista_voucher=lista_voucher)
