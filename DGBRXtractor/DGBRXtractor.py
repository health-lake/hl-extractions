import warnings
import os
import requests
import time
import sys

from unidecode import unidecode

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

class DGBRXtractor:
    
    def __init__(self):
        
        # Ignorar avisos
        warnings.filterwarnings('ignore')

        # Configuração do webdriver
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.browser = webdriver.Chrome(executable_path='./chromedriver.exe', options=self.chrome_options)

    '''
        Este método foi desenvolvido para realizar o download de todos os arquivos do conjunto de dados a partir da sua url.
          url -> variável do tipo string | Contém a url da página do dataset que possui os arquivos a serem baixados.
          ext -> variável do tipo lista | Lista de strings com as extensões dos arquivos que deseja-se baixar. Por exemplo: ['.csv', '.xlsx', '.pdf']. O valor padrão é somente ['.csv'].

        Um exemplo de uso será adicionado na pasta "exemplos"
    '''
    def get_files_by_ds_url(self, url, ext=['.csv']):
        
        # Carregamento da página do dataset
        print('Carregando [{}]'.format(url))
        
        try:
            init = time.time()
            self.browser.get(url)
            end = time.time()
            print('Página carregada com sucesso ({} s).'.format(end-init))
        except:
            print('Ocorreu um erro ao carregar a página, tente novamente por favor.')
            self.browser.close()
            sys.exit()
        
        # Obter o nome do dataset a partir da url da página
        dataset_id = self.browser.current_url.split('/')[-1]

        # Selecionar os elementos HTML <li> que possuem a classe "resource-item" | file_elements é uma lista
        file_elements = self.browser.find_elements_by_css_selector('li.resource-item')
        
        # Iterar por todos os elementos armazenados em file_elements
        for element in file_elements:
            # Obter o formato do arquivo a ser baixado. Esse elemento se encontra no atributo "data-format" da tag <span> que fica dentro dos <li> que selecionamos anteriormente
            file_format = '.' + element.find_element_by_css_selector('span').get_attribute('data-format')
            
            # Transformar arquivos que são denotados como .zip+css ou .zip+xlsx e outros apenas em .zip
            if file_format.startswith('.zip'):
                file_format = '.zip'

            # Verificar se o formato de arquivo raspado está presente na lista de extensões que desejamos baixar
            if file_format in ext:
                # Gerar um nome para o arquivo a ser salvo. Aqui foi utilizado o atributo "title" das tags <a> que contém o link para o detalhamento do dataset, que possuem classe "heading"
                file_name = unidecode(element.find_element_by_css_selector('a.heading').get_attribute('title').lower().strip().replace(' ', '-').replace('/', '-'))
                
                # Formatar o nome do arquivo para adicionar a extensão
                if not file_name.endswith(file_format):
                    file_name += file_format

                # Obter o link para download do arquivo. Ele se encontra no atributo "href" das tags <a> que possuem classe "resource-url-analytics"
                file_url = element.find_element_by_css_selector('a.resource-url-analytics').get_attribute('href')

                # Verificar se já existe uma pasta no diretório de execução com a identificação do dataset que pegamos lá em cima, caso não exista ela será criada
                if not os.path.exists(dataset_id):
                    os.makedirs(dataset_id)

                # Baixar o arquivo utilizando a biblioteca requests
                print('Downloading {}'.format(file_name))
                req = requests.get(file_url)

                # Definir o local e o nome que o arquivo será salvo
                file_path = dataset_id + '/' + file_name

                # Gravar o arquivo
                with open(file=file_path, mode='wb') as f:
                    f.write(req.content)
                    f.close()

        # Fechar o browser
        self.browser.close()