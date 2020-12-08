# -*- coding: utf-8 -*-

from RegistroCivil import RegistroCivil
from datetime import date, timedelta, datetime
import time

print('Iniciando extração total dos dados históricos de óbitos do Transparência Registro Civil...')
ti = time.time()

estados = ['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO']

rc = RegistroCivil()

data_inicial = date(2020, 11, 1)
data_final = date(2020, 12, 7)

delta = data_final - data_inicial

dados = 'dt_coleta,dt_registro,uf,municipio,obitos'
dt_extracao = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

for uf in estados:
    for i in range(delta.days + 1):
        data = data_inicial + timedelta(days=i)

        if data.day == 1:
            dt_registro = data.strftime('%Y-%m')
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