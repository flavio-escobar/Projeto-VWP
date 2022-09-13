from flask import render_template, redirect, url_for, flash, request
from VoucherWeb import app, database, bcrypt
from VoucherWeb.forms import FormCriarConta, FormLogin, FormSolicitarVoucher, FormCarregarVoucher
from VoucherWeb.models import Usuario, Voucher
from flask_login import login_user, logout_user, current_user, login_required
import pandas as pd
import datetime


lista_usuarios = ['admin']

#Pega a data corrente
data = (str(datetime.date.today()))

#Verifica se o usuario quer ser espertão e pegar mais de voucher por dia
def espertao(esperto):
    #pega uma lista de vouchers usados
    usado = Voucher.query.filter_by(data_uso=data).all()
    #Percorre a lista de vouchers usados e ve se tem algum espertão nessa lista
    for i in range(len(usado)):
        if usado[i].cpf == esperto:
            #flash("usado:{}".format(usado[i].cpf),'alert-danger')
            #flash("esperto:{}".format(esperto),'alert-danger')
            return True
    return False      

def valida_cpf(cpf):
    try: 
        #  Verifica se o CPF tem todos os números iguais, ex: 111.111.111-11
        #  Esses CPFs são considerados inválidos mas passam na validação dos dígitos
        if int(cpf) and len(set(cpf)) != 1:  
            num = 11
            ver_cpf = []
            d1 = 0
            d2 = 0

            #povoa a lista auxiliar com os numeros do cpf
            for i in range(9):
                ver_cpf.append(cpf[i])

            #valida o digito verificador 1
            for i in ver_cpf:
                num = num - 1
                d1 += (int(i)*num) #soma os valores do produto entre os 9pri digitos e o fatorial de 10
            d1 = 11 - (d1 % 11) #objetivo é pegar o resto da divisão
            if d1 > 9:
                d1 = 0
            #adiciona o digito verificador 1 na lista auxiliar
            ver_cpf.append(str(d1))
            
            #valida o digito verificador 2
            num = 11
            for i in ver_cpf:
                d2 += (int(i)*num)
                num = num - 1
            d2 = 11 - (d2 % 11)
            if d2 > 9:
                d2 = 0
            #adiciona o digito verificador 2 na lista auxiliar
            ver_cpf.append(str(d2))

            cpf_novo = "".join(ver_cpf)
            
            if cpf == cpf_novo:
                return True
        else:
            return False
    except:
        return False

#o @ é um decorator, serve para atribuir outras caracteristicas para as mesmas funções
@app.route('/', methods=['GET', 'POST'])
def home():
    form_solicitarvoucher = FormSolicitarVoucher()
    if form_solicitarvoucher.validate_on_submit and 'botao_submit_solicitarvoucher' in request.form:
        #verificar se o solicitante ja pediu voucher na data corrente
        if espertao(form_solicitarvoucher.cpf.data):
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
@login_required
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

def limpando_lista(lista_excel, lista_bd):
    verificador = False
    lista_filtrada_voucher = []
    for excel in lista_excel:
        print('excel{}'.format(str(excel)))
        print(lista_bd)
        print(lista_excel)
        if str(excel) not in lista_bd:
            lista_filtrada_voucher.append(str(excel))
            print('Entrou:{}'.format(str(excel)))
        else:
            print('Não entrou: {}'.format(str(excel)))
    return lista_filtrada_voucher

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    form_carregarvoucher = FormCarregarVoucher()
    #Perga a lista de vouchers do BD
    lista_voucher = Voucher.query.all()
    lista_bd = []
    if form_carregarvoucher.validate_on_submit() and 'botao_submit_carregarvoucher' in request.form:
        excel = pd.read_excel(form_carregarvoucher.lista_carga.data)
        #comparar cada voucher da lista de carga com os vouchers que ja estao no sistema para evitar a duplicação
        data = excel[['voucher']]
        print(data.tolist())
        for i in lista_voucher:
            lista_bd.append(str(i.cod_voucher))
        lista_filtrada_voucher = limpando_lista(excel, lista_bd)
        #try:
        for item in lista_filtrada_voucher:
            voucher = Voucher(cod_voucher=item, usado=False, solicitante= '', cpf='', data_uso='')
            database.session.add(voucher)
        database.session.commit()
        flash('Base carregada com Sucesso!', 'alert-success')
        #except:
        #    flash('Erro ao carregar a base!', 'alert-primary')
        #Redirecionar para a pagina admin de novo
        return redirect(url_for('admin'))
    #Pega o tamanho da lista em inteiro para percorrer e mostrar todas as informações do bd
    tam_lista = (int(len(lista_voucher)))
    #passa o caminho de renderização da pagina admin bem como as variaveis para renderzação da tabela de consulta de vouchers
    return render_template('admin.html', form_carregarvoucher=form_carregarvoucher, tam_lista=tam_lista, lista_voucher=lista_voucher)
