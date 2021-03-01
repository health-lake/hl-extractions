# %%
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# importe as libs necessárias
import requests
from bs4 import BeautifulSoup as bs4
from urllib.request import urlretrieve


# %%
# acessar o site
url = "http://dados.turismo.gov.br/cadastur"
headers = {
  'Connection': 'keep-alive',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Accept-Language': 'pt-BR,pt;q=0.9'
}

response = requests.get(url, headers=headers)


# %%
#função gerar lista de links
def geraListaLinks(idlistaStr):
  """Description of what the function does.  
  Args:    
    idlistaStr (str): Div id from website Turismo.gov.br    
  Returns:    
    list  
  """
  #func fot html parser
  def extractSoup(source):
    return bs4(source, 'html.parser')

  # get lis of links
  sitehtml = extractSoup(response.text)
  downloadAnosDiv = sitehtml.find(id= idlistaStr )
  listaString = downloadAnosDiv.getText(separator=' ',strip=True).split()

  # transform the list to fit the links pattern.
  trataLinhas = [x.replace("-","0") for x in listaString]
  listaAno = [x[0:6] for x in trataLinhas]

  # return the right list
  return listaAno

# Unic list for the 3 sections 
listaAno = geraListaLinks('collapse03')


# %%
# download cada csv
def downloadFileUrl(urlPath, filename):
  urlretrieve(urlPath, filename)


# download files form Turismo.gov.br 
def dowloadarquivos(baseUrl,qualificador,extensao):
  """Description of what the function does.  
  Args:    
    listalinks (str): lists of files from fucntion geraListaLinks
    baseUrl (str): Base list for downloaded files
    qualificador (str): qualifier of files to download
    extensao (str): File estension   
  Returns:    
    none  
  """
  #get pattern url for donwloads

  #Donwload all files
  for ano in listaAno[-8:]:
    urlTurista = baseUrl.replace("YEAR",ano)
    fileNameCsv = ''.join([qualificador,ano,extensao])
    # hadle exceptions broken links
    try:
      downloadFileUrl(urlTurista, fileNameCsv)
    except Exception:
      pass
#call fucntion to get files
turismo = dowloadarquivos("http://turismo.gov.br/dadosabertos/cadasturpj/AgenciadeTurismoYEARTrimestreCadasturPJ.csv",'AgenciadeTurismo','TrimestreCadasturPJ.csv')

veiculo = dowloadarquivos("http://turismo.gov.br/dadosabertos/cadasturpj/LocadoradeVeiculosYEARTrimestreCadasturPJ.csv",'LocadoradeVeiculos','TrimestreCadasturPJ.csv')

BaresCia= dowloadarquivos("http://turismo.gov.br/dadosabertos/cadasturpj/RestaurantesCafeteriaseBaresYEARTrimestreCadasturPJ.csv",'RestaurantesCafeteriaseBares','TrimestreCadasturPJ.csv')


