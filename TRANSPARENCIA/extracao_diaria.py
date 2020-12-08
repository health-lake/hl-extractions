# -*- coding: utf-8 -*-

from RegistroCivil import RegistroCivil
from datetime import date, timedelta, datetime
import time

ti = time.time()
print('Iniciando extração diária...')

estados = ['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO']

rc = RegistroCivil()
dt_extracao = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

with open('obitos_geral.csv', 'r') as f:
    dados = f.read()
    f.close()

for uf in estados:
    dt_registro = datetime.today().strftime('%Y-%m-%d')
    requisicao = rc.obitos(data_inicio=dt_registro, data_fim=dt_registro, uf=uf)
    for item in requisicao['data']:
        municipio = item['name'].encode('utf-8')
        obitos = str(item['total'])
        dados += '\n' + dt_extracao + ',' + dt_registro + ',' + uf + ',' + municipio + ',' + obitos

with open('obitos_geral.csv', 'w') as f:
    f.write(dados)
    f.close()

tf = time.time()
print('Extração concluída. Tempo necessário: {:.2f} segundos.'.format(tf-ti))