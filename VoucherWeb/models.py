from VoucherWeb import database
from datetime import datetime

class Voucher(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    cod_voucher = database.Column(database.String, nullable=False, unique=True)
    usado = database.Column(database.Boolean, default = False)
    solicitante = database.Column(database.String, database.ForeignKey('usuario.username'), default='')
    destinatario = database.Column(database.String, default=solicitante)
    validade = database.Column(database.String, default = '')

class Usuario(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False, unique=True)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='dafault.jpg', nullable=False)
    vouchers = database.relationship('Voucher', backref='solicitado', lazy=True)


    