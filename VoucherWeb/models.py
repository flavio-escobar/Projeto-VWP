from VoucherWeb import database, login_manager
from datetime import datetime
from flask_login import UserMixin 
#UserMixin é um classe que serve para atribuir a classe (no nosso caso) usuario para atribuir a ela as caracteristas que o login_manager precisa para trabalhar com as sessões de login

# este @ é um decorator, ele está uma linha acima da declaração de função
# Foi feito dessa forma para que a função load_usuario fosse passada por paramentro para a função login_manager e virce, bem como para faciliar a conversa com o restante do codigo.
@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

#Olha o UserMixin
class Usuario(database.Model, UserMixin):
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