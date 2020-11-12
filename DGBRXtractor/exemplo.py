# Vamos baixar os arquivos .pdf e .csv do conjunto de dados "Gratificação Temporária de Atividade em Escola de Governo – GAEG"
# Também iremos baixar os arquivos .csv de três conjuntos de dados do CEFET-MG

# Importar a biblioteca com a nossa classe
from DGBRXtractor import DGBRXtractor

# Definir a url do primeiro conjunto de dados
url_1 = 'https://dados.gov.br/dataset/gratificacao-temporaria-de-atividade-em-escola-de-governo-gaeg'

# Definir uma lista contendo as urls dos três conjuntos de dados do CEFET-MG, esse passo poderia ser automatizado também
url_2 = ['https://dados.gov.br/dataset/cefetmg-alunos',
         'https://dados.gov.br/dataset/cefetmg-cursos-ativos',
         'https://dados.gov.br/dataset/cefetmg-bolsistas']

# Instanciamos o nosso extrator
extrator = DGBRXtractor()

# Definimos a lista de extensões que desejamos
ext = ['.csv', '.pdf']

# Solicitamos que ele baixe os arquivos da url_1
extrator.get_files_by_ds_url(url=url_1, ext=ext)

# Agora vamos iterar as urls de url_2
for url in url_2:
    # Instanciamos novamente a classe agora em uma nova variável
    extrator2 = DGBRXtractor()
    # Solicitamos o download dos arquivos de cada url e como queremos só os arquivos .csv, não precisamos passar parâmetros no ext
    extrator2.get_files_by_ds_url(url=url)

# O resultado desse processamento deverão ser 4 pastas: gratificacao-temporaria-de-atividade-em-escola-de-governo-gaeg (16 arquivos), cefetmg-alunos (1 arquivo), cefetmg-cursos-ativos (1 arquivo) e cefetmg-bolsistas (1 arquivo)