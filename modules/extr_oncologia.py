from logging import exception
import boto3
from webbrowser import Chrome
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import requests
import os
from datetime import datetime
from utils.chrome_driver import ChromeDriver
from utils.s3_writer_operator import HandlerS3Writer


class ExtractONCO:
    def __init__(self):
        self.url = "http://tabnet.datasus.gov.br/cgi/dhdat.exe?PAINEL_ONCO/PAINEL_ONCOLOGIABR.def"
        #self.driver=webdriver.Chrome()
        self.driver = ChromeDriver.get_driver(self.url)

    def download(self):
        self.driver.get(self.url)
        loop=-1
        #SELECIONANDO OS ANOS DE INTERESSE
        for o in (["{:02d}".format(n) for n in reversed(range(13,22))]):
            loop=loop+1
            print(f'Ano de 20{str(o)}')
            print("Seleciona o tempo de tratamento como linha da tabela")
            
            #Seleciona linha como 'TEMPO DE TRATAMENTO' #Alterar para outro tipo de seleção de elemento
            selectLinha = self.driver.find_element(By.ID,'L') # captura o elemento 
            objLinha = Select(selectLinha)                  #Permite a interação com o códiogo como objeto select
            objLinha.select_by_index(24)                 # Seleciona as opções pelo index
            
            #Seleciona coluna 'Faixa etaria'
            self.driver.find_element_by_xpath('/html/body/center[2]/div/form/div[1]/div/div[2]/select/option[11]').click()
            #coluna regiao:                     /html/body/center[2]/div/form/div[1]/div/div[2]/select/option[2]

            
            #SELECIONA ANOS
            select_tipo = Select(self.driver.find_element_by_name('PAno do diagnóstico'))
            if loop>0:select_tipo.deselect_by_value(f'20{22}|20{22}|4')
            select_tipo.select_by_value(f'20{o}|20{o}|4')
            
            #Botao mostrar
            self.driver.find_element_by_xpath('/html/body/center[2]/div/form/div[3]/div[2]/div[3]/input[1]').click()
            print("Sobe tabela pro S3")     
            self.driver.switch_to.window(self.driver.window_handles[1])
            #self.driver.find_element_by_xpath('/html/body/div/div/div[3]/table[1]/tbody/tr/td[1]/a').click()
            time.sleep(1)
            
            file_name=f'tempo_tratamento_fx_etaria_20{o}.csv'
            #GRAVAR NO S3
            print(self.driver.current_url)
            #self.driver.find_elements_by_xpath('/html/body/center[2]/div[2]/table/tbody/tr/td[2]/a').click()
            elementos = self.driver.find_elements_by_xpath('/html/body/center[2]/div[2]/table/tbody/tr/td[2]/a')
            print(elementos)

            for elem in elementos:
                url = elem.get_attribute("href")
                print(url)
                

                # Verificar se já existe uma pasta no diretório de execução com a identificação do dataset que pegamos lá em cima, caso não exista ela será criada
                dataset_id = url.split("/")[-1]
                if not os.path.exists(dataset_id):
                    os.makedirs(dataset_id)

                try:
                    # Baixar o arquivo utilizando a biblioteca requests
                    downloadable_url = url #.split("=")[1]
                    print("Downloading {}".format(file_name))
                # req = requests.get(downloadable_url)    
                    req = requests.get(url, stream=True, allow_redirects=True,#)
                    headers = {'user-agent': 'MyPC'})
                except Exception as e:
                    print('Erro no get.request')  
                    print(e)  

                try:
                    # Gravando no S3
                    # print(req.content)
                    s3_writer = HandlerS3Writer(
                        extracted_file = req.content,
                        extraction_name = file_name,
                        extraction_source = f'oncologia/20{o}'
                    )            
                except Exception as e:
                    print('Erro ao transferir arquivo para o S3')
                    print('O erro é {e}')

            # CLICANDO NO BOTAO VOLTAR
            # self.driver.find_element_by_xpath('').click()
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
# if __name__=="__main__":
try:
    ExtractONCO().download()
except exception as e:
    print(e)