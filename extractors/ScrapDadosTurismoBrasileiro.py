# %%
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# importe as libs necessárias
import requests
from bs4 import BeautifulSoup as bs4
from urllib.request import urlretrieve


# %%
# acessar o site
url = "http://dados.turismo.gov.br/mapa-do-turismo-brasileiro"
headers = {
  'Connection': 'keep-alive',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Accept-Language': 'pt-BR,pt;q=0.9'
}

response = requests.get(url, headers=headers)


# %%
# Scrpaping do site

def extractSoup(source:str):
  ''' Estrai as informações do site via soup 
  :paramm source : site para usado no scraping

  : retorn: O parser do site
  '''
  return bs4(source, 'html.parser')

def convertStrListInt(strList):
  ''' Função converter string em lista
  :paramm strList: site para usado no scraping
  
  :retorn: Texto convertido em lista
  '''
  return [int(item) for item in strList]

#Extrai os textos do site e pega a tag/id
html = extractSoup(response.text)

#Pega a lista de Anos e estrutra para gerar a lista de anos
listaAnos = html.find('ul',class_='menu')
anosListaString = listaAnos.getText(separator=' ',strip=True).split()
anosListaInt = convertStrListInt(anosListaString)


# %%
# download cada csv

def downloadFileUrl(urlPath, filename):
  urlretrieve(urlPath, filename)

baseUrl = "http://www.turismo.gov.br/dadosabertos/mapa/YEAR-mapa-turismo.csv"


#loop e tratamento dos links
for ano in anosListaString:
  urlTurista = baseUrl.replace("YEAR",ano)
  fileNameCsv = ''.join([ano,'-mapa-turismo.csv'])
  if ano == '2004':
    downloadFileUrl("http://dados.turismo.gov.br/images/csv/mapa/2004-mapa-turismo.csv",fileNameCsv) 
  elif ano == '2017':
    downloadFileUrl("http://dados.turismo.gov.br/images/csv/mapa/2017-mapa-turismo.csv",fileNameCsv) 
  elif ano == '2019':
    downloadFileUrl("http://turismo.gov.br/dadosabertos/mapadoturismobrasileiro/RELATORIO_MAPA_2019_Layout_MKT.xls",'RELATORIO_MAPA_2019_Layout_MKT.xls') 
  else:
    downloadFileUrl(urlTurista, fileNameCsv)


# %%



