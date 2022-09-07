#Esta sessão inicializa automaticamente para instanciar a aplicação, banco de dados e adicionais
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

#instacia a estrutura Flask para nosso app
app = Flask(__name__)

app.config['SECRET_KEY'] = '8b7250cf7c5dc00f81c393043ae04db7e19d08a376b835b0f5a2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///voucher.db'

#intanciamento do BD
database = SQLAlchemy(app)
#instanciamento do sistema de encriptaçao da senha dos usuarios no BD
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

#importação no final do codigo para evitar importação circular
from VoucherWeb import routes