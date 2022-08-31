from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SECRET_KEY'] = '8b7250cf7c5dc00f81c393043ae04db7e19d08a376b835b0f5a2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///voucher.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)


from VoucherWeb import routes