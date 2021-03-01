# %%
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Importe as libs necessárias
import requests
from bs4 import BeautifulSoup as bs4
from urllib.request import urlretrieve


# %%
# Acessar o site
url = "http://dados.turismo.gov.br/index.php/chegada-de-turistas-internacionais"
headers = {
  'Connection': 'keep-alive',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Accept-Language': 'pt-BR,pt;q=0.9'
}
#Valida o url
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
soup = extractSoup(response.text)
downloadAnosDiv = soup.find(id='collapse15')

#Pega a lista de Anos e estrutra para gerar a lista de anos
anosListaString = downloadAnosDiv.getText(separator=' ',strip=True).split()


# %%
#Download cada csv da lista do site

def downloadFileUrl(urlPath:str, filename:str):
  ''' Dowlonload  dos aqruivos dos sites
  :param urlPath: Url completa do download
  :param filename: nomes do arquivo e a extenção

  :restunr: Realiza o download do arquivo
  '''
  urlretrieve(urlPath, filename)

#Dectado o padrão de link foi definido uma url base para os donwloads
baseUrl = "http://dados.turismo.gov.br/images/csv/chegadas/chegadas_YEAR.csv"

#Loop para resgatar cadas urls de download dos arquivos
for ano in anosListaString[-2:]:
  urlTurista = baseUrl.replace("YEAR",ano)
  fileNameCsv = ''.join(['BaseTurista_',ano,'.csv'])
  #downloadFileUrl(urlTurista, fileNameCsv)
  fileNameCsv


# %%



