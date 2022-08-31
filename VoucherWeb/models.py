from dataclasses import dataclass
from email.policy import default
from main import database
from datetime import datetime

class Usuario(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False, unique=True)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='dafault.jpg', nullable=False)
    vouchers = database.relationship('Voucher', backref='solicitante', lazy=True)

class Voucher(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    cod_voucher = database.Column(database.String, nullable=False, unique=True)
    usado = database.Column(database.Bolean, default = False)
    solicitante = database.Column(database.String, database.ForeignKey('usuario.username'), default='')
    destinatario = database.Column(database.String, default=solicitante)
    validade = database.Column(database.String, default = '')
    