from flask import render_template, redirect, url_for, flash, request
from VoucherWeb import app, database, bcrypt
from VoucherWeb.forms import FormCriarConta, FormLogin, FormSolicitarVoucher
from VoucherWeb.models import Usuario, Voucher
from flask_login import login_user, logout_user, current_user, login_required
import datetime


def upar_voucher():
    list_voucher = ['55capk4','n3ad575','cp58cs6','ue7mvm','fvbapp6','b6mnsr','p24fmh4','bbnhuz4','w6d2363','upbs8a3','fnk4ff6',
    '25kmcn3','rvv7dp6','wsaphb6','b7axh34','8u2wxs6','7bm7sp3','rdey7v3','8czdd56','72dmms4','dnmhc23','7eycac6','w66zyp5','x7vnu44','vpeb7m6']   
    for item in list_voucher:
        voucher = Voucher(cod_voucher=item, usado=False, solicitante= '', cpf='', data_uso='')
        database.session.add(voucher)
        print(item)
    database.session.commit()

def reconf():
    voucher = Voucher.query.all()
    for i in range(len(voucher)):
        v = '<tr><th scope="row">{}</th><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(i,voucher[i].cod_voucher, voucher[i].usado, voucher[i].solicitante, voucher[i].cpf, voucher[i].data_uso )
        lista_tabela.append(v)



'''
          {% for i in tam_lista %}
            <tr>
                <th scope="row">{{ i}}</th>
                <td>{{ lista_voucher[i].cod_voucher}}</td>
                <td>{{ lista_voucher[i].usado }}</td>
                <td>{{ lista_voucher[i].solicitante }}</td>
                <td>{{ lista_voucher[i].cpf}}</td>
                <td>{{ lista_voucher[i].data_uso }}</td>
            </tr>
            {% endfor %}

'''