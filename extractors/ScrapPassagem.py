# %%
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# importe as libs necessárias
import requests
from bs4 import BeautifulSoup as bs4
from urllib.request import urlretrieve


# %%
# Acessar o site
url = "https://dados.antt.gov.br/dataset/monitriip-bilhetes-de-passagem"
headers = {
  'Connection': 'keep-alive',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Accept-Language': 'pt-BR,pt;q=0.9'
}

response = requests.get(url, headers=headers)


# %%
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

# Processa link
soup = extractSoup(response.text)

# Resgata links e coloca em uma lista
listaLinks = soup.find_all('a',class_='heading')
listabase = []

#Pega a lista de links e estrutra para gerar a lsista para donwload
for link in soup.find_all('a',class_='resource-url-analytics'):
    listabase.append(link.get('href'))


# %%
# Faz o download dos arquivos da lista
#Loop para resgatar cadas urls de download dos arquivos
for a in listabase[:-1]:
  urlretrieve(a , a[-20:])


