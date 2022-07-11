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
    posts = database.relationship('Post', backref='autor', lazy=True)
    vouchers = database.relationship('Voucher', backref='solicitante', lazy=Ture)

class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)

class Voucher(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    cod_voucher = database.Column(database.String, nullable=False, unique=True)
    usado = database.Column(database.Bolean, default = False)
    solicitante = database.Column(database.String, database.ForeignKey('usuario.username'), default='')