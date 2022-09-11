from VoucherWeb import app, database
from VoucherWeb.models import Voucher
import pandas as pd

def upar_voucher(list_voucher):
    for item in list_voucher:
        voucher = Voucher(cod_voucher=item, usado=False, solicitante= '', cpf='', data_uso='')
        database.session.add(voucher)
        print(item)
    database.session.commit()

def carga():
    #Perga a lista de vouchers do BD
    lista_voucher_bd = Voucher.query.all()
    lista_de_carga = pd.read_excel('voucher_2h.xlsx', index_col=0)
    #comparar cada voucher da lista de carga com os vouchers que ja estao no sistema para evitar a duplicação
    lista_filtrada_voucher=[]
    for i in lista_de_carga:
        for aux in range(len(lista_voucher_bd)):
            if str(i) == lista_voucher_bd[aux].cod_voucher:
                lista_filtrada_voucher.append(str(i))
    print(lista_filtrada_voucher)
    #pegar a lista filtrada com os voucher validos e adicionar no banco
    #for item in lista_filtrada_voucher:
    #    voucher = Voucher(cod_voucher=item, usado=False, solicitante= '', cpf='', data_uso='')
    #    database.session.add(voucher)
    #database.session.commit()

