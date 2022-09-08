from VoucherWeb import app, database
from VoucherWeb.models import Voucher

def upar_voucher():
    list_voucher = ['55capk4','n3ad575','cp58cs6','ue7mvm','fvbapp6','b6mnsr','p24fmh4','bbnhuz4','w6d2363','upbs8a3','fnk4ff6',
    '25kmcn3','rvv7dp6','wsaphb6','b7axh34','8u2wxs6','7bm7sp3','rdey7v3','8czdd56','72dmms4','dnmhc23','7eycac6','w66zyp5','x7vnu44','vpeb7m6']   
    for item in list_voucher:
        voucher = Voucher(cod_voucher=item, usado=False, solicitante= '', cpf='', data_uso='')
        database.session.add(voucher)
        print(item)
    database.session.commit()