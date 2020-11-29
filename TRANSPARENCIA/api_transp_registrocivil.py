# -*- coding: utf-8 -*-

import requests
import json
import time

init_time = time.time()

print('Iniciando operação, por favor aguarde...')

# URL DA API
url = 'https://transparencia.registrocivil.org.br/api/record/death'

# HEADERS
headers = {'Host': 'transparencia.registrocivil.org.br',
           'Connection': 'keep-alive',
           'Accept': 'application/json, text/plain, */*',
           'recaptcha': '03AGdBq247tHEFR8wjhSqNNamh0u5ncPXJ8b8vzEahmmsrjZgbF8n2JKIvk_zNCLkWZZ_aIH3bw-SIPeRBxA2LFLrElvtqS00-myLrGqDGE72x9n_lCw0bQb3hoEBEJNhdB5RVa5uDhs6IE0AXpMNlk-zI4Z_MdA5b_0hKz-H36xlWMBT8f2v0WHo01f-rthLsxqU2UaKwmtwhXrmLNN1FiL1FjaAGvzy3YZt1d924828VROuWYYtDQw_Ml9DoAsi6DpBJO9fpiq34O4p6I7sTDqL5miq4incGjpbWH3nwMDT715s26fkOfyfVzlVV0RM6oMn-Tb4WkR29xIba-W7_BqzTfJxL-ILYmdno10LG4O4YnfHZGGRNymRBD8mb0m6a1EegwiKE07lzAykM1qxN4IVbyVj0AV1A8fc2XwBWdXPnN6xBMiK2uW1nTmFi1hwWbruFM_gmmxvIqDaqluVKZL13zOhN8ihpj_YM-YKErpjtIDsQM3OJJ6HsyVW3gLNkox_6uqJwMK1Mt6k6HHrnMzQXr1lF8hGZKwB59jkN_0fhyzdoM4qtqvo',
           'X-CSRF-TOKEN': 'i2489kcqrVBQpJmb3CxMaImPl64T7pxGnC21UifQ',
           'X-Requested-With': 'XMLHttpRequest',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36',
           'X-XSRF-TOKEN': 'eyJpdiI6IncxU0NkMlFLZUplcmdEbnRDanZuXC9nPT0iLCJ2YWx1ZSI6InRKVXY3MU90cDZ0bjI5SEhLMzhZbkd0MmppMFRIeGtiV1FhYXA4c1B6SXE5UnRyODUwXC9QZzRmSmVEYkRoU1FQIiwibWFjIjoiYTVlNzc3ZGRjNjY5ZDI3OTNhN2E2MzcyZWQwYzM2M2Q2Njg3Yzg3MzZlOTEwMzBkYTk4ODRjOTg1NTRlMmU2YiJ9',
           'Sec-Fetch-Site': 'same-origin',
           'Sec-Fetch-Mode': 'cors',
           'Sec-Fetch-Dest': 'empty',
           'Referer': 'https://transparencia.registrocivil.org.br/registros',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
           'Cookie': 'XSRF-TOKEN=eyJpdiI6IncxU0NkMlFLZUplcmdEbnRDanZuXC9nPT0iLCJ2YWx1ZSI6InRKVXY3MU90cDZ0bjI5SEhLMzhZbkd0MmppMFRIeGtiV1FhYXA4c1B6SXE5UnRyODUwXC9QZzRmSmVEYkRoU1FQIiwibWFjIjoiYTVlNzc3ZGRjNjY5ZDI3OTNhN2E2MzcyZWQwYzM2M2Q2Njg3Yzg3MzZlOTEwMzBkYTk4ODRjOTg1NTRlMmU2YiJ9; _session=eyJpdiI6IjFaMjVJNTFyekJVRzVlN3NHR2pPQWc9PSIsInZhbHVlIjoibE1wUlBzcEdaSUhiOGNrUzhSNmI0Wnc4TWFpK1N6OEtzRWQ2ZnpwNnRheHRiQ1JLWVZKRkxcL2JpTUx2d3I3VkUiLCJtYWMiOiJkZGY5YzVmZDcxNDBiOWVjM2ZhMDY4NWQ4MDBlM2I2MGU3MmYxZjA5MjU4MDQzMDEzNGJjNjQzYTU5OTBjMzc4In0%3D'}

# LISTAS ÚTEIS
estados = ['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO']

anos = ['2015', '2016', '2017', '2018', '2019', '2020']

# PEGAR TODOS OS DADOS POR ANO
dados = 'ano, estado, municipio, obitos\n'
for ano in anos:
    for estado in estados:
        query = '?start_date=' + ano + '-01-01&end_date=' + ano + '-12-31&state=' + estado
        r = requests.get(url+query, headers=headers).json()
        for item in r['data']:
            municipio = item['name']
            obitos = item['total']

            dados += ano + ', ' + estado + ', ' + municipio.encode('utf-8') + ', ' + str(obitos) + '\n'

with open('obitos_brasil.csv', 'w') as f:
    f.write(dados)
    f.close()

end_time = time.time()

print('Código executado com sucesso. Tempo de execução: {:.2f} s.'.format(end_time-init_time))