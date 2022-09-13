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
    lista_df_excel = pd.read_excel('voucher_2h.xlsx')
    lista_string_excel = []
    lista_string_bd = []
    coluna = lista_excel.columns.tolist()#Pega o nome da coluna para ser usada posteriormente na leitura das linhas

    #Transforma a lista Dataframe do pandas em uma lista de strings para facilitar a comparação
    for i in range(len(lista_excel)):
        lista_string_excel.append("".join(map(str, lista_excel.iloc[i][coluna].tolist())))#coloc numa lista o valor de cada linha da coluna inicial
    lista_string_excel.append("".join(coluna))
    #print(lista_string_excel)

    #transforma a lista de voucher do banco em uma lista de string para facilitar a comparação
    for i in lista_voucher_bd:
            lista_string_bd.append(str(i.cod_voucher))

    #comparar cada voucher da lista de carga com os vouchers que ja estao no sistema para evitar a duplicação
    print(lista_string_bd)
    print(lista_string_excel)
    lista_string_excel = set(lista_string_excel).difference(set(lista_voucher_bd))
    print(lista_string_excel)

    #pegar a lista filtrada com os voucher validos e adicionar no banco
    for item in lista_string_excel:
        voucher = Voucher(cod_voucher=item, usado=False, solicitante= '', cpf='', data_uso='')
        database.session.add(voucher)
    database.session.commit()
