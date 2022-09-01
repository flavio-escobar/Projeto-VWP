from VoucherWeb import database, login_manager
from datetime import datetime

def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

class Usuario(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False, unique=True)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)

class Voucher(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    cod_voucher = database.Column(database.String, nullable=False, unique=True)
    usado = database.Column(database.Boolean, default = False)
    solicitante = database.Column(database.String, default = '')
    cpf_mat = database.Column(database.String, nullable=False)
    data_uso = database.Column(database.String, default = '')